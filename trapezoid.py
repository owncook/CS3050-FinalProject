import arcade
import math
import constant
import random
from swooping_enemy import Swooping_Enemy



class Trapezoid():

    def __init__(self):

        # Initialize SpriteLists for each row
        self.row1 = arcade.SpriteList()
        self.row2 = arcade.SpriteList()
        self.row3 = arcade.SpriteList()
        self.row4 = arcade.SpriteList()
        self.row5 = arcade.SpriteList()

        # Create a nested list to hold the rows
        self.enemies_nested_list = [self.row1, self.row2, self.row3, self.row4, self.row5]

        self.attack_timer = 0  # Track time for attacks

        # Populate rows with enemies
        self.populate_rows()

    def get_sprite_lists(self):
        
        return self.enemies_nested_list
    
    #Populate rows()
    def populate_rows(self):

        #TODO:replace magic numbers for y pos
        

        # poulating the rows of the trapezoid with the enemy classes
        #self.populate_row(self.row1, 10, constant.SCREEN_HEIGHT - 400, "bee")
        #self.populate_row(self.row2, 10, constant.SCREEN_HEIGHT - 350, "bee")
        #self.populate_row(self.row3, 8, constant.SCREEN_HEIGHT - 300, "butterfly")
        #self.populate_row(self.row4, 8, constant.SCREEN_HEIGHT - 250, "butterfly")
        #self.populate_row(self.row5, 4, constant.SCREEN_HEIGHT - 200, "json")

        # tester function for attack 

        for row, y_pos in zip(self.enemies_nested_list, range(700, 500, -50)):
            for i in range(10):
                enemy = Swooping_Enemy("sources/enemies/json.jpeg", 0.5, i * 80 + 50, y_pos)
                row.append(enemy)

        


        
    
    def populate_row(self, row, num_enemies, y_position, enemy_class):
        """Helper method to populate a row with a given number of enemies at a specified y_position."""
        # Define the total available width after considering margins (100px on each side)
        available_width = constant.SCREEN_WIDTH - 200
        enemy_spacing = available_width / (num_enemies - 1)  # space between each enemy


        #TODO: add a pause between row populating the screen

        for i in range(num_enemies):
            # Calculate the target x position for each enemy, starting at the left margin (100px)
            target_x = 100 + (i * enemy_spacing)  # 100px left margin + spacing
            target_y = y_position
            # Create a swooping enemy
            match enemy_class:
                case "bee":
                    enemy = Swooping_Enemy("sources/enemies/json.jpeg", constant.ENEMY_SCALE, target_x, target_y)
                case "bee":
                    enemy = Swooping_Enemy("sources/enemies/json.jpeg", constant.ENEMY_SCALE, target_x, target_y)   
                case "butterfly":
                    enemy = Swooping_Enemy("sources/enemies/json.jpeg", constant.ENEMY_SCALE, target_x, target_y)
                case "butterfly":
                    enemy = Swooping_Enemy("sources/enemies/json.jpeg", constant.ENEMY_SCALE, target_x, target_y)
                case "json":
                    enemy = Swooping_Enemy("sources/enemies/json.jpeg", constant.ENEMY_SCALE, target_x, target_y)        
            # Append the enemy to the row's SpriteList
            row.append(enemy)

    def check_trapezoid_empty(self):
        return len(self.enemies_nested_list) > 0
    def draw(self):
        """Draw all rows of enemies."""
        self.row1.draw()
        self.row2.draw()
        self.row3.draw()
        self.row4.draw()
        self.row5.draw()

    def update(self, delta_time, player_x, player_y):
        """Draw all rows of enemies."""
        #self.row1.update()
        #self.row2.update()
        #self.row3.update()
        #self.row4.update()
        #self.row5.update()

        self.attack_timer += delta_time
        if self.attack_timer >= constant.ATTACK_INTERVAL:
            row = random.choice(self.enemies_nested_list)
            if row:
                enemy = random.choice(row)
                enemy.update_attack_timer(delta_time)  # Increment the attack timer
                enemy.attack(player_x, player_y)      # Call the attack method
            self.attack_timer = 0

        for row in self.enemies_nested_list:
            for enemy in row:
                enemy.update_attack_timer(delta_time)  # Increment attack timer for each enemy
                enemy.update(delta_time)  # Update each enemy

            
