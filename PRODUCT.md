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
| Win condition | Collect every beacon in the city over time (progress, badges) | Fastest total time on the route leaderboard | Fastest total time on the **live** event leaderboard |
| Main-board points | 25 per beacon, first collection only | Yes (×1 free, ×1.5 paid) | Yes (×1.5) |
| Price | **Free** | Some free (e.g. a starter route per city), some paid | **Paid ticket** |
| Steps counted | Yes | Yes | Yes |

**Paid games come in two kinds:**
- **Themed routes** for an audience (e.g. kids, history, foodies, nightlife). Anyone can buy one and play it solo.
- **Private group games** bought by **one organiser** for a set number of players (school class,
  company outing, bachelor party). The organiser picks one of your routes **or builds their own**
  (see *Creating games*). The group gets a join code; players join free.
  Everyone plays **on their own phone**, solo, on a private group leaderboard. **These never count
  towards the main leaderboard.**

**Exclusive prize games** are a fourth, invite-only kind: you invite top and Hall of Fame players
(via the in-app inbox) to play for big prizes. They have their own leaderboard **and** count towards
the main leaderboard like a paid game.

## Creating games

Three kinds of creator:

| Creator | Can make | Visible to | Checks | Main-board points |
|---|---|---|---|---|
| **The Chase (you)** | Free routes, paid themed routes, live events, exclusive prize games | Everyone (or invited, for prize games) | You write and check every question | Yes |
| **Verified company** (school, employer, event agency, tourist office) | Private group games | Only people they invite | Business verification once, then auto-checks per game | No |
| **Player** (18+) | Private group games | Only people they invite | Auto-checks per game | No |

**Creator tool** (in the app): pick a city, drop beacon locations on the map, write a multiple-choice
question per location (1 correct + 3 wrong answers, optional "did you know"), set a par time, number of
players and date window, pay, and share the code. Aero's story lines are fixed and added automatically.

**Rules for player and company games**
- **Private only.** Never listed publicly, never searchable; joinable only by invite.
- **Creators must be 18+** (age confirmed at sign-up). Minors can only join games from a **verified
  company** (e.g. their school) or with a parent's approval.
- **Automatic checks before a game goes live:** blocked words and offensive content in questions and
  names; locations must be public places (no homes, private property, schools after hours, motorways,
  railway tracks, water edges or construction sites); locations must be reachable on foot; a maximum
  walking distance between beacons. A game that fails is not published, and the creator sees why.
- **Report button** on every game and invite. You review reports and can take a game down or ban a
  creator. Three upheld reports = creator can no longer make games.

## Trusted invites

A player should only play with people they know or with a well-known company.

- **Verified companies** go through business verification (company registration number, website,
  work email) and get a **verified badge** on their profile and invites.
- **Players can only invite people they know:** friends in the app, phone contacts (only if the player
  allows contact access) or a join code shared in person. No inviting strangers by username, and no
  public "looking for players".
- **Every invite shows who sent it:** name, photo, verified badge (if any), account age, games hosted
  and rating, plus where and when the game takes place. Buttons: **Accept**, **Decline**, **Report**,
  **Block**.
- **Block** stops that creator from inviting or messaging the player again. Blocked and reported
  creators are never told who blocked or reported them.
- Invites from someone who is **not** a friend, contact or verified company show a clear warning:
  "You don't know this person. Only join games from people you know or verified companies."
- Players never see each other's exact location, phone number or email, only name, photo and
  leaderboard times.

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
- **Online required** throughout a game: no offline mode. If the connection drops, the game pauses with
  a reconnecting screen; the clock keeps running (it is measured server-side).
- **Steps** are a stat only: steps per game and lifetime steps on the results screen and profile. They
  never affect score or rank.
- **No hints.** Aero tells the story, but doesn't help answer questions.
- **Aero** speaks in **scripted story beats**: at the start, at each beacon and at the end. Mr. Chase
  appears through the telepathic link.

## Points and leaderboards

**Time decides every game; points add games up.**

Every timed game has its own leaderboard ranked by **total time**, measured to the millisecond:
elapsed time + 5 s × wrong answers. Live events show the leaderboard **live** while they run.

Each game also earns **points** for the **main leaderboard**:

