import arcade
import math

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
PLAYER_SCALE = .075
BULLET_SPEED = 10
SCREEN_TITLE = "Galaga Game Window"
ENEMY_SPAWN_INTERVAL = 3
STAR_COUNT = 100
STAR_SPEED = 2
TWINKLE_SPEED = 0.1
ATTACK_INTERVAL = 4  # Every 8 seconds

class Swooping_Enemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now. Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, home_x, home_y):
        super().__init__(image, scale)
        # set where on the screen the enemies will spawn from
        self.start_x = home_x
        self.start_y = SCREEN_HEIGHT

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

        # initialize boolean for the enemy's attack status
        self.is_attacking = False

        self.bullet_fired = 0
        self.enemy_bullet_list = arcade.SpriteList()


        #TODO: spawnmove()

    def setup(self):
        self.enemy_bullet_list = arcade.SpriteList()

    def attack(self, player_x, player_y):
        """Set the enemy to swoop down and shoot bullets."""
        self.is_attacking = True
        self.target_x = player_x
        self.target_y = player_y
        self.swoop_timer = 0

        # Fire three bullets during attack
        for _ in range(3):
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
        angle = math.atan2(self.target_y - self.center_y, self.target_x - self.center_x)
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
        return bullet
    
    def on_draw(self):
        self.enemy_bullet_list.draw()

    def update_attack_timer(self, delta_time):
        """Increment attack timer by delta_time."""
        self.swoop_timer += delta_time 

    def update(self, delta_time, player_x=None, player_y=None, bullet_list=None):
        """Update the enemy's movement and shooting behavior."""
        if self.is_attacking:
            # Calculate Bézier curve points for a smooth swoop
            control_x = (self.start_x + self.target_x) / 2
            control_y = max(self.start_y, self.target_y) + 150  # control point above player

            # Quadratic Bézier parameter t, from 0 to 1 over 2 seconds
            t = min(self.swoop_timer / 3.5, 1)
            self.center_x = (1 - t)**2 * self.start_x + 2 * (1 - t) * t * control_x + t**2 * self.target_x
            self.center_y = (1 - t)**2 * self.start_y + 2 * (1 - t) * t * control_y + t**2 * self.target_y

            if self.swoop_timer > 1:  # Fire bullets after 1 second
                bullet = self.fire_bullet()
                self.enemy_bullet_list.append(bullet)  # Add bullet to the central bullet list
            
            # Increment swoop timer
            self.swoop_timer += delta_time

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
        for bullet in self.enemy_bullet_list:
            if bullet.bottom < 0:  # if the bullet goes off-screen
                bullet.remove_from_sprite_lists()


        
