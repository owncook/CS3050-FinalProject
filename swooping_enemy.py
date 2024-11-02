import arcade
import math
import constant


BULLET_SPEED = 3


class Swooping_Enemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now.
    Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, home_x, home_y):
        super().__init__(image, scale)
        # set where on the screen the enemies will spawn from
        self.start_x = home_x
        self.start_y = constant.SCREEN_HEIGHT #TODO: will be updated to go with the spawnMovement() method

        # set the center of the curve that the enemies will swoop around 
        self.center_x = self.start_x
        self.center_y = self.start_y

        # set the final position that they enemy will settle into after the swoop 
        self.home_x = home_x
        self.home_y = home_y

        # target for the enemies
        self.target_x = None
        self.target_y = None

        # initialize a timer for the enemy swoop motion
        self.swoop_timer = 0  
        self.frame_count = 0
        self.enemy_bullet_list = arcade.SpriteList()

        # initialize boolean for the enemy's attack status
        self.is_attacking = False


        #TODO: spawnmove()

    def setup(self):
        self.enemy_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

    def attack(self, enemy, player_x, player_y):
        """Set the enemy to swoop down and shoot bullets."""
        self.is_attacking = True
        self.frame_count = 0
        self.swoop_timer = 0
        self.target_x = player_x
        self.target_y = player_y
        bullet = self.fire_bullet()
        self.enemy_bullet_list.append(bullet)

    def swoop_into_position(self):
        #swoop the enemy into position over the course of two seconds
        if self.swoop_timer < 2.0:
            #achieve curved movement using sine calculation

            #the angle of the swoop over one second
            swoop_angle = self.swoop_timer * math.pi * 1 # full circle over 1 second

            #the radius of the swoop 
            radius = 300  

            #calculate new x, y for the enemy as it swoops 
            self.center_x = self.start_x + math.sin(swoop_angle) * radius
            self.center_y = self.start_y - (self.swoop_timer * 100)  

        else:
            #after swooping, move the enemy to the home position if the new y-coordinate is greater than the home y-coordinate 
            if self.center_y > self.home_y:
                self.center_y -= 2  # move downward

        #increment the swoop timer
        self.swoop_timer += 1 / 60  # update timer based on 60 fps

    def fire_bullet(self):
        """Fire a bullet towards the player."""
        bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", scale=1)
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.angle = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
        bullet.change_x = math.cos(bullet.angle) * constant.BULLET_SPEED
        bullet.change_y = math.sin(bullet.angle) * constant.BULLET_SPEED
        return bullet
    
    def on_draw(self):
        arcade.start_render()
        self.enemy_bullet_list.draw()

    def update_attack_timer(self, delta_time):
        """Increment attack timer by delta_time."""
        self.swoop_timer += delta_time 

    def update(self, delta_time, enemy, player_x=None, player_y=None, bullet_list=None):
        """Update the enemy's movement and shooting behavior."""
        if self.is_attacking:
            self.frame_count += 1
            # Calculate Bézier curve points for a smooth swoop
            control_x = (self.start_x + self.target_x) / 2
            control_y = max(self.start_y, self.target_y) + 150  # control point above player

            # Quadratic Bézier parameter t, from 0 to 1 over 2 seconds
            t = min(self.swoop_timer / 8, 1)
            self.center_x = (1 - t)**2 * self.start_x + 2 * (1 - t) * t * control_x + t**8 * self.target_x
            self.center_y = (1 - t)**2 * self.start_y + 2 * (1 - t) * t * control_y + t**8 * self.target_y

            # Increment swoop timer
            self.swoop_timer += delta_time

            if self.frame_count % 60 == 0:  # Fire bullets after 1 second
                print("test")
                print(len(self.enemy_bullet_list))
                
                bullet = arcade.Sprite(":resources:images/space_shooter/laserRed01.png", scale=1)
                bullet.center_x = self.center_x  # Spawn bullet at enemy's current position
                bullet.center_y = self.center_y  # Spawn bullet at enemy's current position
                bullet.change_y = -BULLET_SPEED  # Move bullet straight down
                self.enemy_bullet_list.append(bullet)
            
            # Check if reached target or left screen
            if t >= 1 or self.center_y < 0:
                # Reset after swoop ends
                self.is_attacking = False
                self.center_x = self.home_x
                self.center_y = self.home_y
                self.swoop_timer = 0  # Reset swoop timer for next attack
        else: 
            self.swoop_into_position()

        # Update bullets and remove off-screen bullets
        self.enemy_bullet_list.update()


        
