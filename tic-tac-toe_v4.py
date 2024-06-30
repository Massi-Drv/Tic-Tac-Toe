import json

class TicTacToe:
    def __init__(self, questions_file):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.turn = 0
        self.current_question_index = 0
        with open(questions_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)['Fragen']

    def print_board(self):
        # Drucke das Tic-Tac-Toe-Brett
        for row in self.board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(self, player):
        # Überprüfen, ob der aktuelle Spieler gewonnen hat
        return any(all(s == player for s in row) for row in self.board) or \
               any(all(row[col] == player for row in self.board) for col in range(3)) or \
               all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2 - i] == player for i in range(3))

    def check_draw(self):
        # Überprüfen, ob das Spiel unentschieden ist
        return all(all(cell != " " for cell in row) for row in self.board)

    def get_move(self):
        # Hole den Zug des Spielers
        while True:
            try:
                move = int(input(f"Spieler {self.players[self.turn]}, gib deinen Zug (1-9) ein: ")) - 1
                if 0 <= move < 9 and self.board[move // 3][move % 3] == " ":
                    return move // 3, move % 3
                print("Ungültiger Zug. Bitte versuche es erneut.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl zwischen 1 und 9 ein.")

    def ask_question(self):
        # Stelle eine Frage und überprüfe die Antwort
        question_set = self.questions[self.current_question_index // len(self.questions[0]['Fragen'])]
        question = question_set['Fragen'][self.current_question_index % len(question_set['Fragen'])]
        print(f"Frage: {question['Frage']}")
        answer = input("Bitte antworte mit Ja oder Nein: ").strip().capitalize()
        
        correct_answer = question['Antwort']['key']
        if (answer == 'Ja' and correct_answer == 'A') or (answer == 'Nein' and correct_answer == 'B'):
            print("Richtig!")
            return True
        print(f"Falsch! Die richtige Antwort ist: {question['Antwort']['text']}")
        return False

    def play_game(self):
        # Hauptspielschleife
        while True:
            self.print_board()
            row, col = self.get_move()
            
            if self.ask_question():
                self.board[row][col] = self.players[self.turn]
                if self.check_winner(self.players[self.turn]):
                    self.print_board()
                    print(f"Spieler {self.players[self.turn]} gewinnt!")
                    break
                elif self.check_draw():
                    self.print_board()
                    print("Es ist unentschieden!")
                    break
            
            self.current_question_index = (self.current_question_index + 1) % (len(self.questions) * len(self.questions[0]['Fragen']))
            self.turn = 1 - self.turn

if __name__ == "__main__":
    game = TicTacToe('fragen.json')
    game.play_game()
