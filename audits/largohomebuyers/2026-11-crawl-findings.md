# Largo Home Buyers: Crawl Findings (Nov 21, 2026)

This covers the moves from the [30 moves checklist](../../checklists/website-seo-30-moves.md) that only need a crawl of the site. Anything that needs Search Console is marked as waiting.

- **What was crawled:** every URL in the sitemap, plus every page those link to. 128 URLs in total: 105 live pages, 16 redirects and 7 broken links.
- **Indexable pages:** 55 (the other 50 are tag pages and calculators set to noindex, which is fine).
- **Raw data:** [`data/crawl.csv`](data/crawl.csv) has one row per page and [`data/links.csv`](data/links.csv) has every internal link. Rerun it any time with [`../tools/crawl.py`](../tools/crawl.py).
- **Word counts** are the main page area, without the menu and footer. They're close, but treat them as estimates.

## The short list: what to fix first

| # | Fix | Why it matters | Time |
| --- | --- | --- | --- |
| 1 | Change the WordPress site title to just "Largo Home Buyers" | The site title is "Largo Home Buyers We Are Personal and Honest". It's added to 47 page titles, pushing 39 of them over 60 characters, and it's also the business name in the site's schema. It should match the Google Business Profile name exactly. | 15 min |
| 2 | Fix 20 broken links and 61 links that go through old redirects | 81 links on 28 pages point at old or dead URLs. The 20 broken ones (7 dead URLs) are dead ends for visitors and for Google. | 1 to 2 hours |
| 3 | Link to 6 pages that nothing on the site links to | Apartment buildings, tax liens, Harbor Bluffs, both Largo Central Park pages, and the Locations page can only be found through the sitemap. | 1 hour |
| 4 | On the homepage, link Harbor Bluffs and Largo Central Park to our own pages, not homes.com | The homepage names both neighborhoods but sends visitors to homes.com neighborhood guides instead of our own pages for them. | 15 min |
| 5 | Pick one Largo Central Park page and redirect the other to it | Two pages target the same neighborhood. Neither has a single internal link. | 30 min |
| 6 | Clean up the extra Clearwater page | `/we-buy-houses-clearwater-org-page/sell-my-house-for-cash-clearwater/` is a second Clearwater page that's live and indexable. Also, one post links to `/we-buy-houses-clearwater/.` (with a stray dot). | 30 min |
| 7 | Set category pages to noindex | 9 category pages are indexable but have no heading, no description, and nothing links to them. Tag pages are already noindex, so this matches them. | 15 min |
| 8 | Fix doubled and missing H1 headings | 8 pages repeat their main heading twice ("Title \| Title") and 3 have none. | 1 hour |

Do 1, 2, 3 and 4 first. They're quick, safe, and don't depend on Search Console. Wait on 5 and the groups in move 7 until Search Console shows which page Google already prefers.

---

## Move 5: Indexing problems

Nothing important is blocked. Every money page returns 200, is set to index, and has a canonical pointing to itself. robots.txt allows Google and the AI crawlers. The problems are links pointing at the wrong places.

### Broken links (404)

| Broken URL | Linked from | Change the link to |
| --- | --- | --- |
| `/we-buy-houses-in-largo/` | 14 links on 10 pages, including both 10 reasons posts and cash-home-buyer-in-pinellas-county-2026 | `/` (the homepage is the Largo page) |
| `/we-buy-houses-st-petersburg-fl/` | companies-that-buy-houses-for-cash post | `/we-buy-houses-st-petersburg/` |
| `/inherited-property` | house-clearance-service | `/sell-my-inherited-house-in-largo/` |
| `/sell-rental-property` | house-clearance-service | `/sell-rental-fast-largo/` |
| `/stop-foreclosure` | house-clearance-service | `/foreclosure-service/` (or the winner from move 7) |
| `/cash-offer` | house-clearance-service | `/contact-us/` |
| `/no-commissions` | house-clearance-service | Remove the link, or point it to `/` |

