import arcade
import math
import constant
import time



class Swooping_Enemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now.
    Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, home_x, home_y):
        super().__init__(image, scale)
        # set where on the screen the enemies will spawn from
        self.start_x = constant.SCREEN_WIDTH/2
        self.start_y = constant.SCREEN_HEIGHT + constant.ENEMY_OFFSCREEN_MARGIN #TODO: will be updated to go with the spawnMovement() method

        # set the final position that they enemy will settle into after the swoop 
        self.home_x = home_x
        self.home_y = home_y

        # set the center of the curve that the enemies will swoop around 
        self.center_x = self.start_x
        self.center_y = self.start_y

        # target for the enemies
        self.target_x = None
        self.target_y = None

        # initialize a timer for the enemy swoop motion
        self.swoop_timer = 0  
        self.frame_count = 0
        self.enemy_bullet_list = arcade.SpriteList()

        #In intiliazation set is_spawning to true for movement update
        self.is_spawning = True
        self.start_delay = 0 
        self.swoop_timer = 0

        # initialize boolean for the enemy's attack status
        self.is_attacking = False
        self.attack_bullet_timer = 0
        self.bullet_shot = False

    def setup(self):
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        #self.player_list = arcade.SpriteList() #TODO I don't believe this is being used anywhere, should we remove it? -TS

    def attack(self, enemy, player_x, player_y):
        """Set the enemy to swoop down and shoot bullets."""
        #if enemy is still in spawning process leave function
        if self.is_spawning:
            return
        self.is_attacking = True
        self.frame_count = 0
        self.swoop_timer = 0
        self.target_x = player_x
        self.target_y = player_y
        self.attack_bullet_timer = time.time()



    # def fire_bullet(self):
    #     """Fire a bullet towards the player."""
    #     bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", scale=1)
    #     bullet.center_x = self.center_x
    #     bullet.center_y = self.center_y
    #     bullet.angle = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
    #     bullet.change_x = math.cos(bullet.angle) * constant.BULLET_SPEED
    #     bullet.change_y = math.sin(bullet.angle) * constant.BULLET_SPEED
    #     return bullet
    
    def on_draw(self):
        arcade.start_render()
        self.enemy_bullet_list.draw()

    

    def update_swoop_timer(self, delta_time):
        """Increment attack timer by delta_time."""
        self.swoop_timer += delta_time 

    def update(self, delta_time, enemy, player_x=None, player_y=None, bullet_list=None):
        """Update the enemy's movement and shooting behavior."""
        if self.is_attacking:
            self.frame_count += 1
            # Calculate Bézier curve points for a smooth swoop
            control_x = (self.home_x + self.target_x) / 2
            control_y = max(self.home_y, self.target_y) + 150  # control point above player

            # Quadratic Bézier parameter t, from 0 to 1 over 2 seconds
            t = min(self.swoop_timer / 3, 1)
            self.center_x = (1 - t)**2 * self.home_x + 2 * (1 - t) * t * control_x + t**2 * self.target_x
            self.center_y = (1 - t)**2 * self.home_y + 2 * (1 - t) * t * control_y + t**2 * self.target_y

            
            # Check if reached target or left screen
            if t >= 1 or self.center_y < 0:
                # Reset after swoop ends
                self.is_attacking = False
                self.center_x = self.home_x
                self.center_y = constant.SCREEN_HEIGHT
                self.swoop_timer = 0  # Reset swoop timer for next attack
        
        elif self.is_spawning:
            if self.swoop_timer >= self.start_delay:
                # Set the final target position for swooping to be the enemy's home position
                self.target_x = self.home_x
                self.target_y = self.home_y

                #From here out the is_spawning movement logiv is very similar to the first half of the is_attacking
                control_x = (self.start_x + self.target_x) / 2
                control_y = max(self.start_y, self.target_y) + 150  

              
                t = min(self.swoop_timer / 5, 1)
                
                self.center_x = (1 - t)**2 * self.start_x + 2 * (1 - t) * t * control_x + t**2 * self.target_x
                self.center_y = (1 - t)**2 * self.start_y + 2 * (1 - t) * t * control_y + t**2 * self.target_y

                self.swoop_timer += delta_time

                # Check if the swooping motion is complete (i.e., reached target position)
                if t >= 1:
                    self.is_spawning = False  # Mark spawning as complete to stop swooping motion
                    self.center_x = self.home_x  # Ensure enemy ends at home position
                    self.center_y = self.home_y
                    self.swoop_timer = 0      # Reset swoop timer
        else:
           # When attack is over, reset to start descending from top of screen
            if self.center_y > self.home_y:
                self.center_y -= constant.ENEMY_SPEED  # Move down until reaching home_y
            else:
                # Stop at home_y position
                self.center_y = self.home_y
                
        # Update bullets and remove off-screen bullets
        self.enemy_bullet_list.update()


        
