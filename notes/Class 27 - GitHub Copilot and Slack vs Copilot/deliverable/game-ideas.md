# Childhood games that fit in one HTML file

Each one runs by opening a single file in a browser, with no libraries. Sorted from smallest build to largest.

| # | Game | Why it works in one file | Build size |
|---|---|---|---|
| 1 | Tic-Tac-Toe (with an unbeatable computer player) | 3x3 grid, minimax is about 30 lines | Small |
| 2 | Hangman | Word list in an array, SVG gallows | Small |
| 3 | Snakes and Ladders | Board is a grid, dice is one random call | Small |
| 4 | Simon Says (colour and sound memory) | Web Audio tones, no sound files | Small |
| 5 | Rock Paper Scissors (best of 5) | Pure logic, add animation for polish | Small |
| 6 | Whack-a-Mole | Timers and click events, score and best score | Small |
| 7 | 2048 | Grid slide and merge, swipe and arrow keys | Medium |
| 8 | Minesweeper | Flood-fill reveal, flags, first click safe | Medium |
| 9 | Snake | Canvas loop, speed rises with score | Medium |
| 10 | Sliding Puzzle (15-puzzle) | Solvable shuffle check, move counter | Medium |
| 11 | Connect Four | Gravity drop, win check in four directions | Medium |
| 12 | Ludo (2 to 4 players, local) | Board path array, token capture rules | Large |
| 13 | Word Search | Grid generator, drag to select | Large |
| 14 | Pac-Man style maze chase | Canvas, simple ghost AI | Large |

My pick for a first second-game: **Snakes and Ladders**. It is a game Indian kids actually grew up with, the rules fit on a card, and it gives a good PRD (players, dice, special squares, win state). Tic-Tac-Toe is the quickest if you want a fast win.

Reply with the number and I will write the PRD, build the game and update the README.
