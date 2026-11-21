#!/usr/bin/env python3
"""XRSEO crawler: a polite stand-in for Screaming Frog's "Internal > HTML" export.

Usage:
    python3 crawl.py https://example.com OUT_DIR [--max-pages 500] [--delay 0.5]

Starts from the site's sitemaps and homepage, then follows internal links.
Writes to OUT_DIR:
    crawl.csv           one row per URL (status, title, H1, word count, links...)
    links.csv           every internal link: source, destination, anchor, in_content
    external_links.csv  every link to another site: source, destination, anchor
    robots.txt          a copy of the site's robots.txt
    text/               the main text of each page, one file per page
    meta.json           crawl settings and timing

Politeness: obeys robots.txt rules for all crawlers, waits between requests,
stops at --max-pages, and never submits forms.
"""
import argparse, collections, csv, json, os, re, statistics, sys, time
from urllib.parse import urljoin, urlparse, urldefrag
from urllib import robotparser

import requests
from bs4 import BeautifulSoup

# Some site firewalls block unknown bots outright, so identify as a normal browser.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
SKIP_EXT = re.compile(r"\.(jpe?g|png|gif|webp|svg|avif|pdf|kml|xml|css|js|ico|mp4|mp3|mov|zip|docx?|xlsx?|pptx?)$", re.I)
CHROME = ("header, footer, nav, aside, script, style, noscript, form, iframe, "
          "[data-elementor-type='header'], [data-elementor-type='footer'], "
          ".elementor-location-header, .elementor-location-footer, "
          "#masthead, #colophon, .site-header, .site-footer")


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("out")
    ap.add_argument("--max-pages", type=int, default=500)
    ap.add_argument("--delay", type=float, default=0.5)
    return ap.parse_args()


