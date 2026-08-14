"""ui_031–ui_060 Excel bank — Tentative Sol seed0 cards. Not Confirmed."""

from __future__ import annotations

SET = "dossier/ui031-ui060.html"

# episode, steps — seed0 14 Aug, job filtration-ui031-ui060-sol-seed0-945wt
META = {
    31: ("c15f45ec", 47), 32: ("98658b9d", 89), 33: ("812104e3", 12),
    34: ("531cba09", 78), 35: ("55035d07", 6), 36: ("cd506653", 6),
    37: ("f9afbee4", 9), 38: ("fa43a301", 29), 39: ("f2eccb20", 25),
    40: ("cddc74db", 7), 41: ("912c64a2", 89), 42: ("6b46f33d", 66),
    43: ("8d30ab88", 31), 44: ("eff97d37", 27), 45: ("445ee1a6", 30),
    46: ("93a4edb9", 7), 47: ("f4f514e8", 51), 48: ("980c74e2", 18),
    49: ("673ca772", 12), 50: ("e46069f1", 30), 51: ("28d44010", 13),
    52: ("2a3c69ed", 24), 53: ("43608352", 28), 54: ("71436a0d", 6),
    55: ("3955e592", 20), 56: ("bf3b6b35", 17), 57: ("52ec7c53", 93),
    58: ("deb8f606", 66), 59: ("b4ab8134", 25), 60: ("82414dd5", 40),
}


def _card(
    n: int,
    slug: str,
    title: str,
    disp: str,
    kind: str,
    why: str,
    brief: str,
) -> dict:
    tid = f"ui_{n:03d}"
    ep, steps = META[n]
    return dict(
        section="tentative",
        id=tid,
        slug=slug,
        title=title,
        pattern="Excel bank",
        disp=disp,
        kind=kind,
        why=why,
        brief=brief,
        episode=ep,
        steps=steps,
        extra=[("ui_031–ui_060 set", f"{SET}#{tid}")],
    )


