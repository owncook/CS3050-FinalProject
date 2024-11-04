import arcade
import math
import constant
import random
from swooping_enemy import Swooping_Enemy


class Trapezoid():

    def __init__(self):

        # Initialize SpriteLists for each row
        self.trapezoid_sprites = arcade.SpriteList()

        self.attack_timer = 0  # Track time for attacks\

        self.enemy_bullet_list = arcade.SpriteList()

        # Populate rows with enemies
        self.populate_rows([4, 8, 10])

    
    # Helper function for populate rows
    def populate_row(self, num_enemies, enemy_type, home_y):
        
        image_path = 'sources/enemies/' + enemy_type + '.jpeg'
        sprite_width = arcade.Sprite(image_path, constant.ENEMY_SCALE, 0, 0).width

        group_delay = 0

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
            
            # Set a delay for each pair of enemies (you can adjust this to get the effect you want)
            left_sprite.start_delay = group_delay
            right_sprite.start_delay = group_delay

            # Increase delay for the next group
            group_delay += 1


            self.trapezoid_sprites.append(left_sprite)
            self.trapezoid_sprites.append(right_sprite)


    def populate_rows(self, enemies_per_row):
        """Helper method to populate a row with a given number of enemies at a specified y_position."""

        # Unpacking enemies per row
        num_boss = enemies_per_row[0]
        num_butterflies = enemies_per_row[1]
        num_bees = enemies_per_row[2]


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

    def check_trapezoid_empty(self):
        return len(self.trapezoid_sprites) <= 0

    def draw(self):
        """Draw all rows of enemies."""
        self.trapezoid_sprites.draw()
        self.enemy_bullet_list.draw()

    def update(self, delta_time, player_x, player_y):
        """Update all rows of enemies."""

        self.attack_timer += delta_time

        if self.attack_timer >= constant.ATTACK_INTERVAL:
            
            enemy = random.choice(self.trapezoid_sprites)
            enemy.update_swoop_timer(delta_time)  # Increment the attack timer
            enemy.attack(enemy, player_x, player_y)      # Call the attack method

            self.attack_timer += delta_time
         
            if enemy.is_attacking:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", scale=1)
                print("tester")
                bullet.center_x = enemy.center_x                
                bullet.center_y = enemy.top  # Start the bullet just above the enemy  
                bullet.angle = 180  #downwards is 270 degrees
                bullet.change_y = -constant.BULLET_SPEED  # Moving down
                self.enemy_bullet_list.append(bullet)
         
            self.attack_timer = 0
        



        for enemy in self.trapezoid_sprites:
            enemy.update_swoop_timer(delta_time)  # Increment attack timer for each enemy
            enemy.update(delta_time, player_x, player_y)  # Update each enemy