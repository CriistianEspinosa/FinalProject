import pygame
import sys
import sqlite3

# Pygame Initialization
pygame.init()

# Constants and Global Variables
WIDTH, HEIGHT = 1000, 700
BOARD_WIDTH, BOARD_HEIGHT = 900, 600
BG_COLOR = (214, 201, 227)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Load and Scale Images
BOARD = pygame.image.load("Board.png")
BOARD = pygame.transform.scale(BOARD, (BOARD_WIDTH, BOARD_HEIGHT))
X_IMG = pygame.image.load("X.png")
X_IMG = pygame.transform.scale(X_IMG, (120, 120))
O_IMG = pygame.image.load("O.png")
O_IMG = pygame.transform.scale(O_IMG, (143, 143))
TIC = pygame.image.load("TicTacToe.png")
TIC = pygame.transform.scale(TIC, (450, 210))
START_BUTTON_IMG = pygame.image.load("STAR.png")
START_BUTTON_IMG = pygame.transform.scale(START_BUTTON_IMG, (200, 100))

# Game Variables
board = [['', '', ''], ['', '', ''], ['', '', '']]
graphical_board = [[[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]]]
to_move = 'X'
game_finished = False

# Scoring Variables
score_X = 0
score_O = 0
draws = 0

# Winning Conditions
victories_X = 0
victories_O = 0