The House Clearance page alone has 5 of the 7 dead URLs. It looks like it was written with placeholder links that were never updated.

### Links that go through a redirect

These still work, but each one goes through an extra hop. Change each link to the final URL.

| Old URL in the link | Goes to | Links |
| --- | --- | --- |
| `/sell-my-house-fast-largo/` | `/` | 11 |
| `/we-buy-houses-as-is/` | `/we-buy-houses-as-is-in-pinellas-county/` | 7 |
| `/sell-my-inherited-house-in-largo-fast-what-you-need-to-know/` | `/sell-my-inherited-house-in-largo/` | 7 |
| `/we-buy-houses-dunedin-fl/` | `/` | 8 |
| `/sell-your-house-in-largo/` | `/` | 5 |
| `/we-buy-houses-in-seminole/` | `/sell-my-house-fast-seminole-fl/` | 4 |
| `/cash-home-buyer-largo/` | `/cash-home-buyer-in-pinellas-county-2026/` | 4 (all on the Podcast page) |
| `/sell-my-house-fast-largo/we-buy-houses-for-cash-in-largo/` | `/` | 3 |
| `/the-complete-florida-probate-process-guide-for-heirs-2026-edition/` | `/the-complete-florida-probate-process-guide-for-heirs/` | 3 |
| `/we-buy-houses-clearwater/sell-my-house-for-cash-clearwater/` | the extra Clearwater page (see fix 6) | 2 |
| 6 other old URLs (including `/contact`) | various | 7 |

Things to check while fixing these:

- **Dunedin:** 8 links promise a Dunedin page, but it redirects to the homepage. On cash-home-buyer-in-pinellas-county-2026, the links even sit on step headings ("3. We Make You an Offer"). Either build a Dunedin page later (move 28) or change the link text so it doesn't promise one.
- **Podcast page:** the 4 links with titles like "How To Detect and Avoid Scams" all go to the cash home buyer page. Those look like episode links that were pointed at the wrong place.

The full list, with every source page and anchor text, is in [`data/links.csv`](data/links.csv).

---

## Move 6: Template problems (fix once, fixes many pages)

| Problem | Pages | One-time fix |
| --- | --- | --- |
| Site title "Largo Home Buyers We Are Personal and Honest" added to every title | 47 | WordPress > Settings > General > Site Title: `Largo Home Buyers`. Move "We Are Personal and Honest" to the Tagline field. Then check Rank Math > Titles & Meta > Global Meta, where the title format should be `%title% %sep% %sitename%`. |
| The same long name is the Organization name in the site's schema | All | Fixed by the step above. Then check Rank Math > Titles & Meta > Local SEO, where the name should be `Largo Home Buyers`, matching the GBP exactly. |
| Category pages are indexable with no heading or description | 9 | Rank Math > Titles & Meta > Categories > Robots Meta: No Index. This removes them from the sitemap too. |
| Main heading appears twice ("Title \| Title") | 8: mobile home guide, inherited Pinellas post, Spanish post, real estate investor post, apartment building, sell for cash in Largo post, sell my inherited house, Orange Lake Village post | The theme's page title and an Elementor heading are both H1. Hide the theme title on Elementor pages (Elementor > Site Settings > Layout > "Hide Title") or change the Elementor heading to H2. |
| No main heading (H1) | companies-that-buy-houses-for-cash post, Blog, Privacy Policy | Add an H1 at the top of each. The post is the one that matters. |
| Missing or very short meta descriptions | Categories (none), Contact (36 characters), Blog (31), Podcast (43), cash-home-buyer-in-pinellas-county-2026 (43) | Write a 110 to 160 character description for Contact and the cash home buyer page. The rest don't matter much. |

Good news on templates: every image has alt text, every page has a canonical, and the schema is in place sitewide.

---

## Move 7: Pages that probably compete with each other

