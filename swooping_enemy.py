import arcade
from windows import SCREEN_HEIGHT, SCREEN_WIDTH
import random
import math

class swooping_enemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now. Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, target_x, target_y):
        super().__init__(image, scale)
        # set where on the screen the enemies will spawn from
        self.start_x = random.randint(0, SCREEN_WIDTH)
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

# Creating star class for background
class Star():
    def __init__(self):
        # Randomly initialize the position and size of the star
        self.x = random.uniform(0, SCREEN_WIDTH)
        self.y = random.uniform(0, SCREEN_HEIGHT)
        self.size = random.uniform(1, 3)
        self.speed = random.uniform(1, STAR_SPEED)
        self.alpha = random.uniform(100, 255)  # Alpha controls brightness (transparency)
        self.twinkle_direction = 1  # 1 for increasing brightness, -1 for decreasing

    def update(self):
        # Move the star downward
        self.y -= self.speed
        # If the star moves off the screen, reset it to the top
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            self.x = random.uniform(0, SCREEN_WIDTH)

        self.alpha += self.twinkle_direction * random.uniform(0, TWINKLE_SPEED) * 255

        # Reverse the twinkling direction if alpha reaches the limits (100 to 255)
        if self.alpha >= 255:
            self.alpha = 255
            self.twinkle_direction = -1
        elif self.alpha <= 100:
            self.alpha = 100
            self.twinkle_direction = 1
    def draw(self):
        # Draw the star as a simple circle
        arcade.draw_circle_filled(self.x, self.y, self.size,arcade.make_transparent_color(arcade.color.WHITE, self.alpha))

