# Homepage Fixes, Round 1 (largohomebuyers.com)

Checked against the live homepage on 2026-11-20. Every "Find" below appears on that page exactly as written, so you can search for it and paste the replacement.

> **Status: applied to the live site on 2026-11-20.** Everything below is now live on the homepage (page 1959), and the disclaimer is updated in the site-wide footer (template 362) too. The meta description was updated through Rank Math, and the Elementor and SiteGround caches were cleared. Backups of both pages from just before the change are in [`backups/2026-11-20-before-round-1/`](backups/2026-11-20-before-round-1/). The steps below stay as a record, and as instructions in case anything ever needs redoing by hand.
>
> **What came up while applying it**
> - The footer disclaimer was in two places: the homepage's own HTML box and the site-wide footer template that other pages use. Both were changed.
> - The footer now says "We are not acting as your real estate agent" instead of "We are not real estate agents," so it stays true even if a partner holds a license.
> - Rank Math's image settings change the capital letters in alt text ("Single-story florida home in largo") and add the "We buy houses for cash in largo 1, 2, 3..." titles to every image. Those titles are a Rank Math setting, not page content, so they're a next-round item.

**What this round fixes**

1. Removes the wholesaling language and replaces it with a clear, true statement. Also removes "the person who walks your property is the person who signs the check," which isn't always true, and softens the lines that say the business is only Doug and Matt.
2. Replaces the press logo bar with real proof (title company, Sunbiz, Google reviews).
3. Makes the "7 days" and offer-timing promises match everywhere on the page.

## Before you start

- **Most of the homepage is Elementor "HTML" widgets.** Open the homepage in Elementor, click the HTML widget, press Ctrl+F (Cmd+F on a Mac) inside the code box, and search for the "Find" text.
- **The disclaimer is in two places.** The homepage has its own copy inside its last HTML box, and the site-wide footer template (Templates, Theme Builder, Footer) has another for every other page. Change both.
- **The meta description is in your SEO plugin**, which looks like Rank Math. It's under the homepage's "Edit Snippet" area.
- **Schema is in two places.** One block comes from Rank Math. The second one (LocalBusiness, services and FAQ) is custom code, probably in a code snippet or HTML widget. Where a change also appears in the schema, I've marked it **Also in schema**.
- **Back up first.** Use "Save as Template" in Elementor, or copy the HTML widget's code into a text file.

---

## Fix 1: Remove the wholesaling language

This wording fits how you buy: in your business name (your LLC) or through one of your associated partners. On the rare deal that goes to someone else you know, tell the seller before they sign. That keeps the page true and protects your reviews.

### 1a. Hero image alt text

Alt text should describe the picture, not make a claim.

**Find**
```html
alt="Largo home buyers of residential properties not a wholesaler" title="We buy houses for cash in largo 2"
```

**Replace with**
```html
alt="Single-story Florida home in Largo"
```

### 1b. Footer disclaimer (site-wide)

The current footer says homes are "generally simultaneously resold as-is to a non-affiliated entity for a profit," which describes wholesaling. It's also template text about "licensed agents."

**Find** the whole paragraph that starts with:
```html
<p>*Licensed agents represent Largo Home Buyers
```
and ends with:
```html
licensed real estate agents, salespeople, or brokers at affiliated or unaffiliated brokerages.</p>
```

**Replace with**
```html
<p>Largo Home Buyers buys houses directly from homeowners. We buy in our business name (our LLC) or through one of our associated partners, so your closing papers may show that name instead of "Largo Home Buyers." We are not acting as your real estate agent, and we do not represent you in the sale. You are always welcome to have your own agent or attorney review our offer before you sign.</p>
```

**Only if one of you holds a Florida real estate license**, add this sentence to the end of that paragraph, with the right name filled in:
```html
[Name] holds a Florida real estate license and buys for our LLC or our associated partners, not as your agent.
```

### 1c. Say it plainly in the "Who you are actually dealing with" bio

This tells sellers who will be on the closing papers, in the bio where they can actually read it.

**Find**
```html
<li style="margin-bottom:6px;">Between us we have purchased
```

**Replace with**
```html
<li style="margin-bottom:6px;">We close in our business name (our LLC) or in the name of one of our associated partners.</li><li style="margin-bottom:6px;">Between us we have purchased
```

### 1d. Remove "the person who walks your property is the person who signs the check"

This isn't always true, so it comes out. It's the last sentence of the first paragraph in "Who you are actually dealing with," and it only appears there.

In the code, the sentence is split across line breaks, so search for this short piece, which sits on one line:
```text
the person who walks your property
```

Then delete the whole sentence, from "When you sell your" through "the check." Leave the `</p>` right after it in place. In the live code it looks like this:
```html
center and no acquisition rep who rotates out halfway through your file. When you sell your
 house fast in Largo through us, the person who walks your property is the person who signs
 the check.</p>
```

**Replace it with this true version**, which works with several partners:
```html
center and no acquisition rep who rotates out halfway through your file. Whichever of us walks your property, you are always dealing with an owner of the business.</p>
```

