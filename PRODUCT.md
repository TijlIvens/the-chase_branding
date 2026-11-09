# The Chase — Product spec (v1)

The rules of the game. `BRAND_BOOK.md` §1 has the story and cast; this file says what the app
does. Where they differ, **this file wins on mechanics** and the brand book wins on look and voice.

## In one sentence

A walking trivia game: players visit real places in their city, answer a multiple-choice
question at each one to recover a Diamond Beacon for Mr. Chase and Aero, and every player
earns coupons for local businesses.

## Game modes

| | **Free roam** | **Timed route** | **Live event** |
|---|---|---|---|
| What | Self-guided tour: learn about the city, at your own pace | A fixed route of locations, raced against the clock | A city-wide game on a set date and time; everyone plays together |
| Clock | No | Yes: starts at the first location, stops at the last | Yes |
| Wrong answer | Try again, no penalty | **+5 s, try again** until correct | **+5 s, try again** until correct |
| Win condition | Collect every beacon in the city over time (progress, badges) | Fastest total time on the route leaderboard | Fastest total time on the event leaderboard |
| Price | **Free** | Some free (e.g. a starter route per city), some paid | **Paid ticket** |
| Steps counted | Yes | Yes | Yes |

**Paid games come in two kinds:**
- **Themed routes** for an audience (e.g. kids, history, foodies, nightlife). Anyone can buy one and play it solo.
- **Private group games** bought by a group (school class, company outing, party). The group gets a
  private route and a join code. Everyone plays **on their own phone**, solo, and appears on a private
  group leaderboard.

## Core loop (one location)

1. The map shows the next beacon (`marker-beacon`).
2. The player walks there. Within the **GPS radius** (≈ 30–50 m) the question unlocks; it can't be
   opened from further away.
3. A multiple-choice question appears, on the city, general knowledge or pop culture.
4. **Correct** → points, beacon collected (`marker-collected`), a short scripted line from Aero.
   **Wrong** → in timed modes **+5 s**, then the player answers again. No skipping and **no hints**.
5. Next location. After the last one: results screen with total time (including penalties), rank, steps
   walked and coupons earned.

## Rules

- **Solo only** at launch: one player, one phone, one score.
- **Account required** (Sign in with Apple, Google or email) before playing.
- **Leaderboards** are per route and per event, ranked by total time = elapsed time + 5 s × wrong answers.
  Private group games have their own leaderboard.
- **Steps** are a stat only: steps per game and lifetime steps on the results screen and profile. They
  never affect score or rank.
- **No hints.** Aero tells the story, but doesn't help answer questions.
- **Aero** speaks in **scripted story beats**: at the start, at each beacon and at the end. Mr. Chase
  appears through the telepathic link.

## Cities and progress

- The app detects the player's city and shows **that city's games**: free roam, routes and events.
- Progress is stored **per city**, per player. Visiting another city keeps the progress from earlier
  cities, and the player sees the new city's games alongside.
- Profile shows each city played: beacons collected out of the total, routes completed, best times, steps.

## Prizes: coupons

- **Every participant gets coupons**, win or lose, from local shops, bars, restaurants and businesses
  (partners, `marker-partner`).
- Redeemed by **showing the screen**: a coupon screen with a live countdown or animation so a screenshot
  can't be reused; staff tap to mark it used. One use per coupon.

## Content

- **Now:** the founder writes and checks every route and question per city. AI is used only for
  **translation and spell-checking**, and every translation is reviewed before it goes live.
- **Later:** AI drafts location-based questions from photos and location data for cities worldwide,
  always checked by a person before publishing.
- Every question has: location (lat/lng + radius), category (city / general / pop culture), 1 correct
  and 3 wrong options, and a short "did you know" fact shown after a correct answer.

## Launch

- **Platforms:** iOS and Android.
- **Cities:** several Belgian cities plus major cities abroad.
- **Languages:** English, Dutch, French, German, Spanish, Portuguese.

## Not in v1

Team play, hints, AI chat with Aero, AR, user-made routes, steps affecting score.

## Open questions

1. Points: are points shown at all if ranking is purely by time, or only used in free roam?
2. Live events: how far ahead can people buy, is there a player cap, and when do results go live?
3. Coupons: which coupons each player gets (all partners on the route, or one picked by the result),
   and do they expire?
4. Pricing: ticket prices per route/event, and how a group buys (one payer or per player)?
5. Safety: a "don't play while crossing" warning, plus night-time and age rules for nightlife routes.
6. Offline: should a route still work when mobile data drops (download it before starting)?
