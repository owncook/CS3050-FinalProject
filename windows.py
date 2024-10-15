import random
import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BULLET_SPEED = 5
SCREEN_TITLE = "Galaga Game Window"



class InstructionView(arcade.View):
    """ View to show instructions """

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SEA_GREEN)

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
                                          color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press esc to return to play",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            arcade.set_background_color(arcade.color.BLACK)
            self.window.show_view(self.game_view)


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("game_over.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        # Initialize the game window
        super().__init__()
        
        # Set background color
        arcade.set_background_color(arcade.color.BLACK)
        
        # Initialize variables for the player, enemies, bullets, etc.
        self.player_sprite = None
        self.enemy_list = None
        self.bullet_list = None
        self.score = 0

        # Sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")


        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def setup(self):
        """Set up the game variables and objects"""
        # Initialize player sprite and sprite lists
        self.player_sprite = arcade.Sprite("sources/player.png", scale=5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50
        
        # Initialize sprite lists
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        # Score
        self.score = 0

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        
        # Draw the player
        self.player_sprite.draw()
        
        # Draw enemies and bullets
        self.enemy_list.draw()
        self.bullet_list.draw()
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 5
        elif key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)
        elif key == arcade.key.SPACE:
            arcade.play_sound(self.gun_sound)
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", scale=1)

            bullet.angle = 90

            bullet.change_y = BULLET_SPEED

            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            self.bullet_list.append(bullet)


    def on_key_release(self, key, modifiers):
        """Handle key release events"""
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Update game logic"""
        # Update player, enemies, bullets
        self.player_sprite.update()
        self.bullet_list.update()



def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()