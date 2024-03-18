"""
Author: Kunal Bhaskar
UPI: kbha962

This is is a 2D game of connect four where the aim is to obtain more 4 in a row
sequences than the opponent. The game ends when all slots in the gameboard have been filled.

"""

import pygame
import math

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
        window.fill(BLUE)
        x = token_size / 2
        for col in range(self.size):
            y = token_size / 2 + (self.size - 1) * token_size
            for row in range(self.size):
                item = self.items[col][row]
                if item == 1:
                    pygame.draw.circle(window, RED, (x, y), token_radius)
                elif item == 2:
                    pygame.draw.circle(window, YELLOW, (x, y), token_radius)
                elif item == 3:
                    pygame.draw.circle(window, LIGHT_RED, (x, y), token_radius)
                else:
                    pygame.draw.circle(window, BLACK, (x, y), token_radius)
                y -= token_size

            x += token_size
        self.display_text()

    def display_text(self):
        stats_font = pygame.font.SysFont("euphemiacas", 25, True)
        ctrl_font = pygame.font.SysFont("euphemiacas", 12)
        
        user_stats = f"User's score: {self.points[0]}"
        comp_stats = f"Computer's score: {self.points[1]}"
        ctrl1 = "Press the 'r' key to reset the board."
        ctrl2 = "Move the mouse to see the available slots." 
        ctrl3 = "Click the mouse to drop the disc into the column."

        user_label = stats_font.render(user_stats, 1, RED)
        comp_label = stats_font.render(comp_stats, 1, YELLOW)
        ctrl1_label = ctrl_font.render(ctrl1, 1, BLACK)
        ctrl2_label = ctrl_font.render(ctrl2, 1, BLACK)
        ctrl3_label = ctrl_font.render(ctrl3, 1, BLACK)
        
        window.blit(user_label, (700, 125))
        window.blit(comp_label, (700, 175))
        window.blit(ctrl1_label, (700, 225))
        window.blit(ctrl2_label, (700, 275))
        window.blit(ctrl3_label, (700, 325))

        pygame.display.update()

        
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
        self.board.display()
        fps = 60
        clock = pygame.time.Clock()
        player_number=0
        run = True
        
        while not self.board.game_over() and run:
            clock.tick(fps)

            if player_number == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.board=GameBoard(size)  

                    if event.type == pygame.MOUSEMOTION:
                        x = event.pos[0]
                        column = int(math.floor(x / token_size))
                        if 0 <= column < self.board.size:
                            if self.board.num_free_positions_in_column(column) > 0:
                                self.board.items[column][self.board.num_entries[column]] = 3
                                self.board.display()
                                self.board.items[column][self.board.num_entries[column]] = 0
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x = event.pos[0]
                        column = int(math.floor(x / token_size))
                        if self.board.add(column, player_number+1):
                            player_number = 1
                            self.board.display()
                            

            else:
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                player_number = 0
                self.board.display()
         
    
        if self.board.game_over():
            if (self.board.points[0]>self.board.points[1]):
                label_font = pygame.font.SysFont("euphemiacas", 105, True) 
                label = label_font.render("User wins!", 1, BLACK)
                window.blit(label, (40 , 250))
                
            elif (self.board.points[0]<self.board.points[1]):
                label_font = pygame.font.SysFont("euphemiacas", 75, True) 
                label = label_font.render("Computer wins!", 1, BLACK)
                window.blit(label, (20 , 250))
                
            else:
                label_font = pygame.font.SysFont("euphemiacas", 105, True)
                label = label_font.render("It's a draw!", 1, BLACK)
                window.blit(label, (18 , 250))
            
            pygame.display.update()
            pygame.time.wait(6000)
            
        pygame.quit()



pygame.init()
           
BLUE = (0, 0, 240)
RED = (255, 0, 0)
LIGHT_RED = (150, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

HEIGHT = 700
WIDTH = 1000

valid_input = False
while not valid_input:
    user_input = input("Please enter an integer board size between 1 and 10 inclusive: ")
    try:
        size = int(user_input)
        if 1 <= size <= 10:
            game = FourInARow(size)
            valid_input = True
        elif size.isdigit():
            raise ValueError
        else:
            raise Exception

    except ValueError:
        print("Value given is not an integer")
        
    except Exception:
        print("Integer out of range")
        
        
token_size = 700 / size         
token_radius = token_size /2 - 10

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")

game.play()