# Database Initialization
def init_db():
    conn = sqlite3.connect('tic_tac_toe_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result TEXT,
            score_X INTEGER,
            score_O INTEGER,
            draws INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_result(result, score_X, score_O, draws):
    conn = sqlite3.connect('tic_tac_toe_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (result, score_X, score_O, draws)
        VALUES (?, ?, ?, ?)
    ''', (result, score_X, score_O, draws))
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect('tic_tac_toe_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results ORDER BY date DESC')
    results = cursor.fetchall()
    conn.close()
    return results

# Function to Display Rules Screen
def show_rules_screen():
    SCREEN.fill(BG_COLOR)
    rules_font = pygame.font.Font("Mario-Kart-DS.ttf", 55)
    text1 = rules_font.render("Welcome   To   Tic   Tac   Toe", True, (0, 0, 0))
    rules_font = pygame.font.Font("VerilySerifMono.otf", 20)
    text2 = rules_font.render("Rules:", True, (0, 0, 0))
    text3 = rules_font.render("1. Players take turns placing 'X' and 'O' on the board.", True, (0, 0, 0))
    text4 = rules_font.render("2. The first player to get three of their marks in a row wins.", True, (0, 0, 0))
    text5 = rules_font.render("3. If all nine squares are filled and no winner is determined, it's a draw.", True, (0, 0, 0))
    
    start_button_rect = START_BUTTON_IMG.get_rect(center=(WIDTH // 2, 615))
    rules_font = pygame.font.Font("mario.ttf", 75)
    textB = rules_font.render("B        C", True, (0, 0, 0))
    
    SCREEN.blit(text1, (160, 50))
    SCREEN.blit(text2, (50, 130))
    SCREEN.blit(text3, (50, 180))
    SCREEN.blit(text4, (50, 230))
    SCREEN.blit(text5, (50, 280))
    SCREEN.blit(textB, (300, 590))
    SCREEN.blit(START_BUTTON_IMG, start_button_rect)
    SCREEN.blit(TIC, (275, 335))
    pygame.display.flip()

# Function to Render Board on Screen
def render_board(board, ximg, oimg):
    global graphical_board
    cell_width = BOARD_WIDTH // 3
    cell_height = BOARD_HEIGHT // 3
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j * cell_width + cell_width // 2 + 50, i * cell_height + cell_height // 2 + 50))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j * cell_width + cell_width // 2 + 50, i * cell_height + cell_height // 2 + 50))

# Function to Add 'X' or 'O' to the Board
def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    cell_width = BOARD_WIDTH // 3
    cell_height = BOARD_HEIGHT // 3
    converted_x = (current_pos[0] - 50) // cell_width
    converted_y = (current_pos[1] - 50) // cell_height
    if 0 <= converted_x < 3 and 0 <= converted_y < 3 and board[converted_y][converted_x] == '':
        board[converted_y][converted_x] = to_move
        to_move = 'O' if to_move == 'X' else 'X'
    
    render_board(board, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board, to_move

# Function to Check for Winner or Draw
def check_win(board):
    winner = None
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            winner = board[row][0]
            return winner

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            winner = board[0][col]
            return winner
   
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        winner = board[0][0]
        return winner
          
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        winner = board[0][2]
        return winner
    
    if winner is None:
        for row in board:
            for cell in row:
                if cell not in ['X', 'O']:
                    return None
        return "DRAW"

# Function to Display Result Screen
def show_result_screen(result):
    global score_X, score_O, draws, victories_X, victories_O
    SCREEN.fill(BG_COLOR)
    rules_font = pygame.font.Font("mario.ttf", 200)
    textGame = rules_font.render("H", True, (0, 0, 0))
    font = pygame.font.Font("VerilySerifMono.otf", 80)
    if result == "DRAW":
        text = font.render("IT'S A DRAW!", True, (0, 0, 0))
        draws += 1
    else:
        text = font.render(f"{result} WINS!", True, (0, 0, 0))
        if result == 'X':
            score_X += 1
            victories_X += 1
        elif result == 'O':
            score_O += 1
            victories_O += 1

    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
    
    # Display Score
    font = pygame.font.Font("VerilySerifMono.otf", 30)
    score_text = font.render(f"Score - X: {score_X}  O: {score_O}  Draws: {draws}", True, (0, 0, 0))
    SCREEN.blit(score_text, (WIDTH // 2.5 - score_text.get_width() // 3, HEIGHT // 3 - score_text.get_height() // 3 + 100))

    # Restart Button
    font = pygame.font.Font("Mario-Kart-DS.ttf", 45)
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(SCREEN, (0, 128, 0), restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    # Quit Button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
    pygame.draw.rect(SCREEN, (128, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (255, 255, 255))
    SCREEN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

    SCREEN.blit(textGame, (440, 60))
    pygame.display.flip()

    # Store result in the database
    insert_result(result, score_X, score_O, draws)

    # Check if game should end
    if victories_X >= 3 or victories_O >= 3 or draws >= 3:
        pygame.time.wait(2000)  # Wait for 2 seconds to show final message
        if victories_X >= 3:
            final_message = "X WINS THE GAME!"
        elif victories_O >= 3:
            final_message = "O WINS THE GAME!"
        else:
            final_message = "IT'S A DRAW GAME!"
        
        SCREEN.fill(BG_COLOR)
        font = pygame.font.Font("VerilySerifMono.otf", 80)
        final_text = font.render(final_message, True, (0, 0, 0))
        SCREEN.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2 - final_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds to show final message
        pygame.quit()
        sys.exit()

# Main Game Function
def main():
    init_db()  # Initialize the database
    show_rules_screen()  # Show Initial Rules Screen

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # On Click of Start Button
                if 380 <= event.pos[0] <= 580 and 595 <= event.pos[1] <= 645:
                    SCREEN.fill(BG_COLOR)  # Change Background to BG_COLOR
                    SCREEN.blit(BOARD, (50, 50))  # Adjust Position According to New Board Size
                    pygame.display.update()
                    run_game()  # Start the Game

# Function to Run the Game
def run_game():
    global board, graphical_board, to_move, game_finished

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_finished:
                    # Check Click on Restart Button
                    if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 50 <= event.pos[1] <= HEIGHT // 2 + 100:
                        # Reset Variables for a New Game
                        board = [['', '', ''], ['', '', ''], ['', '', '']]
                        graphical_board = [[[None, None], [None, None], [None, None]],
                                           [[None, None], [None, None], [None, None]],
                                           [[None, None], [None, None], [None, None]]]
                        to_move = 'X'
                        game_finished = False
                        SCREEN.fill(BG_COLOR)
                        SCREEN.blit(BOARD, (50, 50))
                        pygame.display.update()
                    # Check Click on Quit Button
                    elif WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 150 <= event.pos[1] <= HEIGHT // 2 + 200:
                        pygame.quit()
                        sys.exit()
                else:
                    board, to_move = add_XO(board, graphical_board, to_move)
                    winner = check_win(board)
                    if winner is not None:
                        show_result_screen(winner)
                        game_finished = True
                
                pygame.display.update()

# Start the Game
if __name__ == "__main__":
    main()
