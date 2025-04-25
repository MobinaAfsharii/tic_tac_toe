import math
import os
import random
import sys
from typing import Literal

try:
    from rich import print
    from rich.panel import Panel
    from rich.prompt import Confirm, IntPrompt, Prompt
except ImportError:
    print("Error: 'rich' library not found.")
    print("Please install it using: pip install rich")
    sys.exit(1)

Board = list[str]
PlayerMarker = Literal["X", "O"]
ScoreDict = dict[str, int]

EMPTY = " "
PLAYER_DEFAULT: PlayerMarker = "X"
AI_DEFAULT: PlayerMarker = "O"

PLAYER_COLOR = "bold blue"
AI_COLOR = "bold red"
BOARD_COLOR = "grey70"
WIN_COLOR = "bold green"
DRAW_COLOR = "bold yellow"
ERROR_COLOR = "bold red"
INFO_COLOR = "cyan"

WINNING_COMBINATIONS: list[tuple[int, int, int]] = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def clear_screen() -> None:
    _ = os.system("cls" if os.name == "nt" else "clear")


def print_board(
    board: Board,
    player_marker: PlayerMarker,
    ai_marker: PlayerMarker,
    winning_combo: tuple[int, int, int] | None = None,
) -> None:
    clear_screen()
    print(
        Panel(
            "[bold magenta]Tic-Tac-Toe AI[/bold magenta]",
            expand=False,
            border_style="magenta",
        )
    )

    grid = "\n[{}]{}---{}---{}[/]\n".format(BOARD_COLOR, "+", "+", "+")
    for i in range(0, 9, 3):
        row_cells: list[str] = []
        for j in range(3):
            idx = i + j
            cell_content = board[idx]
            cell_style = BOARD_COLOR

            if cell_content == player_marker:
                cell_style = PLAYER_COLOR
            elif cell_content == ai_marker:
                cell_style = AI_COLOR
            else:

                cell_content = str(idx + 1)

            if winning_combo and idx in winning_combo:
                cell_style = f"{WIN_COLOR} on {BOARD_COLOR}"

            row_cells.append(
                f"[on {BOARD_COLOR}][{cell_style}]{' ' + cell_content + ' '}[/][on {BOARD_COLOR}]"
            )

        grid += "[{}]{}[/]{}[{}]{}[/]{}[{}]{}[/]\n".format(
            BOARD_COLOR,
            "|",
            row_cells[0],
            BOARD_COLOR,
            "|",
            row_cells[1],
            BOARD_COLOR,
            "|",
        )
        if i < 6:
            grid += "[{}]{}---{}---{}[/]\n".format(BOARD_COLOR, "+", "+", "+")

    print(grid)


def get_available_moves(board: Board) -> list[int]:
    return [i for i, spot in enumerate(board) if spot == EMPTY]


def is_board_full(board: Board) -> bool:
    return EMPTY not in board


def check_win(board: Board, player: PlayerMarker) -> tuple[int, int, int] | None:
    for combo in WINNING_COMBINATIONS:
        if all(board[i] == player for i in combo):
            return combo
    return None


def check_game_over(
    board: Board, player_marker: PlayerMarker, ai_marker: PlayerMarker
) -> bool:
    return (
        bool(check_win(board, player_marker))
        or bool(check_win(board, ai_marker))
        or is_board_full(board)
    )


def get_player_move(board: Board, player_marker: PlayerMarker) -> int:
    available_moves = get_available_moves(board)
    while True:
        try:
            move_num = IntPrompt.ask(
                f"[{PLAYER_COLOR}]Your turn ({player_marker})[/]. Enter move ([bold yellow]1-9[/])",
                choices=[str(m + 1) for m in available_moves],
                show_choices=False,
            )
            move_index = move_num - 1

            if move_index in available_moves:
                return move_index
            else:

                print(
                    f"[{ERROR_COLOR}]Invalid move. Cell not available or out of range.[/]"
                )
        except ValueError:
            print(f"[{ERROR_COLOR}]Invalid input. Please enter a number.[/]")
        except Exception as e:
            print(f"[{ERROR_COLOR}]An unexpected error occurred: {e}[/]")


def evaluate_board(
    board: Board, player_marker: PlayerMarker, ai_marker: PlayerMarker
) -> int:
    if check_win(board, ai_marker):
        return 10
    elif check_win(board, player_marker):
        return -10
    else:
        return 0


