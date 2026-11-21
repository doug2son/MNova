"""Small site crawler: a stand-in for the Screaming Frog 'Internal > HTML' export.

Usage: python3 crawl.py <out_dir>

Writes crawl.csv (one row per page), links.csv (every internal link)
and a text/ folder with each page's main text. Change SITE and HOST
at the top to crawl a different site.
"""
import collections, csv, json, re, sys, time, os
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

SITE = "https://largohomebuyers.com"
HOST = "largohomebuyers.com"
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "text"), exist_ok=True)

S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|pdf|kml|xml|css|js|ico|mp4|mp3|zip)(\?|$)", re.I)


def norm(u):
    u, _ = urldefrag(u)
    p = urlparse(u)
    if p.netloc.replace("www.", "") != HOST:
        return None
    path = p.path or "/"
    if SKIP_EXT.search(path):
        return None
    if "/wp-" in path or "/feed" in path or p.query:
        return None
    return f"https://{HOST}{path}"


def sitemap_urls():
    urls = []
    idx = S.get(SITE + "/sitemap_index.xml", timeout=30).text
    for sm in re.findall(r"<loc>([^<]+)</loc>", idx):
        if sm.endswith(".xml"):
            body = S.get(sm, timeout=30).text
            # only page <loc>, not image:loc
            for loc in re.findall(r"<url>\s*<loc>([^<]+)</loc>", body):
                urls.append(loc.strip())
    return urls


def content_root(soup):
    for sel in ["main", "article", "div.entry-content", "div[data-elementor-type='wp-page']", "div[data-elementor-type='wp-post']"]:
        el = soup.select_one(sel)
        if el:
            return el
    return soup.body


def strip_chrome(root):
    root = BeautifulSoup(str(root), "lxml")
    for tag in root.select("header, footer, nav, script, style, noscript, form, [data-elementor-type='header'], [data-elementor-type='footer'], .elementor-location-header, .elementor-location-footer"):
        tag.decompose()
    return root


sm = sitemap_urls()
sm_set = set(filter(None, (norm(u) for u in sm)))
queue = collections.deque(sorted(sm_set))
seen = set(queue)
rows = []
links = []  # (src, dst, anchor, in_content)

while queue and len(rows) < 400:
    url = queue.popleft()
    try:
        r = S.get(url, timeout=30, allow_redirects=False)
    except Exception as e:
        rows.append({"url": url, "status": f"ERR {e}"})
        continue
    row = {"url": url, "status": r.status_code, "in_sitemap": url in sm_set}
    if r.is_redirect:
        loc = urljoin(url, r.headers.get("Location", ""))
        row["redirect_to"] = loc
        rows.append(row)
        n = norm(loc)
        if n and n not in seen:
            seen.add(n); queue.append(n)
        continue
    row["x_robots"] = r.headers.get("X-Robots-Tag", "")
    if r.status_code != 200 or "text/html" not in r.headers.get("Content-Type", ""):
        rows.append(row)
        continue
    soup = BeautifulSoup(r.text, "lxml")
    t = soup.find("title")
    row["title"] = t.get_text(" ", strip=True) if t else ""
    md = soup.find("meta", attrs={"name": "description"})
    row["meta_description"] = md.get("content", "").strip() if md else ""
    rb = soup.find("meta", attrs={"name": "robots"})
    row["meta_robots"] = rb.get("content", "") if rb else ""
    cn = soup.find("link", rel="canonical")
    row["canonical"] = cn.get("href", "") if cn else ""
    row["h1"] = " | ".join(h.get_text(" ", strip=True) for h in soup.find_all("h1"))
    row["h1_count"] = len(soup.find_all("h1"))
    for k in ("article:published_time", "article:modified_time"):
        m = soup.find("meta", attrs={"property": k})
        row[k.split(":")[1]] = m.get("content", "") if m else ""
    types = set()
    for s in soup.find_all("script", type="application/ld+json"):
        for m in re.findall(r'"@type"\s*:\s*"([^"]+)"', s.string or ""):
            types.add(m)
        for m in re.findall(r'"@type"\s*:\s*\[([^\]]+)\]', s.string or ""):
            types.update(x.strip(' "') for x in m.split(","))
    row["schema_types"] = ", ".join(sorted(types))

    root = content_root(soup)
    body = strip_chrome(root)
    text = re.sub(r"\s+", " ", body.get_text(" ", strip=True))
    row["word_count"] = len(text.split())
    row["h2"] = " | ".join(h.get_text(" ", strip=True) for h in body.find_all("h2"))
    row["h2_count"] = len(body.find_all("h2"))
    row["h3_count"] = len(body.find_all("h3"))
    # first paragraph
    fp = next((p.get_text(" ", strip=True) for p in body.find_all("p") if len(p.get_text(strip=True)) > 40), "")
    row["first_paragraph"] = fp[:400]
    imgs = body.find_all("img")
    row["images"] = len(imgs)
    row["images_no_alt"] = sum(1 for i in imgs if not (i.get("alt") or "").strip())
    row["has_iframe_video"] = bool(body.find("iframe"))
    row["phone_links"] = len(soup.select("a[href^='tel:']"))
    with open(os.path.join(OUT, "text", re.sub(r"[^a-z0-9]+", "_", urlparse(url).path.strip("/") or "home") + ".txt"), "w") as f:
        f.write(url + "\n" + row["title"] + "\n\n" + text)

    content_hrefs = {id(a) for a in body.find_all("a")}
    content_links = set()
    for a in body.find_all("a", href=True):
        n = norm(urljoin(url, a["href"]))
        if n and n != url:
            content_links.add(n)
            links.append((url, n, a.get_text(" ", strip=True)[:80], True))
    all_links = set()
    for a in soup.find_all("a", href=True):
        n = norm(urljoin(url, a["href"]))
        if n and n != url:
            all_links.add(n)
            if n not in seen:
                seen.add(n); queue.append(n)
    row["outlinks_all"] = len(all_links)
    row["outlinks_content"] = len(content_links)
    ext = {urlparse(urljoin(url, a["href"])).netloc for a in soup.find_all("a", href=True)
           if urlparse(urljoin(url, a["href"])).netloc not in ("", HOST, "www." + HOST)}
    row["external_domains"] = ", ".join(sorted(ext))
    # sitewide links (all minus content) tracked to compute inlinks
    for n in all_links - content_links:
        links.append((url, n, "", False))
    rows.append(row)
    time.sleep(0.3)

# inlink counts
inl_all = collections.defaultdict(set)
inl_content = collections.defaultdict(set)
for src, dst, _, inc in links:
    inl_all[dst].add(src)
    if inc:
        inl_content[dst].add(src)
for row in rows:
    row["inlinks_all"] = len(inl_all.get(row["url"], ()))
    row["inlinks_content"] = len(inl_content.get(row["url"], ()))

keys = []
for r_ in rows:
    for k in r_:
        if k not in keys:
            keys.append(k)
with open(os.path.join(OUT, "crawl.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, "links.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["source", "destination", "anchor", "in_content"])
    w.writerows(links)
print(len(rows), "urls crawled;", len(links), "links")
