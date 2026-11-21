# Working notes for Claude

Read this first. It carries what earlier sessions learned, so nothing has to be re-explained.

## How I like to work

- Write in plain, natural language, not technical writing.
- Don't use em-dashes.
- Every business gets its own Claude session. Don't mix work for two businesses in one session.
- The goal is better rankings for real businesses. Fix things on the live site when allowed; don't stop at reports.
- Ask before changing a live website. Back up a page before editing it, and log every change.

## What this repo is

- Notes on Google Business Profiles and website SEO: `articles/`, `checklists/`, `ideas/`, `how-i-judge-advice.md` (what advice I keep, test or trash).
- `audits/<business>/`: crawl data and findings for each business site.
- `xrseo/`: the XRSEO audit kit (see below).

## AEOXR and XRSEO

- AEOXR is my brand (logo files are in `D:\AEOXR\LOGOS` on my PC). Spelling to confirm: the folder says AEOXR, I once wrote AEXOR.
- XRSEO is AEOXR's website SEO audit process, built from the 30-move playbook in `articles/2026-11-thirty-seo-moves.md` and tracked in `checklists/website-seo-30-moves.md`.
- Two modes:
  - **Quick scan:** crawl only. Used as a lead magnet report for prospects.
  - **Full audit:** uses Search Console and analytics, covers all 30 moves, and includes monthly measurement for clients.
- Reports are branded AEOXR, never with a client's logo.

### Kit status (Nov 21, 2026)

- Done:
  - `xrseo/scripts/crawl.py`: crawls any site politely and obeys robots.txt.
  - `xrseo/scripts/analyze_crawl.py`: turns a crawl into findings.json with a pass/warn/fail checklist.
  - `xrseo/scripts/screenshots.js` and `xrseo/scripts/to_pdf.js`.
- In progress: the topic-overlap check groups pages on generic words, so it needs a better rule. Ignoring words found on more than 20% of pages helped.
- To do:
  - Report template and builder, with AEOXR branding.
  - `SKILL.md` and the reference files (rules, moves, intake checklist).
  - Package the skill so it can be uploaded to Claude.
  - Later: Search Console analysis scripts, monthly report and change log.

## Businesses

| Business | Site | Status |
| --- | --- | --- |
| Largo Home Buyers | largohomebuyers.com | A real, live site. It has its own session ("Largo Home Buyers: SEO fixes"). Findings are in `audits/largohomebuyers/2026-11-crawl-findings.md`. The first batch of fixes is waiting for my go. Duplicate-page merges wait for Search Console data. |

Other businesses in my accounts: Alternative Realization Hypnotherapy, Lincoln Hypnosis Center, Advanced Medical Weight Loss and Wellness Center, RateM.

## Lessons from earlier sessions

- largohomebuyers.com blocks unknown crawlers, so crawl with a normal browser user agent.
- The long name "Largo Home Buyers We Are Personal and Honest" is the WordPress site title (the website name in schema). The business name in schema is already correct.
- Cloud sessions started from the phone can't see files on my PC. Use Google Drive or a desktop session for local files.
