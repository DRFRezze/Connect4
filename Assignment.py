"""
Author: KUNAL BHASKAR
UPI: kbha962

This is the implementation of the methods for the GameBoard class of the Connect 4 game (the solutions to sections 1-5)
with the template code for the four in a row game.

"""
class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
        
    def num_free_positions_in_column(self, column):
        return self.items[column].count(0)
        
    def game_over(self):
        for col in range(self.size):
            if self.num_free_positions_in_column(col) != 0:
                return False
        return True
    
    def display(self):
        for row in range(self.size -1, -1, -1):
            for col in range (self.size):
                item = self.items[col][row]
                if item == 1:
                    print("o ", end = "")
                elif item == 2:
                    print("x ", end = "")
                else:
                    print("  ", end = "")
            print()
        print("-" * (2 * self.size - 1))
        print("".join([str(n) + " " for n in range(self.size)]))
        print(f"Points player 1: {self.points[0]} \nPoints player 2: {self.points[1]}")
        
    def num_new_points(self, column, row, player):
        points = 0
        count = 0
        for pos in range(-3, 4):
            if 0 <= row + pos < self.size:
                if self.items[column][row + pos] == player:
                    count += 1
                else:
                    count = 0
                    
                if count >= 4:
                    points += 1
                
        count = 0
        row_list = [self.items[index][row] for index in range(self.size)]
        for pos in range(-3, 4):
            if 0 <= column + pos < self.size:
                if row_list[column + pos] == player:
                    count += 1
                else:
                    count = 0

                if count >= 4:
                    points += 1
                
        count = 0
        for pos in range(-3, 4):
            if 0 <= (column + pos) < self.size and 0 <= (row + pos) < self.size:
                if self.items[column + pos][row + pos] == player:
                    count += 1
                else:
                    count = 0

                if count >= 4:
                    points += 1

        count = 0
        for pos in range(-3, 4):
            if 0 <= (column + pos) < self.size and 0 <= (row - pos) < self.size:
                if self.items[column + pos][row - pos] == player:
                    count += 1
                else:
                    count = 0

                if count >= 4:
                    points += 1
        return points
        
    def add(self, column, player):
        if column < 0 or column >= self.size:
            return False
        elif self.num_entries[column] >= self.size:
            return False
        else: 
            self.items[column][self.num_entries[column]] = player
            self.points[player - 1] += self.num_new_points(column, self.num_entries[column], player)
            self.num_entries[column] += 1
            return True
    
    def free_slots_as_close_to_middle_as_possible(self):
        ordered_list = []
        if self.size % 2 != 0:
            mid = self.size // 2
            if self.num_free_positions_in_column(mid) > 0:
                ordered_list.append(mid)
            left = mid - 1
            right = mid + 1
        else:
            left = int((self.size - 1) / 2 - 0.5)
            right = int((self.size - 1) / 2 + 0.5)
            
        while left >= 0 and right < self.size:
            left_free = self.num_free_positions_in_column(left)
            right_free = self.num_free_positions_in_column(right)
            
            if left_free != 0 and right_free != 0:
                if left_free >= right_free:
                    ordered_list.append(left)
                    ordered_list.append(right)
                else:
                    ordered_list.append(right)
                    ordered_list.append(left)
            else:
                if left_free != 0:
                    ordered_list.append(left)
                elif right_free != 0:
                    ordered_list.append(right)
                
            left -= 1
            right += 1
        return ordered_list
    
    def column_resulting_in_max_points(self, player):
        ordered_list = self.free_slots_as_close_to_middle_as_possible()
        most_points = -1
        
        for pos in ordered_list:
            self.items[pos][self.num_entries[pos]] = player
            points = self.num_new_points(pos, self.num_entries[pos], player)
            
            if points > most_points:
                most_points = points
                most_points_pos = pos
                
            self.items[pos][self.num_entries[pos]] = 0

        return (most_points_pos, most_points)


class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()        

