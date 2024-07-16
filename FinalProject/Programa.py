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
X_IMG = pygame.transform.scale(X_IMG, (120, 120))
O_IMG = pygame.image.load("O.png")
O_IMG = pygame.transform.scale(O_IMG, (120, 120))

# Variables del juego
board = [['', '', ''], ['', '', ''], ['', '', '']]
to_move = 'X'
game_finished = False

# Función para renderizar el tablero en la pantalla
def render_board(board):
    cell_width = BOARD_WIDTH // 3
    cell_height = BOARD_HEIGHT // 3
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (50, 50))
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                SCREEN.blit(X_IMG, (j * cell_width + 50 + (cell_width - X_IMG.get_width()) // 2, i * cell_height + 50 + (cell_height - X_IMG.get_height()) // 2))
            elif board[i][j] == 'O':
                SCREEN.blit(O_IMG, (j * cell_width + 50 + (cell_width - O_IMG.get_width()) // 2, i * cell_height + 50 + (cell_height - O_IMG.get_height()) // 2))
    pygame.display.update()

# Función para añadir 'X' u 'O' al tablero
def add_XO(board, to_move):
    current_pos = pygame.mouse.get_pos()
    cell_width = BOARD_WIDTH // 3
    cell_height = BOARD_HEIGHT // 3
    converted_x = (current_pos[0] - 50) // cell_width
    converted_y = (current_pos[1] - 50) // cell_height
    if 0 <= converted_x < 3 and 0 <= converted_y < 3 and board[converted_y][converted_x] == '':
        board[converted_y][converted_x] = to_move
        if to_move == 'O':
            to_move = 'X'
        else:
            to_move = 'O'
    return board, to_move

# Función para verificar si hay un ganador o un empate
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

# Función para mostrar la pantalla de resultado
def show_result_screen(result):
    SCREEN.fill(BG_COLOR)
    font = pygame.font.Font(None, 80)
    if result == "DRAW":
        text = font.render("IT'S A DRAW!", True, (0, 0, 0))
    else:
        text = font.render(f"{result} WINS!", True, (0, 0, 0))
    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
    
    # Botón de reiniciar
    font = pygame.font.Font(None, 45)
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
    global board, to_move, game_finished
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (50, 50))
    pygame.display.update()

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
                        board = [['', '', ''], ['', '', ''], ['', '', '']]
                        to_move = 'X'
                        game_finished = False
                        render_board(board)
                    # Verificar clic en el botón de salir
                    elif WIDTH // 2 - 100 <= event.pos[0] <= WIDTH // 2 + 100 and HEIGHT // 2 + 150 <= event.pos[1] <= HEIGHT // 2 + 200:
                        pygame.quit()
                        sys.exit()
                else:
                    board, to_move = add_XO(board, to_move)
                    render_board(board)
                    winner = check_win(board)
                    if winner is not None:
                        show_result_screen(winner)
                        game_finished = True
                
                pygame.display.update()

# Iniciar el juego
if __name__ == "__main__":
    main()


