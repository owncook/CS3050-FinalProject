import arcade
import math
import constant
import time
import random

class Swooping_Enemy(arcade.Sprite):
    """Enemy class that swoops towards the player dynamically, updating its attack target as the player moves."""
    def __init__(self, image_paths, scale, home_x, home_y):
        super().__init__(image_paths[0], scale)
        
        # -- Animation setup
        self.frames = [arcade.load_texture(img) for img in image_paths]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.5

        # Initial spawn and home positions
        self.start_x = constant.SCREEN_WIDTH / 2
        self.start_y = constant.SCREEN_HEIGHT + constant.ENEMY_OFFSCREEN_MARGIN
        self.home_x = home_x
        self.home_y = home_y

        # Center position for movement
        self.center_x = self.start_x
        self.center_y = self.start_y

        # Target position for attacking the player
        self.target_x = None
        self.target_y = None

        # Initialization of timers and state flags
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
        """Initiate an attack towards the player's position, sometimes slightly offset."""
        if self.is_spawning:
            return
        self.is_attacking = True
        self.frame_count = 0
        self.swoop_timer = 0
        
        # randomly decide whether to apply an offset
        # set the chance of an offset at 60% so the enemies don't always hit the player directly (makes gameplay too difficult)
        should_offset = True  
        # this offset value determines whether or not the enemy swoops directly at the player or if they swoop a little to the left/right 
        self.target_offset_x = random.uniform(-250, 250) if should_offset else 0  

        # initial target calculation with potential offset
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

            # Calculate control points for Bézier curve
            control_x = (self.home_x + self.target_x) / 2
            control_y = max(self.home_y, self.target_y or self.home_y) + 150

            # Bézier curve parameter
            t = min(self.swoop_timer / 3, 1)
            self.center_x = (1 - t)**2 * self.home_x + 2 * (1 - t) * t * control_x + t**2 * self.target_x
            self.center_y = (1 - t)**2 * self.home_y + 2 * (1 - t) * t * control_y + t**2 * self.target_y

            if t >= 1 or self.center_y < 0:
                # Reset after swoop
                self.is_attacking = False
                self.center_x = self.home_x
                self.center_y = self.home_y
                self.swoop_timer = 0

        elif self.is_spawning:
            if self.swoop_timer >= self.start_delay:
                # Calculate spawn movement
                control_x = (self.start_x + self.home_x) / 2
                control_y = max(self.start_y, self.home_y) + 150
                t = min(self.swoop_timer / 5, 1)
                self.center_x = (1 - t)**2 * self.start_x + 2 * (1 - t) * t * control_x + t**2 * self.home_x
                self.center_y = (1 - t)**2 * self.start_y + 2 * (1 - t) * t * control_y + t**2 * self.home_y
                self.swoop_timer += delta_time
                if t >= 1:
                    self.is_spawning = False
                    self.center_x = self.home_x
                    self.center_y = self.home_y
                    self.swoop_timer = 0

        # Update bullets
        self.enemy_bullet_list.update()
