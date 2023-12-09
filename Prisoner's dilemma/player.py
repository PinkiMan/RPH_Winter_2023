class MyPlayer:
    '''Hráč který upravuje strategii podle odhadnuté strategie protihráče'''

    def __init__(self, payoff_matrix, number_of_iterations=10000):
        self.matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations
        self.History = []  # History of moves
        self.Enemy_True = 0  # Times enemy played True
        self.Enemy_False = 0  # Times enemy played False
        self.Round = 0  # Number of rounds played
        self.Swapper = 0  # Times enemy played swapping strategy
        self.CopyCat = 0  # Times enemy played copycat strategy
        self.Pavlov = 0  # Times enemy played Pavlov strategy

    def Enemy_expected_turn(self):  # Get possible enemy turn
        if self.Enemy_True / (self.Enemy_True + self.Enemy_False) > 0.99:  # Only True
            return True
        elif self.Enemy_False / (self.Enemy_True + self.Enemy_False) > 0.99:  # Only False
            return False
        elif self.Swapper > 5:  # Swapper
            return not self.History[-1]
        elif self.Pavlov > 5:  # Pavlov
            return self.History[-1][0] == self.History[-1][1]

        elif self.Enemy_True / (self.Enemy_True + self.Enemy_False) > 0.47 and self.Enemy_True / (  # Random player
                self.Enemy_True + self.Enemy_False) < 0.5:
            return True
        elif self.Enemy_False / (self.Enemy_True + self.Enemy_False) > 0.47 and self.Enemy_False / (  # Random plyer
                self.Enemy_True + self.Enemy_False) < 0.5:
            return False
        return None

    def move(self):
        if self.Round > 10:  # possibly: self.Round > self.number_of_iterations/1000
            Enemy_Output = self.Enemy_expected_turn()
            if Enemy_Output != None:
                if self.matrix[0][int(Enemy_Output)][0] >= self.matrix[1][int(Enemy_Output)][
                    0]:  # play best counter move
                    return False
                else:
                    return True

        if self.matrix[0][0][0] + self.matrix[0][1][0] > self.matrix[1][0][0] + self.matrix[1][1][
            0]:  # my strategy if not counter move
            return False
        else:
            return True

    def record_last_moves(self, my_turn, enemy_turn):
        if enemy_turn == True:  # record enemy turns
            self.Enemy_True += 1
        else:
            self.Enemy_False += 1

        if len(self.History) > 0:
            if self.History[-1][1] != enemy_turn:  # record swapper strategy
                self.Swapper += 1
            else:
                self.Swapper = 0

            if (self.History[-1][0] == self.History[-1][1] and enemy_turn == True) or (
                    self.History[-1][0] != self.History[-1][1] and enemy_turn == False):  # record Pavlov strategy
                self.Pavlov += 1
            else:
                self.Pavlov = 0

        if len(self.History) > 1:
            if self.History[-1][1] == self.History[-2][0]:  # record copycat strategy
                self.CopyCat += 1
            else:
                self.CopyCat = 0

        self.Round += 1
        self.History.append([my_turn, enemy_turn])  # record moves