**This needs Search Console to confirm.** File 2 shows which pages actually get impressions for the same search. Until then, these are groups of pages that target the same thing, based on titles, headings and URLs.

| Topic | Pages | First thought |
| --- | --- | --- |
| Largo Central Park | `/sell-my-house-fast-largo-central-park/` (1,006 words) and `/sell-my-house-fast-near-largo-central-park/` (744 words) | Clear duplicate. Keep one, 301 the other. If Search Console shows no clicks on either, keep the longer one and move the FAQ from the other into it. |
| Clearwater | `/we-buy-houses-clearwater/`, `/we-buy-houses-clearwater-org-page/sell-my-house-for-cash-clearwater/` (1,966 words, indexable, not in the sitemap), and `/we-buy-houses-clearwater/.` | Keep `/we-buy-houses-clearwater/`. Move anything useful from the org-page version into it, then 301 the org page. |
| Foreclosure | `/foreclosure-service/`, `/foreclosure-service-stop-foreclosure-fast/`, `/pre-foreclosure-largo/` | Three pages for one worry. Probably keep one service page plus the pre-foreclosure guide, and merge the "stop foreclosure fast" page. Wait for the data. |
| Inherited house | `/sell-my-inherited-house-in-largo/` (money page), `/how-to-sell-an-inherited-house-in-largo-a-local-guide-to-probate/`, `/how-to-sell-your-inherited-house-in-pinellas-county/` (488 words), `/inherited-a-house-here-is-what-to-do-next/`, plus the probate guide | The highest-risk group. The money page should win "sell inherited house Largo". Guides should target the questions instead (what to do first, how probate works). The 488-word Pinellas post is the most likely to merge. |
| Trust | `/sell-house-in-trust-largo/` and `/how-to-set-up-a-trust-to-sell-a-home-in-florida/` | The second page's title ("How We Put a Florida House in a Trust to Sell in Largo") overlaps the first. Retitle it to match its URL: setting up a trust, not selling from one. |
| Largo cash buyer | Homepage, `/sell-my-house-for-cash-in-largo-fast-stress-free-options-with-largo-home-buyers/`, `/real-estate-investor-in-largo-fl-how-largo-home-buyers-helps-you-sell-fast-for-cash/`, `/companies-that-buy-houses-for-cash-what-homeowners-in-largo-need-to-know/`, both 10 reasons posts, `/cash-home-buyer-in-pinellas-county-2026/` | Seven pages that could all show up for "sell my house for cash Largo". The homepage must win. Search Console will show whether any post is stealing impressions from it. |

---

## Move 3 and 9: Who actually shows up

From web searches for "we buy houses Largo FL", "sell inherited house Largo FL cash", "we buy houses Clearwater FL", "we buy houses St Petersburg FL cash" and "sell my house fast Seminole FL".

**Warning from the article, and it applies here:** web search isn't Google's real top 10. Tomorrow, Google the 5 biggest searches in a private window and paste the top 10 URLs into the chat.

**What showed up:**

- **Directories and list posts dominate every search:** HomeLight ("6 Top We Buy Houses for Cash Companies in Largo"), ListWithClever, BBB, Houzeo, plus big national brands (Opendoor, Offerpad).
- **Local or real competitors:** New Again Houses (Clearwater, St. Pete), We Buy Ugly Houses St. Petersburg (a franchise), HouseCashin (matches sellers with investors), "We Buy St Pete Houses", Pinellas Cash Buyers, and a Largo probate page on `quickofferhomesfl1.pages.dev`.
- **Our own press releases** show up for "we buy houses Largo" (EIN Presswire) and for "sell inherited house Largo" (National Law Review). The press releases are getting seen, which ties back to the [press release notes](../../checklists/press-release-plan.md).

**What this means, using the article's rule:** when most results are directories, building links to our page is the wrong fix. The fix is getting onto those directories and lists:

