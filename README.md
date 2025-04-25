# Tic-Tac-Toe AI

A classic Tic-Tac-Toe game with an unbeatable AI opponent, implemented in two versions: a Python console application and a web-based HTML/JavaScript application.

## Features
- Play against an AI using the Minimax algorithm for optimal moves.
- Python version: Rich library for a colorful console interface, score tracking, and replay option.
- Web version: Responsive UI with Tailwind CSS, visual feedback for wins/draws, and restart functionality.
- Choose your marker (X or O) and who goes first (Python version).
- Highlights winning combinations and displays game status.

## Prerequisites
### Python Version
- Python 3.10+
- `rich` library (`pip install rich`)

### Web Version
- Modern web browser (no additional dependencies)

## Files
- `main.py`: Python console-based Tic-Tac-Toe game.
- `index.html`: Web-based Tic-Tac-Toe game with HTML, CSS (Tailwind), and JavaScript.

## How to Run
### Python Version
1. Ensure Python and `rich` are installed:
   ```bash
   pip install rich
   ```
   or
   ```bash
   uv sync
   ```
3. Run the script:
   ```bash
   python main.py
   ```
   or
   ```bash
   uv run main.py
   ```
5. Follow prompts to choose your marker, who goes first, and make moves (1-9).

### Web Version
1. Open `index.html` in a web browser.
2. Click cells to make moves as X; AI plays as O.
3. Use the "Restart Game" button to play again.

## Gameplay
- The game alternates between player and AI turns.
- The AI uses the Minimax algorithm to make optimal moves, ensuring it never loses.
- A game ends with a win (three markers in a row, column, or diagonal) or a draw (board full).
- Python version tracks scores across multiple games.
- Web version highlights winning cells and shows a message for game outcomes.

## License
This project is open-source and available under the MIT License.
