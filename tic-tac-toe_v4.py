import json

# Tic-Tac-Toe Funktionen
def print_board(board):
    # Druckt das aktuelle Spielbrett auf die Konsole
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Überprüft, ob der angegebene Spieler gewonnen hat
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    # Überprüft, ob das Spiel ein Unentschieden ist
    return all(all(cell != " " for cell in row) for row in board)

def get_move(player, board):
    # Fordert den Spieler auf, einen gültigen Zug einzugeben
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if move < 0 or move >= 9:
                print("Invalid move. Please try again.")
            elif board[move // 3][move % 3] != " ":
                print("Cell already taken. Please try again.")
            else:
                return move // 3, move % 3
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def ask_question(questions, current_question_index):
    # Zeigt die nächste Frage in der Reihenfolge an und aktualisiert den Index
    question_set = questions[current_question_index // len(questions[0]['Fragen'])]  # Wählt den Katalog
    question = question_set['Fragen'][current_question_index % len(question_set['Fragen'])]  # Wählt die Frage
    print(f"Question: {question['Frage']}")
    input("Press Enter to continue...")  # Warte auf Benutzereingabe, um fortzufahren
    return (current_question_index + 1) % (len(questions) * len(questions[0]['Fragen']))  # Nächster Index

def play_game(questions):
    # Führt das Tic-Tac-Toe-Spiel durch
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0
    current_question_index = 0

    while True:
        print_board(board)
        row, col = get_move(players[turn], board)
        board[row][col] = players[turn]
        current_question_index = ask_question(questions, current_question_index)

        if check_winner(board, players[turn]):
            print_board(board)
            print(f"Player {players[turn]} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        turn = 1 - turn

# Lade Fragen aus JSON-Datei
with open('fragen.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)['Fragen']

if __name__ == "__main__":
    # Startet das Spiel, wenn das Skript direkt ausgeführt wird
    play_game(questions)
