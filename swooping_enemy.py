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

class Swooping_Enemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now. Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, target_x, target_y):
        super().__init__(image, scale)
        # set where on the screen the enemies will spawn from
        self.start_x = target_x
        self.start_y = SCREEN_HEIGHT

        # set the center of the curve that the enemies will swoop around 
        self.center_x = self.start_x
        self.center_y = self.start_y

        # set the final position that they enemy will settle into after the swoop 
        self.target_x = target_x
        self.target_y = target_y

        # initialize a timer for the enemy swoop motion
        self.swoop_timer = 0  

    def update(self):
        """Update the enemy's movement."""
        # swoop the enemy into position over the course of two seconds
        if self.swoop_timer < 2.0:
            # achieve curved movement using sine calculation

            # the angle of the swoop over one second
            swoop_angle = self.swoop_timer * math.pi * 1 # full circle over 1 second

            # the radius of the swoop 
            radius = 300  

            # calculate new x, y for the enemy as it swoops 
            self.center_x = self.start_x + math.sin(swoop_angle) * radius
            self.center_y = self.start_y - (self.swoop_timer * 100)  

        else:
            # after swooping, move the enemy to the target position if the new y-coordinate is greater than the target y-coordinate 
            if self.center_y > self.target_y:
                self.center_y -= 2  # move downward

        # increment the swoop timer
        self.swoop_timer += 1 / 60  # update timer based on 60 fps
