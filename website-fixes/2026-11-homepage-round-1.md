# Homepage Fixes, Round 1 (largohomebuyers.com)

Checked against the live homepage on 2026-11-20. Every "Find" below appears on that page exactly as written, so you can search for it and paste the replacement.

**What this round fixes**

1. Removes the wholesaling language and replaces it with a clear, true statement.
2. Replaces the press logo bar with real proof (title company, Sunbiz, Google reviews).
3. Makes the "7 days" and offer-timing promises match everywhere on the page.

## Before you start

- **Most of the homepage is Elementor "HTML" widgets.** Open the homepage in Elementor, click the HTML widget, press Ctrl+F (Cmd+F on a Mac) inside the code box, and search for the "Find" text.
- **The footer is site-wide.** The disclaimer lives in your footer template, so changing it once updates every page.
- **The meta description is in your SEO plugin**, which looks like Rank Math. It's under the homepage's "Edit Snippet" area.
- **Schema is in two places.** One block comes from Rank Math. The second one (LocalBusiness, services and FAQ) is custom code, probably in a code snippet or HTML widget. Where a change also appears in the schema, I've marked it **Also in schema**.
- **Back up first.** Use "Save as Template" in Elementor, or copy the HTML widget's code into a text file.

---

## Fix 1: Remove the wholesaling language

This assumes you buy houses yourselves and don't assign contracts to other investors. If that's ever not true, stop here and use the "disclose it" wording from our chat instead.

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
<p>Largo Home Buyers buys houses directly from homeowners. We buy through a company we own, so your closing papers may show that company's name instead of "Largo Home Buyers." We are the buyer, not a real estate agent, and we do not represent you in the sale. You are always welcome to have your own agent or attorney review our offer before you sign.</p>
```

**Only if one of you holds a Florida real estate license**, add this sentence to the end of that paragraph, with the right name filled in:
```html
[Name] holds a Florida real estate license and buys for our own company, not as your agent.
```

### 1c. Say it plainly in the "Who you are actually dealing with" bio

This puts the claim where sellers can read it, right next to "the person who walks your property is the person who signs the check."

**Find**
```html
<li style="margin-bottom:6px;">Between us we have purchased
```

**Replace with**
```html
<li style="margin-bottom:6px;">We are the buyer. We close in our own company's name, and we never put your house under contract just to sell that contract to someone else.</li><li style="margin-bottom:6px;">Between us we have purchased
```

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

1. Clear the SiteGround cache (SiteGround Optimizer, then Purge cache).
2. Look at the homepage on a phone and a computer. Check that the new trust boxes stack neatly on the phone.
3. Paste the homepage into Google's Rich Results Test to make sure the schema still reads cleanly after the edits.
4. In Search Console, use URL Inspection on the homepage and click "Request indexing."
5. Make sure your Google Business Profile description doesn't still say "close in 7 days" without the clear-title caveat.

## Next round (not done here)

- The "Rated #1 citations and local investor service" badge. Remove it, or name who rated you.
- "Open 24 hours, 7 days a week," while the page says "Come by" the office. Match it to your real hours and your Google Business Profile.
- The keyword titles on every image ("We buy houses for cash in largo 69" and so on).
- Typos: "Pascal county" (Pasco), "your facing," "a local guys running a company," "Trusted" mid-sentence, the empty H2, and the "~" marks around the locations heading.
- The menu links to `/sell-my-house-fast-largo/` and `/we-buy-houses-in-seminole/`, which both redirect. Link to the final pages instead.
- Rewriting the cliché lines in the top half ("curveball," "dignified path forward") in the voice of the timeline section.
