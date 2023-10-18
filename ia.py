import random
import copy

assert __name__!="__main__", ("Lancez le jeu via main.py")

# Retourne la valeur de la case où l'on peut jouer sur une colonne
def find_row(column, cells):
    row = 5

    while cells[row][column] != 0 and row >= 0:
        row -= 1

    return row


# Vérifie si il y a une position de victoire
def win(cells, row, column, player):

    def vertical_win():
        score = 0

        for _row in range(row, 6):
            if cells[_row][column] == player:
                score += 1
            else:
                break

        return True if score >= 4 else False

    def horizontal_win():
        score = 0

        for _column in range(7):
            if cells[row][_column] == player:
                score += 1
                if score >= 4:
                    break
            else:
                score = 0

        return True if score >= 4 else False

    def diagonal_win():

        def diagonal_1():
            score = 1

            if row != 0 and column != 0:
                i, j = row - 1, column - 1
                while i in range(6) and j in range(7) and score < 4:
                    if cells[i][j] == player:
                        score += 1
                        i -= 1
                        j -= 1
                    else:
                        break

            if row != 7 and column != 6:
                i, j = row + 1, column + 1
                while i in range(6) and j in range(7) and score < 4:
                    if cells[i][j] == player:
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
                    if cells[i][j] == player:
                        score += 1
                        i += 1
                        j -= 1
                    else:
                        break

            if row != 0 and column != 7:
                i, j = row - 1, column + 1
                while i in range(6) and j in range(7) and score < 4:
                    if cells[i][j] == player:
                        score += 1
                        i -= 1
                        j += 1
                    else:
                        break

            return True if score >= 4 else False

        return True if diagonal_1() or diagonal_2() else False

    return (vertical_win() or horizontal_win() or diagonal_win())


# Attribue un score à chaque colonne et renvoie une liste
def get_scores(real_cells, cells, player, step):
    cells = copy.deepcopy(cells)

    ennemy = 2 if player == 1 else 1

    scores = [5] * 7  # On met tous les scores à 5 par defaut

    for j in range(7):
        i = find_row(j, cells)  # le i avec le plateau de test
        real_i = find_row(j, real_cells)  # le i avec le vrai plateau
        sur_de_perdre = False
        sur_de_gagner = False

        if (real_i == -1 and step == 1) or (i == -1 and step == 2):
            scores[j] = -1 # si la colonne est complete
        else:
            cells[i][j] = player

            if step < 2:
                # On teste toutes les possibilités de l'ennemi au coup suivant
                for j2 in range(7):
                    i2 = find_row(j2, cells)

                    cells[i2][j2] = ennemy

                    # On refait le score de chaque colonne pour l'ordi
                    a = get_scores(real_cells, cells, player, 2)

                    # S'il y a deux 9 dans les scores c'est que l'ennemi est sûr de gagner
                    if a.count(9) > 1:
                        sur_de_perdre = True
                    # S'il y a deux 10 dans les scores c'est que l'IA est sûr de gagner
                    if a.count(10) > 1:
                        sur_de_gagner = True

                    cells[i2][j2] = real_cells[i2][j2]

            cells[i][j] = player

            # S'il y a un coup gagnant pour l'ordi
            if win(cells, i, j, player):
                scores[j] = 10
            else:
                cells[i][j] = ennemy

                # S'il y a un coup gagnant pour l'ennemi
                if win(cells, i, j, ennemy):
                    scores[j] = 9
                elif real_i > 0 and step == 1:
                    # Vérifie si le coup offre au coup suivant un coup gagnant à l'ennemi
                    cells[i - 1][j] = ennemy
                    cells[i][j] = player

                    # S'il y a un coup gagnant pour l'ennemi
                    if win(cells, i - 1, j, ennemy):
                        scores[j] = 0
                    elif sur_de_perdre:
                        # Si au 2ème coup suivant il y a une possiblité où l'ennemi gagne forcément
                        scores[j] = 1
                    elif sur_de_gagner:
                        # Si au 2ème coup suivant il y a une possiblité où l'ia gagne forcément
                        scores[j] = 8

                    cells[i - 1][j] = 0

                cells[i][j] = 0

            cells[i][j] = 0

    return scores


# Retourne la colonne dans laquelle l'ia joue
def ia_play(cells, game_counter,number):  # number est le numéro de joueur de l'ia
    scores = get_scores(cells, cells, number, 1)
    max_indexes = []

    for i in range(len(scores)):
        if scores[i] == max(scores):
            max_indexes.append(i)

    a = []
    for i in max_indexes:
        if i in [2, 3, 4]:
            a.append(i)

    if 3 in max_indexes and game_counter < 2:
        column = 3
    elif len(a) > 0:
        column = random.choice(a)
    else:
        column = random.choice(max_indexes)

    return column