- [ ] Check whether we're listed on ListWithClever for Largo, Clearwater and St. Pete. Claim or update the listing.
- [ ] Check whether we have a BBB profile in the Largo "Home Buyers" category.
- [ ] HomeLight and Houzeo "top companies" posts are written by their editors. See whether they take suggestions or updates.

---

## Move 11: Thin pages (our side only)

Competitor pages couldn't be fetched from this environment, so the comparison with the top 3 has to happen on desktop. Our own numbers:

| Money page | Words |
| --- | --- |
| Sell my inherited house in Largo | 6,995 |
| Homepage | 4,379 |
| St. Petersburg | 3,908 |
| As-is in Pinellas County | 3,604 |
| Seminole | 2,174 |
| Clearwater | 1,471 |
| Foreclosure service | 1,564 |
| House clearance | 1,424 |
| Tax liens | 830 |
| Harbor Bluffs | 764 |
| Largo Central Park (two pages) | 1,006 and 744 |
| Property investment company | 186 |
| About | 285 |

The big money pages are not thin. If anything, the 7,000-word inherited page may be too long for someone who just wants an offer. Checking it against the top 3 will tell. The pages to watch are Property Investment Company (186 words) and the neighborhood pages.

---

## Move 14: The first screen of money pages

I looked at the first screen of 6 money pages on a laptop-size screen.

**Working well:**

- **Homepage:** the headline answers the search ("Sell Your House Fast For Cash in Largo"). The first screen also has the offer form, phone number, star rating, and what's included (no fees, no repairs, no closing costs, close on your date).
- **Inherited page:** same layout, also strong.

**To fix:**

- **The promises don't match.** The homepage says "offer in 24 to 48 hours, close in as little as 7 days". The as-is Pinellas page says "offer in about 24 hours, close in as little as 10 days". Pick one set of numbers and use it everywhere.
- **The as-is Pinellas page has no form or button on the first screen.** It opens with a big photo heading, then text. Add the same offer form or a "Get My Cash Offer" button near the top.
- **Check the "#1 Local House Buyer, Florida Real Estate Reporter" badge on the homepage.** If it came from a paid placement, it falls under the "As seen on" rule in my [trash list](../../how-i-judge-advice.md). Keep it only if it was earned.
- **Nothing says what kind of offer to expect.** That means a price, or "most offers are X% of after-repair value", or an example deal. This is the move 14 item most often missing on buying pages. Add it if you're comfortable sharing it.

---

## Move 15: Near-duplicate pages

Very little text is copied between pages. The only real copy is the Clearwater page and its stray-dot twin. The problem on this site isn't copied text, it's **several pages on the same topic** (see move 7). The area pages (Clearwater, St. Pete, Seminole) share about 28% of their text, which is normal for a shared template.

---

## Moves 16, 17 and 18: Internal links

The median indexable page gets **2** links from other pages' main content. The menu and footer add more, but those are the same on every page.

### Pages with zero links from anywhere on the site

| Page | Words | Notes |
| --- | --- | --- |
| `/sell-my-apartment-building-in-largo/` | 2,471 | |
| `/tax-liens-back-taxes-largo/` | 830 | |
| `/sell-my-house-fast-harbor-bluffs/` | 764 | The homepage names Harbor Bluffs but links it to homes.com |
| `/sell-my-house-fast-largo-central-park/` | 1,006 | Same, homes.com |
| `/sell-my-house-fast-near-largo-central-park/` | 744 | Duplicate (move 7) |
| `/locations/` | 155 | The "Locations" menu item opens a dropdown but doesn't link to this page |

### Pages only reached through old redirect links

These pages get links, but only through old URLs that redirect. Fixing the redirect links in move 5 fixes these:

- `/we-buy-houses-as-is-in-pinellas-county/` (7 links via `/we-buy-houses-as-is/`)
- `/cash-home-buyer-in-pinellas-county-2026/` (4 links via `/cash-home-buyer-largo/`)
- `/sell-my-inherited-house-in-largo/`: only 2 direct links from content, plus 8 through old URLs

