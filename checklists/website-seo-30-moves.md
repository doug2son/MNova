# Website SEO: The 30 Moves

Based on [Noel Ceta's playbook](../articles/2026-11-thirty-seo-moves.md). Run them in order, one move per chat. This page tracks where Largo Home Buyers stands.

**Status key:** Done = finished from the crawl. Partly = started, needs data to finish. Waiting = needs Search Console or analytics. Later = only after earlier moves.

## Before starting: get the data

| # | File | Where it comes from | Have it? |
| --- | --- | --- | --- |
| 1 | Searches and pages (`Queries.csv`, `Pages.csv`) | Search Console > Performance > compare last 3 months to the 3 months before > Export | [ ] |
| 2 | Which page ranks for which search (`query-page-now.csv`, `query-page-before.csv`) | Google Sheets add-on "Search Analytics for Sheets", grouped by Query and Page | [ ] |
| 3 | Pages Google won't show | Search Console > Indexing > Pages > export each reason | [ ] |
| 4 | Links | Search Console > Links > export "Top linked pages" and "Internal links" | [ ] |
| 5 | Site crawl | **Done.** Our own crawl replaces Screaming Frog: [`crawl.csv`](../audits/largohomebuyers/data/crawl.csv) | [x] |
| 6 | What makes money | Google Analytics landing pages with key events, or list money pages by hand (see notes below) | [ ] |
| - | One page of business notes | Written by me (template below) | [ ] |

**Easier option for files 1 to 4:** connect Google Search Console in Windsor.ai. Claude can then pull the data directly and files 1 and 2 aren't needed as exports. File 3 (indexing reasons) still has to be exported by hand.

### Business notes template

- What we sell, and to who:
- Money pages (5 to 20 URLs where sellers call or fill in the form):
- Rough value of one closed deal:
- Areas we serve:
- 3 to 5 competitors we lose deals to:
- Brand name to leave out of every analysis: Largo Home Buyers
- 10 questions sellers ask before they say yes (from calls and texts):

### Master prompt (paste into the Claude project instructions)

> You're a senior SEO working on my site. The project files are my real data: Search Console exports, a site crawl, links, and conversions by landing page. My notes describe the business.
>
> Rules:
> - Use code for every calculation. Only use numbers from my files. No industry averages, no made-up benchmarks.
> - Leave out every search that contains my brand name, including when you work out my averages.
> - Compare me with my own site, never with "typical" CTRs or positions from the internet.
> - Prioritise by value, not traffic: searches x what that page is worth to me. Money pages first.
> - Fix existing pages before suggesting new ones.
> - One search = one page. Never suggest two pages for the same intent.
> - For any page, say whether the problem is: Google can't index it, two of my pages compete, the format is wrong, the content is thin, it lacks internal links, or it lacks backlinks. In that order. Don't skip to links.
> - If my files can't answer something, say what file you need instead of guessing.
> - Plain English. Give me a table first, then exact changes. Say how long each fix takes (15 min, 1 hour, half a day).
> - Never suggest exact-match keyword anchor text, paid links, or anything against Google's spam policies.

The last rule is mine, added to match [how I judge advice](../how-i-judge-advice.md).

## Week 1: Know what matters, and fix what stops Google

| # | Move | Needs | Status |
| --- | --- | --- | --- |
| 1 | Rank pages by money, not traffic | Files 1, 6, notes | Waiting |
| 2 | Give every page one main keyword | Files 2, 5, notes | Waiting |
| 3 | Find real competitors (drop directories and big brands) | Notes, web search | Partly: first pass in the [findings](../audits/largohomebuyers/2026-11-crawl-findings.md#move-3-and-9-who-actually-shows-up) |
| 4 | Find pages Google quietly dropped | Files 1, 2 | Waiting |
| 5 | Indexing problems on pages that matter | Files 3, 5, notes | Partly: crawl side done |
| 6 | Template problems | File 5 | Done |
| 7 | Pages competing for one search | File 2 | Partly: suspected groups listed, Search Console must confirm |
| 8 | Merge, redirect or retarget the losers | Files 1, 2, 6 | Waiting (needs move 7) |

## Week 2: Match what Google ranks, rewrite, internal links

| # | Move | Needs | Status |
| --- | --- | --- | --- |
| 9 | Check format against the top 10 | Web search or pasted top 10s | Partly: directories dominate. Check Google top 10 by hand |
| 10 | Check price intent | File 2, notes | Waiting |
| 11 | Find thin pages (vs the median of the top 3) | File 5, web search | Partly: our side measured. Competitor pages were blocked here, so do it on desktop |
| 12 | Find missing subtopics | Web search, one URL at a time | Later |
| 13 | Answer buyer questions on the page | Notes, File 2 | Waiting (needs the 10 questions) |
| 14 | Rewrite the top of every money page | Notes, one URL at a time | Partly: first screens checked |
| 15 | Fix near-duplicate pages | File 5 | Done: little copied text, but duplicate topics |
| 16 | Find under-linked pages | Files 4, 5 | Done |
| 17 | Write the links for you | Files 2, 5 | Done (draft), refine with File 2 |
| 18 | Connect guides and money pages | File 5, notes | Done |

## Week 3: Lost traffic and more clicks

| # | Move | Needs | Status |
| --- | --- | --- | --- |
| 19 | Find what fell, and why | Files 1, 2 | Waiting |
| 20 | Push positions 11 to 20 onto page one | File 2 | Waiting |
| 21 | Set refresh dates | File 5 | Done |
| 22 | Rewrite titles only where the numbers say so | Files 1, 2 | Waiting |
| 23 | Fix titles and H1s across the site | File 5, move 2 | Partly: template fixes done, keyword check needs move 2 |

## Month 2: Links and new pages (only where the data says so)

| # | Move | Needs | Status |
| --- | --- | --- | --- |
| 24 | Decide which pages actually need links | File 4, link tool, web search | Later |
| 25 | Size the link plan | Move 24 | Later. Use my anchor rules, not his 10% exact match |
| 26 | Sites linking to competitors, not us | Backlink exports | Later. Run anything found through [checking competitors](checking-competitors.md) |
| 27 | Link-worthy data we already have | Notes, File 6 | Later |
| 28 | Gaps competitors already proved | Keyword gap export, File 2 | Later |
| 29 | Prune safely | Files 1, 4, 5, 6 | Waiting |
| 30 | Measure what worked | Fresh exports, change log | Every month |

## Rules to remember

- [ ] Keep a change log: date, page, what changed. Move 30 is impossible without it.
- [ ] Don't rewrite a page and build links to it in the same month.
- [ ] After fixing a page, paste its URL into Search Console's inspection bar and click Request indexing.
- [ ] Don't blame a Google update unless Google's Search Status Dashboard shows one on those dates.
