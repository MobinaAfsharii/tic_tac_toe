import random


def generate_population():
    return [[random.choice(range(9)) for _ in range(9)] for _ in range(50)]


def calculate_fitness(chromosome, current_state):
    wins = sum(play_round(chromosome, current_state, player=-1) for _ in range(10))
    return wins


def play_round(chromosome, current_state, player):
    board = current_state.copy()
    current_player = 1

    for move in chromosome:
        if board[move] == 0:
            board[move] = current_player
            if check_victory(board, current_player):
                return 1 if current_player == player else 0
            current_player *= -1

    return 0


def check_victory(board, player):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(all(board[i] == player for i in combo) for combo in winning_combinations)


def evaluate_move(move, board, player):
    temp_board = board.copy()
    temp_board[move] = player

    if check_victory(temp_board, player):
        return 2
    temp_board[move] = -player

    if check_victory(temp_board, -player):
        return 1
    return 0


def genetic_strategy(current_state):
    population = generate_population()

    for _ in range(50):
        fitness_scores = [
            calculate_fitness(chromosome, current_state) for chromosome in population
        ]
        best_chromosome = population[fitness_scores.index(max(fitness_scores))]
        new_population = [best_chromosome]

        for _ in range(50 - 1):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            crossover_point = random.randint(1, len(parent1) - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]

            if random.uniform(0, 1) < 0.1:
                gene_to_mutate = random.randint(0, len(child) - 1)
                child[gene_to_mutate] = random.choice(
                    [i for i in range(9) if current_state[i] == 0]
                )

            new_population.append(child)

        population = new_population

    available_moves = [move for move in range(9) if current_state[move] == 0]
    move_scores = [evaluate_move(move, current_state, -1) for move in available_moves]
    best_move = available_moves[move_scores.index(max(move_scores))]

    return best_move


def display_board(board):
    for i in range(0, 9, 3):
        print(" | ".join(map(str, board[i : i + 3])))
        if i < 6:
            print("********")


def is_board_filled(board):
    return all(cell != 0 for cell in board)


def get_player_move(board):
    while True:
        try:
            move = int(input("یک عدد بین یک تا ۹ وارد کن. "))
            if 1 <= move <= 9 and board[move - 1] == 0:
                return move - 1
            else:
                print("لطفا یکی از اعداد استفاده نشده را وارد کنید.")
        except ValueError:
            print("لطفا یکی از اعداد استفاده نشده را وارد کنید.")


game_board = [0] * 9
current_player = 1

while 1:
    if current_player == 1:
        display_board(game_board)
        player_move = get_player_move(game_board)
        game_board[player_move] = current_player
    else:
        opponent_move = genetic_strategy(current_state=game_board)
        game_board[opponent_move] = current_player

    if check_victory(game_board, current_player):
        display_board(game_board)
        print("بردیییی!!!!!!!!!" if current_player == 1 else "باختی :()")
        break

    if is_board_filled(game_board):
        display_board(game_board)
        print("مساوی شد.")
        break

    current_player *= -1