If you'd rather drop the idea completely, end the paragraph at "your file.</p>" instead.

### 1e. Doug and Matt lead, but there are more partners

Several lines say the business is only Doug and Matt. These changes keep them as the faces of the business without claiming they're the only two owners.

**Find**
```text
Largo Home Buyers is two people, Doug and Matt.
```
**Replace with**
```text
Largo Home Buyers is run by a small group of local partners, led by Doug and Matt.
```

**Find**
```text
We both live in Pinellas County and we answer our own phone.
```
**Replace with**
```text
Doug and Matt both live in Pinellas County, and we answer our own phone.
```

**Find** (near the top, under "Selling Your House Doesn't Have to Be Complicated")
```text
You work directly with Doug and Matt — real people who live and invest in this community.
```
**Replace with**
```text
You work directly with Doug, Matt and our partners, real people who live and invest in this community.
```

**FAQ: "Who buys houses for cash in Largo, FL?"** This also fixes the "a local guys running a company" typo.

**Find**
```text
is a local guys running a company that buys
```
**Replace with**
```text
is a locally owned company that buys
```

**Also in schema.** This next one appears twice, in the visible FAQ and in the FAQ schema, so replace both.

**Find**
```text
Doug and Matt, real people who live and invest here
```
**Replace with**
```text
a small group of local partners led by Doug and Matt, real people who live and invest here
```

**FAQ: "Why sell to Largo Home Buyers instead of a national company?"** **Also in schema**, so replace both.

**Find**
```text
Doug and Matt live and invest in Pinellas County, answer the phone themselves, and have helped
```
**Replace with**
```text
Doug, Matt and our partners invest in Pinellas County, answer the phone themselves, and have helped
```

**One thing only you can check**

- "Between us we have purchased more than 25 houses in Pinellas County since 2020." Make sure that number counts every partner's purchases, since "us" now means the whole group.

**Left as is, on purpose:** "Meet Doug (left) and Matt (right)," "Call Doug and Matt" in the search description, and the schema listing Doug and Matt as founders. Those are all still true.

---

## Fix 2: Replace the press logo bar

The current bar shows four "news" logos that all link to the same paid press release (article 864729847), plus an Outlook email logo that links to Gulfside Title. Sellers read a logo bar as "featured in the news," which this isn't.

**Find** the whole section. It starts with:
```html
<section class="lhb-w lhb-press">
```
and ends with the first `</section>` after it (just before `<section class="lhb-s"><h2 class="lhb-hd">Our Simple 3-Step Process</h2>`).

**Replace with**
```html
<section class="lhb-w" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:8px auto 12px;">
  <a href="https://gulfsidetitleservices.com/" target="_blank" rel="noopener" style="display:block;padding:16px 18px;border:1px solid #d9e2ec;border-radius:10px;background:#ffffff;color:#0f2b46;text-decoration:none;">
    <strong style="display:block;font-size:17px;margin-bottom:4px;">Gulfside Title Services</strong>
    <span style="font-size:15px;color:#52606d;">Every closing goes through this licensed local title company. Your money stays in escrow.</span>
  </a>
  <a href="https://dos.sunbiz.org/scripts/ficidet.exe?action=DETREG&amp;docnum=G25000115112&amp;rdocnum=G25000115112" target="_blank" rel="noopener" style="display:block;padding:16px 18px;border:1px solid #d9e2ec;border-radius:10px;background:#ffffff;color:#0f2b46;text-decoration:none;">
    <strong style="display:block;font-size:17px;margin-bottom:4px;">Registered on Sunbiz</strong>
    <span style="font-size:15px;color:#52606d;">Florida Division of Corporations, registration G25000115112. Look us up.</span>
  </a>
  <a href="https://www.google.com/maps/place/?cid=18410327459304036016" target="_blank" rel="noopener" style="display:block;padding:16px 18px;border:1px solid #d9e2ec;border-radius:10px;background:#ffffff;color:#0f2b46;text-decoration:none;">
    <strong style="display:block;font-size:17px;margin-bottom:4px;">Read our Google reviews</strong>
    <span style="font-size:15px;color:#52606d;">Check them on Google yourself, not just on our website.</span>
  </a>
</section>
<p style="text-align:center;font-size:14px;color:#52606d;margin:0 auto 24px;">We also shared a <a href="https://www.florida-observer.com/article/864729847-homeowners-can-now-sell-houses-in-any-condition-or-situation-with-largo-home-buyers" target="_blank" rel="nofollow noopener">press release</a> about how we work.</p>
```

The last line is optional. It keeps the press release, labeled for what it is. Delete it if you'd rather not mention it.

**After publishing, click all three boxes** to confirm the Sunbiz record and your Google profile open correctly. I couldn't open those two sites from here to test them.

---

## Fix 3: Make the timing promises match

Right now the page says "close in 7 days" at the top, "7 to 45 days" in the honest timeline section, and gives three different offer times (24 hours, 24 to 48 hours, and 24 hours after seeing the house).

**The two standard lines used below**

