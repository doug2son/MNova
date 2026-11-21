#!/usr/bin/env python3
"""XRSEO crawl analysis: turns a crawl folder into findings.json.

Usage:
    python3 analyze_crawl.py CRAWL_DIR [--brand "Business Name"]

Reads crawl.csv, links.csv, external_links.csv, robots.txt and text/ from
CRAWL_DIR (made by crawl.py) and writes CRAWL_DIR/findings.json.

Everything here is counted from the crawl. Nothing is estimated, so every
number can go straight into a report. Judgment calls (which page should win,
what to write) are left to the person or model reading the findings.
"""
import argparse, collections, csv, datetime, itertools, json, os, re, statistics
from urllib.parse import urlparse

STOP = set("""a an and are as at be by can do for from has have how i if in into is it its
me my no not of on or our out so than that the their them they this to up us was we
what when where which who why will with you your here there - | : vs""".split())
ARCHIVE = re.compile(r"/(category|tag|author|topics?|archives?)/|/page/\d+/?$|/\d{4}/\d{2}/?$", re.I)
UTILITY = re.compile(r"(contact|privacy|terms|legal|disclaimer|cookie|thank|login|cart|checkout|account|sitemap)", re.I)


def load(crawl_dir):
    rows = list(csv.DictReader(open(os.path.join(crawl_dir, "crawl.csv"))))
    links = list(csv.DictReader(open(os.path.join(crawl_dir, "links.csv"))))
    ext_path = os.path.join(crawl_dir, "external_links.csv")
    ext = list(csv.DictReader(open(ext_path))) if os.path.exists(ext_path) else []
    meta = json.load(open(os.path.join(crawl_dir, "meta.json")))
    rpath = os.path.join(crawl_dir, "robots.txt")
    robots = open(rpath).read() if os.path.exists(rpath) else ""
    return rows, links, ext, meta, robots


def short(url, origin):
    return url[len(origin):] or "/" if url.startswith(origin) else url


def page_text(crawl_dir, url):
    slug = re.sub(r"[^a-z0-9]+", "_", urlparse(url).path.strip("/").lower()) or "home"
    p = os.path.join(crawl_dir, "text", slug[:150] + ".txt")
    if not os.path.exists(p):
        return ""
    return open(p).read().split("\n", 3)[-1]


def find_suffix(titles):
    """The text most titles end with after a separator, e.g. ' - Brand Name'."""
    c = collections.Counter()
    for t in titles:
        m = re.search(r"\s[-|–—•:]\s([^-|–—•]+)$", t)
        if m:
            c[m.group(0)] += 1
    if not c:
        return None, 0
    suffix, n = c.most_common(1)[0]
    return (suffix, n) if n >= max(3, len(titles) * 0.3) else (None, 0)