def main():
    a = parse_args()
    start = a.site if a.site.startswith("http") else "https://" + a.site
    host = urlparse(start).netloc.lower().removeprefix("www.")
    os.makedirs(os.path.join(a.out, "text"), exist_ok=True)

    S = requests.Session()
    S.headers["User-Agent"] = UA

    def get(url, **kw):
        return S.get(url, timeout=30, **kw)

    # Final scheme + host after the homepage's redirects (http->https, www or not).
    home = get(start)
    base = urlparse(home.url)
    origin = f"{base.scheme}://{base.netloc}"

    def norm(u):
        u, _ = urldefrag(u.strip())
        p = urlparse(u)
        if p.scheme not in ("http", "https", ""):
            return None
        if p.netloc and p.netloc.lower().removeprefix("www.") != host:
            return None
        path = p.path or "/"
        if SKIP_EXT.search(path) or "/wp-content/" in path or "/wp-json" in path or "/feed" in path:
            return None
        return f"{origin}{path}" + (f"?{p.query}" if p.query else "")

    # robots.txt
    rp = robotparser.RobotFileParser()
    robots_txt = ""
    try:
        r = get(origin + "/robots.txt")
        if r.status_code == 200:
            robots_txt = r.text
    except Exception:
        pass
    rp.parse(robots_txt.splitlines())
    with open(os.path.join(a.out, "robots.txt"), "w") as f:
        f.write(robots_txt)

    # Sitemaps: robots.txt lines, then the usual places.
    sm_queue = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots_txt)
    sm_queue += [origin + p for p in ("/sitemap_index.xml", "/sitemap.xml", "/wp-sitemap.xml")]
    seen_sm, sm_urls = set(), []
    while sm_queue and len(seen_sm) < 50:
        sm = sm_queue.pop(0)
        if sm in seen_sm:
            continue
        seen_sm.add(sm)
        try:
            r = get(sm)
        except Exception:
            continue
        if r.status_code != 200 or "<" not in r.text[:200]:
            continue
        body = r.text
        if "<sitemapindex" in body:
            sm_queue += [x.strip() for x in re.findall(r"<sitemap>\s*<loc>([^<]+)</loc>", body)]
        else:
            # Page <loc> only, not <image:loc>.
            sm_urls += [x.strip() for x in re.findall(r"<url>\s*<loc>([^<]+)</loc>", body)]
    sm_set = set(filter(None, (norm(u) for u in sm_urls)))

    queue = collections.deque([norm(home.url) or origin + "/"] + sorted(sm_set))
    seen = set(queue)
    rows, links, ext_links = [], [], []
    t0 = time.time()

    while queue and len(rows) < a.max_pages:
        url = queue.popleft()
        if robots_txt and not rp.can_fetch("*", url):
            rows.append({"url": url, "status": "blocked by robots.txt", "in_sitemap": url in sm_set})
            continue
        try:
            r = get(url, allow_redirects=False)
        except Exception as e:
            rows.append({"url": url, "status": f"error: {type(e).__name__}", "in_sitemap": url in sm_set})
            continue
        row = {"url": url, "status": r.status_code, "in_sitemap": url in sm_set,
               "x_robots": r.headers.get("X-Robots-Tag", "")}
        if r.is_redirect:
            loc = urljoin(url, r.headers.get("Location", ""))
            row["redirect_to"] = loc
            rows.append(row)
            n = norm(loc)
            if n and n not in seen:
                seen.add(n)
                queue.append(n)
            time.sleep(a.delay)
            continue
        if r.status_code != 200 or "text/html" not in r.headers.get("Content-Type", ""):
            rows.append(row)
            time.sleep(a.delay)
            continue

        soup = BeautifulSoup(r.text, "lxml")
        t = soup.find("title")
        row["title"] = t.get_text(" ", strip=True) if t else ""
        md = soup.find("meta", attrs={"name": "description"})
        row["meta_description"] = (md.get("content") or "").strip() if md else ""
        rb = soup.find("meta", attrs={"name": "robots"})
        row["meta_robots"] = (rb.get("content") or "") if rb else ""
        cn = soup.find("link", rel="canonical")
        row["canonical"] = (cn.get("href") or "") if cn else ""
        h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
        row["h1"] = " | ".join(h1s)
        row["h1_count"] = len(h1s)
        html_tag = soup.find("html")
        row["lang"] = html_tag.get("lang", "") if html_tag else ""
        for k in ("article:published_time", "article:modified_time"):
            m = soup.find("meta", attrs={"property": k})
            row[k.split(":")[1]] = (m.get("content") or "") if m else ""

        types, org_names = set(), set()
        for s in soup.find_all("script", type="application/ld+json"):
            raw = s.string or s.get_text() or ""
            types.update(re.findall(r'"@type"\s*:\s*"([^"]+)"', raw))
            for m in re.findall(r'"@type"\s*:\s*\[([^\]]+)\]', raw):
                types.update(x.strip(' "\n') for x in m.split(","))
            try:
                data = json.loads(raw)
            except Exception:
                continue
            stack = [data]
            while stack:
                d = stack.pop()
                if isinstance(d, list):
                    stack += d
                elif isinstance(d, dict):
                    tp = d.get("@type")
                    tps = tp if isinstance(tp, list) else [tp]
                    if any(x in ("Organization", "LocalBusiness", "RealEstateAgent", "ProfessionalService",
                                 "MedicalBusiness", "HealthAndBeautyBusiness") or
                           (isinstance(x, str) and x.endswith("Business")) for x in tps) and d.get("name"):
                        org_names.add(str(d["name"]).strip())
                    stack += [v for v in d.values() if isinstance(v, (dict, list))]
        row["schema_types"] = ", ".join(sorted(t for t in types if t))
        row["schema_business_names"] = " || ".join(sorted(org_names))

        root = soup.find("main") or soup.find("article") or soup.select_one(".entry-content") or soup.body or soup
        body = BeautifulSoup(str(root), "lxml")
        for tag in body.select(CHROME):
            tag.decompose()
        text = re.sub(r"\s+", " ", body.get_text(" ", strip=True))
        row["word_count"] = len(text.split())
        row["h2"] = " | ".join(h.get_text(" ", strip=True) for h in body.find_all("h2"))
        row["h2_count"] = len(body.find_all("h2"))
        fp = next((p.get_text(" ", strip=True) for p in body.find_all("p") if len(p.get_text(strip=True)) > 60), "")
        row["first_paragraph"] = fp[:400]
        imgs = soup.find_all("img")
        row["images"] = len(imgs)
        row["images_no_alt"] = sum(1 for i in imgs if not (i.get("alt") or "").strip())
        row["phone_links"] = len(soup.select("a[href^='tel:']"))
        row["has_form"] = bool(soup.find("form"))

        slug = re.sub(r"[^a-z0-9]+", "_", urlparse(url).path.strip("/").lower()) or "home"
        with open(os.path.join(a.out, "text", slug[:150] + ".txt"), "w") as f:
            f.write(url + "\n" + row["title"] + "\n\n" + text)

        content_links = set()
        for el in body.find_all("a", href=True):
            n = norm(urljoin(url, el["href"]))
            if n and n != url:
                content_links.add(n)
                links.append((url, n, el.get_text(" ", strip=True)[:100], True))
        all_links = set()
        ext_seen = set()
        for el in soup.find_all("a", href=True):
            href = urljoin(url, el["href"])
            n = norm(href)
            if n:
                if n != url:
                    all_links.add(n)
                    if n not in seen:
                        seen.add(n)
                        queue.append(n)
            elif urlparse(href).scheme in ("http", "https") and href not in ext_seen:
                ext_seen.add(href)
                ext_links.append((url, href, el.get_text(" ", strip=True)[:100]))
        for n in all_links - content_links:
            links.append((url, n, "", False))
        row["outlinks_all"] = len(all_links)
        row["outlinks_content"] = len(content_links)
        rows.append(row)
        time.sleep(a.delay)

    inl_all, inl_content = collections.defaultdict(set), collections.defaultdict(set)
    for src, dst, _, inc in links:
        inl_all[dst].add(src)
        if inc:
            inl_content[dst].add(src)
    for row in rows:
        row["inlinks_all"] = len(inl_all.get(row["url"], ()))
        row["inlinks_content"] = len(inl_content.get(row["url"], ()))

    keys = []
    for row in rows:
        keys += [k for k in row if k not in keys]
    with open(os.path.join(a.out, "crawl.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(a.out, "links.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "destination", "anchor", "in_content"])
        w.writerows(links)
    with open(os.path.join(a.out, "external_links.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source", "destination", "anchor"])
        w.writerows(ext_links)
    meta = {"site": origin, "host": host, "crawled": len(rows), "sitemap_urls": len(sm_set),
            "hit_page_limit": bool(queue), "seconds": round(time.time() - t0),
            "date": time.strftime("%Y-%m-%d"), "max_pages": a.max_pages}
    with open(os.path.join(a.out, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
