
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
