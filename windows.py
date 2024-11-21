import random
import arcade
import arcade.key
import arcade.gui
from arcade.gui import UIManager

import constant
from constant import *

from database import *


from planet import Planet

from trapezoid import Trapezoid
from star import Star

arcade.load_font("sources/fonts/emulogic-font/Emulogic-zrEw.ttf")
arcade.load_font("sources/fonts/ozone-font/Ozone-xRRO.ttf")
from explosions import Smoke, Particle


class StartView(arcade.View):
    """ View that is initially loaded """

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)
        self.ui_manager_start = arcade.gui.UIManager()
        self.ui_manager_start.enable()
        self.window.set_mouse_visible(True)
        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        start_button = arcade.gui.UIFlatButton(text="Start Game",
                                               width=200)
        # Depending on galaga versions, the start screen has space art ie: planets/stars. 
        # I am adding stars to ours via a list of random coordinates.
        self.star_list = []
        # Generate star positions
        for _ in range(50):  # Adjust the passed range to change the amount of stars
            x = random.randint(0, constant.SCREEN_WIDTH)
            y = random.randint(0, constant.SCREEN_HEIGHT)
            self.star_list.append((x, y))
        self.ui_manager_start.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-50, child=start_button))
        start_button.on_click = self.start_button_click

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # Draw stars
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)

        # Setting variables used in the drawing of start screen
        text = "GALAGA"
        text_x = constant.SCREEN_WIDTH // 2
        text_y = constant.SCREEN_HEIGHT // 1.75
        outline_color = arcade.color.RED
        fill_color = arcade.color.GREEN

        # To create an outline effect, draw GALAGA slightly offset in all 4 directions in red
        arcade.draw_text(text, text_x - 2, text_y - 2, outline_color, font_size=50, anchor_x="center",
                         anchor_y="center")
        arcade.draw_text(text, text_x + 2, text_y - 2, outline_color, font_size=50, anchor_x="center",
                         anchor_y="center")
        arcade.draw_text(text, text_x - 2, text_y + 2, outline_color, font_size=50, anchor_x="center",
                         anchor_y="center")
        arcade.draw_text(text, text_x + 2, text_y + 2, outline_color, font_size=50, anchor_x="center",
                         anchor_y="center")

        # Draw the main text on top in green
        arcade.draw_text(text, text_x, text_y, fill_color, font_size=50, anchor_x="center", anchor_y="center")
        self.ui_manager_start.draw()

    def start_button_click(self, event):
        """ If the user presses the mouse button, start the game. """
        self.ui_manager_start.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        self.clear()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an orange filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
                                          right=player_sprite.right,
                                          top=player_sprite.top,
                                          bottom=player_sprite.bottom,
                                          color=arcade.color.GREEN + (200,))

        arcade.draw_text("PAUSED", constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press esc to return to play",
                         constant.SCREEN_WIDTH / 2,
                         constant.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            arcade.set_background_color(arcade.color.BLACK)
            self.window.show_view(self.game_view)


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.star_list = []
        self.ui_manager_end = arcade.gui.UIManager()
        self.text_input = ""

    def on_show_view(self):
        # Generate star positions
        for _ in range(50):  # Adjust the passed range to change the amount of stars
            x = random.randint(0, constant.SCREEN_WIDTH)
            y = random.randint(0, constant.SCREEN_HEIGHT)
            self.star_list.append((x, y))
        self.ui_manager_end.enable()
        self.window.set_mouse_visible(True)
        # Creating Button using UIFlatButton
        self.text_box = arcade.gui.UIInputText(
            SCREEN_WIDTH / 2 - 95, SCREEN_HEIGHT / 2 - 105,
            width=200, height=30,
            text_color=arcade.color.RED,
        )
        restart_button = arcade.gui.UIFlatButton(text="Restart Game",
                                                 width=200)
        leaderboard_button = arcade.gui.UIFlatButton(text="Enter Score",
                                                     width=200)
        self.ui_manager_end.add(self.text_box)
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=200)

        # Assigning our on_buttonclick() function
        leaderboard_button.on_click = self.leaderboard_button_click
        restart_button.on_click = self.restart_button_click
        quit_button.on_click = self.quit_button_click

        # Adding button in our uimanager
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-145, child=leaderboard_button))
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-220, child=restart_button))
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-295, child=quit_button))

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.

    def on_draw(self):
        """ Draw this view """
        self.clear()
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)
        arcade.draw_text("Enter Initials Below:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, arcade.color.RED, 15,
                         anchor_x="center", anchor_y="center")
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 85, 200, 30, arcade.color.WHITE)
        self.ui_manager_end.draw()
        arcade.draw_text("GAME OVER", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.75, arcade.color.RED, 50,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")

    def limit_text_length(self):
        if len(self.text_box.text) > 3:
            self.text_box.text = self.text_box.text[:3]

    def leaderboard_button_click(self, event):
        self.limit_text_length()
        self.text_input = self.text_box.text
        load_database(self.text_input, self.window.shared_score)
        self.text_box.text = ""
        self.ui_manager_end.disable()
        leaderboard_view = LeaderboardView(self)
        self.window.show_view(leaderboard_view)

    def quit_button_click(self, event):
        self.ui_manager_end.disable()
        arcade.close_window()

    def restart_button_click(self, event):
        """ If the user presses the mouse button, re-start the game. """
        self.ui_manager_end.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class LeaderboardView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.ui_manager_leaderboard = arcade.gui.UIManager()
        self.star_list = []

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_manager_leaderboard.enable()
        self.window.set_mouse_visible(True)
        # Generate star positions
        for _ in range(50):  # Adjust the passed range to change the amount of stars
            x = random.randint(0, constant.SCREEN_WIDTH)
            y = random.randint(0, constant.SCREEN_HEIGHT)
            self.star_list.append((x, y))
        restart_button = arcade.gui.UIFlatButton(text="Restart Game",
                                                 width=200)
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=200)
        restart_button.on_click = self.restart_button_click
        quit_button.on_click = self.quit_button_click
        self.ui_manager_leaderboard.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-220, child=restart_button))
        self.ui_manager_leaderboard.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-295, child=quit_button))
        arcade.set_viewport(0, constant.SCREEN_WIDTH - 1, 0, constant.SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        top_five = query_database()
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)
        self.ui_manager_leaderboard.draw()
        arcade.draw_text("HIGH SCORE", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.05, arcade.color.RED, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][1]), constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.1, arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("3GDOWN", constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.05, arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][1]), constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.1, arcade.color.WHITE,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("-BEST 5-", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.25, arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("RANK  SCORE  STAGE  INI", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.37,
                         arcade.color.WHITE,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("NO.1", constant.SCREEN_WIDTH // 2 - 255, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("NO.2", constant.SCREEN_WIDTH // 2 - 255, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("NO.3", constant.SCREEN_WIDTH // 2 - 255, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("NO.4", constant.SCREEN_WIDTH // 2 - 255, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("NO.5", constant.SCREEN_WIDTH // 2 - 255, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][1]), constant.SCREEN_WIDTH // 2 - 75, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[1][1]), constant.SCREEN_WIDTH // 2 - 75, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[2][1]), constant.SCREEN_WIDTH // 2 - 75, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[3][1]), constant.SCREEN_WIDTH // 2 - 75, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[4][1]), constant.SCREEN_WIDTH // 2 - 75, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("10", constant.SCREEN_WIDTH // 2 + 107, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("5", constant.SCREEN_WIDTH // 2 + 107, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("5", constant.SCREEN_WIDTH // 2 + 107, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("5", constant.SCREEN_WIDTH // 2 + 107, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("5", constant.SCREEN_WIDTH // 2 + 107, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[0][0], constant.SCREEN_WIDTH // 2 + 270, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[1][0], constant.SCREEN_WIDTH // 2 + 270, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[2][0], constant.SCREEN_WIDTH // 2 + 270, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[3][0], constant.SCREEN_WIDTH // 2 + 270, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[4][0], constant.SCREEN_WIDTH // 2 + 270, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")

    def quit_button_click(self, event):
        self.ui_manager_leaderboard.disable()
        arcade.close_window()

    def restart_button_click(self, event):
        """ If the user presses the mouse button, re-start the game. """
        self.ui_manager_leaderboard.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        # Initialize the game window
        super().__init__()
        # -- Animation
        self.player_image_paths = ['sources/uvmship.png',
                                   'sources/uvmship_frame2.png']
        self.frames = [arcade.load_texture(img) for img in self.player_image_paths]
        self.current_frame = 0
        self.animation_timer = 0.0  # Timer to track animation speed
        self.animation_speed = 0.5  # Time in seconds between frames

        self.player_sprite = arcade.Sprite()
        self.player_sprite.texture = self.frames[self.current_frame]
        self.player_sprite.scale = constant.PLAYER_SCALE
        self.player_sprite.center_x = constant.SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50
        self.home_x = self.player_sprite.center_x
        self.home_y = self.player_sprite.center_y

        self.invincibility_timer = 0  # Timer to track invincibility duration
        self.is_invincible = False  # Flag to check if player is currently invincible
        self.invincibility_duration = 1.0  # Duration of invincibility in seconds


        # Set background color
        arcade.set_background_color(arcade.color.BLACK)
        # Set up star positions
        self.star_list = []

        # Initialize variables for the player, enemies, bullets, etc.
        self.test_enemy = None
        self.enemy_list = None
        self.bullet_list = None
        self.lives = 3
        self.heart_texture = arcade.load_texture('sources/heart.png')

        self.score = 0
        self.time_elapsed = 0  # Track time for enemy spawning
        self.pressed_keys = set()  # List to track movement keys pressed

        # Sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound("sources/sounds/wilhelm.wav")
        self.explosions_list = None

        # Don't show the mouse cursor 
        self.window.set_mouse_visible(False)

        self.frame_count = 0


        # Enemy trapezoid creation and tracking variables
        self.enemy_trapezoid = Trapezoid()
        self.stage_counter = 1



    def setup(self):
        """Set up the game variables and objects"""

        # Initialize sprite lists
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.hearts = arcade.SpriteList()

        self.planet_sprite_list = arcade.SpriteList()
        self.planet_tracker = 0

        # Score
        self.score = 0


        # Setup stars
        for _ in range(constant.STAR_COUNT):
            star = Star()
            self.star_list.append(star)


    def update_animation(self, delta_time):
        # Increment animation timer
        self.animation_timer += delta_time
        # If enough time has passed, change frame
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # Switch to the next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            # Update player sprite texture to show the current frame
            self.player_sprite.texture = self.frames[self.current_frame]

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        # Draw stars on background
        for star in self.star_list:
            star.draw()

        for planet in self.planet_sprite_list:
            planet.draw()

        # Draw the player
        self.player_sprite.draw()

        # Draw enemies and bullets
        self.enemy_list.draw()
        self.bullet_list.draw()

        # Draw the trapezoid
        self.enemy_trapezoid.draw()

        # Put the text on the screen.
        # ---Score ---
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

        # ---Lives ---
        for i in range(self.lives):
            x_position = 150 + i * 30
            y_position = 32

            arcade.draw_texture_rectangle(x_position, y_position, 40, 40, self.heart_texture)

        # ---Stage ---
        output = f"Stage: {self.stage_counter}"
        arcade.draw_text(output, 900, 20, arcade.color.WHITE, 14)

        # Draw explosions
        self.explosions_list.draw()

    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        if key == arcade.key.LEFT:
            self.pressed_keys.add(arcade.key.LEFT)
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.pressed_keys.add(arcade.key.RIGHT)
            self.player_sprite.change_x = 5
        elif key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)
        elif key == arcade.key.SPACE and len(self.bullet_list) < constant.MAX_BULLETS:
            arcade.play_sound(self.gun_sound)
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=1)

            bullet.angle = 90

            bullet.change_y = constant.BULLET_SPEED

            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """Handle key release events"""
        if key == arcade.key.LEFT:
            self.pressed_keys.discard(arcade.key.LEFT)
            # Check if RIGHT is still pressed
            if arcade.key.RIGHT in self.pressed_keys:
                self.player_sprite.change_x = 5
            else:
                self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.pressed_keys.discard(arcade.key.RIGHT)
            # Check if LEFT is still pressed
            if arcade.key.LEFT in self.pressed_keys:
                self.player_sprite.change_x = -5
            else:
                self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Update game logic"""
        self.player_sprite.update()

        # Update invincibility timer
        if self.is_invincible:
            self.invincibility_timer += delta_time
            if self.invincibility_timer >= self.invincibility_duration:
                # End invincibility period
                self.is_invincible = False
                self.invincibility_timer = 0

        # Check if enemy is attacking and update with the player's current position
        for enemy in self.enemy_trapezoid.trapezoid_sprites:
            if enemy.is_attacking:
                enemy.update(delta_time, self.player_sprite.center_x, self.player_sprite.center_y)
            else:
                enemy.update(delta_time, self.home_x, self.home_y)

        self.bullet_list.update()
        self.enemy_list.update()
        self.enemy_trapezoid.enemy_bullet_list.update()
        self.enemy_trapezoid.update(delta_time, self.player_sprite.center_x, self.player_sprite.center_y)
        self.frame_count += 1
        self.time_elapsed += delta_time

        self.explosions_list.update()
        self.update_animation(delta_time)

        # Keep the player on the screen
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > constant.SCREEN_WIDTH:
            self.player_sprite.right = constant.SCREEN_WIDTH

        # Collision detection for enemy bullets
        if not self.is_invincible:
            for enemy_bullet in self.enemy_trapezoid.enemy_bullet_list:
                if arcade.check_for_collision(enemy_bullet, self.player_sprite):
                    enemy_bullet.remove_from_sprite_lists()
                    self.lives -= 1
                    self.is_invincible = True  # Enable invincibility
                    print("Lives: " + str(self.lives))
                    if self.lives <= 0:
                        game_over_view = GameOverView()
                        self.window.show_view(game_over_view)

            # Collision detection for enemies
            for enemy in self.enemy_trapezoid.trapezoid_sprites:
                if arcade.check_for_collision(enemy, self.player_sprite):
                    enemy.remove_from_sprite_lists()
                    self.lives -= 1
                    self.is_invincible = True  # Enable invincibility
                    if self.lives <= 0:
                        game_over_view = GameOverView()
                        self.window.show_view(game_over_view)

        # Stage and score updates
        if self.enemy_trapezoid.check_trapezoid_empty():
            self.stage_counter += 1
            if self.stage_counter % 3 == 1:  # Every third stage the player earns a life
                self.lives += 1
            self.enemy_trapezoid.populate_rows([4, 8, 10])

        # Update bullets, planets, and stars
        for bullet in self.bullet_list:
            enemy_list = self.enemy_trapezoid.trapezoid_sprites
            enemies_hit = arcade.check_for_collision_with_list(bullet, enemy_list)

            if len(enemies_hit) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in enemies_hit:
                enemy.remove_from_sprite_lists()
                self.score += constant.SCORE * (self.stage_counter / 10)
                for i in range(PARTICLE_COUNT):
                    particle = Particle(self.explosions_list)
                    particle.position = enemy.position
                    self.explosions_list.append(particle)

                smoke = Smoke(50)
                smoke.position = enemy.position
                self.explosions_list.append(smoke)

                arcade.play_sound(self.hit_sound)

            if bullet.bottom > constant.SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        self.window.shared_score = self.score

        for star in self.star_list:
            star.update()

        match self.planet_tracker:
            case 0:
                rand_key = random.randint(0, 100)
                if rand_key == 1:
                    current_planet = Planet()
                    self.planet_sprite_list.append(current_planet)
                    self.planet_tracker += 1
            case 1:
                rand_key = random.randint(0, 1000)
                if rand_key == 1:
                    current_planet = Planet()
                    self.planet_sprite_list.append(current_planet)
                    self.planet_tracker += 1

        for planet in self.planet_sprite_list:
            planet.on_update()
            if planet.center_y < 0:
                planet.remove_from_sprite_lists()
                self.planet_tracker -= 1
