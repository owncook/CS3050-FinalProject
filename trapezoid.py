import arcade
import time
import constant
import random
from swooping_enemy import Swooping_Enemy


class Trapezoid():

    def __init__(self):

        # Initialize SpriteLists for each row
        self.trapezoid_sprites = arcade.SpriteList()

        self.attack_timer = 0  # Track time for attacks\

        self.selected_enemy  = None
        self.selected_enemy_2 = None
        self.selected_enemy_3 = None

        self.enemy_bullet_list = arcade.SpriteList()

        # Populate rows with enemies
        self.populate_rows([4, 8, 10])

    
    # Helper function for populate rows
    def populate_row(self, num_enemies, enemy_type, home_y):
        if enemy_type == "bee":
            image_paths = [
                'sources/enemies/bee.png',
                'sources/enemies/bee_frame2.png'
            ]
        elif enemy_type == "butterfly":
            image_paths = [
                'sources/enemies/butterfly.png',
                'sources/enemies/butterfly_frame2.png'
            ]
        else:
            image_paths = ['sources/enemies/' + enemy_type + '.png']
        
        sprite_width = arcade.Sprite(image_paths[0], constant.ENEMY_SCALE, 0, 0).width

        group_delay = 0

        for i in range(int(num_enemies / 2)):

            home_x = (((i + 1) * (constant.ENEMY_SPACING_X / 2 + sprite_width / 2))
                      + (i * (sprite_width / 2 + constant.ENEMY_SPACING_X / 2)))


            left_sprite = (Swooping_Enemy(image_paths,
                                          constant.ENEMY_SCALE,
                                          constant.SCREEN_WIDTH // 2 - home_x,
                                          home_y))
            right_sprite = (Swooping_Enemy(image_paths,
                                          constant.ENEMY_SCALE,
                                          constant.SCREEN_WIDTH // 2 + home_x,
                                          home_y))
            
            # Set a delay for each pair of enemies (you can adjust this to get the effect you want)
            left_sprite.start_delay = group_delay
            right_sprite.start_delay = group_delay

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
        self.populate_row(num_boss, 'evilthing', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_butterflies, 'butterfly', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_butterflies, 'butterfly', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_bees, 'bee', home_y)
        home_y -= constant.ENEMY_SPACING_Y
        self.populate_row(num_bees, 'bee', home_y)

    def check_trapezoid_empty(self):
        return len(self.trapezoid_sprites) <= 0

    def draw(self):
        """Draw all rows of enemies."""
        self.trapezoid_sprites.draw()
        self.enemy_bullet_list.draw()


    def update(self, delta_time, player_x, player_y):
        """Update all rows of enemies."""

        self.attack_timer += delta_time
        three = [1, 2, 3]
        
        
        if self.attack_timer >= constant.ATTACK_INTERVAL:

            num_of_enemies = random.choice(three)
            if num_of_enemies == 1:
                self.selected_enemy = random.choice(self.trapezoid_sprites)
                self.selected_enemy.bullet_shot = False
                self.selected_enemy.attack(self.selected_enemy, player_x, player_y)      # Call the attack method

            elif num_of_enemies == 2:
                self.selected_enemy = random.choice(self.trapezoid_sprites)
                self.selected_enemy.bullet_shot = False
                self.selected_enemy.attack(self.selected_enemy, player_x, player_y)      # Call the attack method
                self.selected_enemy_2 = random.choice(self.trapezoid_sprites)
                self.selected_enemy_2.bullet_shot = False
                self.selected_enemy_2.attack(self.selected_enemy, player_x, player_y)      # Call the attack method
                self.attack_timer = 0

            elif num_of_enemies == 3:
                self.selected_enemy = random.choice(self.trapezoid_sprites)
                self.selected_enemy.bullet_shot = False
                self.selected_enemy.attack(self.selected_enemy, player_x, player_y)      # Call the attack method
                self.selected_enemy_2 = random.choice(self.trapezoid_sprites)
                self.selected_enemy_2.bullet_shot = False
                self.selected_enemy_2.attack(self.selected_enemy, player_x, player_y)      # Call the attack method
                self.selected_enemy_3 = random.choice(self.trapezoid_sprites)
                self.selected_enemy_3.bullet_shot = False
                self.selected_enemy_3.attack(self.selected_enemy, player_x, player_y)      # Call the attack method
                self.attack_timer = 0

            
        if self.selected_enemy and not self.selected_enemy.bullet_shot:
            fired = self.fire_bullet(self.selected_enemy)
            if fired:
                self.selected_enemy.bullet_shot = True
            

        if self.selected_enemy_2 and not self.selected_enemy_2.bullet_shot:
            self.fire_bullet(self.selected_enemy_2)
            fired = self.fire_bullet(self.selected_enemy_2)
            if fired:
                self.selected_enemy_2.bullet_shot = True

        if self.selected_enemy_3 and not self.selected_enemy_3.bullet_shot:
            self.fire_bullet(self.selected_enemy_3)
            fired = self.fire_bullet(self.selected_enemy_3)
            if fired:
                self.selected_enemy_3.bullet_shot = True


        for enemy in self.trapezoid_sprites:
            enemy.update_animation(delta_time) 
            enemy.update_swoop_timer(delta_time)  # Increment attack timer for each enemy
            enemy.update(delta_time, player_x, player_y)  # Update each enemy


    def fire_bullet(self, enemy):
        "A helper function responsible for the firing of the bullet which is called from update"
        if(time.time() - enemy.attack_bullet_timer) > 1.5 and enemy.bullet_shot == False:
            if(enemy in self.trapezoid_sprites):
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", scale=1)
                bullet.center_x = enemy.center_x                
                bullet.center_y = enemy.top  # Start the bullet just above the enemy  
                bullet.angle = 180  #downwards 
                bullet.change_y = -constant.ENEMY_BULLET_SPEED  # Moving down
                self.enemy_bullet_list.append(bullet)
            return True
            
            

