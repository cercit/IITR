# PRD: Snakes and Ladders (single HTML file)

## 1. Problem
Classic board games from childhood are hard to play when the people are in different rooms, the board is lost, or the dice roll under the sofa. A browser game that needs no install, no account and no internet fixes that.

## 2. Goal
A complete, playable Snakes and Ladders in one `.html` file. Open it, pick the players, play to 100.

## 3. Users
- Adults who want a quick nostalgic game on a laptop or phone.
- Kids playing with a parent on the same screen.

## 4. Scope (v1)
| In | Out |
|---|---|
| 10x10 board, numbered 1 to 100 in the traditional zig-zag | Online multiplayer |
| 2 to 4 players on one device | Accounts, leaderboards |
| Optional computer player for Player 2 | Sound files (a short beep via Web Audio is fine) |
| Dice roll with animation | Custom boards |
| 10 snakes and 9 ladders, drawn on the board | |
| Exact roll needed to land on 100 | |
| Roll a 6 and you play again | |
| Move log, winner screen, New Game button | |
| Works on phone and desktop, keyboard playable | |

## 5. Rules implemented
1. Everyone starts off the board (square 0). Players take turns.
2. Roll one die and move that many squares.
3. Land on the bottom of a ladder: climb to the top. Land on a snake's head: slide to its tail.
4. A roll of 6 gives another turn.
5. You must land exactly on 100. If the roll is too big, you stay put.
6. First to 100 wins.

**Snakes (head to tail):** 16-6, 47-26, 49-11, 56-53, 62-19, 64-60, 87-24, 93-73, 95-75, 98-78
**Ladders (bottom to top):** 1-38, 4-14, 9-31, 21-42, 28-84, 36-44, 51-67, 71-91, 80-100

## 6. Requirements
| ID | Requirement |
|---|---|
| R1 | Board shows squares 1-100, bottom-left start, alternating direction each row |
| R2 | Each player has a coloured token and name; the current player is highlighted |
| R3 | Roll button and Space key both roll; disabled while a move is animating or when it is the computer's turn |
| R4 | Token moves square by square, then snake or ladder move is shown |
| R5 | Rules in section 5 enforced exactly |
| R6 | Computer rolls on its own after a short pause |
| R7 | Game log lists the last moves in plain words |
| R8 | Winner message and a New Game button |
| R9 | Layout fits a 360px wide phone with no sideways scroll |
| R10 | No external libraries, fonts or images |

## 7. Success checks (what I will test)
- Token path for a roll that crosses a row end follows the zig-zag (e.g. from 8, roll 4, ends on 12).
- Landing on 1, 4, 9... climbs; landing on 16, 47... slides.
- Overshoot at 98 with a roll of 5 leaves the player on 98.
- A 6 gives the same player another turn; a 6 that wins ends the game.
- 4 players cycle in order; the computer takes its turn without clicks.
- New Game resets everything.

## 8. Risks
| Risk | Handling |
|---|---|
| Snakes and ladders chain (a ladder top is a snake head) | Board data has none; a test checks this |
| Computer turn clicked by a human | Roll button disabled during computer turns |
| Animation timers overlapping after New Game | A turn counter cancels stale timers |
