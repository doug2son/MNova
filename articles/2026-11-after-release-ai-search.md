# After the Release: Getting Found by AI Search

- **Link:** not saved yet (same source as the [first](2026-11-press-release-gbp-links.md) and [second](2026-11-second-release-and-tiers.md) press release notes)
- **Author / site:** 
- **Date published:** 
- **Date I read it:** November 2026
- **Tags:** Website, Ranking, Setup

## Verdict

**Keep (mostly).** This is the most useful part of the source so far.

Why: The core idea is sound. AI assistants like ChatGPT, Claude, and Gemini look things up on the web when they answer questions, and they lean on search engines to do it. If a business isn't listed on those search engines, or its website blocks their crawlers, it's much less likely to show up in AI answers. The setup steps here are free, low risk, and good practice anyway.

Two parts need care: whether press release pages actually get cited by AI (**test first**), and the "schema tactic" promised at the end (**wait and see**, see below).

## In a nutshell

- AI tools now act like search engines, and they can only use what they can find on the web.
- Plan ahead so AI tools can find the articles about the business, not only Google.
- ChatGPT leans on Bing, so list the business on Bing and submit the website there.
- Claude leans on Brave Search, so make sure the site can be found there.
- Check the web host's settings. Some hosts block AI crawlers by default.
- After the release, gather a list of every placement and its web address. The source says a "schema tactic" will get them indexed quickly and keep them indexed.

## What checks out

- **AI tools use search engines.** ChatGPT's search relies heavily on Bing. Claude's web search has used Brave Search. Gemini uses Google. These can change over time, so it's worth checking now and then.
- **Being on Bing matters.** Setting up Bing Places for Business and adding the site to Bing Webmaster Tools are both free and also help with regular Bing searches.
- **Hosting can quietly block crawlers.** This is real. Some hosts and services like Cloudflare can block AI crawlers by default, and some website plugins do too. If a crawler gets turned away, the AI tool can't read the page.

## Things to add that the source left out

- **Apple Business Connect.** This is Apple's version of a business profile. It feeds Apple Maps and Siri, so it's worth claiming too.
- **Training crawlers and search crawlers are different.** Each AI company has more than one crawler. Some gather data to train the AI, and others fetch pages to answer questions live. A business can block the training ones if it wants to and still allow the search ones. The search ones are what matter for being cited. Examples: OpenAI uses `OAI-SearchBot` and `ChatGPT-User` for search and `GPTBot` for training. Anthropic uses `Claude-SearchBot` and `Claude-User` for search and `ClaudeBot` for training. Check each company's own help pages for the current names.
- **Brave is harder to "submit" to.** As far as I know, Brave doesn't offer a sign up tool like Google Search Console or Bing Webmaster Tools. Getting into Brave mostly comes down to the site being open to crawlers and being linked from other places. Double check this, since it may have changed.
- **Use IndexNow.** Bing supports a free tool called IndexNow that tells it right away when a page is added or changed. Many website plugins turn it on with one click.

## About the "schema tactic"

The source hasn't shared it yet, so I can't judge it. But a warning ahead of time: schema (behind the scenes code that describes a page to search engines) does **not** make Google index a page, and Google says so plainly. If the tactic means adding links to press release pages inside the website's schema, for example in a `sameAs` field, that's a misuse. `sameAs` is meant for the business's own official profiles, like its Facebook page or its Google Business Profile, not for articles about it. Judge it once it arrives.

## Things I want to try

- [ ] Claim the business on Bing Places for Business
- [ ] Add the website to Bing Webmaster Tools and submit the sitemap
- [ ] Turn on IndexNow
- [ ] Claim the business on Apple Business Connect
- [ ] Check the site's robots.txt file and the host or Cloudflare settings to make sure AI search crawlers aren't blocked
- [ ] Ask ChatGPT, Claude, and Gemini about the business and its services, and write down what they say before and after these changes

## Questions or doubts

- Do AI tools actually cite reposted press release pages, or mostly real news coverage and the business's own site? Test it.
- What exactly is the schema tactic? Get the details before using it.
