import random
import arcade.key
import arcade.gui
from constant import *
from database import *
from planet import Planet
from trapezoid import Trapezoid
from star import Star


import os
import sys

def resource_path(relative_path):
    # This handles the resource path for both PyInstaller and when running the script normally
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Now use the updated resource path to load the fonts
font_path_1 = resource_path('sources/fonts/emulogic-font/Emulogic-zrEw.ttf')
font_path_2 = resource_path('sources/fonts/lantenia-font/LanteniaRegular-DOVgR.ttf')
print(font_path_1)  # Check this printed path to verify it's correct
print(font_path_2)


arcade.load_font(font_path_1)
arcade.load_font(font_path_2)


from explosions import Smoke, Particle

default_style = {
        "font_name": "Emulogic",
        "text_color": "arcade.color.RED"
    }



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
                                               width=300, style=default_style)
        self.star_list = []
        # Generate star positions
        for _ in range(50):  # Adjust the passed range to change the amount of stars
            x = random.randint(0, constant.SCREEN_WIDTH)
            y = random.randint(0, constant.SCREEN_HEIGHT)
            self.star_list.append((x, y))
        self.ui_manager_start.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-150, child=start_button))
        start_button.on_click = self.start_button_click

    def on_draw(self):
        """ Draw this view """
        counter = 0
        self.clear()
        if counter == 0:
            top_five = query_database()
        counter += 1
        # Draw stars
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)

        # Setting variables used in the drawing of start screen
        text = "Galaga"
        text_x = constant.SCREEN_WIDTH // 2
        text_y = constant.SCREEN_HEIGHT // 1.75
        outline_color = arcade.color.RED
        fill_color = arcade.color.GREEN

        # To create an outline effect, draw GALAGA slightly offset in all 4 directions in red
        arcade.draw_text(text, text_x - 2, text_y - 2, outline_color, font_size=180, anchor_x="center",
                         anchor_y="center", font_name='Lantenia')
        arcade.draw_text(text, text_x + 2, text_y - 2, outline_color, font_size=180, anchor_x="center",
                         anchor_y="center", font_name='Lantenia')
        arcade.draw_text(text, text_x - 2, text_y + 2, outline_color, font_size=180, anchor_x="center",
                         anchor_y="center", font_name='Lantenia')
        arcade.draw_text(text, text_x + 2, text_y + 2, outline_color, font_size=180, anchor_x="center",
                         anchor_y="center", font_name='Lantenia')
        # Draw the main text on top in green
        arcade.draw_text(text, text_x, text_y, fill_color, font_size=180, anchor_x="center", anchor_y="center", font_name='Lantenia')
        self.ui_manager_start.draw()
        arcade.draw_text("HIGH SCORE", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.05, arcade.color.RED, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][2]), constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.1,
                         arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("3GDOWN", constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.05,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text('0', constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.1,
                         arcade.color.WHITE,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("© 2024 Group 3", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 2 - 300, arcade.color.WHITE, 10,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text('All rights reserved', constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 2 - 350,
                         arcade.color.WHITE, 10,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")


    def start_button_click(self, event):
        """ If the user presses the mouse button, start the game. """
        self.ui_manager_start.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


# PauseView displays what the user sees when the esc button is pressed and the game is paused
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

    # If the esc button is pressed again, the game resumes
    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:  # resume game
            arcade.set_background_color(arcade.color.BLACK)
            self.window.show_view(self.game_view)


# The view that the user sees when the game is over
class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        # Initialize star list and the UI manager
        self.star_list = []
        self.ui_manager_end = arcade.gui.UIManager()
        self.text_input = ""
        # Create button default style


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
            SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT / 2 - 105,
            width=200, height=30,
            text_color=arcade.color.RED
        )
        # Create buttons for restarting and to view the leaderboard
        restart_button = arcade.gui.UIFlatButton(text="Restart Game",
                                                 width=300, style=default_style)
        leaderboard_button = arcade.gui.UIFlatButton(text="Enter Score",
                                                     width=300, style=default_style)
        self.ui_manager_end.add(self.text_box)
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=300, style=default_style)

        # Assigning button click functions
        leaderboard_button.on_click = self.leaderboard_button_click
        restart_button.on_click = self.restart_button_click
        quit_button.on_click = self.quit_button_click

        # Adding buttons in our uimanager
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-145, child=leaderboard_button))
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-220, child=restart_button))
        self.ui_manager_end.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-295, child=quit_button))

    def on_draw(self):
        """ Draw this view """
        self.clear()
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)
        arcade.draw_text("Enter Initials Below:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40, arcade.color.RED, 15,
                         anchor_x="center", anchor_y="center",font_name='Emulogic')
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 85, 300, 30, arcade.color.WHITE)
        self.ui_manager_end.draw()
        arcade.draw_text("GAME OVER", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.75, arcade.color.RED, 50,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")

    # Limits the amount of characters that can be taken from the text box to length 3
    def limit_text_length(self):
        if len(self.text_box.text) > 3:
            self.text_box.text = self.text_box.text[:3]

    # Button click function for leaderboard
    def leaderboard_button_click(self, event):
        self.limit_text_length()
        self.text_input = self.text_box.text
        load_database(self.text_input, self.window.shared_stage, self.window.shared_score)
        self.text_box.text = ""
        self.ui_manager_end.disable()
        leaderboard_view = LeaderboardView(self)
        self.window.show_view(leaderboard_view)

    # Button click function for quit
    def quit_button_click(self, event):
        self.ui_manager_end.disable()
        arcade.close_window()

    # Button click function for restarting
    def restart_button_click(self, event):
        """ If the user presses the mouse button, re-start the game. """
        self.ui_manager_end.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


# The view the user has when the leaderboard view is requested
class LeaderboardView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # Create UI manager and star list
        self.star_list = []
        self.ui_manager_leaderboard = arcade.gui.UIManager()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_manager_leaderboard.enable()
        self.window.set_mouse_visible(True)
        # Generate star positions
        for _ in range(50):  # Adjust the passed range to change the amount of stars
            x = random.randint(0, constant.SCREEN_WIDTH)
            y = random.randint(0, constant.SCREEN_HEIGHT)
            self.star_list.append((x, y))
        # Create restart and quit buttons
        restart_button = arcade.gui.UIFlatButton(text="Restart Game",
                                                 width=300, style=default_style)
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=300, style=default_style)
        # Implement function when button is clicked
        restart_button.on_click = self.restart_button_click
        quit_button.on_click = self.quit_button_click
        # Add the buttons to the UI manager
        self.ui_manager_leaderboard.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-220, child=restart_button))
        self.ui_manager_leaderboard.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=-295, child=quit_button))
        arcade.set_viewport(0, constant.SCREEN_WIDTH - 1, 0, constant.SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        # information from the firebase database
        top_five = query_database()
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)
        self.ui_manager_leaderboard.draw()
        # Draw leaderboard
        arcade.draw_text("HIGH SCORE", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.05, arcade.color.RED, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][2]), constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.1,
                         arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("3GDOWN", constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.05,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][2]), constant.SCREEN_WIDTH // 2 - 245, constant.SCREEN_HEIGHT // 1.1,
                         arcade.color.WHITE,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("-BEST 5-", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.25, arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text("RANK  INI  STAGE  SCORE", constant.SCREEN_WIDTH // 2, constant.SCREEN_HEIGHT // 1.37,
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
        arcade.draw_text(str(top_five[0][0]), constant.SCREEN_WIDTH // 2 - 110, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[1][0]), constant.SCREEN_WIDTH // 2 - 110, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[2][0]), constant.SCREEN_WIDTH // 2 - 110, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[3][0]), constant.SCREEN_WIDTH // 2 - 110, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[4][0]), constant.SCREEN_WIDTH // 2 - 110, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[0][1]), constant.SCREEN_WIDTH // 2 + 50, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[1][1]), constant.SCREEN_WIDTH // 2 + 50, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[2][1]), constant.SCREEN_WIDTH // 2 + 50, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[3][1]), constant.SCREEN_WIDTH // 2 + 50, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(str(top_five[4][1]), constant.SCREEN_WIDTH // 2 + 50, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[0][2], constant.SCREEN_WIDTH // 2 + 240, constant.SCREEN_HEIGHT // 2 + 125,
                         arcade.color.RED,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[1][2], constant.SCREEN_WIDTH // 2 + 240, constant.SCREEN_HEIGHT // 2 + 75,
                         arcade.color.BARBIE_PINK,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[2][2], constant.SCREEN_WIDTH // 2 + 240, constant.SCREEN_HEIGHT // 2 + 25,
                         arcade.color.YELLOW,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[3][2], constant.SCREEN_WIDTH // 2 + 240, constant.SCREEN_HEIGHT // 2 - 25,
                         arcade.color.GREEN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")
        arcade.draw_text(top_five[4][2], constant.SCREEN_WIDTH // 2 + 240, constant.SCREEN_HEIGHT // 2 - 75,
                         arcade.color.CYAN,
                         20,
                         anchor_x="center", anchor_y="center", font_name="Emulogic")

    # The user quit when quit button is clicked
    def quit_button_click(self, event):
        self.ui_manager_leaderboard.disable()
        arcade.close_window()

    # The user restart when restart button is clicked
    def restart_button_click(self, event):
        """ If the user presses the mouse button, re-start the game. """
        self.ui_manager_leaderboard.disable()
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


# The view that the user sees when playing the game
class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        # Initialize the game window
        super().__init__()
        # -- Animation
        self.player_image_paths = [resource_path('sources/uvmship.png'),
                                   resource_path('sources/uvmship_frame2.png')]
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

        # Set background color
        arcade.set_background_color(arcade.color.BLACK)
        # Set up star positions
        self.star_list = []

        # Initialize variables for the player, enemies, bullets, etc.
        self.test_enemy = None
        self.enemy_list = None
        self.bullet_list = None
        self.lives = 3
        self.heart_texture = arcade.load_texture(resource_path('sources/heart.png'))

        self.score = 0
        self.time_elapsed = 0  # Track time for enemy spawning
        self.pressed_keys = set()  # List to track movement keys pressed

        # Sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(resource_path("sources/sounds/wilhelm.wav"))
        self.explosions_list = None

        # Don't show the mouse cursor 
        self.window.set_mouse_visible(False)

        self.frame_count = 0

        # Enemy trapezoid creation and tracking variables
        self.enemy_trapezoid = Trapezoid()
        self.stage_counter = 1

        # Invincibility
        self.is_invincible = False
        self.invincibility_timer = 0  # Timer for invincibility
        self.flash_interval = 0.10    # Time between flashes
        self.last_flash_time = time.time()  # Tracks the last flash timestamp
        self.invincibility_duration = 1.5  # Duration of invincibility in seconds

        # Game over conditions
        self.is_game_over = False       # Tracks if the game over sequence has started
        self.game_over_timer = 0.0      # Timer for the game over flashing effect
        self.game_over_flash_interval = 0.10  # Time between flashes during game over



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
        output = f"Score:{int(self.score)}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 10,font_name='Emulogic')

        # ---Lives ---
        for i in range(self.lives):
            x_position = 150 + i * 30
            y_position = 32

            arcade.draw_texture_rectangle(x_position, y_position, 40, 40, self.heart_texture)

        # ---Stage ---
        output = f"Stage:{self.stage_counter}"
        arcade.draw_text(output, 870, 20, arcade.color.WHITE, 10, font_name='Emulogic')

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

         # If the game is over, handle the game over flashing and transition
        if self.is_game_over:
            self.game_over_timer += delta_time

            # Flash the player sprite
            current_time = time.time()
            if current_time - self.last_flash_time > self.game_over_flash_interval:
                self.player_sprite.alpha = 255 if self.player_sprite.alpha == 100 else 100
                self.last_flash_time = current_time

            # Transition to GameOverView after 2 seconds
            if self.game_over_timer >= 1:
                self.player_sprite.alpha = 255  # Ensure the player is fully visible
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            return  # Prevent further updates while in game over sequence


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

                    for i in range(PARTICLE_COUNT):
                        particle = Particle(self.explosions_list)
                        particle.position = self.player_sprite.position
                        self.explosions_list.append(particle)

                        smoke = Smoke(50)
                        smoke.position = self.player_sprite.position
                        self.explosions_list.append(smoke)

                        arcade.play_sound(self.hit_sound)
                    self.is_invincible = True  # Enable invincibility
                    if self.lives <= 0:
                        self.is_game_over = True
                        self.game_over_timer = 0.0  # Reset the game over timer

        # Collision detection for enemies
        if not self.is_invincible:
            for enemy in self.enemy_trapezoid.trapezoid_sprites:
                if arcade.check_for_collision(enemy, self.player_sprite):
                    enemy.remove_from_sprite_lists()
                    self.lives -= 1
                    for i in range(PARTICLE_COUNT):
                        particle = Particle(self.explosions_list)
                        particle.position = self.player_sprite.position
                        self.explosions_list.append(particle)

                        smoke = Smoke(50)
                        smoke.position = self.player_sprite.position
                        self.explosions_list.append(smoke)

                        arcade.play_sound(self.hit_sound)
                    self.is_invincible = True  # Enable invincibility
                    if self.lives <= 0:
                        self.is_game_over = True
                        self.game_over_timer = 0.0  # Reset the game over timer
                
        # Manage player invincibility and flashing effect
        if self.is_invincible:
            current_time = time.time()

            # Toggle flashing effect based on flash interval
            if current_time - self.last_flash_time > self.flash_interval:
                # Alternate between fully visible and semi-transparent
                self.player_sprite.alpha = 255 if self.player_sprite.alpha == 50 else 50
                self.last_flash_time = current_time

            # Increment invincibility timer
            self.invincibility_timer += delta_time
            if self.invincibility_timer >= self.invincibility_duration:  # Total duration for flashing
                self.is_invincible = False
                self.invincibility_timer = 0
                self.player_sprite.alpha = 255  # Fully reset visibility
        else:
            # Ensure the player remains fully visible when not invincible
            self.player_sprite.alpha = 255


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

        self.window.shared_score = int(self.score)
        self.window.shared_stage = int(self.stage_counter)

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
