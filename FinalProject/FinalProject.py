import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("3 en Raya Game")
        self.create_main_interface()

    def create_main_interface(self):
        self.clear_window()
        
        # Título del juego
        title_label = tk.Label(self.root, text="3 en Raya Game", font=("Helvetica", 24))
        title_label.pack(pady=20)

        # Introducción y reglas
        intro_text = (
            "Bienvenidos a 3 en Raya Game!\n\n"
            "Reglas del Juego:\n"
            "1. El juego se juega en una cuadrícula de 3x3.\n"
            "2. Dos jugadores se turnan para marcar un espacio con su símbolo (X o O).\n"
            "3. El primer jugador en alinear tres de sus símbolos horizontalmente, verticalmente o diagonalmente gana.\n"
            "4. Si todos los espacios están llenos y nadie ha alineado tres símbolos, el juego termina en empate."
        )
        intro_label = tk.Label(self.root, text=intro_text, justify=tk.LEFT, padx=20)
        intro_label.pack(pady=20)

        # Imagen representativa del juego (Placeholder)
        image_label = tk.Label(self.root, text="Imagen del Juego Aquí", bg="grey", width=30, height=10)
        image_label.pack(pady=20)

        # Botón para iniciar la partida
        start_button = tk.Button(self.root, text="Iniciar Partida", command=self.create_player_setup_interface)
        start_button.pack(pady=20)

    def create_player_setup_interface(self):
        self.clear_window()

        # Título de la pantalla
        setup_title_label = tk.Label(self.root, text="Configuración de Jugadores", font=("Helvetica", 18))
        setup_title_label.pack(pady=20)

        # Entradas para el nombre de los jugadores
        player1_label = tk.Label(self.root, text="Jugador 1:")
        player1_label.pack()
        self.player1_name = tk.Entry(self.root)
        self.player1_name.pack(pady=10)

        player2_label = tk.Label(self.root, text="Jugador 2:")
        player2_label.pack()
        self.player2_name = tk.Entry(self.root)
        self.player2_name.pack(pady=10)

        # Selección de símbolos
        symbols_frame = tk.Frame(self.root)
        symbols_frame.pack(pady=20)

        symbol_label = tk.Label(symbols_frame, text="Selecciona tu símbolo:")
        symbol_label.grid(row=0, column=0, padx=10)

        self.symbol_var1 = tk.StringVar(value="X")
        self.symbol_var2 = tk.StringVar(value="O")

        symbol_radio1 = tk.Radiobutton(symbols_frame, text="X", variable=self.symbol_var1, value="X")
        symbol_radio1.grid(row=0, column=1)

        symbol_radio2 = tk.Radiobutton(symbols_frame, text="O", variable=self.symbol_var2, value="O")
        symbol_radio2.grid(row=0, column=2)

        # Selección de colores (Placeholder)
        colors_frame = tk.Frame(self.root)
        colors_frame.pack(pady=20)

        color_label = tk.Label(colors_frame, text="Selecciona tu color:")
        color_label.grid(row=0, column=0, padx=10)

        self.color_var1 = tk.StringVar(value="Rojo")
        self.color_var2 = tk.StringVar(value="Azul")

        color_radio1 = tk.Radiobutton(colors_frame, text="Rojo", variable=self.color_var1, value="Rojo")
        color_radio1.grid(row=0, column=1)

        color_radio2 = tk.Radiobutton(colors_frame, text="Azul", variable=self.color_var2, value="Azul")
        color_radio2.grid(row=0, column=2)

        # Botón para continuar
        continue_button = tk.Button(self.root, text="Continuar", command=self.create_game_board_interface)
        continue_button.pack(pady=20)

    def create_game_board_interface(self):
        self.clear_window()

        # Título de la pantalla
        game_title_label = tk.Label(self.root, text="3 en Raya - Tablero de Juego", font=("Helvetica", 18))
        game_title_label.pack(pady=20)

        # Nombres de los jugadores
        players_frame = tk.Frame(self.root)
        players_frame.pack(pady=10)

        player1_label = tk.Label(players_frame, text=f"{self.player1_name.get()}: X", font=("Helvetica", 12))
        player1_label.grid(row=0, column=0, padx=20)

        player2_label = tk.Label(players_frame, text=f"{self.player2_name.get()}: O", font=("Helvetica", 12))
        player2_label.grid(row=0, column=1, padx=20)

        # Tablero de juego
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        self.board_buttons = []
        self.board_state = [[None]*3 for _ in range(3)]  # Estado inicial del tablero

        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(board_frame, text=" ", font=("Helvetica", 20), width=6, height=3,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.board_buttons.append(row)

        # Estado del juego
        self.current_turn = 1
        self.current_player = self.player1_name.get()
        self.status_label = tk.Label(self.root, text=f"Turno de: {self.current_player}", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

    def on_button_click(self, row, col):
        # Verificar si la casilla está vacía
        if self.board_state[row][col] is None:
            # Marcar la casilla con el símbolo del jugador actual
            if self.current_turn % 2 == 1:
                symbol = self.symbol_var1.get()
            else:
                symbol = self.symbol_var2.get()

            self.board_state[row][col] = symbol
            self.board_buttons[row][col].config(text=symbol)

            # Verificar si hay un ganador
            if self.check_winner(symbol):
                winner = self.current_player
                messagebox.showinfo("¡Felicidades!", f"{winner} ha ganado el juego.")
                self.create_results_interface(winner)
            elif self.current_turn == 9:
                messagebox.showinfo("Empate", "El juego ha terminado en empate.")
                self.create_results_interface("Empate")
            else:
                # Cambiar al siguiente turno
                self.current_turn += 1
                if self.current_turn % 2 == 1:
                    self.current_player = self.player1_name.get()
                else:
                    self.current_player = self.player2_name.get()
                self.status_label.config(text=f"Turno de: {self.current_player}")

    def check_winner(self, symbol):
        # Verificar filas y columnas
        for i in range(3):
            if (self.board_state[i][0] == symbol and
                self.board_state[i][1] == symbol and
                self.board_state[i][2] == symbol):
                return True
            if (self.board_state[0][i] == symbol and
                self.board_state[1][i] == symbol and
                self.board_state[2][i] == symbol):
                return True

        # Verificar diagonales
        if (self.board_state[0][0] == symbol and
            self.board_state[1][1] == symbol and
            self.board_state[2][2] == symbol):
            return True
        if (self.board_state[0][2] == symbol and
            self.board_state[1][1] == symbol and
            self.board_state[2][0] == symbol):
            return True

        return False

    def create_results_interface(self, result):
        self.clear_window()

        # Título de la pantalla
        results_title_label = tk.Label(self.root, text="Resultados del Juego", font=("Helvetica", 18))
        results_title_label.pack(pady=20)

        # Mensaje de resultado
        if result == "Empate":
            result_label = tk.Label(self.root, text="¡El juego ha terminado en empate!", font=("Helvetica", 14))
        else:
            result_label = tk.Label(self.root, text=f"¡{result} ha ganado el juego!", font=("Helvetica", 14))
        result_label.pack(pady=20)

        # Botones para repetir o salir del juego
        repeat_button = tk.Button(self.root, text="Repetir Juego", command=self.create_main_interface)
        repeat_button.pack(pady=10)

        quit_button = tk.Button(self.root, text="Salir", command=self.root.destroy)
        quit_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()