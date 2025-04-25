
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
