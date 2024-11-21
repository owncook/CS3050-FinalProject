import random
import arcade
import arcade.key
from constant import *
import math
from trapezoid import Trapezoid
from star import Star
arcade.load_font("sources/fonts/emulogic-font/Emulogic-zrEw.ttf")


class Smoke(arcade.SpriteCircle):
    """ This class represents a puff of smoke that appears behind the exploded sprite. """
    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self):
        """ Update the smoke particle """
        if self.alpha <= PARTICLE_FADE_RATE:
            # Remove faded out particles.
            self.remove_from_sprite_lists()
        else:
            # Update values.
            self.alpha -= SMOKE_FADE_RATE
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += SMOKE_EXPANSION_RATE


class Particle(arcade.SpriteCircle):
    """ This class represents an explosion particle that flies out of the center of the exploded sprite. """
    def __init__(self, my_list):
        # Choose a random color.
        color = random.choice(PARTICLE_COLORS)

        # Make the particle
        super().__init__(PARTICLE_RADIUS, color)

        # Track normal particle texture, this allows us to flip on sparkle.
        self.normal_texture = self.texture

        # Keep track of the list we are in, this allows us to add a smoke trail.
        self.my_list = my_list

        # Set direction/speed of the explosion particles.
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        # Track original alpha. Used as part of sparkle where alpha is temporarily set back to 255.
        self.my_alpha = 255

        # Add smoke particles to the list we are currently in. 
        self.my_list = my_list

    def update(self):
        """ Update the explosion particle """
        if self.my_alpha <= PARTICLE_FADE_RATE:
            # Remove the particle if it has faded out. 
            self.remove_from_sprite_lists()
        else:
            # Update particle position and opacity.
            self.my_alpha -= PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= PARTICLE_GRAVITY

            # Randomly sparkle the explosion.
            if random.random() <= PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(int(self.width),
                                                          arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            # Randomly leave smoke behind after the explosion.
            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)
