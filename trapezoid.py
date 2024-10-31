import arcade
import math
import constant
from swooping_enemy import Swooping_Enemy


class Trapezoid():

    def __init__(self):

        # Initialize SpriteLists for each row
        self.trapezoid_sprites = arcade.SpriteList()

        # Populate rows with enemies
        self.populate_rows([4, 8, 10])

    
    # Helper function for populate rows
    def populate_row(self, num_enemies, enemy_type, home_y):
        
        image_path = 'sources/enemies/' + enemy_type + '.jpeg'
        sprite_width = arcade.Sprite(image_path, constant.ENEMY_SCALE, 0, 0).width

        for i in range(int(num_enemies / 2)):

            home_x = (((i + 1) * (constant.ENEMY_SPACING_X / 2 + sprite_width / 2))
                      + (i * (sprite_width / 2 + constant.ENEMY_SPACING_X / 2)))


            left_sprite = (Swooping_Enemy(image_path,
                                          constant.ENEMY_SCALE,
                                          constant.SCREEN_WIDTH // 2 - home_x,
                                          home_y))
            right_sprite = (Swooping_Enemy(image_path,
                                          constant.ENEMY_SCALE,
                                          constant.SCREEN_WIDTH // 2 + home_x,
                                          home_y))

            self.trapezoid_sprites.append(left_sprite)
            self.trapezoid_sprites.append(right_sprite)


    def populate_rows(self, enemies_per_row):
        """Helper method to populate a row with a given number of enemies at a specified y_position."""

        # Unpacking enemies per row
        num_boss = enemies_per_row[0]
        num_butterflies = enemies_per_row[1]
        num_bees = enemies_per_row[2]

        #TODO: add a pause between row populating the screen

        home_y = constant.SCREEN_HEIGHT - constant.MARGIN_Y
        self.populate_row(num_boss, 'json', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_butterflies, 'json', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_butterflies, 'json', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_bees, 'json', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_bees, 'json', home_y)
        
        
        

    def draw(self):
        """Draw all rows of enemies."""
        self.trapezoid_sprites.draw()

    def update(self):
        """Draw all rows of enemies."""
        self.trapezoid_sprites.update()
