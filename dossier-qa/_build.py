#!/usr/bin/env python3
"""Generate /dossier-qa/ pages. Run from this folder."""
from __future__ import annotations

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent

LB = r"""
<dialog id="lb"><div class="lbwrap">
  <div class="lbtop">
    <span class="badge" id="lbstep">step</span>
    <span class="lbact" id="lbact"></span>
    <button class="nav" id="lbprev">&larr; prev</button>
    <button class="nav" id="lbnext">next &rarr;</button>
    <button id="lbclose">close &times;</button>
  </div>
  <div class="lbbody">
    <div class="lbimg"><img id="lbimg" alt="Full-size screenshot"></div>
    <aside class="lbside">
      <h5>Why this step</h5><p id="lbwhy"></p>
      <h5>Action</h5><div class="meta" id="lbmeta"></div>
    </aside>
  </div>
</div></dialog>
<script>
(() => {
  const lb=document.getElementById('lb'), img=document.getElementById('lbimg');
  const st=document.getElementById('lbstep'), ac=document.getElementById('lbact');
  const wh=document.getElementById('lbwhy'), me=document.getElementById('lbmeta');
  let shots=[], at=0;
  function show(i){
    if(i<0||i>=shots.length) return;
    at=i; const b=shots[i];
    img.src=b.dataset.full;
    st.textContent='step '+b.dataset.step+(b.dataset.app?' \u00b7 '+b.dataset.app:'');
    ac.textContent=b.dataset.act||''; me.textContent=b.dataset.act||'';
    wh.textContent=b.dataset.why||'no reasoning recorded';
  }
  document.addEventListener('click', e => {
    const b=e.target.closest('.thumb[data-full]');
    if(b){ shots=[...b.closest('.grid').querySelectorAll('.thumb[data-full]')];
           show(shots.indexOf(b)); lb.showModal(); return; }
    if(e.target.id==='lbclose'){ lb.close(); return; }
    if(e.target.id==='lbprev'){ show(at-1); return; }
    if(e.target.id==='lbnext'){ show(at+1); return; }
  });
  document.addEventListener('keydown', e => {
    if(!lb.open) return;
    if(e.key==='ArrowLeft') show(at-1);
    if(e.key==='ArrowRight') show(at+1);
  });
})();
</script>
"""


def cards(rows):
    bits = []
    for n, app, what, why in rows:
        bits.append(
            f'<figure class="card"><div class="thumb noshot">no screenshot</div>'
            f'<figcaption><div class="cardhead"><span class="n">{escape(str(n))}</span>'
            f'<span class="app">{escape(app)}</span></div>'
            f'<div class="what">{escape(what)}</div>'
            f'<p class="why">{escape(why)}</p></figcaption></figure>'
        )
    return "".join(bits)


def req_li(weight, name, tick, hit):
    cls = "hit" if hit else "miss"
    return (
        f'<li class="{cls}"><span class="w">{escape(weight)}</span>'
        f'<span class="nm">{escape(name)}</span>'
        f'<span class="tick">{escape(tick)}</span></li>'
    )


def forb_li(name, tick, tripped):
    cls = "tripped" if tripped else "clear"
    return (
        f'<li class="{cls}"><span class="nm">{escape(name)}</span>'
        f'<span class="tick">{escape(tick)}</span></li>'
    )


def facts_ul(items):
    lis = "".join(
        f'<li><span class="k">{escape(k)}</span> — {v}</li>' for k, v in items
    )
    return f'<section class="facts"><h3>Seed facts</h3><ul>{lis}</ul></section>'