### Links to add (move 17)

The link text describes the page it goes to. Never use "click here", and never put a link inside a heading.

**To the apartment building page**

| Add on | Sentence | Link text |
| --- | --- | --- |
| `/sell-rental-fast-largo/` | "Own more than a single rental? We also buy apartment buildings in Largo as-is, tenants and all." | apartment buildings in Largo |
| `/property-investment-company/` | "That includes small multifamily properties. See how we buy apartment buildings in Largo." | buy apartment buildings in Largo |
| `/real-estate-investor-in-largo-fl-how-largo-home-buyers-helps-you-sell-fast-for-cash/` | Where it mentions apartments: "If you own a multifamily property, here's how selling an apartment building in Largo works." | selling an apartment building in Largo |
| `/out-of-state-owners-with-vacant-homes-in-largo-remote-cash-sale-made-simple/` | "Managing a whole building from out of state? We also buy apartment buildings in Largo." | apartment buildings in Largo |

**To the tax liens page**

| Add on | Sentence | Link text |
| --- | --- | --- |
| `/sell-my-inherited-house-in-largo/` | In the paragraph that mentions tax liens being paid at closing: "Here's more on selling a house with tax liens or back taxes in Largo." | tax liens or back taxes in Largo |
| `/pre-foreclosure-largo/` | "Behind on property taxes too? See how we handle tax liens and back taxes." | tax liens and back taxes |
| `/foreclosure-service/` | "A tax lien can lead to losing the house just like a missed mortgage. Here's what to do about back taxes in Largo." | back taxes in Largo |
| `/out-of-state-owners-with-vacant-homes-in-largo-remote-cash-sale-made-simple/` | "Vacant homes often fall behind on taxes. Learn how to sell a Largo house with back taxes owed." | sell a Largo house with back taxes owed |
| `/how-to-sell-an-inherited-house-in-largo-a-local-guide-to-probate/` | "If the estate owes property taxes, read our guide to tax liens and back taxes in Largo." | tax liens and back taxes in Largo |

**To Harbor Bluffs and Largo Central Park**

| Add on | Change | Link text |
| --- | --- | --- |
| Homepage | Point "Harbor Bluffs" and "Largo Central Park" in the areas list to our own pages instead of homes.com | Harbor Bluffs / Largo Central Park |
| `/locations/` | List every area page with a link | the neighborhood name |
| `/we-buy-houses-as-is-in-pinellas-county/` | This page lists the areas we buy in. Link each one to its page. | the area name |
| `/hoarder-homes-largo/`, `/pre-foreclosure-largo/`, `/sell-house-in-trust-largo/` | These already mention Harbor Bluffs in the text. Link that mention. | Harbor Bluffs |

**To the Locations page:** make the "Locations" menu item itself link to `/locations/`, and link to it from the footer.

### Guides and money pages (move 18)

| Guide | Should link to | Links now? |
| --- | --- | --- |
| Inherited guides (local probate guide, Pinellas post, "inherited a house" post, probate guide) | `/sell-my-inherited-house-in-largo/` | Only through old redirect URLs. Fix the URLs. |
| `/pre-foreclosure-largo/` | `/foreclosure-service/` (or the move 7 winner) | No |
| Both trust guides | `/sell-my-inherited-house-in-largo/` (trusts often come with an inheritance) | No |
| `/sell-rental-fast-largo/` | Apartment building page | No |
| `/hoarder-homes-largo/` | `/house-clearance-service/` | No |
| `/how-do-we-get-rid-of-a-mobile-home-a-practical-guide-for-owners/` | Homepage or as-is page | Only through a redirect |

