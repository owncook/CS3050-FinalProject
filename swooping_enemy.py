import arcade
import math
import constant
from constant import *
import time
import random
import os 
import sys

def resource_path(relative_path):
    # This handles the resource path for both PyInstaller and when running the script normally
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Swooping_Enemy(arcade.Sprite):
    """Enemy class that swoops towards the player dynamically, updating its attack target as the player moves."""
    def __init__(self, image_paths, scale, home_x, home_y):
        super().__init__(image_paths[0], scale)
        
        # Animation setup.
        self.frames = [arcade.load_texture(img) for img in image_paths]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.5

        # Initialize spawn positions for the enemies.
        self.start_x = constant.SCREEN_WIDTH / 2
        self.start_y = constant.SCREEN_HEIGHT + constant.ENEMY_OFFSCREEN_MARGIN

        # Initialize home positions for the enemies (where they return to in the trapezoid).
        self.home_x = home_x
        self.home_y = home_y

        # Initialize the center positions (x and y) of the enemy to use in movement calculations.
        self.center_x = self.start_x
        self.center_y = self.start_y

        # Target position for attacking the player--initially set to none (so that we can dynamically update the values).
        self.target_x = None
        self.target_y = None

        # Initialization of timers and state flags.
        self.swoop_timer = 0
        self.frame_count = 0
        self.enemy_bullet_list = arcade.SpriteList()
        self.is_spawning = True
        self.start_delay = 0
        self.is_attacking = False
        self.attack_bullet_timer = 0
    
    def update_animation(self, delta_time):
        """Update sprite animation."""
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame]

    def attack(self, enemy, player_x, player_y):
        """Initiate an attack towards the player's position, slightly offset. We offset the player's 
        position so that the game is playable but the enemy still swoops towards the player dynamically. """
        # If the player is spawning, then do not attack.
        if self.is_spawning:
            return
        
        # Set self.is_attacking to True.
        self.is_attacking = True

        # Initialize the frame count and swoop timer to track the enemies position over time. 
        self.frame_count = 0
        self.swoop_timer = 0
        
        # Apply an offset to the final target position of the enemy. 
        # We add this offset so that the enemies don't always hit the player directly
        # which makes the game more playable but allows us to swoop the enemies towards the players
        # as the player's position dynamically updates. 
        should_offset = True  

        # This offset value makes it so that the enemy's final target x-position is a little to the left or right
        # of the player. 
        self.target_offset_x = random.uniform(-250, 250) if should_offset else 0  

        # Initial target calculation with offset value accounted for. 
        self.target_x = player_x + self.target_offset_x
        self.target_y = player_y
        self.attack_bullet_timer = time.time()

    def update_swoop_timer(self, delta_time):
        """Update swoop timer."""
        self.swoop_timer += delta_time

    def update(self, delta_time, player_x, player_y):
        """Update enemy movement and attack behavior."""
        if self.is_attacking:
            self.frame_count += 1
            # Dynamically update target as the player's position changes with a consistent offset
            self.target_x = player_x + self.target_offset_x
            self.target_y = player_y

            # Bézier curve 
            # We use a Bézier curve with three control pointsto implementing the swooping motion of the enemies. 
            # The formula for a Bézier curve with three controll points is: P = (1−t)2P1 + 2(1−t)tP2 + t2P3
            # We replace P with x and y to get corresponding coordinates. Now our three-point curve is formed by points (x,y) calculated as:
            # x = (1−t)**2*x1 + 2(1−t)t*x2 + t**2*x3
            # y = (1−t)**2*y1 + 2(1−t)t*y2 + t**2*y3
            # where t is on the interval t = min(self.swoop_timer / MAX_SWOOP_DURATION, 1)
            # control point x1 is the home position of the enemy
            # control point x2 is the intermediary between the home and target position
            # and control point x3 is the target position of the enemy (a destination slightly offset from the player)

            # Calculate intermediary control points (x2, y2) for Bézier curve
            control_x = (self.home_x + self.target_x) / 2
            control_y = max(self.home_y, self.target_y or self.home_y) + 150

            # Set Bézier curve parameter, `t`, (the interval of the swoop over time) normalized by MAX_SWOOP_DURATION
            t = min(self.swoop_timer / MAX_SWOOP_DURATION, BEZIER_T_PARAMETER)

            # Quadratic Bézier curve formula for `center_x` and `center_y` of the enemy using control the previously commented control points 
            self.center_x = ((1 - t)**BEZIER_POWER * self.home_x + 2 * (1 - t) * t * control_x + t**BEZIER_POWER * self.target_x)
            self.center_y = ((1 - t)**BEZIER_POWER * self.home_y + 2 * (1 - t) * t * control_y + t**BEZIER_POWER * self.target_y)
            
            # When the t parameter has hit the max or the enemy has gone below the window the enemy has completed their swoop.
            if t >= 1 or self.center_y < 0:
                # Reset after swoop
                self.is_attacking = False
                self.start_x = self.home_x
                self.start_y = SCREEN_HEIGHT + 100
                self.swoop_timer = 0
                self.is_spawning = True

        elif self.is_spawning:
            if self.swoop_timer >= self.start_delay:
                # Calculate spawn movement
                control_x = (self.start_x + self.home_x) / 2
                control_y = max(self.start_y, self.home_y) + 150
                t = min(self.swoop_timer / 5, 1)
                self.center_x = (1 - t)**BEZIER_POWER * self.start_x + 2 * (1 - t) * t * control_x + t**BEZIER_POWER * self.home_x
                self.center_y = (1 - t)**BEZIER_POWER * self.start_y + 2 * (1 - t) * t * control_y + t**BEZIER_POWER * self.home_y
                self.swoop_timer += delta_time
                # When the t parameter has hit the max the enemy has completed their swoop
                if t >= 1:
                    # Settle after swoop
                    self.is_spawning = False
                    self.center_x = self.home_x
                    self.center_y = self.home_y
                    self.swoop_timer = 0

        # Update bullets
        self.enemy_bullet_list.update()
