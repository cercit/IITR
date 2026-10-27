# One-Page Research Plan: Blinkit — Why Do Users Abandon Full Carts?

## Business question

Blinkit's funnel data likely shows users adding 4+ items to the cart and then leaving without placing the order. The question: **what is causing cart abandonment among users who have already committed to building a basket?**

This is not about users who browse and leave. Those users never signalled purchase intent. The interesting cohort is the one that did the work of selecting items, got to the finish line, and stopped.

## What secondary research would tell me first

Before talking to anyone, I'd pull from three sources:

**Internal data (if I were on the team):**
- Cart abandonment rate segmented by basket size, time of day, and delivery ETA shown at checkout
- Drop-off point in the checkout flow — do users leave at the cart screen, the address screen, or the payment screen?
- Correlation between delivery fee display and exit rate
- Surge pricing or "busy slot" frequency during peak abandonment windows

**App store reviews (public, available now):**
- Scan 100 recent 1-star and 2-star Play Store reviews for complaints mentioning cart, checkout, pricing, or delivery
- Common patterns I'd expect to find: "prices higher than store", "delivery fee too high for small orders", "items went out of stock while I was shopping", "ETA changed after I added items"

**Competitor behaviour:**
- How Zepto and Swiggy Instamart handle delivery fees, minimum order thresholds, and out-of-stock replacements at checkout
- Whether competitors show final price (including fees) earlier in the flow

## Hypothesis

**Users who build a basket of 4+ items and abandon do so primarily because the total at checkout — after delivery fee, handling charge, and platform fee — is meaningfully higher than what they expected while browsing.**

The gap between perceived price (item prices while browsing) and actual price (total at checkout with fees stacked) creates a moment of sticker shock that kills the order.

## Target cohort

Users who:
- Have placed at least 3 orders on Blinkit in the past 60 days (not new, not churned — active users who know the product)
- Have abandoned a cart with 4+ items at least once in the past 30 days
- Are in Tier 1 cities where Blinkit operates at full density

Excluding: users on Blinkit Pass (they already pay a subscription that waives delivery fees, so the fee-shock hypothesis doesn't apply to them the same way).

## Two primary research methods

**Method 1: Survey (quantitative, 600+ respondents from the cohort above)**

One key question, designed to invalidate:

> "Think about the last time you added items to your Blinkit cart but did not place the order. What was the main reason you stopped?"
>
> - I found the same items cheaper elsewhere
> - The total at checkout was higher than I expected
> - An item I wanted was out of stock or substituted
> - The delivery time was too long
> - I was just browsing and not planning to buy
> - My reason is not listed here

If "I was just browsing" or "out of stock" dominates and the pricing option gets under 20%, my hypothesis is dead. The problem is inventory or intent, not pricing. Different solution entirely.

**Method 2: 1:1 interviews (qualitative, 8 users from the cohort)**

Goal: understand the emotional sequence at checkout. Not "what features do you want" — but "walk me through the last time you left without ordering."

Key questions:
1. "Tell me about the last time you opened Blinkit and added things to your cart but didn't order."
2. "At what point did you decide not to go through with it?"
3. "What did you do instead — did you buy those items somewhere else, or skip them entirely?"

I'm listening for: the moment of hesitation, whether they did mental math, whether they compared to a kirana store or BigBasket price, and whether the decision was rational (too expensive) or emotional (felt nickel-and-dimed).

## What result kills the idea

If the survey shows that fewer than 25% of abandoning users cite price-related reasons, and the interviews reveal that the dominant pattern is stockouts or "just browsing", then the checkout pricing hypothesis is wrong. The fix is upstream — in catalogue reliability or in how the app handles browse-mode users — not in fee transparency at checkout.

## What a positive result leads to

If pricing shock is confirmed, the next step is an A/B test: show the running total including all fees as items are added to the cart (variant B) versus the current flow where fees appear only at checkout (variant A). Metric: cart-to-order conversion rate. Run on 20,000 users per group, then flip the cohorts.