| Money page | Should link back to | Links now? |
| --- | --- | --- |
| `/sell-my-inherited-house-in-largo/` | The probate guide and the local probate guide | Only the 488-word Pinellas post |
| `/foreclosure-service/` | `/pre-foreclosure-largo/` | No |
| `/house-clearance-service/` | `/hoarder-homes-largo/` | No |
| Clearwater, St. Pete, Seminole | 1 or 2 of the guides most useful to sellers there (inherited, foreclosure) | St. Pete links the probate guide. The others don't. |

---

## Move 21: Refresh list

It's late November. In about six weeks every "2026" in a title looks a year old.

| Page | What's dated | When |
| --- | --- | --- |
| `/cash-home-buyer-in-pinellas-county-2026/` | "2026" in the title, H1 **and URL** | January. Change the title and H1, but leave the URL alone. Changing it means another redirect. |
| `/the-complete-florida-probate-process-guide-for-heirs/` | "(2026)" and "2026 Edition", plus 26 years, prices or percentages in the text | January. Recheck Florida probate fees and timelines. |
| `/sell-house-in-trust-largo/` | "(2026)" in the title | January |
| `/how-to-set-up-a-trust-to-sell-a-home-in-florida/` | "2026 Guide" in the title | January |
| `/real-estate-consultant/`, `/we-buy-houses-as-is-in-pinellas-county/`, `/we-buy-houses-st-petersburg/`, `/sell-my-inherited-house-in-largo/`, homepage | Many prices, percentages or years in the text | Once a year. Check every number. |

---

## Move 23: Titles and H1s

Fixing the site title (fix 1) takes care of most of the length problems. For the money pages, here are suggested titles. Confirm the main keyword with move 2 once Search Console is in.

| Page | Suggested title | Characters |
| --- | --- | --- |
| `/sell-my-inherited-house-in-largo/` | Sell an Inherited House in Largo for Cash \| Largo Home Buyers | 60 |
| `/we-buy-houses-clearwater/` | We Buy Houses Clearwater FL for Cash \| Largo Home Buyers | 56 |
| `/we-buy-houses-st-petersburg/` | We Buy Houses St. Petersburg FL for Cash \| Largo Home Buyers | 60 |
| `/sell-my-house-fast-seminole-fl/` | Sell My House Fast Seminole FL \| Largo Home Buyers | 51 |
| `/we-buy-houses-as-is-in-pinellas-county/` | We Buy Houses As-Is in Pinellas County \| Largo Home Buyers | 58 |
| `/tax-liens-back-taxes-largo/` | Tax Liens and Back Taxes in Largo: Sell Your House As-Is | 56 |
| `/sell-my-apartment-building-in-largo/` | Sell My Apartment Building in Largo for Cash, As-Is | 51 |
| `/house-clearance-service/` | House Clearance Service in Largo: Sell As-Is, We Clean Out | 58 |
| `/cash-home-buyer-in-pinellas-county-2026/` | Cash Home Buyer in Pinellas County \| Largo Home Buyers | 54 |
| `/companies-that-buy-houses-for-cash-what-homeowners-in-largo-need-to-know/` | Companies That Buy Houses for Cash in Largo: What to Know | 57 |
| `/how-to-sell-an-inherited-house-in-largo-a-local-guide-to-probate/` | How to Sell an Inherited House in Largo: Probate Guide | 54 |
| `/out-of-state-owners-with-vacant-homes-in-largo-remote-cash-sale-made-simple/` | Out-of-State Owner? Sell Your Vacant Largo Home for Cash | 56 |

The homepage title (57 characters) is already good. Leave it.

---

## For tomorrow on desktop

1. Connect Search Console in Windsor.ai (`searchconsole` connector), or export Files 1 to 4 by hand.
2. Export Search Console > Indexing > Pages, once for each reason a page isn't indexed.
3. Write the one page of business notes, especially the 10 questions sellers ask.
4. Google the 5 biggest searches in a private window and save the top 10 URLs.
5. Then run moves 1, 2, 4, 7 and 8. Move 7 decides the Central Park, foreclosure and inherited-page questions above.
6. Start a change log before making any of the fixes, so move 30 can measure them.