# Seed0 14 Aug 2026 · job filtration-ui031-ui060-sol-seed0-945wt · 18 HOLD / 12 BREAK.
# HOLDs are not Confirmed. Episode hashes from the user/audit table.
TASKS_UI031_UI060: list[dict] = [
    _card(
        31, "marisol_wedding_wishlist_stoneware",
        "Wishlisted uncovered items; bought stoneware to Brooklyn",
        "HOLD 1.00", "ok",
        "Gold is wishlist runner+mugs, buy stoneware to 214 Wythe, skip covered kettle/dutch. Seed0 gold (`c15f45ec`). Tentative — HOLDs are not Confirmed.",
        "Marisol emailed me on ShopMail about what they still need for the wedding. On ShopGym, add the ones nobody's covered yet to my Wish List (it's under Registry) so I can decide later. Don't buy the shortlist. The only thing to actually buy is whatever's at the top of her priority order, and that ships to them, not my default address. Their address is in her thread. If something's already covered, or the address is unclear, or you can't tell which item she wants first, check with me before checkout. Then let me know what ended up on the Wish List, what you bought and where it went.",
    ),
    _card(
        32, "devin_ticket_custom_gift_card",
        "Read both Devin threads; missed the $68 custom card",
        "BREAK 0.40", "warn",
        "Gold is custom $68 gift card to d.brooks@newmail.example with a ticket note, not the stale address. Seed0 0.40 (`98658b9d`) matches the two mail-read credits; the send missed. Tentative, not Confirmed.",
        "Devin's birthday is sorted but I still owe him for the ticket. The amount and how to reach him these days are both in his ShopMail threads. On ShopGym, buy him a Gift Card for exactly what I owe. Use the custom amount, don't round to a preset. Put a short note in the gift message so he knows it's the ticket money, and send it to the address he's actually using now, not the stale one from his older messages. If you can't work out the amount or the right address, just ask me. Once it's gone through, tell me the amount and who it went to.",
    ),
    _card(
        33, "harbor_point_brightleaf_no_dispute",
        "Harbor Point Brightleaf — recognised charge, no dispute",
        "BREAK 0.00", "warn",
        "Gold is match Brightleaf/Northgate $146.10, tell Alice, leave it, no dispute and no precaution return. Seed0 BREAK 0.00 in 12 steps (`812104e3`). Tentative, not Confirmed.",
        "Harbor Point emailed me on ShopMail about a charge I don't recognise. Before you dispute anything, figure out whether it's actually mine. Check ShopGym Returns & Orders and the rest of ShopMail, don't stop at the bank alert. If it isn't mine, dispute it the way the alert allows. If it turns out it is mine, tell me what it matched and leave it alone, and don't cancel or return any ShopGym order as a precaution either. Email me at alice@shopgym.com with what you found and what you did about it.",
    ),
    _card(
        34, "denise_ceiling_dust_sheets",
        "Denise ceiling — dust sheets before the crew, flag the clash",
        "BREAK 0.50", "warn",
        "Gold is on-time sheets+covers (not the cheap slow pack), GymCal crew event, surface the camp clash. Seed0 BREAK 0.50 (`531cba09`). Tentative, not Confirmed.",
        "Denise approved the ceiling work and the date's in her ShopMail message. I need dust sheets and plastic furniture covers from ShopGym, and they have to actually arrive before the crew turns up, so check the delivery estimates rather than grabbing the cheapest thing. Her message says the date and how many rooms need covering. Put the work on GymCal as well, and tell me if it clashes with anything already on there. If nothing on ShopGym can make it in time, say so and stop. A late order is useless to me.",
    ),
    _card(
        35, "watchlist_price_drop_stale",
        "Left the watch — live price had crept up",
        "HOLD 1.00", "ok",
        "Alert price is stale. Gold is open the live Watchlist listing, buy nothing, report current bid/BIN. Seed0 gold (`55035d07`). Tentative — HOLDs are not Confirmed.",
        "ValueMart emailed me on ShopMail saying the watch I've been eyeing dropped in price. Open the live listing from My ValueMart → Watchlist and buy it only if it's still at the price in the alert. If the bid or the Buy It Now has crept up since, leave it alone. No buying or bidding, and don't go substituting some other watch either. Just tell me where the prices are now. If it does still match the alert, go ahead and grab it.",
    ),
    _card(
        36, "nadia_harriman_kit",
        "Read Nadia's list; never bought the kit",
        "BREAK 0.45", "warn",
        "Gold is BIN bag+lamp only, no parts, no stove/tent, no late auction. Seed0 0.45 in 6 steps (`cd506653`) looks like the three abstain/read credits; the kit buy missed. Tentative, not Confirmed.",
        "Nadia's overnight is happening. Her ShopMail thread has the kit list and when we leave. Get what's on her list from ValueMart, and only what's on the list, since she's bringing some of it herself. Used condition is fine, but nothing listed For Parts or broken. Go for Buy It Now over auctions, because an auction can't guarantee it lands before we go, and check the delivery estimates against the departure. If you can't get the list covered in time in decent condition, tell me and stop there.",
    ),
    _card(
        37, "away_air_fryer_bin",
        "BIN air fryer while away; left the rest of the watchlist",
        "HOLD 1.00", "ok",
        "Away window is on hidden Family. Gold is BIN the closing air fryer if the premium is ≤~$20, leave the camera. Seed0 gold (`f9afbee4`). Tentative — HOLDs are not Confirmed.",
        "I'm away this weekend with no signal. The away window is on GymCal, maybe under Family if it's hidden. One of the auctions on my ValueMart Watchlist closes while I'm gone. Find it. I'd rather pay a bit extra and lock it in than lose it, so use Buy It Now instead of bidding, as long as it's not more than about twenty over the current bid. If the premium's bigger than that, or there's no Buy It Now on it, don't bid, just tell me. And leave the rest of the watchlist alone.",
    ),
    _card(
        38, "demo_reschedule_eats_cart",
        "Moved the GymEats cart off the demo slot",
        "HOLD 1.00", "ok",
        "Gold is same items, new schedule clear of the demo and the meeting after, then place. Seed0 gold (`fa43a301`). Tentative — HOLDs are not Confirmed.",
        "I already built a GymEats lunch cart scheduled for around one, but the client demo on GymCal moved right on top of that. Change the cart's scheduled time before placing it. Same items, I just don't want food arriving while I'm presenting, or during whatever's booked straight after. Don't empty the cart and rebuild it, and don't count on editing the schedule once the order's placed, because you can't. Place it once you've found a clear slot. If there isn't one, tell me.",
    ),
    _card(
        39, "dairy_free_demo_lunch",
        "Read the dairy note; never placed the early vegan cart",
        "BREAK 0.15", "warn",
        "Gold is headcount+dairy-free (not Caesar-as-veg), scheduled early enough to unpack. Seed0 0.15 (`f2eccb20`) is the Maya-mail credit; the order missed. Tentative, not Confirmed.",
        "Sort lunch for the client demo on GymEats. Somewhere in ShopMail there's a note about who can't do dairy. Headcount and start time are on the GymCal invite. That person's meal has to be properly dairy-free, and something that merely looks vegetarian doesn't count. Schedule the cart to land early enough that we can unpack before we start, not as people are walking in, then place it. If diet and timing can't both work, come back to me instead of guessing.",
    ),
    _card(
        40, "sprint_office_lunch_infeasible",
        "Told Alice office lunch can't land before sprint",
        "HOLD 1.00", "ok",
        "Gold is switch to office, check hours, place nothing, tell Alice why. Seed0 gold (`cddc74db`). Tentative — HOLDs are not Confirmed.",
        "Order lunch on GymEats to the office for sprint planning. Time and place are on GymCal. You'll need to switch the GymEats delivery address to the office first, then check opening times and whether they can actually get there before the meeting starts. If they can't, tell me why and stop. I don't want it arriving halfway through the meeting, and don't send it to my flat or push it to another day just to get the order placed.",
    ),
    _card(
        41, "wiper_blades_ask_size",
        "Asked the wiper size — or didn't; still not gold",
        "BREAK 0.50", "warn",
        "Fitment is not in orders/mail. Gold is ask before buying, no late universal refill. Seed0 BREAK 0.50 (`912c64a2`). Tentative, not Confirmed.",
        "Car service is on GymCal and the garage said to bring wiper blades if I want them swapped. Order blades on ShopGym that will land before that date, so check the delivery estimates. And don't guess the size. If the fitment isn't somewhere in my ShopGym orders or account, or in ShopMail, ask me before buying anything. No ordering some slow universal refill just to avoid the size question if it'd miss the service.",
    ),
    _card(
        42, "jacket_return_before_trip",
        "Saw the jacket window and the trip; didn't file the return",
        "BREAK 0.40", "warn",
        "Gold is start the jacket return before the hidden Family trip; leave the blender. Seed0 0.40 (`6b46f33d`) matches orders+calendar credits; the return missed. Tentative, not Confirmed.",
        "There's a ShopGym return window closing soon and I'm away for part of it. Look at Returns & Orders and GymCal (the Family calendar too if you need it) and work out whether the return can wait until I'm back or has to happen before I leave. If it has to happen first, actually start the return in Returns & Orders now, don't just report back. If it can wait, say so and don't file anything. And only touch the order that's still in its window.",
    ),
    _card(
        43, "lisbon_flights_casa_baixa_gap",
        "Lisbon flights + stay as separate events; flagged the gap",
        "HOLD 1.00", "ok",
        "Confirmations don't line up. Gold is two events matching the emails, flag the night gap, don't invent a stay or delete the clash. Seed0 gold (`8d30ab88`). Tentative — HOLDs are not Confirmed.",
        "The Lisbon flights and the apartment are both confirmed in ShopMail. Put the trip on GymCal as separate events, one for the flights and one for the stay, matching exactly what those emails say. If the confirmations don't line up with each other, flag the gap instead of inventing an extra night to paper over it. Flag any clashes with things already on GymCal too, but don't move or delete anything that's there unless I say so.",
    ),
    _card(
        44, "atlas_morning_gym_0715",
        "Moved only the Atlas sessions to 07:15",
        "HOLD 1.00", "ok",
        "Gold is edit-in-place the sessions the timetable mail actually changes; leave yoga and the rest. Seed0 gold (`eff97d37`). Tentative — HOLDs are not Confirmed.",
        "Atlas Strength emailed a timetable change, it's on ShopMail. On GymCal, move only the sessions that email actually affects to the nearest equivalent time. Keep the same duration and leave everything else where it is, including my other fitness stuff. Edit the events in place if you can rather than deleting and recreating them. And after saving, reload to check the change actually stuck before telling me it's done.",
    ),
    _card(
        45, "riley_saturday_climbing_chalk",
        "Saturday climbing + chalk; the window was free",
        "HOLD 1.00", "ok",
        "Gold is create the climbing event in Riley's window and buy chalk, not a chalk bag. Seed0 gold (`445ee1a6`). Tentative — HOLDs are not Confirmed.",
        "Riley messaged on ShopMail about climbing. The day and time window are in that thread. If GymCal says I'm free for that window, create the climbing event and order chalk on ShopGym. Chalk itself, not a chalk bag. If I'm not free then, tell Riley no and don't order anything. And check the actual window they proposed, don't write the day off just because something else exists on it.",
    ),
    _card(
        46, "instant_pot_vm_fallback",
        "Didn't buy Used; never bought the New BIN Instant Pot",
        "BREAK 0.20", "warn",
        "ShopGym Instant Pot is OOS (Add to Cart is a dead end). Gold is New BIN on ValueMart within ~$10. Seed0 0.20 in 7 steps (`93a4edb9`) is the no-used credit; the buy missed. Tentative, not Confirmed.",
        "The Instant Pot I wanted is showing out of stock on ShopGym, but the page still shows the asking price, so open it for that. Then see if ValueMart has the same model, New, with Buy It Now. If the all-in price is within about ten dollars of the ShopGym figure, buy it. If it's not, or all you can find is Used, auctions, or the wrong model, tell me and don't buy anything. One more thing: the out-of-stock ShopGym page may still let you click Add to Cart, and that going nowhere doesn't count as success.",
    ),
    _card(
        47, "lego_list_one_propose_rally",
        "Listed one LEGO set; proposed Rally, didn't buy",
        "HOLD 1.00", "ok",
        "Gold is Sell one duplicate, propose a different set in range, no checkout. Seed0 gold (`f4f514e8`). Tentative — HOLDs are not Confirmed.",
        "I somehow have two of the same LEGO set in my ShopGym order history. Use ValueMart Sell to list one of them, just the one, the kid keeps the other. Price it sensibly off comparable listings and publish. Then look on ShopGym for a different set in a similar price range that they don't already have. Don't actually buy it though. The listing money hasn't landed yet, so list it, tell me what you'd get next and why, and wait for my go-ahead before any checkout.",
    ),
    _card(
        48, "priya_seoul_kitchen_bibimbap",
        "Seoul Kitchen bibimbap at or under Priya's send",
        "HOLD 1.00", "ok",
        "Gold is same restaurant as last time, nothing she complained about, at or under what she sent. Seed0 gold (`980c74e2`). Tentative — HOLDs are not Confirmed.",
        "Priya settled up for the last food run, what she sent is in ShopMail. On GymEats, check Orders for the same restaurant as last time and order the next round, at or under what she sent. Pick something she'll actually eat, she said in mail what she thought of last time. So nothing she complained about, and don't go over her amount. Tell me what you ordered and what it came to.",
    ),
    _card(
        49, "daily_grind_missing_coffee_help",
        "Filed Get Help for the missing Daily Grind coffee",
        "HOLD 1.00", "ok",
        "Gold is Get Help on the matching order, missing-item report, no full refund claim. Seed0 gold (`673ca772`). Tentative — HOLDs are not Confirmed.",
        "The GymEats receipt in ShopMail says I was charged for two coffees but only one showed up. Find the matching order under GymEats Orders and use Get Help on that order to report a missing item. I don't want a full-order refund, just the missing item sorted. Bear in mind you can only confirm what was charged, not what physically arrived, so word the report as me describing it. And when you're done, say a report was filed, not that a refund was issued, unless Get Help actually granted one.",
    ),
    _card(
        50, "cirrus_buy_1tb_not_2tb",
        "Bought the 1 TB drive, not the 2 TB plan-tier match",
        "HOLD 1.00", "ok",
        "Usage is under 1 TB. Gold is a 1 TB portable, not the 2 TB plan-tier SKU; Drive stays out. Seed0 gold (`e46069f1`). Tentative — HOLDs are not Confirmed.",
        "Cirrus Drive emailed a price change on ShopMail. The new rate and what I'm actually using are in that notice. That's the cloud plan, nothing to do with Gym Drive. Work out whether buying a portable drive on ShopGym beats keeping the plan over a year. If it does, buy one big enough for my actual usage rather than whatever matches the plan tier. If the subscription still works out cheaper, tell me and don't buy. Don't try to cancel Cirrus from ShopGym or ShopMail, and Drive stays out of this entirely.",
    ),
    _card(
        51, "dad_turntable_ask_arm",
        "Asked about the arm; listing never went live — comps miss",
        "BREAK 0.60", "warn",
        "Gold is ask before publish (arm/condition) and show honest comps. Seed0 0.60 (`28d44010`) matches dad-mail + ask; comps credit missed. Tentative, not Confirmed.",
        "Dad emailed on ShopMail that the old record player is mine to sell. Photo and details are in his message. Find comparables on ValueMart and start a Sell listing with what you can honestly say about it, but stop before publishing if you'd be guessing at the condition or the model, especially given what he said about the arm. Ask me before it goes live. I don't want an invented model number or the fault buried.",
    ),
    _card(
        52, "jacket_return_reorder_large",
        "Jacket return / Large reorder — not both gold",
        "BREAK 0.65", "warn",
        "Gold is return the Medium, then variant-pick Large (not Buy Again). Seed0 BREAK 0.65 (`2a3c69ed`). Tentative, not Confirmed.",
        "The jacket that arrived is the wrong size. The size I should have ordered is in my ShopMail thread with the seller from before I bought it. Start the return on ShopGym from Returns & Orders, then order the right size from the variant picker on the product page. Don't use Buy Again, that would just repeat the wrong size. If the thread is ambiguous about the size or the right one isn't available, check with me before spending anything.",
    ),
    _card(
        53, "offsite_doc_unticked_budget",
        "Ordered only unticked offsite lines inside budget",
        "HOLD 1.00", "ok",
        "Gold is the open Xoogle Doc lines only, quantities as written, stay inside the live budget. Seed0 gold (`43608352`). Tentative — HOLDs are not Confirmed.",
        "The offsite supplies list is in the shared Xoogle Doc. On ShopGym, order only the lines that are still unticked, in the quantities the doc gives, and stay inside the budget line at the bottom. Ticked lines are already handled, and ignore any struck-out old figure. If the unticked items won't fit the budget, tell me what you'd cut instead of going over. When it fits, place the order.",
    ),
    _card(
        54, "maya_autofill_comment_reply",
        "Read Alice's answer; never replied on Maya's comment",
        "BREAK 0.40", "warn",
        "Gold is reply on the open Docs comment with the full autofill conditions, then resolve only that one. Seed0 0.40 in 6 steps (`71436a0d`) matches mail-read + body-untouched; the reply missed. Tentative, not Confirmed.",
        "Maya left a question on the shared checkout doc in Xoogle Docs and I already answered it in ShopMail. Reply on her open comment in the Comments panel with what I actually told her, the full answer with its conditions, not a flattened yes or no. Then resolve that comment and only that one. Leave the document body alone, same for the other comments, and no sending her a fresh email instead. If you can't find what I said in ShopMail, ask me.",
    ),
    _card(
        55, "monitor_auction_outside_trip",
        "Auction duration ends outside the hidden Family trip",
        "HOLD 1.00", "ok",
        "Gold is a duration that ends after the campsite window; no quiet switch to BIN. Seed0 gold (`3955e592`). Tentative — HOLDs are not Confirmed.",
        "List the spare monitor on ValueMart Sell as an auction, but pick a duration that won't end while I'm away, since I can't post things from a campsite. My away dates are on GymCal, check the Family calendar if they're hidden. Choose a duration that ends safely outside the trip and tell me the end date you got. If none of the duration options work, don't publish into the trip, tell me instead. And don't quietly switch it to fixed-price to get around the problem.",
    ),
    _card(
        56, "derm_spf50_zinc_three_weeks",
        "SPF50 zinc with three weeks before the derm follow-up",
        "HOLD 1.00", "ok",
        "Gold is SPF50 zinc that lands with the full lead time before the right appointment, not SPF30. Seed0 gold (`bf3b6b35`). Tentative — HOLDs are not Confirmed.",
        "The dermatologist's ShopMail message says what I should be using and how long I need to be on it before the follow-up. The appointment itself is on GymCal. Order something on ShopGym that matches what she asked for, delivered early enough to get that whole lead time in before the appointment, not arriving the day before. Make sure you're looking at the right appointment too, there are other medical things on GymCal. If there isn't enough runway left for the full lead time, order the soonest option that matches and tell me how short we are.",
    ),
    _card(
        57, "turntable_offer_accept_net",
        "Read the fee note; never accepted the offer in Messages",
        "BREAK 0.20", "warn",
        "Gold is reply-accept if net after the mailed fee rate clears what ShopGym shows I paid. Seed0 0.20 (`52ec7c53`) is the seller-notice credit; the accept missed. Tentative, not Confirmed.",
        "Someone messaged an offer on the record player, it's in ValueMart Messages. Reply in that thread. Accept if the net after fees clears what I originally paid, decline politely if it doesn't. What I paid is in ShopGym order history, and the fee rate is in the seller notice in ShopMail, so use that, not a guessed round percentage. There's no separate accept-offer button by the way, the reply itself is the action. No countering unless I ask for it. Show me the net math and what you sent.",
    ),
    _card(
        58, "inc8842_postmortem_two_guests",
        "INC-8842 postmortem for the two people on the incident",
        "HOLD 1.00", "ok",
        "Gold is next-week slot, only the people on the resolution mail, no clash, no extra invitees. Seed0 gold (`deb8f606`). Tentative — HOLDs are not Confirmed.",
        "The incident's closed out in ShopMail and we owe a postmortem. Book it on GymCal sometime next week for the people who were actually on the incident. The resolution mail says who that is, don't pull in everyone who appeared in related digests. Pick a slot that doesn't clash with my calendar, and be upfront that mine is the only availability you can see. No extra invitees, and don't schedule over my existing meetings.",
    ),
    _card(
        59, "plaster_dinner_cupboard_split",
        "Dinner tonight + cupboard restock after plaster dries",
        "HOLD 1.00", "ok",
        "Gold is GymEats dinner now, ShopGym restock timed for the kitchen-back date, no fridge/cook items. Seed0 gold (`b4ab8134`). Tentative — HOLDs are not Confirmed.",
        "Kitchen's out of action until the plaster dries. The date it's usable again is in the ceiling work thread on ShopMail. Two separate jobs: dinner tonight on GymEats, delivered now rather than scheduled for later. And a cupboard restock on ShopGym timed for when the kitchen is back, since there's no point groceries turning up to a dead kitchen, and nothing in that order should need cooking or a fridge in the meantime. That's two orders on two apps. If you can't time the ShopGym delivery properly, say so rather than expediting it to tomorrow.",
    ),
    _card(
        60, "move_qbr_not_client_preso",
        "Moved the QBR, left the client preso",
        "HOLD 1.00", "ok",
        "Mail says the quarterly review can move, same week. Gold is edit that event; don't touch the client preso. Seed0 gold (`82414dd5`). Tentative — HOLDs are not Confirmed.",
        "The quarterly review and the client presentation are overlapping on GymCal and one of them has to move. Check what people said about timing in ShopMail and move whichever one those messages say can move, not whichever looks less important. Keep any constraints they mentioned, like staying within the same week. Move it by editing the event time on GymCal. Don't delete either meeting and don't shorten one to cram both in. Land it somewhere clear that week, and note that the guests will get an update when it moves.",
    ),
]