def status(count, warn_at=1, fail_at=1, invert=False):
    if count >= fail_at:
        return "fail"
    if count >= warn_at:
        return "warn"
    return "pass"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("crawl_dir")
    ap.add_argument("--brand", default="", help="Business name, left out of topic matching")
    a = ap.parse_args()
    rows, links, ext, meta, robots = load(a.crawl_dir)
    origin = meta["site"]
    S = lambda u: short(u, origin)
    by_url = {r["url"]: r for r in rows}

    live = [r for r in rows if r["status"] == "200"]
    redirects = [r for r in rows if r["status"].startswith("3")]
    broken = [r for r in rows if r["status"][:1] in ("4", "5")]

    def indexable(r):
        robots_meta = (r.get("meta_robots", "") + " " + r.get("x_robots", "")).lower()
        canon = r.get("canonical", "")
        canon_ok = (not canon) or canon.rstrip("/") == r["url"].rstrip("/")
        return r["status"] == "200" and "noindex" not in robots_meta and canon_ok

    idx = [r for r in live if indexable(r)]
    idx_pages = [r for r in idx if not ARCHIVE.search(urlparse(r["url"]).path)]

    # Where each redirect finally lands.
    def final(url, hops=0):
        r = by_url.get(url)
        if r and r["status"].startswith("3") and r.get("redirect_to") and hops < 10:
            nxt = r["redirect_to"]
            nxt = nxt if nxt in by_url else nxt.split("#")[0]
            return final(nxt, hops + 1)
        return url

    # --- Links pointing at broken pages or redirects ---
    to_bad = collections.defaultdict(list)
    for l in links:
        d = by_url.get(l["destination"])
        if d and (d["status"].startswith("3") or d["status"][:1] in ("4", "5")):
            to_bad[l["destination"]].append(l)

    def link_summary(url):
        ls = to_bad[url]
        return {"links": len(ls), "pages": sorted({S(l["source"]) for l in ls}),
                "anchors": sorted({l["anchor"] for l in ls if l["anchor"]})[:8]}

    broken_links = sorted(
        [{"url": S(u), "status": by_url[u]["status"], **link_summary(u)}
         for u in to_bad if by_url[u]["status"][:1] in ("4", "5")],
        key=lambda x: -x["links"])
    redirect_links = sorted(
        [{"url": S(u), "goes_to": S(final(u)),
          "final_status": by_url.get(final(u), {}).get("status", "not crawled"), **link_summary(u)}
         for u in to_bad if by_url[u]["status"].startswith("3")],
        key=lambda x: -x["links"])

    # --- Internal link counts ---
    content_in = collections.defaultdict(set)
    any_in = collections.defaultdict(set)
    via_redirect = collections.defaultdict(lambda: collections.defaultdict(int))
    for l in links:
        any_in[l["destination"]].add(l["source"])
        if l["in_content"] == "True":
            content_in[l["destination"]].add(l["source"])
        d = by_url.get(l["destination"])
        if d and d["status"].startswith("3"):
            via_redirect[final(l["destination"])][S(l["destination"])] += 1
    median_content = statistics.median([len(content_in[r["url"]]) for r in idx_pages]) if idx_pages else 0

    orphans, redirect_only, weak = [], [], []
    for r in idx_pages:
        if r["url"].rstrip("/") == origin:
            continue
        n_any = len(any_in[r["url"]])
        n_content = len(content_in[r["url"]])
        vr = via_redirect.get(r["url"], {})
        item = {"url": S(r["url"]), "title": r.get("title", ""), "words": int(r.get("word_count") or 0),
                "content_links_in": n_content, "links_in_any": n_any}
        if n_any == 0 and vr:
            redirect_only.append({**item, "via": dict(vr), "redirect_links": sum(vr.values())})
        elif n_any == 0:
            orphans.append(item)
        elif n_content < median_content / 2:
            weak.append(item)

    # --- Titles, descriptions, headings ---
    titles = [r.get("title", "") for r in idx]
    suffix, suffix_n = find_suffix(titles)
    long_titles = [{"url": S(r["url"]), "title": r["title"], "length": len(r["title"])}
                   for r in idx if len(r.get("title", "")) > 60]
    short_titles = [{"url": S(r["url"]), "title": r["title"], "length": len(r["title"])}
                    for r in idx if 0 < len(r.get("title", "")) < 30]
    missing_titles = [S(r["url"]) for r in idx if not r.get("title")]
    tcount = collections.Counter(titles)
    dup_titles = [{"title": t, "pages": [S(r["url"]) for r in idx if r["title"] == t]}
                  for t, n in tcount.items() if n > 1 and t]
    no_desc = [S(r["url"]) for r in idx if not r.get("meta_description")]
    short_desc = [{"url": S(r["url"]), "length": len(r["meta_description"])} for r in idx
                  if 0 < len(r.get("meta_description", "")) < 70]
    long_desc = [{"url": S(r["url"]), "length": len(r["meta_description"])} for r in idx
                 if len(r.get("meta_description", "")) > 160]
    dcount = collections.Counter(r.get("meta_description", "") for r in idx)
    dup_desc = [{"description": d[:90], "pages": [S(r["url"]) for r in idx if r["meta_description"] == d]}
                for d, n in dcount.items() if n > 1 and d]
    h1_missing = [S(r["url"]) for r in idx_pages if r.get("h1_count") == "0"]
    h1_multi = []
    for r in idx_pages:
        if int(r.get("h1_count") or 0) > 1:
            parts = [p.strip() for p in r["h1"].split(" | ") if p.strip()]
            h1_multi.append({"url": S(r["url"]), "count": int(r["h1_count"]),
                             "repeated": len(set(p.lower() for p in parts)) < len(parts), "h1": r["h1"][:160]})

    # --- Archives, thin pages, business names ---
    archives = [{"url": S(r["url"]), "words": int(r.get("word_count") or 0), "has_h1": r.get("h1_count") != "0",
                 "has_description": bool(r.get("meta_description"))}
                for r in idx if ARCHIVE.search(urlparse(r["url"]).path)]
    thin = [{"url": S(r["url"]), "title": r.get("title", ""), "words": int(r.get("word_count") or 0),
             "utility_page": bool(UTILITY.search(r["url"]))}
            for r in idx_pages if int(r.get("word_count") or 0) < 300]
    names = collections.Counter()
    for r in live:
        for n in (r.get("schema_business_names") or "").split(" || "):
            if n:
                names[n] += 1

    # --- Near-duplicate text ---
    shingles = {}
    for r in idx_pages:
        w = re.findall(r"[a-z0-9]+", page_text(a.crawl_dir, r["url"]).lower())
        shingles[r["url"]] = set(" ".join(w[i:i + 5]) for i in range(len(w) - 4))
    near_dupes = []
    for x, y in itertools.combinations(shingles, 2):
        if len(shingles[x]) < 30 or len(shingles[y]) < 30:
            continue
        share = len(shingles[x] & shingles[y]) / min(len(shingles[x]), len(shingles[y]))
        if share >= 0.5:
            near_dupes.append({"a": S(x), "b": S(y), "shared_text": round(share, 2)})
    near_dupes.sort(key=lambda d: -d["shared_text"])

    # --- Pages that look like they target the same thing ---
    brand_words = set(re.findall(r"[a-z0-9]+", (a.brand + " " + (suffix or "")).lower()))

    def topic_words(r):
        text = " ".join([urlparse(r["url"]).path.replace("-", " ").replace("/", " "),
                         (r.get("title") or "").replace(suffix or "\0", ""), r.get("h1") or ""]).lower()
        return {w for w in re.findall(r"[a-z][a-z0-9]+", text)
                if w not in STOP and w not in brand_words and not re.fullmatch(r"20\d\d", w)}

    tw = {r["url"]: topic_words(r) for r in idx_pages}
    parent = {u: u for u in tw}

    def root(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    pair_scores = {}
    for x, y in itertools.combinations(tw, 2):
        if not tw[x] or not tw[y]:
            continue
        shared = tw[x] & tw[y]
        j = len(shared) / len(tw[x] | tw[y])
        if j >= 0.5 and len(shared) >= 2:
            parent[root(x)] = root(y)
            pair_scores[(x, y)] = round(j, 2)
    groups = collections.defaultdict(list)
    for u in tw:
        groups[root(u)].append(u)
    overlap = []
    for g in groups.values():
        if len(g) > 1:
            common = set.intersection(*(tw[u] for u in g))
            overlap.append({"pages": [{"url": S(u), "title": by_url[u].get("title", ""),
                                       "words": int(by_url[u].get("word_count") or 0)} for u in g],
                            "shared_words": sorted(common)})
    overlap.sort(key=lambda g: -len(g["pages"]))

    # --- Dated content ---
    this_year = datetime.date.today().year
    dated = []
    for r in idx_pages:
        years = sorted(set(re.findall(r"\b(20[12]\d)\b", " ".join([r["url"], r.get("title", ""), r.get("h1", "")]))))
        txt = page_text(a.crawl_dir, r["url"])
        facts = len(re.findall(r"\$\s?\d[\d,]*|\b\d+(?:\.\d+)?%|\b20[12]\d\b", txt))
        if years or facts >= 10:
            dated.append({"url": S(r["url"]), "years_in_title_or_url": years, "year_in_url": bool(re.search(r"20[12]\d", r["url"])),
                          "prices_percents_years_in_text": facts,
                          "modified": (r.get("modified_time") or "")[:10]})
    dated.sort(key=lambda d: (-len(d["years_in_title_or_url"]), -d["prices_percents_years_in_text"]))

    # --- Sitemap and robots ---
    in_sm = [r for r in rows if r.get("in_sitemap") == "True"]
    sitemap = {
        "urls": meta.get("sitemap_urls", 0),
        "not_loading": [{"url": S(r["url"]), "status": r["status"]} for r in in_sm if r["status"] != "200"],
        "noindex_listed": [S(r["url"]) for r in in_sm if r["status"] == "200" and "noindex" in (r.get("meta_robots", "") + r.get("x_robots", "")).lower()],
        "canonical_elsewhere": [{"url": S(r["url"]), "canonical": r.get("canonical", "")} for r in in_sm
                                if r["status"] == "200" and r.get("canonical") and r["canonical"].rstrip("/") != r["url"].rstrip("/")],
        "indexable_missing": [S(r["url"]) for r in idx_pages if r.get("in_sitemap") != "True"],
    }
    rlines = [l.strip().lower() for l in robots.splitlines()]
    ai_bots = ["gptbot", "oai-searchbot", "chatgpt-user", "claudebot", "perplexitybot", "google-extended", "applebot-extended"]
    blocked_ai = []
    agent = None
    for l in rlines:
        if l.startswith("user-agent:"):
            agent = l.split(":", 1)[1].strip()
        elif l.startswith("disallow:") and l.split(":", 1)[1].strip() == "/" and agent in ai_bots:
            blocked_ai.append(agent)
    robots_info = {
        "found": bool(robots.strip()),
        "blocks_everything": any(l == "disallow: /" for l in rlines) and "user-agent: *" in rlines,
        "sitemap_listed": any(l.startswith("sitemap:") for l in rlines),
        "ai_crawlers_blocked": blocked_ai,
    }

    odd_urls = [S(r["url"]) for r in live if re.search(r"[A-Z]|//|\.$|/\.$|\s", urlparse(r["url"]).path)]
    ext_domains = collections.Counter(urlparse(e["destination"]).netloc.removeprefix("www.") for e in ext)

    pages = sorted([{"url": S(r["url"]), "title": r.get("title", ""), "title_length": len(r.get("title", "")),
                     "h1": r.get("h1", ""), "words": int(r.get("word_count") or 0),
                     "content_links_in": len(content_in[r["url"]]), "links_in_any": len(any_in[r["url"]]),
                     "in_sitemap": r.get("in_sitemap") == "True", "has_form": r.get("has_form") == "True",
                     "phone_links": int(r.get("phone_links") or 0), "modified": (r.get("modified_time") or "")[:10]}
                    for r in idx_pages], key=lambda p: p["url"])

    n_bad_links = sum(b["links"] for b in broken_links)
    n_redirect_links = sum(b["links"] for b in redirect_links)
    checks = [
        {"id": "pages_load", "label": "Every page in the sitemap loads", "count": len(sitemap["not_loading"]),
         "status": status(len(sitemap["not_loading"]))},
        {"id": "broken_links", "label": "No internal links to missing pages", "count": n_bad_links,
         "status": status(n_bad_links)},
        {"id": "redirect_links", "label": "Internal links go straight to the right page (no redirects)",
         "count": n_redirect_links, "status": status(n_redirect_links, 1, 20)},
        {"id": "orphans", "label": "Every page has at least one link pointing to it", "count": len(orphans),
         "status": status(len(orphans))},
        {"id": "title_length", "label": "Page titles fit in Google results (60 characters or less)",
         "count": len(long_titles), "status": status(len(long_titles), 1, max(5, len(idx) // 4))},
        {"id": "title_unique", "label": "Every page has its own title", "count": sum(len(d["pages"]) for d in dup_titles) + len(missing_titles),
         "status": status(sum(len(d["pages"]) for d in dup_titles) + len(missing_titles), 1, 4)},
        {"id": "descriptions", "label": "Pages have a search description", "count": len(no_desc),
         "status": status(len(no_desc), 1, max(5, len(idx) // 4))},
        {"id": "h1", "label": "Each page has one main heading (H1)", "count": len(h1_missing) + len(h1_multi),
         "status": status(len(h1_missing) + len(h1_multi), 1, 5)},
        {"id": "archives", "label": "Category and tag pages are kept out of Google or made useful",
         "count": len([x for x in archives if x["words"] < 300]), "status": status(len([x for x in archives if x["words"] < 300]), 1, 5)},
        {"id": "business_name", "label": "One business name used in the site's structured data",
         "count": len(names), "status": "pass" if len(names) == 1 else ("warn" if len(names) == 0 else "fail")},
        {"id": "duplicates", "label": "No pages that copy each other's text", "count": len(near_dupes),
         "status": status(len(near_dupes), 1, 3)},
        {"id": "overlap", "label": "One page per topic (no pages competing for the same search)",
         "count": sum(len(g["pages"]) for g in overlap), "status": status(len(overlap), 1, 3)},
        {"id": "thin", "label": "Service and guide pages have enough content (300+ words)",
         "count": len([t for t in thin if not t["utility_page"]]), "status": status(len([t for t in thin if not t["utility_page"]]), 1, 4)},
        {"id": "robots", "label": "Google is allowed in and the sitemap is listed",
         "count": int(robots_info["blocks_everything"]) + int(not robots_info["sitemap_listed"]),
         "status": "fail" if robots_info["blocks_everything"] else ("warn" if not robots_info["sitemap_listed"] else "pass")},
        {"id": "dated", "label": "No years in titles that will look out of date",
         "count": len([d for d in dated if d["years_in_title_or_url"]]),
         "status": "warn" if any(d["years_in_title_or_url"] for d in dated) else "pass"},
    ]

    findings = {
        "site": origin, "date": meta.get("date"), "crawl": meta,
        "counts": {"urls_checked": len(rows), "live_pages": len(live), "redirects": len(redirects),
                   "missing_pages": len(broken), "indexable_pages": len(idx), "indexable_content_pages": len(idx_pages),
                   "noindex_pages": len(live) - len(idx), "median_content_links_in": median_content},
        "checks": checks,
        "broken_links": broken_links, "redirect_links": redirect_links,
        "orphans": orphans, "redirect_only": redirect_only, "weakly_linked": weak,
        "title_suffix": {"suffix": suffix, "pages": suffix_n},
        "long_titles": long_titles, "short_titles": short_titles, "missing_titles": missing_titles,
        "duplicate_titles": dup_titles, "missing_descriptions": no_desc, "short_descriptions": short_desc,
        "long_descriptions": long_desc, "duplicate_descriptions": dup_desc,
        "h1_missing": h1_missing, "h1_multiple": h1_multi,
        "archives_indexable": archives, "thin_pages": thin, "business_names": dict(names),
        "near_duplicates": near_dupes, "topic_overlap": overlap, "dated": dated,
        "sitemap": sitemap, "robots": robots_info, "odd_urls": odd_urls,
        "external_domains": dict(ext_domains.most_common(25)), "pages": pages,
    }
    out = os.path.join(a.crawl_dir, "findings.json")
    with open(out, "w") as f:
        json.dump(findings, f, indent=2)
    print(json.dumps({"checks": {c["id"]: [c["status"], c["count"]] for c in checks}, **findings["counts"]}, indent=1))


if __name__ == "__main__":
    main()
