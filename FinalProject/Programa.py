import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Definición de constantes y variables globales
WIDTH, HEIGHT = 1000, 700
BOARD_WIDTH, BOARD_HEIGHT = 900, 600
BG_COLOR = (214, 201, 227)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Carga de imágenes y escalado
BOARD = pygame.image.load("Board.png")
BOARD = pygame.transform.scale(BOARD, (BOARD_WIDTH, BOARD_HEIGHT))
X_IMG = pygame.image.load("X.png")
O_IMG = pygame.image.load("O.png")

# Variables del juego
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]], 
                   [[None, None], [None, None], [None, None]]]
to_move = 'X'
game_finished = False

# Función para mostrar la pantalla de reglas
def show_rules_screen():
    SCREEN.fill(BG_COLOR)
    rules_font = pygame.font.Font(None, 60)  # Using default font
    text1 = rules_font.render("Welcome to Tic Tac Toe!", True, (0, 0, 0))
    rules_font = pygame.font.Font(None, 30)  # Using default font
    text2 = rules_font.render("Rules:", True, (0, 0, 0))
    text3 = rules_font.render("1. Players take turns placing 'X' and 'O' on the board.", True, (0, 0, 0))
    text4 = rules_font.render("2. The first player to get three of their marks in a row wins.", True, (0, 0, 0))
    text5 = rules_font.render("3. If all nine squares are filled and no winner is determined, it's a draw.", True, (0, 0, 0))
    start_button = pygame.Rect(380, 595, 200, 50)
    pygame.draw.rect(SCREEN, (0, 128, 0), start_button)
    button_font = pygame.font.Font(None, 40)  # Using default font
    start_text = button_font.render("Start Game", True, (255, 255, 255))
    SCREEN.blit(text1, (220, 50))
    SCREEN.blit(text2, (50, 150))
    SCREEN.blit(text3, (50, 200))
    SCREEN.blit(text4, (50, 250))
    SCREEN.blit(text5, (50, 300))
    SCREEN.blit(start_text, (400, 610))
    pygame.display.flip()

# Función para renderizar el tablero en la pantalla
def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*250+200, i*250+200))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*250+200, i*250+200))

# Función para añadir 'X' u 'O' al tablero
def add_XO(board, graphical_board, to_move):
    current_pos = pygame.mouse.get_pos()
    converted_x = current_pos[0] // (BOARD_WIDTH // 3)
    converted_y = current_pos[1] // (BOARD_HEIGHT // 3)
    if board[converted_y][converted_x] not in ['O', 'X']:
        board[converted_y][converted_x] = to_move
        if to_move == 'O':
            to_move = 'X'
        else:
            to_move = 'O'
    
    render_board(board, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
    return board, to_move

# Función para verificar si hay un ganador o un empate
def check_win(board):
    winner = None
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            winner = board[row][0]
            return winner

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            winner = board[0][col]
            return winner
   
    if board[0][0] == board[1][1] == board[2][2]:
        winner = board[0][0]
        return winner
          
    if board[0][2] == board[1][1] == board[2][0]:
        winner = board[0][2]
        return winner
    
    if winner is None:
        for row in board:
            for cell in row:
                if cell not in ['X', 'O']:
                    return None
        return "DRAW"

# Función para mostrar la pantalla de resultado
def show_result_screen(result):
    SCREEN.fill(BG_COLOR)
    font = pygame.font.Font(None, 80)  # Using default font
    if result == "DRAW":
        text = font.render("IT'S A DRAW!", True, (0, 0, 0))
    else:
        text = font.render(f"{result} WINS!", True, (0, 0, 0))
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
    
    # Botón de reiniciar
    font = pygame.font.Font(None, 50)  # Using default font
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(SCREEN, (0, 128, 0), restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    # Botón de salir
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
    pygame.draw.rect(SCREEN, (128, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (255, 255, 255))
    SCREEN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.flip()

# Función principal del juego
def main():
    show_rules_screen()  # Mostrar pantalla de reglas inicial

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Al hacer clic en el botón de inicio
                if 380 <= event.pos[0] <= 580 and 595 <= event.pos[1] <= 645:
                    SCREEN.fill(BG_COLOR)  # Cambiar el fondo al color BG_COLOR
                    SCREEN.blit(BOARD, (50, 50))  # Ajustar posición según el nuevo tamaño del tablero
                    pygame.display.update()
                    run_game()  # Iniciar el juego

# Función para ejecutar el juego
def run_game():
    global board, graphical_board, to_move, game_finished

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_finished:
                    # Verificar clic en el botón de reiniciar
                    if WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 50 <= event.pos[1] <= HEIGHT // 2 + 100:
                        # Reiniciar las variables para un nuevo juego
                        board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                        graphical_board = [[[None, None], [None, None], [None, None]], 
                                           [[None, None], [None, None], [None, None]], 
                                           [[None, None], [None, None], [None, None]]]
                        to_move = 'X'
                        game_finished = False
                        SCREEN.fill(BG_COLOR)
                        SCREEN.blit(BOARD, (50, 50))
                        pygame.display.update()
                    # Verificar clic en el botón de salir
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

# Iniciar el juego
if __name__ == "__main__":
    main()