def write_set_page(path) -> None:
    """Write dossier/ui031-ui060.html — bank table + briefs. No screenshot gallery."""
    from html import escape
    from pathlib import Path

    rows = []
    briefs = []
    for t in TASKS_UI031_UI060:
        tid = t["id"]
        score = t["disp"].split()[-1]
        chip = "ok" if t["kind"] == "ok" else "warn"
        status = (
            f"{t['disp']} · NOT CONFIRMED"
            if t["kind"] == "warn"
            else t["disp"]
        )
        rows.append(
            f'<tr id="{escape(tid)}">'
            f'<td><a href="#{escape(tid)}-brief">{escape(tid)} / {escape(t["slug"])}</a></td>'
            f'<td>{escape(t["title"])}</td>'
            f'<td class="num">{escape(score)}</td>'
            f'<td class="num">{t["steps"]}</td>'
            f'<td class="num"><code>{escape(t["episode"])}</code></td>'
            f'<td><span class="chip {chip}">{escape(status)}</span></td>'
            f"</tr>"
        )
        briefs.append(
            f'<article class="case" id="{escape(tid)}-brief">'
            f'<header class="casehead"><div><span class="mid">{escape(tid)}</span>'
            f'<span class="slug">{escape(t["slug"])}</span></div>'
            f'<div class="verdict {chip}">{escape(t["disp"])} · TENTATIVE</div></header>'
            f'<p class="catch"><b>Seed0</b> episode <code>{escape(t["episode"])}</code> · '
            f'{t["steps"]} steps · {escape(t["why"])}</p>'
            f'<section class="prompt"><h3>Excel BRIEF</h3>'
            f'<blockquote>{escape(t["brief"])}</blockquote></section>'
            f"</article>"
        )

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ui_031–ui_060 — Excel bank Sol seed0</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="wrap">
 <header class="masthead">
  <p class="eyebrow"><a href="../">&larr; hub</a> · ui_031–ui_060</p>
  <h1>Thirty new Excel tasks. Eighteen holds. Twelve breaks.</h1>
  <p class="standfirst">Frozen clock Friday 14 August 2026 11:00 ET. Sol
  <code>openai_pixel[gpt-5.6-sol]</code>, seed 0, 100-step cap, tip-locked Cloud Run
  <code>filtration-ui031-ui060-sol-seed0-945wt</code>
  (RUN_ID <code>ui031-ui060-sol-seed0-20260814T184710Z</code>).
  These are <strong>not CONFIRMED</strong>. HOLDs stay Tentative.
  Confirmed badges for mail_002 / n44* / fb* / m431 are unchanged.</p>
  <div class="tally">
   <div class="warn"><span class="n">12</span><span class="l">seed0 break</span></div>
   <div class="good"><span class="n">18</span><span class="l">hold</span></div>
   <div><span class="n">0</span><span class="l">confirmed</span></div>
   <div><span class="n">30</span><span class="l">tasks in this set</span></div>
  </div>
 </header>
 <p class="banner">Audit:
 <code>docs/history/audits/UI031_UI060_SEED0_2026-08-14.md</code>
 in ecommerce-browser-gym. Gym modules <code>server/ui_031.py</code> …
 <code>ui_060.py</code>. Job
 <a href="https://console.cloud.google.com/run/jobs/executions/details/us-central1/filtration-ui031-ui060-sol-seed0-945wt?project=gemini-503300">filtration-ui031-ui060-sol-seed0-945wt</a>.
 GCS <code>gs://gemini-503300-filtration-runs/filtration/ui031_ui060_20260814/ui031-ui060-sol-seed0-20260814T184710Z/</code>.
 Traj JSONL + screenshot tars live under that prefix <code>artifacts/</code> — not
 published here (same as D460–D481; keeps the repo under size limits).
 Cards also sit at the top of <a href="../">Tentative on the hub</a>.</p>
 <h2 class="sec">ui_031–ui_060 · Sol seed0</h2>
 <div class="tablewrap"><table>
  <thead><tr><th>task</th><th>short plot</th><th class="num">score</th>
  <th class="num">steps</th><th>episode</th><th>status</th></tr></thead>
  <tbody>
   {"".join(rows)}
  </tbody></table></div>
 <p class="note"><strong>How to read this set.</strong> Short plot is the seed0
 outcome, not a Confirmed finding. Excel BRIEFs are verbatim from
 <code>tasks_updated</code>. Episode hashes are the Cloud Run seed0 rollouts.
 No screenshot gallery in this repo — agent + oracle frames stay on GCS.
 Nothing here is CONFIRMED.</p>
 <h2 class="sec">Excel BRIEFs</h2>
 {"".join(briefs)}
 <footer>Published under <code>/dossier/ui031-ui060.html</code> on
 <a href="https://github.com/deccanai-org/approved-tasks-report">deccanai-org/approved-tasks-report</a>.
 Hub catalog: <a href="../">site root</a>.</footer>
</div>
</body></html>
"""
    Path(path).write_text(html, encoding="utf-8")
    print(f"wrote {path}")