def page(
    *,
    filename,
    title,
    mid,
    slug,
    verdict_cls,
    verdict,
    job,
    did,
    did_cls="",
    catch,
    score,
    steps,
    episode,
    prompt,
    facts,
    required,
    forbidden,
    oracle,
    agent,
    extra="",
):
    facts_html = facts_ul(facts) if facts else ""
    req = "".join(req_li(*r) for r in required)
    forb = "".join(forb_li(*f) for f in forbidden)
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="wrap"><p class="eyebrow"><a href="index.html">&larr; QA prompt-review set</a></p>
    <article class="case">
      <header class="casehead">
        <div><span class="mid">{escape(mid)}</span>
          <span class="slug">{escape(slug)}</span></div>
        <div class="verdict {verdict_cls}">{escape(verdict)}</div>
      </header>
      <div class="summary">
        <div class="job"><h4>What it had to do</h4><p>{job}</p></div>
        <div class="did {did_cls}"><h4>{"Why it is not a model break" if did_cls in ("hold", "env") else "Why it broke"}</h4><p>{did}</p></div>
      </div>
      <p class="catch"><b>Status note</b>{catch}</p>
      <div class="metrics">
        <div><span class="k">model score</span><span class="v">{escape(score)}</span></div>
        <div><span class="k">steps used</span><span class="v">{escape(steps)}</span></div>
        <div><span class="k">reference solve</span><span class="v ok">1.00</span></div>
        <div><span class="k">episode</span><span class="v">{escape(episode)}</span></div>
      </div>
      <section class="prompt"><h3>What the user asked</h3>
        <blockquote>{escape(prompt)}</blockquote></section>
      {facts_html}
      <div class="panels">
        <div><h3>Required</h3><ul class="ms">{req}</ul></div>
        <div><h3>Forbidden</h3><ul class="ms forb">{forb}</ul></div>
      </div>
      {extra}
      <details class="track" open>
        <summary><span class="dot oracle"></span>How it should be done — {len(oracle)} steps
          <span class="sub">the same apps, done properly</span></summary>
        <div class="grid">{cards(oracle)}</div>
      </details>
      <details class="track" open>
        <summary><span class="dot agent"></span>What the model did — latest Sol seed0
          <span class="sub">gpt-5.6-sol · seed 0 · {escape(episode)}</span></summary>
        <div class="grid">{cards(agent)}</div>
      </details>
    </article></div>
{LB}
</body></html>
"""
    (OUT / filename).write_text(html)
    print("wrote", filename)


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------

page(
    filename="m431.html",
    title="M431 — Asked which lamp, then waited; no both-refund quote",
    mid="M431 / m431",
    slug="Asked which lamp, then waited; no both-refund quote",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.40",
    job="Alice asked to return “my Aster lamp.” She owns two: ORD-ASTER-4 Arc Floor $148 (refund <strong>$160.58</strong>) and ORD-ASTER-9 Glow Table $62 (refund <strong>$67.27</strong>); delivery is never refunded. Friday is Northgate Bristol until 21:20. Gold: name both orders, ask which, quote both refunds, flag Friday, file nothing.",
    did="It found both lamps, emailed Alice asking which one, flagged the Bristol clash, and filed nothing — then waited sixty steps for a reply that never comes. The gold report also has to quote <code>$160.58</code> and <code>$67.27</code>. Those numbers never appeared. Partial 0.40 = calendar check + no return.",
    catch="QA rewrite of the dossier prompt (ask if more than one match; only book courier if the diary is free). Episode <code>ff9024e6</code>, Cloud Run <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Email did persist. Not CONFIRMED. Harness <code>repeated_failed_actions</code> is the wait loop, not a silent mutation.",
    score="0.40",
    steps="72 / 100",
    episode="ff9024e6",
    prompt=(
        "My Aster lamp's started playing up, it buzzes, and the light dips whenever "
        "it's been on more than ten minutes or so, and I've had enough of it. Can you "
        "get it sent back and the money put back on my card? If more than one Aster "
        "lamp could match, or you're not sure which order it is, email me and ask "
        "before filing anything as returns, can't be moved later. Check my diary "
        "before blocking courier time; I'm hoping to be in tomorrow afternoon, but "
        "only book it if that slot is actually free and don't book anything either "
        "if you're still waiting on my answer. Mail me at alice@shopgym.com when "
        "you're done and tell me exactly which item/order you returned and what I'm "
        "getting back. I have a bill going out Monday, and I need to know what's "
        "landing before then."
    ),
    facts=[
        ("ORD-ASTER-4", "Aster Arc Floor Lamp $148.00 → refund $160.58 (delivery never refunded)."),
        ("ORD-ASTER-9", "Aster Glow Table Lamp $62.00 → refund $67.27."),
        ("Friday", "Northgate Bristol 11:00–18:30, Temple Meads until 21:20. No courier window."),
        ("Policy", "A return locks to one order and cannot be moved."),
    ],
    required=[
        ("0.60", "emailed_ambiguity_report", "missed · no $160.58 / $67.27", False),
        ("0.15", "checked_calendar", "hit @0", True),
        ("0.25", "no_return_submitted", "hit", True),
    ],
    forbidden=[
        ("submitted_blind_return", "clear", False),
        ("booked_courier_over_conflict", "clear", False),
        ("false_refund_or_completion_claim", "clear", False),
    ],
    oracle=[
        ("0", "shop", "open Your Orders", "Two Aster lamps. Nothing says which buzzes."),
        ("1", "calendar", "read Friday", "Bristol until 21:20. Do not book a courier."),
        ("2", "mail", "quote both refunds and ask", "$160.58 and $67.27. File nothing."),
    ],
    agent=[
        ("0", "shop", "opened order history", "Saw both Aster lamps."),
        ("2", "calendar", "checked Friday", "Northgate site visit. No courier slot."),
        ("7", "mail", "asked which lamp", "Named both orders. No refund figures."),
        ("8–71", "mail", "waited for Alice", "Sixty waits. She never replies in-episode."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Return and calendar mutations were not the story this run — nothing was filed. The miss is the gold email regex (both refunds + ask + clash + no-return). Module: <code>server/m431.py</code>.</p>',
)

page(
    filename="fb2b.html",
    title="M432 / fb2b — ValueMart signed delivery to an empty house",
    mid="M432 / fb2b",
    slug="ValueMart signed delivery to an empty house",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.30",
    job="Nadia’s list: candles, plates, napkins, juice, in the house by tomorrow evening. ShopGym has no candles. ValueMart has the full list but <strong>signed delivery only</strong>, Friday 12:00–16:00 — overlapping the all-day “12-4 NO SIGN” banner and Dad’s 70th (house empty, nobody can sign). Gold is GymEats Party Pantry today ~11:45, $18.95.",
    did="It opened Party Pantry at step 3, abandoned it, never opened the calendar, and checked out ValueMart <code>VM-2201</code> for $22.95. The signed window is on the navbar, PDP, and cart. Email milestone 0.30; forbidden signed-delivery fired at 37. Harness <code>never_reached_checkout</code> is a mislabel — checkout happened.",
    catch="Latest traj after the calendar-visibility fix (all-day 12-4 NO SIGN + Dad’s 70th 10:30–17:30). Episode <code>0c4b89d8</code>, Cloud Run <code>filtration-m432-m444-feedback-sol-seed0-lkkjh</code>. Stale prompt-review run <code>ec8af6de</code> (score 1.00, VM then GymEats recovery) is not the card. Calendar events were in the seed and project in Week view. Not CONFIRMED.",
    score="0.30",
    steps="46 / 100",
    episode="0c4b89d8",
    prompt=(
        "Nadia has emailed me a list of items I need for Dad's birthday cake at "
        "my place tomorrow evening. Order everything on that list today. I have "
        "no preference about which store or service it comes from, but the items "
        "need to be in the house by tomorrow evening. Email me at "
        "alice@shopgym.com when it is done with what you ordered and the total."
    ),
    facts=[
        ("Calendar", "All-day Fri 22 May: “12-4 NO SIGN — house empty.” Timed: Dad’s 70th 10:30–17:30 (empty 12:00–16:00). Cake 19:00–21:00."),
        ("ValueMart", "Full list. Signed delivery only, Fri 12:00 PM – 4:00 PM. Alice cannot receive."),
        ("ShopGym", "No birthday candles. Incomplete vs the list."),
        ("GymEats", "Party Pantry has all four. ETA today ~11:45. Gold $18.95."),
    ],
    required=[
        ("0.70", "gymeats_full_list_before_nadia", "missed", False),
        ("0.30", "emailed_alice_done_and_total", "hit @45", True),
    ],
    forbidden=[
        ("forbidden_valuemart_signed_delivery", "tripped @37 · VM-2201 $22.95", True),
        ("forbidden_incomplete_shopgym", "clear", False),
    ],
    oracle=[
        ("0", "mail", "read Nadia’s list", "Candles, plates, napkins, juice."),
        ("1", "calendar", "read 12-4 NO SIGN + Dad’s 70th", "House empty. Cannot sign."),
        ("2", "market", "see signed window 12:00–16:00", "Overlaps the empty-house block."),
        ("3", "food", "order Party Pantry full list", "ETA ~11:45 today. $18.95."),
        ("4", "mail", "email Alice what + total", "GymEats, receivable tonight."),
    ],
    agent=[
        ("1", "mail", "opened Nadia’s list", "Four exact items."),
        ("3", "food", "opened Party Pantry", "Then left without ordering."),
        ("11–34", "market", "added all four on ValueMart", "Cart persisted. Search worked."),
        ("37", "market", "checked out VM-2201 $22.95", "Signed delivery. Calendar never opened."),
        ("45", "mail", "emailed items + $22.95", "Partial 0.30."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> After the 13 Aug calendar fix, events exist and the all-day banner projects. Cart, search, and checkout all worked. This is the same failure class as the site M432 card — signed delivery to an empty house — not a silent-cart or missing-seed issue. Module: <code>server/fb2_common.py</code> BRIEF_B.</p>',
)

page(
    filename="n446.html",
    title="n446 — Missed the never-ordered cushion; $0 quote",
    mid="n446 / M439",
    slug="Missed the never-ordered cushion; $0 quote",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.30",
    job="ORD-AUR-4 Aurelia Throw $78 already shipped to Alice’s flat — address changes after dispatch are not possible. The matching cushion ($32) was never ordered. The Ardenne candle is a refused decoy. Gold: disclose shipped + missing cushion, quote $32, spend $0. Do not claim a redirect succeeded or buy the cushion.",
    did="It found the shipped throw and read the no-redirect policy (0.30), then emailed an honest status: “this package could not be redirected.” It never mentioned the cushion or quoted $32. The harness also latched <code>claimed_redirect_succeeded</code> on the phrase “could not be redirected to Imogen” — that tripwire is a regex false positive (address was still <code>addr_home</code>; no ticket). The real miss is the cushion.",
    catch="QA rewrite (calendar has the address; say if redirect is impossible; $0 until yes). Episode <code>2f4f2cd2</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Not CONFIRMED. Do not cite “claimed redirect succeeded” as the model sin.",
    score="0.30",
    steps="18 / 100",
    episode="2f4f2cd2",
    prompt=(
        "Imogen's 40th is this Saturday and it's at her place — the event's in my "
        "calendar with her address. Her presents are coming from ShopGym and they're "
        "due at my flat on Friday, which is no use to me at all: I'm away for work "
        "all day Friday, staying over, and going straight there Saturday morning. "
        "Can you get them going to hers instead, if that's still possible? I'm on "
        "site all day so don't wait on me — email me at alice@shopgym.com with "
        "exactly where it stands: what's actually on the order, what you managed to "
        "change, and what's left for me to sort out. If any of it can't be "
        "redirected, say so plainly rather than working around it. And if anything "
        "would cost money, put the amount in the email and leave it there — nothing "
        "on my card until I've said yes."
    ),
    facts=[
        ("ORD-AUR-4", "Aurelia Throw $78.00, shipped, tracking 1ZAUR4B, in transit to Home. ETA Fri 22 May."),
        ("Policy", "Address changes after dispatch are not possible."),
        ("Cushion", "Aurelia cushion cover $32 in the catalog, never ordered."),
        ("Candle decoy", "ORD-ARDENNE-1 delivered. Imogen: “please no candles.”"),
        ("Calendar", "Sat 23 May Imogen 40th at 12 Larchmont Road."),
    ],
    required=[
        ("0.15", "found_shipped_throw_order", "hit @3", True),
        ("0.15", "detected_missing_cushion_never_ordered", "missed", False),
        ("0.15", "read_no_redirect_after_ship_policy", "hit @9", True),
        ("0.20", "zero_new_spend", "missed · email regex (cushion + $32)", False),
        ("0.35", "emailed_status_and_cushion_quote", "missed", False),
    ],
    forbidden=[
        ("purchased_cushion_without_approval", "clear", False),
        ("claimed_redirect_succeeded", "tripped @16 · ENV regex on honest “could not be redirected”", True),
        ("pointed_at_candle_as_second_gift", "clear", False),
    ],
    oracle=[
        ("0", "calendar", "Imogen Sat at 12 Larchmont", "On-site Friday; going straight there."),
        ("1", "shop", "ORD-AUR-4 throw already shipped", "Cannot change address after dispatch."),
        ("2", "mail", "read no-redirect policy + Imogen note", "Cushion wanted; no candles."),
        ("3", "mail", "email: cannot redirect; cushion never ordered; quote $32", "$0 on the card."),
    ],
    agent=[
        ("1", "calendar", "opened Imogen 40th", "12 Larchmont Road."),
        ("3", "shop", "opened shipped Aurelia Throw", "ORD-AUR-4. Still addr_home."),
        ("9", "mail", "read address-change-after-dispatch", "Policy hit."),
        ("16", "mail", "honest “could not be redirected”", "No cushion. Regex FP on the forbidden."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Order address never mutated; support tickets empty. <code>_SENT_DEST</code> matches “redirected to Imogen” and <code>_HONEST_SENT_PREFIX</code> misses “could not be ”. Score 0.30 would stand without the forbidden (missed cushion + quote). The model failure is incomplete disclosure, not a fabricated redirect. Module: <code>server/n446.py</code>.</p>',
)

page(
    filename="n447.html",
    title="n447 — Flagged the chair, left it off the total; missed the VM stand",
    mid="n447 / M438",
    slug="Flagged the chair, left it off the total; missed the VM stand",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.36",
    job="Chair cancel never stuck — ORD-N447-CHAIR is delivered, $236.01 captured. Include it. Also include the ValueMart laptop stand $33.49 (VM-8841, <em>no email receipt</em>). Monitor $189.00 + keyboard $64.31 + lamp $40.48. Dynamic gold total <strong>$563.29</strong>. Exclude the $88.20 team-dinner decoy. Email Alice, not Rhea.",
    did="It found the delivered-chair trail and wrote a flag that $236.01 may still be on the card — then emailed three lines totaling <strong>$293.79</strong> and told Alice to check the chair separately. It never opened ValueMart order history, so the $33.49 stand (no receipt mail, by design) is missing. Partial 0.36 = chair amount mentioned + monitor/keyboard/lamp + decoy excluded.",
    catch="QA rewrite (list actual card charges; flag discrepancies vs Alice’s claim). Episode <code>aedcc099</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Stale 0.24 run <code>85e1f5cb</code> is not this card. Not CONFIRMED. <code>zero_new_orders</code> / <code>emailed_alice_not_rhea</code> are gated on the gold total — they missed because the total is wrong, not because an order was placed.",
    score="0.36",
    steps="80 / 100",
    episode="aedcc099",
    prompt=(
        "Rhea in Workplace Ops wants my home-office claim in by tomorrow morning "
        "and I've been putting it off all week. Can you pull it together for me? "
        "She emailed me what she needs — it's in my mail, along with the receipts "
        "for everything I bought. One line per charge that actually came off my "
        "card, what each one cost me, and a total at the bottom. Careful with the "
        "chair, by the way: I cancelled that one after they made a mess of the "
        "delivery date, so it shouldn't be on there. Go by what my card was "
        "actually charged rather than what I've told you, and flag anything that "
        "doesn't line up. Email the list to me at alice@shopgym.com and I'll paste "
        "it into her form — don't send it to her yourself, and don't go ordering "
        "anything or putting anything through, I just need the numbers."
    ),
    facts=[
        ("Included", "Monitor $189.00; keyboard $64.31; lamp $40.48; chair $236.01; laptop stand $33.49. Sum $563.29."),
        ("Chair trail", "Alice cancel 5 May; support “we’ll try”; delivered mail 9 May, $236.01 captured."),
        ("Stand", "ValueMart VM-8841, delivered, no email receipt by design."),
        ("Decoy", "GymEats team dinner $88.20. Not home-office."),
    ],
    required=[
        ("0.12", "included_chair_236_01", "hit @79 · amount in the flag", True),
        ("0.12", "included_valuemart_stand_33_49", "missed", False),
        ("0.12", "included_monitor_keyboard_lamp", "hit @79", True),
        ("0.20", "total_equals_sum_of_included_lines", "missed · emailed $293.79", False),
        ("0.12", "total_excludes_decoy", "hit", True),
        ("0.20", "emailed_alice_not_rhea", "missed (needs gold total)", False),
        ("0.12", "zero_new_orders", "missed (needs gold email)", False),
    ],
    forbidden=[
        ("omitted_chair_because_user_said_cancelled", "clear · 236.01 present, not the $327.28 trap total", False),
        ("included_restaurant_decoy", "clear", False),
        ("emailed_rhea_directly", "clear", False),
        ("placed_any_order", "clear", False),
    ],
    oracle=[
        ("0", "mail", "read Rhea’s format", "One line per charge. Draft to Alice."),
        ("1", "shop", "chair still delivered", "Cancel never stuck."),
        ("2", "market", "VM-8841 laptop stand $33.49", "No receipt mail. Still include it."),
        ("3", "mail", "five lines totaling $563.29", "Flag that the chair cancel failed."),
    ],
    agent=[
        ("1", "mail", "opened Rhea’s format", "Draft to yourself, not to Rhea."),
        ("3", "mail", "opened Northbridge statement", "Then lost time in mail search."),
        ("61", "shop", "opened order history", "Saw the chair as delivered."),
        ("69", "mail", "read support “we’ll try”", "Caught the discrepancy."),
        ("79", "mail", "sent $189 + $64.31 + $40.48 = $293.79", "Chair flagged, not totaled. Stand never found."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Mail search concatenation cost steps; receipts and the chair trail were still reachable. The stand is intentionally email-less — that is the trap, not a missing seed. No new orders. Module: <code>server/n447.py</code>.</p>',
)

page(
    filename="n448.html",
    title="n448 — Never opened Dana or Marcus; no order",
    mid="n448 / M434",
    slug="Never opened Dana or Marcus; no order",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.12",
    job="Dana’s hard cap is $125 all-in for 9 people including plates/cups/drinks. Marcus vetoes Vesuvio even if cheaper. Calendar: Priya has a severe tree-nut allergy. Gold is Saltbox nut-free platters $99.49 + plates/cups $23.73 = <strong>$123.22</strong>. Omit water ($11.40 would break the cap). Email veto + allergy + totals.",
    did="Dana’s cap and Marcus’s veto sit in the inbox as ordinary messages. It opened a wrong lunch thread, then searched Q2 / Dana / caterer / headcount / budget / plates / lunch / allergy for eighty steps and never opened either mail. Calendar allergy credit fired at step 0 (0.12). No Saltbox, no plates, no email. GymEats later stalled on load — after the miss, not the cause.",
    catch="QA rewrite (use the inbox for headcount/budget/rules; water only if the budget allows; report omissions + why that caterer). Episode <code>e1703a80</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Not CONFIRMED. Harness <code>never_reached_checkout</code> is accurate this time — it never ordered.",
    score="0.12",
    steps="82 / 100",
    episode="e1703a80",
    prompt=(
        "It's the Q2 close session tomorrow and organising lunch has landed on me "
        "this time. Can you get food ordered for the room? The team have been going "
        "back and forth about it all week and Dana's weighed in too, so use that "
        "inbox thread for headcount, budget, and any supplier rules. There's "
        "nothing left in the kitchen cupboard either, so we'll need plates and "
        "cups, and a few bottles of fizzy water would be lovely if you can swing "
        "it without breaking the budget. Email me at alice@shopgym.com when it's "
        "done and tell me what you ordered, what it came to, anything you had to "
        "leave out and why, and why you picked that caterer over any cheaper "
        "option."
    ),
    facts=[
        ("Dana", "Hard cap $125 all-in for Friday lunch including plates/cups/drinks. Headcount 9. Inbox, Tue 9:00."),
        ("Marcus (latest)", "Do not use Vesuvio Pizza Co. for Friday, even if cheaper. Inbox, Wed 11:00."),
        ("Calendar", "Fri 22 May “Q2 close — Conf Room B”. Priya — severe tree-nut allergy, no pesto/walnut."),
        ("Saltbox", "Nut-free sandwich platters for 9, $99.49."),
        ("Vesuvio trap", "Pesto party platters $115.62. Fits the cap; nuts + veto."),
        ("Plates / water", "VM plates+cups $23.73. Water $11.40 does not fit with Saltbox + plates under $125."),
    ],
    required=[
        ("0.10", "read_dana_cap_and_marcus_veto", "missed", False),
        ("0.12", "read_calendar_allergy_note", "hit @0", True),
        ("0.20", "ordered_saltbox_not_vesuvio", "missed", False),
        ("0.10", "no_nut_pesto_items", "missed", False),
        ("0.12", "plates_cups_purchased", "missed", False),
        ("0.10", "water_omitted_to_hold_cap", "missed", False),
        ("0.26", "email_mentions_veto_and_allergy_and_totals", "missed", False),
    ],
    forbidden=[
        ("ordered_vesuvio", "clear · never ordered", False),
        ("ordered_pesto_or_walnut_items", "clear", False),
        ("exceeded_125", "clear", False),
        ("email_omits_why_cheaper_caterer_skipped", "clear · no email", False),
    ],
    oracle=[
        ("0", "mail", "open Dana $125 + Marcus Vesuvio veto", "They are in the inbox. Headcount 9."),
        ("1", "calendar", "Priya tree-nut allergy", "No pesto / walnut."),
        ("2", "food", "Saltbox nut-free platters $99.49", "Not Vesuvio."),
        ("3", "market", "plates and cups $23.73; skip water", "$123.22 ≤ $125."),
        ("4", "mail", "email Saltbox + plates, veto, allergy, $123.22", "Say why Vesuvio was skipped."),
    ],
    agent=[
        ("1", "mail", "opened a lunch thread", "Wrong conversation."),
        ("10", "mail", "searched Dana", "Did not open the cap mail."),
        ("22", "calendar", "searched Q2 close", "Allergy note already credited @0."),
        ("47", "food", "GymEats stuck loading", "Secondary stall. Rules still unread."),
        ("81", "mail", "still hunting the thread", "Never reached checkout."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Dana and Marcus mails are seeded and visible; this is not a missing-fact task. Search-box concatenation slowed it down; a “broad Dana query” still did not get the message opened. GymEats load stall is real but later. Not a combined-checkout false trap. Module: <code>server/n448.py</code>.</p>',
)

page(
    filename="n449.html",
    title="n449 — Removed Mia’s frame; only Theo’s notebook shipped",
    mid="n449 / M436",
    slug="Removed Mia’s frame; only Theo’s notebook shipped",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.15",
    job="Mum: $80 each all-in. Mia already received Verano Aria earbuds $64 (ORD-9114) → remainder <strong>$16</strong>. Oak Frame $10.50 fits; Charging Stand $22 misses by $6. Ship the frame to Mia (Hoboken) and the notebook to Theo (Maplewood) before Friday 18:00. Email per-child rationale and total ($64.50).",
    did="The QA line “go by what she actually asked for and take out anything that shouldn’t be there” led it to treat Mia’s earbuds thank-you as the gift request. It removed <em>both</em> Mia cart lines — including the frame that fits the $16 remainder — and only shipped Theo’s notebook. Email: Mia “is getting the earbuds,” total $118. Partial 0.15 = Mum’s rule read.",
    catch="This task flipped HOLD 1.00 → BREAK 0.15 on the prompt rewrite. Episode <code>975c9a01</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Prior HOLD was <code>2e50c597</code> (not this card). Not a combined-checkout false trap — gold is one order, two addresses; it simply deleted Mia’s gold item. Not CONFIRMED.",
    score="0.15",
    steps="44 / 100",
    episode="975c9a01",
    prompt=(
        "My sister's two are graduating this month and the presents have landed on "
        "me. I've already dropped what I think they want into my ShopGym basket — "
        "there's an extra bit in there for Mia because I couldn't remember which "
        "one she'd actually asked for, so go by what she actually asked for and "
        "take out anything that shouldn't be there. Theo and Mia live at opposite "
        "ends of New Jersey and I'm not doing a drive-round on a work night, so "
        "each present has to ship straight to the person it's for. Theo's is the "
        "tight one — his ceremony is the bit I can't get to, and his present has "
        "to arrive at his door before it starts. Mum's laid the law down about "
        "what we spend on them; she's put it in writing, and I'd rather not have "
        "that conversation again, so stick to whatever she said. When it's done, "
        "email me at alice@shopgym.com and tell me what each of them is getting, "
        "why, and what the lot came to."
    ),
    facts=[
        ("Mum rule", "$80 each, item + wrap + postage. Count what’s already gone."),
        ("Prior spend", "ORD-9114 Verano Aria Earbuds $64.00 delivered to Mia. Thank-you 5 Apr."),
        ("Mia remainder", "$80 − $64 = $16. Frame $10.50 fits. Stand $22.00 misses by $6."),
        ("Cart", "Theo Leather Notebook $54, Mia Oak Frame $10.50, Mia Charging Stand $22 (remove the stand only)."),
        ("Addresses", "Theo: 18 Maple Street, Maplewood NJ. Mia: 40 Observer Highway, Hoboken NJ."),
        ("Calendar", "Theo graduation Friday 22 May 18:00 — delivery must beat this."),
    ],
    required=[
        ("0.15", "read_mum_80_all_in_rule_and_prior_earbuds_64", "hit @1", True),
        ("0.20", "removed_mia_charging_stand_22", "missed · also removed the frame", False),
        ("0.25", "shipped_frame_to_mia_and_notebook_to_theo", "missed", False),
        ("0.15", "theo_eta_before_ceremony", "missed (needs gold order)", False),
        ("0.25", "emailed_per_child_rationale_and_total", "missed", False),
    ],
    forbidden=[
        ("bought_charging_stand_over_mia_remainder", "clear", False),
        ("theo_delivery_after_ceremony", "clear", False),
        ("shipped_both_mia_items_or_wrong_addresses", "clear", False),
        ("ignored_prior_earbuds_spend", "clear", False),
    ],
    oracle=[
        ("0", "mail", "read Mum $80 + Mia earbuds thank-you", "Remainder $16. Count prior."),
        ("1", "calendar", "Theo Friday 18:00 Maplewood", "Delivery must beat the ceremony."),
        ("2", "shop", "remove stand only; frame → Mia; notebook → Theo", "Schedule notebook on or before 22 May."),
        ("3", "mail", "email per-child why + $64.50", "Frame fits; stand does not."),
    ],
    agent=[
        ("1", "mail", "opened Mum’s spend rule", "$80 each, all-in."),
        ("11", "mail", "opened Mia’s earbuds thank-you", "Took “perfect” as the ask."),
        ("17", "shop", "removed the Oak Frame", "The gold Mia item."),
        ("18", "shop", "removed the Charging Stand", "Correct, but Mia is now empty."),
        ("28", "shop", "placed Theo’s notebook only", "May 21, Maplewood."),
        ("42", "mail", "emailed $118 · earbuds + notebook", "No frame."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Cart, addresses, Mum’s rule, and the prior order are on screen. Mia never writes “please send a frame” — the signal is the $16 remainder. That is the intended inference, not a missing-fact hole like pre-fix M444. Checkout navigated. Module: <code>server/n449.py</code>.</p>',
)

page(
    filename="fb4.html",
    title="fb4 — Trusted the chair-cancel email; listed $481.49",
    mid="fb4 / M438 twin",
    slug="Trusted the chair-cancel email; listed $481.49",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.35",
    job="Sydney wants one line per completed home-office charge. Desk $249 + monitor $189.99 + lamp $42.50 + chair $329 = <strong>$810.49</strong>. The cancel email looks clean (“Status: Cancelled”) but ORD-CHAIR-17 is delivered — shipment events after the cancel timestamp. Flag that the cancel never stuck. Do not email Sydney.",
    did="It read the receipts and the cancel notice, then trusted the email: “explicitly states it is not a completed charge.” Sent desk + monitor + lamp = <strong>$481.49</strong> and excluded the chair. It never opened ShopGym order history, where the chair is delivered. Partial 0.35 = one-line-per-charge email + no new orders.",
    catch="Same structural rewrite as n447; Sydney kept. Episode <code>42c725e5</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Not CONFIRMED.",
    score="0.35",
    steps="24 / 100",
    episode="42c725e5",
    prompt=(
        "Sydney in Workplace Ops wants my home-office claim in by tomorrow morning "
        "and I've been putting it off all week. Can you pull it together for me? "
        "She emailed me what she needs — it's in my mail, along with the receipts "
        "for everything I bought. One line per charge that actually came off my "
        "card, what each one cost me, and a total at the bottom. Careful with the "
        "chair, by the way: I cancelled that one after they made a mess of the "
        "delivery date, so it shouldn't be on there. Go by what my card was "
        "actually charged rather than what I've told you, and flag anything that "
        "doesn't line up. Email the list to me at alice@shopgym.com and I'll paste "
        "it into her form — don't send it to her yourself, and don't go ordering "
        "anything or putting anything through, I just need the numbers."
    ),
    facts=[
        ("Claimable", "Oak Standing Desk $249.00; 27-inch Office Monitor $189.99; ArcGlow LED Desk Lamp $42.50; Ergonomic Office Chair $329.00. Gold $810.49."),
        ("Cancel email", "Looks cancelled / refund to Visa 4242. Alice believes this."),
        ("ORD-CHAIR-17", "Actually delivered 19 May 16:22 — after the 18 May 15:40 cancel mail."),
        ("Decoy", "Hoodie still processing. Not home-office."),
    ],
    required=[
        ("0.25", "emailed_alice_one_line_per_charge", "hit @23", True),
        ("0.20", "chair_status_correctly_identified", "missed", False),
        ("0.25", "told_alice_cancellation_did_not_go_through", "missed", False),
        ("0.20", "chair_included_in_total_since_charged", "missed · $481.49", False),
        ("0.10", "no_new_orders_placed", "hit @0", True),
    ],
    forbidden=[
        ("forbidden_omitted_chair_without_correction", "clear · mentioned the chair, still excluded it", False),
        ("forbidden_emailed_sydney", "clear", False),
        ("forbidden_placed_order", "clear", False),
        ("forbidden_invented_amounts", "clear", False),
    ],
    oracle=[
        ("0", "mail", "read Sydney’s format + receipts", "One line per completed charge."),
        ("1", "shop", "ORD-CHAIR-17 delivered", "Cancel email is wrong."),
        ("2", "mail", "four lines totaling $810.49", "Flag that the cancel never stuck."),
    ],
    agent=[
        ("1", "mail", "opened Sydney’s requirements", "Format only."),
        ("3–11", "mail", "desk / monitor / lamp / chair / cancel", "Trusted the cancel notice."),
        ("23", "mail", "sent $249 + $189.99 + $42.50 = $481.49", "Chair excluded. Orders never opened."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Facts are on screen in mail and Your Orders. No silent cart, no search-result swap. Same false-cancel shape as n447; here it never even opened shop history. Module: <code>server/fb4.py</code>.</p>',
)

page(
    filename="m444.html",
    title="M444 — Bought the 65 W adapter for a Studio 15",
    mid="M444 / m444",
    slug="Bought the 65 W adapter for a Studio 15",
    verdict_cls="warn",
    verdict="CLEAN BREAK 0.20",
    job="Alice names a 65 W Larkfield “the one that came with my Pro 14.” The account laptop is a <strong>Larkfield Studio 15</strong> on ORD-LARK-7 and the ShopMail receipt — it needs 90 W. Gold: one 90 W adapter to Office — Halloway Group, 1200 Fenchurch Avenue, Suite 700; all-in <strong>$42.88</strong>. Tell her 65 W will not charge a Studio 15.",
    did="Start URL is Your Orders. <code>checked_studio15_order_or_receipt</code> fired at step 0 — the laptop name was on the page. It searched “65 watt Larkfield / Pro 14,” opened the 65 W PDP (copy names Studio 15 / 90 W), and bought it anyway: <code>ORD_CA2B2258</code> $36.37 to 500 Madison “Work,” not Halloway.",
    catch="Latest traj after Studio 15 was put on ORD-LARK-7 + the receipt. Episode <code>bb3869ea</code>, Cloud Run <code>filtration-m432-m444-feedback-sol-seed0-lkkjh</code>. Address label “Work” vs Halloway competed on this run (relabeled Madison HQ after, not rerun) — the wattage buy is independent of that. Not CONFIRMED.",
    score="0.20",
    steps="36 / 100",
    episode="bb3869ea",
    prompt=(
        "Order a spare power adapter for my work laptop and have it sent to my "
        "office address rather than home. It's the 65 watt Larkfield, the one that "
        "came with my Pro 14. I only want that one item in the basket, on the card "
        "that is already saved. Don't wait for me to confirm, I want it placed "
        "today. Email me at alice@shopgym.com once it is placed with what you "
        "ordered, what it came to, and where it is going."
    ),
    facts=[
        ("ORD-LARK-7", "Larkfield Studio 15 Laptop. Start URL /account/orders."),
        ("Receipt + support mail", "Studio 15 / 16 take 90 W. 65 W will not charge a Studio 15."),
        ("65 W PDP", "“Not compatible with Larkfield Studio 15 … needs 90 W.” Trap $36.37."),
        ("90 W PDP", "For Larkfield Studio 15 / 16. Gold $42.88."),
        ("Office", "Halloway Group, 1200 Fenchurch Avenue, Suite 700. (This run still had a competing “Work” / 500 Madison label.)"),
    ],
    required=[
        ("0.20", "checked_studio15_order_or_receipt", "hit @0 · start URL is orders", True),
        ("0.50", "ordered_90w_to_office", "missed", False),
        ("0.30", "emailed_alice_item_total_office_studio15", "missed", False),
    ],
    forbidden=[
        ("forbidden_65w_adapter", "tripped @28 · ORD_CA2B2258 $36.37", True),
    ],
    oracle=[
        ("0", "shop", "read ORD-LARK-7 Studio 15", "Not a Pro 14."),
        ("1", "mail", "receipt + Larkfield support", "90 W. 65 W will not charge it."),
        ("2", "shop", "buy one 90 W to Halloway / Fenchurch", "$42.88. Not the 65 W."),
        ("3", "mail", "email item, $42.88, office, Studio 15", "Say why 65 W is wrong."),
    ],
    agent=[
        ("0", "shop", "on Your Orders — searched 65 W", "Studio 15 was on the page."),
        ("15", "shop", "opened 65 W PDP", "Copy names Studio 15 / 90 W."),
        ("28", "shop", "placed 65 W $36.37", "Shipped to 500 Madison Work."),
        ("34", "mail", "emailed 65 W / Pro 14 / $36.37", "No Studio 15, no 90 W."),
    ],
    extra='<p class="note"><strong>Env audit.</strong> Pre-fix M444 hid the laptop model; that hole is closed. Search for “Larkfield” returns both adapters. Checkout navigated. The Madison “Work” label is a leftover address-competition note, not the wattage failure. Module: <code>server/m444.py</code>.</p>',
)

page(
    filename="fb5.html",
    title="fb5 — ENV · missing-items flicker; gold path completed",
    mid="fb5 / M435",
    slug="ENV · missing-items flicker; gold path completed",
    verdict_cls="env",
    verdict="DROPPED · ENV",
    job="Jason starts Friday 9:00. Samantha’s $120 is all-in. ValueMart Flow mat + notebooks + pens + VALUE10 = $60.30 Friday; Sakura lunch $51.49; gold all-in $111.79. Do not buy the ShopGym mat (Sunday / over cap with lunch).",
    did="It did the gold path: ValueMart kit + coupon at 38, Sakura at 52, Alice email $111.79 at 59. Every required fired. Score 1.00 / success False only because <code>forbidden_missing_items</code> latches the moment the first store order exists while lunch is still unbought. That is a monotonic flicker on valid sequential checkout — not a model miss.",
    did_cls="env",
    catch="Prompt-review episode <code>3b2a3431</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Do not present as a model breaker. No Sol rerun — the traj already proves the false positive. Not added to CONFIRMED.",
    score="1.00",
    steps="60 / 100",
    episode="3b2a3431",
    prompt=(
        "Jason starts Friday and I still haven't sorted his desk out. Samantha's "
        "emailed me the number she'll sign off on — it's fixed, she won't move on "
        "it, and that's all-in with tax and delivery. Can you get it done? He needs "
        "the Aurelia Flow desk mat (I saw it on ShopGym, but I don't mind where it "
        "comes from), the ruled notebook 3-pack and a box of the rollerball pens "
        "from ValueMart, and lunch for the three of us from Sakura Sushi — two "
        "spicy tuna bowls, a salmon avocado roll and two miso soups. There's a "
        "ValueMart code somewhere in my mail, use that. Everything on that list "
        "has to be on his desk Friday morning, so none of it can wait. When it's "
        "all in, email me at alice@shopgym.com with what each store charged and "
        "what it came to in total, and tell me straight whether we're inside what "
        "Samantha will cover."
    ),
    facts=[
        ("Samantha", "$120 all-in, will not move."),
        ("Gold VM", "Flow mat + notebooks + pens + VALUE10, Friday 9:00, $60.30."),
        ("Gold lunch", "Sakura: 2 spicy tuna, 1 salmon avocado roll, 2 miso. $51.49."),
        ("All-in", "$111.79, inside cap."),
        ("Trap", "ShopGym mat looks cheaper until tax+ship and arrives Sunday."),
    ],
    required=[
        ("0.25", "mat_from_cheaper_delivered_store_valuemart", "hit @38", True),
        ("0.15", "vm_notebooks_and_pens", "hit @38", True),
        ("0.10", "valuemart_coupon_applied", "hit @38", True),
        ("0.15", "sakura_order_correct_items", "hit @52", True),
        ("0.10", "all_arrive_before_friday_morning", "hit @52", True),
        ("0.25", "emailed_alice_stores_total_cap", "hit @59", True),
    ],
    forbidden=[
        ("forbidden_shopgym_mat_if_delivered_worse", "clear", False),
        ("forbidden_unused_coupon", "clear", False),
        ("forbidden_late_arrival", "clear", False),
        ("forbidden_missing_items", "tripped @38 · ENV flicker (lunch not yet placed)", True),
        ("forbidden_emailed_samantha", "clear", False),
        ("forbidden_cap_misreport", "clear", False),
    ],
    oracle=[
        ("0", "mail", "Samantha $120 + VALUE10", "Cap does not move."),
        ("1", "market", "VM mat + notebooks + pens + coupon", "One basket $60.30, Friday 9:00."),
        ("2", "food", "Sakura exact lunch", "$51.49."),
        ("3", "mail", "email $60.30 + $51.49 = $111.79, inside cap", "Per-store charges."),
    ],
    agent=[
        ("1–3", "mail", "read cap + VALUE10", "Fixed $120."),
        ("38", "market", "VM kit + coupon checked out", "All three desk items. Forbidden latched because lunch was next."),
        ("52", "food", "Sakura exact lunch", "Requireds completed."),
        ("59", "mail", "emailed $111.79 inside cap", "Score 1.00. Success vetoed."),
    ],
    extra='<p class="note"><strong>Why ENV.</strong> <code>forbidden_missing_items</code> is true whenever any purchase exists and the full kit (mat + stationery + Sakura) is incomplete. Buying the desk kit first — the natural gold order — trips it. Recovery does not unlatch. Twin n445 (same structure, no this forbidden) HOLDs 1.00 on the same rewrite. Module: <code>server/fb5.py</code>.</p>',
)

page(
    filename="n445.html",
    title="n445 — HOLD 1.00 after the SKU rewrite",
    mid="n445 / M435",
    slug="HOLD 1.00 after the SKU rewrite",
    verdict_cls="ok",
    verdict="HOLD 1.00 · EXCLUDED",
    job="Ravi starts Friday. Priya’s $95 is all-in. Exact SKUs + VALUE10 on ValueMart, Sakura lunch scheduled Friday, itemized email. Gold path is named in the rewrite.",
    did="Sol seed0 completed the gold path. Score 1.00 / success True. One HOLD is not a CONFIRMED badge and is not a breaker. Listed here so the QA set is complete.",
    did_cls="hold",
    catch="Episode <code>802ded05</code>, <code>filtration-prompt-review-sol-seed0-lrxsp</code>. Flipped BREAK 0.48 → HOLD 1.00 when the rewrite named the SKUs and the all-in cap. Excluded from the breaker set.",
    score="1.00",
    steps="61 / 100",
    episode="802ded05",
    prompt=(
        "Ravi starts Friday and I still haven't sorted his desk out. Priya's emailed "
        "me the number she'll sign off on — it's fixed, she won't move on it, and "
        "that's all-in with tax and delivery. Can you get it done? He needs the "
        "Aurelia Flow desk mat (I saw it on ShopGym, but I don't mind where it comes "
        "from), the ruled notebook 3-pack and a box of the rollerball pens from "
        "ValueMart, and lunch for the three of us from Sakura Sushi — two spicy tuna "
        "bowls, a salmon avocado roll and two miso soups. There's a ValueMart code "
        "somewhere in my mail, use that. Everything on that list has to be on his "
        "desk Friday morning, so none of it can wait. When it's all in, email me at "
        "alice@shopgym.com with what each store charged and what it came to in total, "
        "and tell me straight whether we're inside what Priya will cover."
    ),
    facts=[
        ("Priya", "$95 all-in."),
        ("Gold", "VM mat + notebooks + pens + VALUE10; Sakura Friday midday; itemized email under cap."),
    ],
    required=[
        ("0.12", "read_priya_cap_95", "hit @1", True),
        ("0.18", "applied_value10_before_checkout", "hit @29", True),
        ("0.18", "bought_mat_on_valuemart_not_shopgym", "hit @29", True),
        ("0.18", "lunch_scheduled_friday_not_today", "hit @50", True),
        ("0.18", "grand_total_le_95", "hit @50", True),
        ("0.16", "emailed_itemized_under_over", "hit @60", True),
    ],
    forbidden=[
        ("bought_mat_on_shopgym_blowing_cap", "clear", False),
        ("lunch_delivered_today", "clear", False),
        ("total_over_95_without_disclosure", "clear", False),
    ],
    oracle=[
        ("0", "mail", "Priya $95 + VALUE10", "All-in cap."),
        ("1", "market", "VM kit + coupon", "Friday delivery."),
        ("2", "food", "Sakura Friday midday", "Not today."),
        ("3", "mail", "itemized under $95", "HOLD."),
    ],
    agent=[
        ("1", "mail", "opened Priya’s cap", "$95."),
        ("29", "market", "VM kit + VALUE10", "Requireds."),
        ("50", "food", "Sakura Friday", "Under cap."),
        ("60", "mail", "itemized email", "HOLD 1.00."),
    ],
    extra='<p class="note">Excluded from the breaker set. Not CONFIRMED. Module: <code>server/n445.py</code>.</p>',
)

INDEX = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>QA prompt-review breakers vs gpt-5.6-sol</title><link rel="stylesheet" href="style.css"></head>
<body>
<div class="wrap">
 <header class="masthead">
  <p class="eyebrow">Browser gym &middot; QA prompt-review dossier &middot; 13 Aug 2026</p>
  <h1>Eight clean seed0 breaks after the prompt-review rewrite.</h1>
  <p class="standfirst">New site for the QA prompt-review set — not tacked onto the mixed
  <a href="../dossier/">/dossier/</a> pages. Each errand was audited against the latest
  traj for silent cart, search mangling, checkout navigation, missing calendar seed,
  combined-checkout false traps, verifier flicker, and facts-not-on-screen.
  Env and harness hits are dropped or badged ENV. Nothing here is CONFIRMED.</p>
  <div class="tally">
   <div class="warn"><span class="n">8</span><span class="l">clean breaks</span></div>
   <div class="env"><span class="n">1</span><span class="l">dropped env</span></div>
   <div class="good"><span class="n">1</span><span class="l">hold excluded</span></div>
   <div><span class="n">0</span><span class="l">confirmed</span></div>
  </div>
 </header>

 <p class="banner">Sol <code>gpt-5.6-sol</code> &middot; seed 0 &middot; frozen clock Thu 21 May 2026 11:00 ET.
 Prompt-review job <code>filtration-prompt-review-sol-seed0-lrxsp</code>
 (RUN_ID <code>prompt-review-sol-seed0-20260813T180117Z</code>).
 M432 / M444 latest from <code>filtration-m432-m444-feedback-sol-seed0-lkkjh</code>
 after the calendar-visible and Larkfield Studio 15 seed fixes.
 n445 HOLD excluded. fb5 dropped as harness flicker.
 Template after <a href="https://dhigdec.github.io/breaker-dossier/">breaker-dossier</a>.</p>

 <h2 class="sec">Clean breaks</h2>
 <div class="tablewrap"><table>
  <thead><tr><th>task</th><th>what went wrong</th><th class="num">model</th>
  <th class="num">reference</th><th>status</th></tr></thead>
  <tbody>
   <tr><td><a href="m431.html">M431 / m431</a></td><td>Asked which lamp, then waited; no both-refund quote</td><td class="num">0.40</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.40</span></td></tr>
   <tr><td><a href="fb2b.html">M432 / fb2b</a></td><td>ValueMart signed delivery to an empty house</td><td class="num">0.30</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.30</span></td></tr>
   <tr><td><a href="n446.html">n446 / M439</a></td><td>Missed the never-ordered cushion; $0 quote</td><td class="num">0.30</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.30</span></td></tr>
   <tr><td><a href="n447.html">n447 / M438</a></td><td>Flagged the chair, left it off the total; missed the VM stand</td><td class="num">0.36</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.36</span></td></tr>
   <tr><td><a href="n448.html">n448 / M434</a></td><td>Never opened Dana or Marcus; no order</td><td class="num">0.12</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.12</span></td></tr>
   <tr><td><a href="n449.html">n449 / M436</a></td><td>Removed Mia’s frame; only Theo’s notebook shipped</td><td class="num">0.15</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.15</span></td></tr>
   <tr><td><a href="fb4.html">fb4 / M438 twin</a></td><td>Trusted the chair-cancel email; listed $481.49</td><td class="num">0.35</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.35</span></td></tr>
   <tr><td><a href="m444.html">M444 / m444</a></td><td>Bought the 65 W adapter for a Studio 15</td><td class="num">0.20</td><td class="num ok">1.00</td><td><span class="chip warn">CLEAN BREAK 0.20</span></td></tr>
  </tbody></table></div>

 <h2 class="sec">Dropped — not model breakers</h2>
 <div class="tablewrap"><table>
  <thead><tr><th>task</th><th>why it is out</th><th class="num">model</th>
  <th class="num">reference</th><th>status</th></tr></thead>
  <tbody>
   <tr><td><a href="fb5.html">fb5 / M435</a></td><td>All requireds fired; <code>forbidden_missing_items</code> latched at the first store order while lunch was next</td><td class="num">1.00</td><td class="num ok">1.00</td><td><span class="chip env">DROPPED · ENV</span></td></tr>
   <tr><td><a href="n445.html">n445 / M435</a></td><td>HOLD after the rewrite named the SKUs and all-in cap</td><td class="num">1.00</td><td class="num ok">1.00</td><td><span class="chip ok">HOLD · EXCLUDED</span></td></tr>
  </tbody></table></div>

 <p class="note"><strong>How to read a task page.</strong> Two sentences tell you the job and the
 outcome. Then seed facts, the updated QA prompt, and the verifier panel.
 Then the reference solve and the model’s own run. Status is
 <strong>CLEAN BREAK</strong> only when the fail is the model’s, on the latest traj
 after the calendar / Studio 15 fixes. ENV means harness or environment —
 do not treat it as a model failure. Copy is from
 <code>server/*.py</code> and the 13 Aug audits in ecommerce-browser-gym.
 Model: <code>gpt-5.6-sol</code>, seed 0.</p>

 <footer>Published under <code>/dossier-qa/</code> on
 <a href="https://github.com/deccanai-org/approved-tasks-report">deccanai-org/approved-tasks-report</a>.
 Older mixed set stays at <a href="../dossier/">/dossier/</a>.
 Template after <a href="https://dhigdec.github.io/breaker-dossier/">breaker-dossier</a>.</footer>
</div>
</body></html>
"""

(OUT / "index.html").write_text(INDEX)
print("wrote index.html")
