import arcade
import math
from swooping_enemy import Swooping_Enemy

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ENEMY_SCALE = 0.5
ENEMY_SPACING_X = 80  # Horizontal spacing between enemies
ENEMY_SPACING_Y = 100  # Vertical spacing between rows


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

        # Populate rows with enemies
        self.populate_rows()

    def get_sprite_lists(self):
        
        return self.enemies_nested_list
    
    #Populate rows()
    def populate_rows(self):
        # Row 1 and Row 2: 10 enemies each
        self.populate_row(self.row1, 10, SCREEN_HEIGHT - 300)
        self.populate_row(self.row2, 10, SCREEN_HEIGHT - 400)
    
    def populate_row(self, row, num_enemies, y_position):
        """Helper method to populate a row with a given number of enemies at a specified y_position."""
        # Define the total available width after considering margins (100px on each side)
        available_width = SCREEN_WIDTH - 200
        enemy_spacing = available_width / (num_enemies - 1)  # space between each enemy

        for i in range(num_enemies):
            # Calculate the target x position for each enemy, starting at the left margin (100px)
            target_x = 100 + (i * enemy_spacing)  # 100px left margin + spacing
            target_y = y_position
            # Create a swooping enemy
            enemy = Swooping_Enemy("sources/enemies/json.jpeg", ENEMY_SCALE, target_x, target_y)
            # Append the enemy to the row's SpriteList
            row.append(enemy)

    def draw(self):
        """Draw all rows of enemies."""
        self.row1.draw()
        self.row2.draw()

    def update(self):
        """Draw all rows of enemies."""
        self.row1.update()
        self.row2.update()
