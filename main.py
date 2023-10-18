import tkinter as tk
import ia


class Game:

    # Initialise les fondamentaux du jeu
    def __init__(self):

        # Définit les couleurs nécessaires tout au long du jeu
        self.bg_color = "#364bb8"
        self.red = "#e51f1f"
        self.yellow = "#ffb000"

        # Crée la fenêtre globale de l'app
        self.window = tk.Tk()
        self.window.title("Puissance 4")
        self.window.iconphoto(False, tk.PhotoImage(file='./src/png/icon.png'))
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.window.configure(bg=self.bg_color)

        # Crée la frame qui contiendra la grille de jeu
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.pack(side=tk.TOP)

        # Crée les variables importantes globales
        self.player = 1
        self.cells = [[0] * 7 for i in range(6)]
        self.buttons = {}
        self.is_finished = False
        self.is_started = False
        self.game_counter = 0
        self.game_mode = 0  # 1: 2 joueurs, 2: IA en joueur 1, 3: IA en joueur 2

        self.score1 = 0  # score du joueur 1
        self.score2 = 0  # score du joueur 2

        # Définit les différentes images des boutons
        self.b_empty = tk.PhotoImage(file=r"./src/png/b_empty_50px.png")
        self.b_red = tk.PhotoImage(file=r"./src/png/b_red_50px.png")
        self.b_yellow = tk.PhotoImage(file=r"./src/png/b_yellow_50px.png")

        # Crée la grille
        self.grid()

        # Crée la fenêtre pour demander le mode de jeu
        mode_prompt = tk.LabelFrame(self.window,
                                    bg="white",
                                    text="Choisissez un mode de jeu")

        mode_prompt.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Button(mode_prompt,
                  text="Deux joueurs",
                  borderwidth=1,
                  command=lambda mode=1, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)
        tk.Button(mode_prompt,
                  text="IA en joueur 1",
                  borderwidth=1,
                  command=lambda mode=2, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)
        tk.Button(mode_prompt,
                  text="IA en joueur 2",
                  borderwidth=1,
                  command=lambda mode=3, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)

        # Crée le texte affichant le nom du joueur actuel
        self.player_text = tk.Label(self.window, text="Joueur 1", bg=self.red)
        self.player_text.pack(side=tk.LEFT, padx=10)

        # Affiche du score
        score_frame = tk.Frame(self.window)
        score_frame.pack(side=tk.RIGHT, padx=10)

        self.score1_text = tk.Label(score_frame, text="0", bg=self.red)
        self.score1_text.grid(row=0, column=0)

        tk.Label(score_frame, text=" - ", bg=self.bg_color).grid(row=0,
                                                                 column=1)

        self.score2_text = tk.Label(score_frame, text="0", bg=self.yellow)
        self.score2_text.grid(row=0, column=2)

        if self.game_mode == 2:
            self.play(0, ia.ia_play(self.cells, self.game_counter, 1))

        # Lance l'app
        self.window.mainloop()

    # Met à jour le mode de jeu
    def set_mode(self, mode, mode_prompt):
        if mode != self.game_mode:
            self.score1 = 0
            self.score2 = 0
            self.score1_text.configure(text=self.score1)
            self.score2_text.configure(text=self.score2)

        self.game_mode = mode
        self.is_started = True
        mode_prompt.destroy()

        # Si le mode est IA en joueur 1, on fait jouer l'IA en premier (elle commencera toujours par la colonne du milieu)
        if self.game_mode == 2:
            self.cells[5][3] = 1
            self.game_counter += 1

            self.buttons["6x4"].config(image=self.b_red)
            self.player_text.configure(text="Joueur 2", bg=self.yellow)
            self.player = 2

    # Crée la grille
    def grid(self):
        for row in range(6):
            for column in range(7):
                self.buttons[f"{row + 1}x{column + 1}"] = tk.Button(
                    self.grid_frame,
                    image=self.b_empty,
                    height=50,
                    width=50,
                    borderwidth=0,
                    bg=self.bg_color,
                    relief="flat",
                    command=lambda _row=row, _column=column: self.play(
                        _row, _column))

                self.buttons[f"{row + 1}x{column + 1}"].grid(row=row,
                                                             column=column)

    # À chaque fois qu'une cellule est cliquée
    def play(self, row, column):
        # Pour qu'on ne puisse pas jouer tant que le mode de jeu n'est pas choisi
        if not self.is_started:
            return

        self.game_counter += 1

        # Les deux boucles while servent à pouvoir cliquer n'importe où dans une colonne et le bloc sera placé au bon endroit
        # Regarde si l'état de la cellule cliquée n'est pas 0:vide, si c'est le cas, regarde la cellule au dessus jusqu'à trouver une cellule vide ou atteindre la fin de la grille
        while self.cells[row][column] != 0:
            if row == 0:
                return
            else:
                row -= 1
        # Regarde si la cellule cliquée n'est pas sur la dernière ligne et si l'état de la cellule en dessous est 0:vide, si c'est le cas, regarde la cellule en dessous jusqu'à trouver une cellule rempli en dessous
        while row != 5 and self.cells[row + 1][column] == 0:
            row += 1

        # Défini le nouvel état de la cellule
        self.cells[row][column] = self.player

        # Vérifie si il y a une position gagnante et fini le jeu si oui
        if self.win(row, column):
            self.end_winner()

        # Vérifie si il y a une égalité et fini le jeu si oui
        else:
            cells_full = 0
            for _row in self.cells:
                for cell in _row:
                    if cell != 0:
                        cells_full += 1
            if cells_full == 42:
                self.end_draw()

        # Modification de l'état de la cellule cliquée ainsi que du texte indiquant le nom du joueur et passe au joueur suivant
        if self.player == 1:
            self.buttons[f"{row + 1}x{column + 1}"].config(image=self.b_red)
            if not self.is_finished:
                self.player_text.configure(bg=self.yellow)
            self.player = 2

            # Si le mode est IA en joueur 2, on fait jouer l'IA
            if self.game_mode == 3:
                self.play(0, ia.ia_play(self.cells, self.game_counter, 2))

        else:
            self.buttons[f"{row + 1}x{column + 1}"].config(image=self.b_yellow)
            if not self.is_finished:
                self.player_text.configure(bg=self.red)
            self.player = 1

            # Si le mode est IA en joueur 1, on fait jouer l'IA
            if self.game_mode == 2:
                self.play(0, ia.ia_play(self.cells, self.game_counter, 1))


        if not self.is_finished:
            self.player_text.configure(text="Joueur " + str(self.player))

    # Vérifie si il y a une position de victoire
    def win(self, row, column):

        # Vérifie la ligne de la cellule cliquée
        def vertical_win():
            score = 0

            for _row in range(row, 6):
                if self.cells[_row][column] == self.player:
                    score += 1
                else:
                    break

            return True if score >= 4 else False

        # Vérifie la colonne de la cellule cliquée
        def horizontal_win():
            score = 0

            for _column in range(7):
                if self.cells[row][_column] == self.player:
                    score += 1
                    if score >= 4:
                        break
                else:
                    score = 0

            return True if score >= 4 else False

        # Vérifie les deux diagonales de la cellule cliquée
        def diagonal_win():

            def diagonal_1():
                score = 1

                if row != 0 and column != 0:
                    i, j = row - 1, column - 1
                    while i in range(6) and j in range(7) and score < 4:
                        if self.cells[i][j] == self.player:
                            score += 1
                            i -= 1
                            j -= 1
                        else:
                            break

                if row != 7 and column != 6:
                    i, j = row + 1, column + 1
                    while i in range(6) and j in range(7) and score < 4:
                        if self.cells[i][j] == self.player:
                            score += 1
                            i += 1
                            j += 1
                        else:
                            break

                return True if score >= 4 else False

            def diagonal_2():
                score = 1

                if row != 6 and column != 0:
                    i, j = row + 1, column - 1
                    while i in range(6) and j in range(7) and score < 4:
                        if self.cells[i][j] == self.player:
                            score += 1
                            i += 1
                            j -= 1
                        else:
                            break

                if row != 0 and column != 7:
                    i, j = row - 1, column + 1
                    while i in range(6) and j in range(7) and score < 4:
                        if self.cells[i][j] == self.player:
                            score += 1
                            i -= 1
                            j += 1
                        else:
                            break

                return True if score >= 4 else False

            return True if diagonal_1() or diagonal_2() else False

        # Renvoie True si une position gagnante est détectée
        return (vertical_win() or horizontal_win() or diagonal_win())

    # Appelée dès qu'il y a une position de victoire. Arrête le jeu
    def end_winner(self):

        self.is_finished = True

        # Désactive les boutons
        for button in self.buttons:
            self.buttons[button].configure(state=tk.DISABLED)

        # Augmente le score du gagnant et affiche le nom du gagnant au lieu du joueur actuel
        if self.player == 1:
            self.score1 += 1
        else:
            self.score2 += 1

        self.score1_text.configure(text=str(self.score1))
        self.score2_text.configure(text=str(self.score2))

        # Crée le menu permettant d'afficher le gagnant ainsi que les boutons "Rejouer" et "Quitter"
        menu = tk.LabelFrame(self.window,
                             bg=self.bg_color,
                             text=f"Le joueur {str(self.player)} a gagné",
                             fg="white")
        menu.place(relx=0.5, rely=1, anchor=tk.S)

        tk.Button(menu,
                  text="Rejouer",
                  borderwidth=1,
                  command=lambda _menu=menu: self.replay(_menu),
                  bg="white",
                  relief="flat").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(menu,
                  text="Quitter",
                  borderwidth=1,
                  command=self.window.quit,
                  bg="white",
                  relief="flat").pack(side=tk.RIGHT, padx=5, pady=5)

    # Appelée quand il y a égalité
    def end_draw(self):

        self.is_finished = True

        # Désactive les boutons
        for button in self.buttons:
            self.buttons[button].configure(state=tk.DISABLED)

        # Crée le menu permettant d'afficher le gagnant ainsi que les boutons "Rejouer" et "Quitter"
        menu = tk.LabelFrame(self.window,
                             bg=self.bg_color,
                             text="Égalité",
                             fg="white")
        menu.place(relx=0.5, rely=1, anchor=tk.S)

        tk.Button(menu,
                  text="Rejouer",
                  borderwidth=1,
                  command=lambda _menu=menu: self.replay(_menu),
                  bg="white",
                  relief="flat").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(menu,
                  text="Quitter",
                  borderwidth=1,
                  command=self.window.quit,
                  bg="white",
                  relief="flat").pack(side=tk.RIGHT, padx=5, pady=5)

    def replay(self, menu):

        # Réinitialise les variables importantes globales
        self.player = 1
        self.cells = [[0] * 7 for i in range(6)]
        self.buttons = {}
        self.is_finished = False
        self.is_started = False
        self.game_counter = 0

        # Détruit le menu
        menu.destroy()

        # Supprime la grille de boutons
        for button in self.buttons:
            self.buttons[button].destroy()

        # Recrée la grille
        self.grid()

        # Crée la fenêtre pour demander le mode de jeu
        mode_prompt = tk.LabelFrame(self.window,
                                    bg="white",
                                    text="Choisissez un mode de jeu")

        mode_prompt.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Button(mode_prompt,
                  text="Deux joueurs",
                  borderwidth=1,
                  command=lambda mode=1, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)
        tk.Button(mode_prompt,
                  text="IA en joueur 1",
                  borderwidth=1,
                  command=lambda mode=2, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)
        tk.Button(mode_prompt,
                  text="IA en joueur 2",
                  borderwidth=1,
                  command=lambda mode=3, _mode_prompt=mode_prompt: self.
                  set_mode(mode, _mode_prompt),
                  bg="white",
                  relief="flat").pack(padx=5, pady=5)

        # Réinitialise le texte du nom du joueur
        self.player_text.configure(text="Joueur 1", bg="red")


# Lance le jeu
if __name__=="__main__":
    Game()
