import json
import RPi.GPIO as GPIO
from time import sleep
from RPLCD.i2c import CharLCD

class Keypad:
    def __init__(self, column_count=4):
        GPIO.setmode(GPIO.BOARD)
        self.KEYPAD = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ["*", 0, "#", "D"]
        ]
        self.ROW = [26, 24, 23, 22]
        self.COLUMN = [18, 19, 21, 32]

    def get_key(self):
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        row_val = -1
        for i in range(len(self.ROW)):
            tmp_read = GPIO.input(self.ROW[i])
            if tmp_read == 0:
                row_val = i
        if row_val < 0 or row_val > 3:
            self.exit()
            return None
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.ROW[row_val], GPIO.OUT)
        GPIO.output(self.ROW[row_val], GPIO.HIGH)
        col_val = -1
        for j in range(len(self.COLUMN)):
            tmp_read = GPIO.input(self.COLUMN[j])
            if tmp_read == 1:
                col_val = j
        if col_val < 0 or col_val > 3:
            self.exit()
            return None
        self.exit()
        return self.KEYPAD[row_val][col_val]

    def exit(self):
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

class TicTacToe:
    def __init__(self, questions_file):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = ["X", "O"]
        self.turn = 0
        self.current_question_index = 0
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)['Fragen']
        
        self.keypad = Keypad()
        
        self.lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)
        self.lcd.clear()

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(self, player):
        return any(all(s == player for s in row) for row in self.board) or \
               any(all(row[col] == player for row in self.board) for col in range(3)) or \
               all(self.board[i][i] == player for i in range(3)) or \
               all(self.board[i][2 - i] == player for i in range(3))

    def check_draw(self):
        return all(all(cell != " " for cell in row) for row in self.board)

    def get_move(self):
        while True:
            move = self.keypad.get_key()
            if isinstance(move, int) and 1 <= move <= 9:
                move -= 1
                if self.board[move // 3][move % 3] == " ":
                    return move // 3, move % 3

    def scroll_text(self, text, choices, num_rows=4, num_cols=20, delay=2.0):
        pos = 0
        lines = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
        for key in choices:
            lines.append(f"{key}: {choices[key]}")
        print(lines)
        curr_line = 0
        while True:
            self.lcd.clear()
            for i in range(num_rows):
                self.lcd.cursor_pos = (i, 0)
                line_text = lines[i + curr_line]
                self.lcd.write_string(line_text)
            curr_line += 1
            if (curr_line + num_rows) > len(lines):
                curr_line = 0
            
            for i in range(20):
                key = self.keypad.get_key()
                if key in ["A", "B"]:
                    return key
                sleep(delay / 20)

    def ask_question(self):
        question_set = self.questions[self.current_question_index // len(self.questions[0]['Fragen'])]
        question = question_set['Fragen'][self.current_question_index % len(question_set['Fragen'])]
        
        choice = question["Optionen"]
        answer = self.scroll_text(question['Frage'],choice)
        
        correct_answer = question['Antwort']['key']
        #if (answer == 'A' and correct_answer == 'A') or (answer == 'B' and correct_answer == 'B'):
        if answer == correct_answer:
            self.lcd.clear()
            self.lcd.cursor_pos = (0, 0)
            self.lcd.write_string("Richtig!")
            sleep(2)
            return True
        
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string("Falsch!")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(f"Antwort: {question['Antwort']['text']}")
        sleep(2)
        return False

    def play_game(self):
        while True:
            self.print_board()
            row, col = self.get_move()
            print(f"Spieler {self.players[self.turn]} wählt Feld ({row}, {col})")

            if self.ask_question():
                self.board[row][col] = self.players[self.turn]
                if self.check_winner(self.players[self.turn]):
                    self.print_board()
                    print(f"Spieler {self.players[self.turn]} gewinnt!")
                    self.lcd.clear()
                    self.lcd.cursor_pos = (0, 0)
                    self.lcd.write_string(f"Spieler {self.players[self.turn]} gewinnt!")
                    sleep(2)
                    break
                elif self.check_draw():
                    self.print_board()
                    print("Es ist unentschieden!")
                    self.lcd.clear()
                    self.lcd.cursor_pos = (0, 0)
                    self.lcd.write_string("Es ist unentschieden!")
                    sleep(2)
                    break

            self.current_question_index = (self.current_question_index + 1) % (len(self.questions) * len(self.questions[0]['Fragen']))
            self.turn = 1 - self.turn

if __name__ == "__main__":
    game = TicTacToe('fragen.json')
    game.play_game()
    GPIO.cleanup()
