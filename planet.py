import arcade
import constant
import random

import arcade
import constant
import random

class Planet(arcade.Sprite):  # Make Planet a subclass of arcade.Sprite
    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Planet type/sprite info
        self.planet_type = f"{random.randrange(1,5)}"

        # Set the texture for the sprite
        self.texture = arcade.load_texture(f'sources/planets/planet{self.planet_type}.png')
        self.scale = constant.PLANET_SCALE

        # Finding the starting x position for planet
        self.start_x_random_multiplier = random.randrange(0, 11) 
        self.center_x = 100 * self.start_x_random_multiplier
        self.center_y = constant.SCREEN_HEIGHT + 100

        
    def on_update(self, delta_time: float = 1/60):
        # Move the planet down
        self.center_y -= constant.PLANET_SPEED