```
points = beacons collected × 100 × speed factor × game multiplier
speed factor    = par time ÷ total time, capped between 0.5 and 2.0
game multiplier = 1.0 free route · 1.5 paid route · 1.5 live event · 1.5 exclusive prize game
free roam       = 25 points per beacon, the first time it is collected (no clock, no multiplier)
```

- **Par time** is set per route by the route author (expected walking + answering time). Later it can
  be tuned to the median player time.
- Example: paid 10-beacon route, par 60:00, finished in 45:00.000 →
  10 × 100 × 1.333 × 1.5 = **2,000 points**. The same run on a free route = 1,333.
- **Best score per route counts.** Replaying a route only adds the difference if you beat your best,
  so farming one route doesn't work. Each live event counts once.
- Points are calculated from millisecond times. Ties go to whoever reached the total first.
- **Private group games are excluded.** Free routes, paid routes, live events, exclusive prize games and
  free roam all count.
- Paid games earn 1.5× points; the app says so on paid routes ("Earns 1.5× points") to recommend them.

**Main leaderboard** views: **worldwide**, **per country**, **per city** (a player's city total
counts only games played in that city).

**Hall of Fame** (per city): the city's all-time **top 10 by points**. Spots can be lost: anyone who
earns more points takes the place.
- **Heads-up:** when another player gets within 10% of a Hall of Fame member's points, the member gets
  an inbox message and push notification: "Someone is catching up on your Hall of Fame spot in
  Antwerp. Play a game to defend it." It suggests a paid route (1.5× points). Sent at most once a week.
- Hall of Fame and top main-board players are the pool for **exclusive prize game** invites.

**Invites and messages** go only to the **in-app inbox** (with optional push notifications), never to
email. Players can turn prize-game invites off in settings. Sign-in email is used for the account
only (GDPR).

## Cities and progress

- The app detects the player's city and shows **that city's games**: free roam, routes and events.
- Progress is stored **per city**, per player. Visiting another city keeps the progress from earlier
  cities, and the player sees the new city's games alongside.
- Profile shows each city played: beacons collected out of the total, routes completed, best times, steps.

## Prizes: coupons

- **Every participant gets coupons** after **every** game, win or lose: free roam tours, routes, events,
  private group games and prize games. They come from local shops, bars, restaurants and businesses
  (partners, `marker-partner`).
- Coupons are **available immediately** after the last question is answered and the game or tour ends,
  on the results screen and in a **Coupons wallet**.
- A player gets **all coupons that are active** for that game's city at the moment it ends. Expired
  coupons are never given out (this matters for private games booked in advance).
- **Each partner sets its own expiry date.** The wallet shows it and warns 2 days before.
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

Team play, hints, AI chat with Aero, AR, public player-made games, steps affecting score, offline
play, email marketing, direct chat between players.

## Safety

**Warnings the app shows**

| When | Warning |
|---|---|
| First launch and the start of every game | "Stay aware of your surroundings. Watch for traffic and never use your phone while crossing the street." |
| Joining any private game | "Only play with people you know or verified companies. Meet in public places. Tell someone where you're going." |
| Invite from someone not in your friends or contacts | "You don't know this person. Only join games from people you know or verified companies." |
| Moving fast (bike, car) | Questions stay locked: "Stop somewhere safe to answer." |
| Evening game or nightlife route | "It's getting dark. Stay in well-lit areas and keep your group together." 18+ routes need a confirmed age |
| Phone battery below 20% | "Battery low. Make sure you can still get home and contact someone." |
| Creating a game | "Choose public, safe places. Your game is checked before it goes live, and players can report it." |

**Other safety rules**
- Questions never unlock while the player is moving fast (e.g. on a bike or in a car).
- Nightlife and pub routes are marked **18+** and require a confirmed age.
- Routes avoid private property and dangerous crossings; live events have an end time before dark
  unless they're explicitly night events.

## Open questions

1. Ticket prices per paid route, live event, and private group game (per player), and whether
   creating your own private game costs more than booking one of yours.
2. Player cap per live event, and how far ahead tickets can be bought.
3. Prizes for exclusive prize games: who funds them (you or partners)?
4. Free roam badges: which milestones (e.g. 25 / 50 / 100% of a city's beacons)?
5. Business verification: done by you by hand, or by an external service?