- **Offer:** within 24 to 48 hours of seeing your house.
- **Closing:** in as little as 7 days when the title is clear. Most homes close within three weeks.

If you reliably make offers within 24 hours, use "24 hours" everywhere instead. The point is to use one number.

### 3a. Meta description (Rank Math, homepage)

**Replace the current description with** (150 characters):
```text
Sell your Largo, FL house for cash, as-is. No repairs, no fees. Close in as little as 7 days when title is clear. Call Doug and Matt at (727) 500-1042
```
If you've set separate Facebook and X descriptions in Rank Math, update those too.

### 3b. Hero

**Find**
```html
Get a Fair Cash Offer in 24 Hours<br>Close in as little as 7 days
```
**Replace with**
```html
Fair Cash Offer in 24 to 48 Hours<br>Close in as little as 7 days with clear title
```

### 3c. Benefit icons

**Find**
```html
<h3>Close in 7 Days</h3>
```
**Replace with**
```html
<h3>Close on Your Date</h3>
```

### 3d. "Selling Your House Doesn't Have to Be Complicated" paragraph

**Find**
```text
can close in as little as 7 days with a fair offer.
```
**Replace with**
```text
can close in as little as 7 days when the title is clear.
```

### 3e. 3-step process

**Find**
```text
competitive cash offer within 24-48 hours
```
**Replace with**
```text
competitive cash offer within 24 to 48 hours of seeing it.
```

**Find**
```html
we can close in as little as 7 days, and you will have cash in hand! We use <span style="color:blue">Trusted Gulfside Title Services.</span>
```
**Replace with**
```html
we can close in as little as 7 days when the title is clear, and most homes close within three weeks. Every closing goes through <span style="color:blue">Gulfside Title Services</span>, a licensed local title company.
```

### 3f. "Compare Your Options" table

**Find**
```text
7–10 days</strong>
```
**Replace with**
```text
7 days to 3 weeks</strong>
```

**Find**
```text
Never</strong>
```
**Replace with**
```text
None, we pay cash</strong>
```

**Find**
```text
6% average
```
**Replace with**
```text
Often 5–6%
```

**Find**
```text
On a $300,000 Largo home, a 6% commission is $18,000 you keep.
```
**Replace with**
```text
On a $300,000 Largo home, a 6% commission is $18,000. Ask us and we will show you both numbers side by side: what you would likely net by listing, and what you net with our offer.
```

### 3g. FAQ: "How fast can I sell my house in Largo or Pinellas County?"

**Also in schema.** This answer appears twice, once in the visible FAQ and once in the FAQ schema. Change both so they match.

**Find**
```text
In most cases we can close in as little as 7 to 10 days.
```
**Replace with**
```text
If the title is clear, we can close in as little as 7 to 10 days. Liens, a second owner who has to sign, or an open probate add time, and we will tell you which applies on the first call.
```

**Find**
```text
We can give you a fair cash offer within 24 hours of seeing the property.
```
**Replace with**
```text
We will give you a fair cash offer within 24 to 48 hours of seeing the property.
```

### 3h. Service schema

**Also in schema.**

**Find**
```text
with a fair offer in 24 hours and closing
```
**Replace with**
```text
with a fair offer within 24 to 48 hours of seeing the house and closing
```

### Left as is, on purpose

- **The 4-step graphic.** It already says "24-48 hrs" and "as little as 7 days," which match.
- **The foreclosure block and the agent FAQ.** They say "often" and "as little as 7 to 10 days," which is fair.
- **The video schema.** It says "24 hours" because it describes what Doug says in the video. Change it only if the video changes.

---

## After you publish

1. Clear caches in this order: Elementor first (Elementor, Tools, Clear Files & Data), then load the homepage once, then purge SiteGround last (SiteGround Optimizer, Purge cache). Purging SiteGround before Elementor finishes rebuilding can leave a broken copy cached, which is what made the review stars look broken on 2026-11-20.
2. Look at the homepage on a phone and a computer. Check that the new trust boxes stack neatly on the phone.
3. Paste the homepage into Google's Rich Results Test to make sure the schema still reads cleanly after the edits.
4. In Search Console, use URL Inspection on the homepage and click "Request indexing."
5. Make sure your Google Business Profile description doesn't still say "close in 7 days" without the clear-title caveat.

## Next round (not done here)

- The "Rated #1 citations and local investor service" badge. Remove it, or name who rated you.
- "Open 24 hours, 7 days a week," while the page says "Come by" the office. Match it to your real hours and your Google Business Profile.
- The keyword titles on every image ("We buy houses for cash in largo 69" and so on). These come from Rank Math's image SEO settings (the "add missing title" option), so the fix is in Rank Math, not on the page.
- Typos: "Pascal county" (Pasco), "your facing," "a local guys running a company," "Trusted" mid-sentence, the empty H2, and the "~" marks around the locations heading.
- The menu links to `/sell-my-house-fast-largo/` and `/we-buy-houses-in-seminole/`, which both redirect. Link to the final pages instead.
- Rewriting the cliché lines in the top half ("curveball," "dignified path forward") in the voice of the timeline section.