def minimax(
    board: Board,
    depth: int,
    is_ai_turn: bool,
    player_marker: PlayerMarker,
    ai_marker: PlayerMarker,
) -> float:
    score = evaluate_board(board, player_marker, ai_marker)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if is_board_full(board):
        return 0

    available_moves = get_available_moves(board)

    if is_ai_turn:
        best_score = -math.inf
        for move in available_moves:
            board[move] = ai_marker
            current_score = minimax(board, depth + 1, False, player_marker, ai_marker)
            board[move] = EMPTY
            best_score = max(best_score, current_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves:
            board[move] = player_marker
            current_score = minimax(board, depth + 1, True, player_marker, ai_marker)
            board[move] = EMPTY
            best_score = min(best_score, current_score)
        return best_score


def find_best_move(
    board: Board, player_marker: PlayerMarker, ai_marker: PlayerMarker
) -> int:
    best_score = -math.inf
    best_move = -1
    available_moves = get_available_moves(board)

    if not available_moves:
        return -1

    for move in available_moves:
        board[move] = ai_marker
        move_score = minimax(board, 0, False, player_marker, ai_marker)
        board[move] = EMPTY

        if move_score > best_score:
            best_score = move_score
            best_move = move

    if best_move == -1 and available_moves:

        return random.choice(available_moves)

    return best_move


def display_scores(scores: ScoreDict) -> None:
    print(
        Panel(
            f"[bold green]Player Wins:[/bold green] {scores['player']} | [bold red]AI Wins:[/bold red] {scores['ai']} | [bold yellow]Draws:[/bold yellow] {scores['draws']}",
            title="[bold]Scoreboard[/bold]",
            expand=False,
            border_style="blue",
        )
    )


def play_game() -> None:
    scores: ScoreDict = {"player": 0, "ai": 0, "draws": 0}

    while True:
        clear_screen()
        print(
            Panel(
                "[bold magenta]Welcome to Tic-Tac-Toe AI![/bold magenta]",
                expand=False,
                border_style="magenta",
            )
        )

        player_marker_choice = Prompt.ask(
            f"Choose your marker ([{PLAYER_COLOR}]X[/] or [{AI_COLOR}]O[/])",
            choices=["X", "O"],
            default="X",
        ).upper()
        player_marker: PlayerMarker = "X" if player_marker_choice == "X" else "O"
        ai_marker: PlayerMarker = "O" if player_marker == "X" else "X"

        first_turn = Prompt.ask(
            "Who goes first?", choices=["Player", "AI"], default="Player"
        )
        current_player_marker: PlayerMarker = (
            player_marker if first_turn == "Player" else ai_marker
        )

        current_board: Board = [EMPTY] * 9
        game_is_over = False
        winning_combo = None

        while not game_is_over:
            print_board(current_board, player_marker, ai_marker, winning_combo)
            display_scores(scores)

            if current_player_marker == player_marker:
                move = get_player_move(current_board, player_marker)
                current_board[move] = player_marker
                winning_combo = check_win(current_board, player_marker)
                if winning_combo:
                    print_board(current_board, player_marker, ai_marker, winning_combo)
                    display_scores(scores)
                    print(
                        Panel(
                            f"[{WIN_COLOR}]🎉 Congratulations! You won! 🎉[/]",
                            border_style=WIN_COLOR,
                        )
                    )
                    scores["player"] += 1
                    game_is_over = True
                else:
                    current_player_marker = ai_marker

            else:
                print(f"[{INFO_COLOR}]AI's turn ({ai_marker})...[/]")
                move = find_best_move(current_board, player_marker, ai_marker)

                if move != -1:
                    current_board[move] = ai_marker
                    winning_combo = check_win(current_board, ai_marker)
                    if winning_combo:
                        print_board(
                            current_board, player_marker, ai_marker, winning_combo
                        )
                        display_scores(scores)
                        print(
                            Panel(
                                f"[{ERROR_COLOR}]🤖 AI wins! Better luck next time. 🤖[/]",
                                border_style=ERROR_COLOR,
                            )
                        )
                        scores["ai"] += 1
                        game_is_over = True
                    else:
                        current_player_marker = player_marker
                else:
                    print(f"[{ERROR_COLOR}]Error: AI could not find a move.[/]")
                    game_is_over = True

            if not game_is_over and is_board_full(current_board):
                print_board(current_board, player_marker, ai_marker)
                display_scores(scores)
                print(
                    Panel(
                        f"[{DRAW_COLOR}]🤝 It's a draw! 🤝[/]", border_style=DRAW_COLOR
                    )
                )
                scores["draws"] += 1
                game_is_over = True

        display_scores(scores)
        if not Confirm.ask("\n[bold green]Play again?[/]", default=True):
            break

    print("\n[bold magenta]Thanks for playing![/bold magenta]\n")


if __name__ == "__main__":
    play_game()
