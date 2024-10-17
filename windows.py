import random
import arcade
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SCALE = .075
BULLET_SPEED = 10
SCREEN_TITLE = "Galaga Game Window"
ENEMY_SPAWN_INTERVAL = 3
STAR_COUNT = 100
STAR_SPEED = 2
TWINKLE_SPEED = 0.1


class SwoopingEnemy(arcade.Sprite):
    """Enemy class to populate the enemies in a swooping motion every two seconds for now. Will potentially update as we count time game has gone on for/to make grid more rigid instead of random."""
    def __init__(self, image, scale, target_x, target_y):
        super().__init__(image, scale)
        self.start_x = random.randint(0, SCREEN_WIDTH)
        self.start_y = SCREEN_HEIGHT
        self.center_x = self.start_x
        self.center_y = self.start_y
        self.target_x = target_x
        self.target_y = target_y
        self.swoop_timer = 0  # Timer for loop swoop motion

    def update(self):
        """Update the enemy's movement."""
        # Swoop the enemy into position over the course of two seconds
        if self.swoop_timer < 2.0:
            # Achieve curved movement using sine calculation
            angle = self.swoop_timer * math.pi * 1 # Full circle over 1 second
            radius = 300  # Radius of the loop
            self.center_x = self.start_x + math.sin(angle) * radius
            self.center_y = self.start_y - (self.swoop_timer * 100)  # Move downward gradually
        else:
            # After swooping, move the enemy to the target position
            if self.center_y > self.target_y:
                self.center_y -= 2  # Move downward

        # Increment the swoop timer
        self.swoop_timer += 1 / 60  # Update timer based on 60 fps

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


class StartView(arcade.View):
    """ View that is initially loaded """

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        # Depending on galaga versions, the start screen has space art ie: planets/stars. 
        # I am adding stars to ours via a list of random coordinates.
        self.star_list = []
        # Generate star positions
        for _ in range(50): # Adjust the passed range to change the amount of stars
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            self.star_list.append((x, y))

    def on_draw(self):
        """ Draw this view """
        self.clear()
        # Draw stars
        for star in self.star_list:
            x, y = star
            arcade.draw_circle_filled(x, y, 2, arcade.color.WHITE)
    
        # Setting variables used in the drawing of start screen
        text = "GALAGA"
        text_x = SCREEN_WIDTH // 2
        text_y = SCREEN_HEIGHT // 1.75
        outline_color = arcade.color.RED
        fill_color = arcade.color.GREEN

        # To create an outline effect, draw GALAGA slightly offset in all 4 directions in red
        arcade.draw_text(text, text_x - 2, text_y - 2, outline_color, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text(text, text_x + 2, text_y - 2, outline_color, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text(text, text_x - 2, text_y + 2, outline_color, font_size=50, anchor_x="center", anchor_y="center")
        arcade.draw_text(text, text_x + 2, text_y + 2, outline_color, font_size=50, anchor_x="center", anchor_y="center")

        # Draw the main text on top in green
        arcade.draw_text(text, text_x, text_y, fill_color, font_size=50, anchor_x="center", anchor_y="center")

        #Advance to game instruction
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
        # Set up star positions
        self.star_list = []
        
        # Initialize variables for the player, enemies, bullets, etc.
        self.player_sprite = None
        self.test_enemy = None
        self.enemy_list = None
        self.bullet_list = None
        self.score = 0
        self.time_elapsed = 0  # Track time for enemy spawning

        # Sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound("sources/sounds/wilhelm.wav")

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def setup(self):
        """Set up the game variables and objects"""
        # Initialize player sprite and sprite lists
        self.player_sprite = arcade.Sprite("sources/player.png", scale=PLAYER_SCALE)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50
        
        # Initialize sprite lists
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        # Score
        self.score = 0

        # Enemies (testing for now)
        self.test_enemy = arcade.Sprite("sources/enemies/json.jpeg", scale=1)
        self.test_enemy.center_x = SCREEN_WIDTH // 2
        self.test_enemy.center_y = SCREEN_HEIGHT // 2
        self.enemy_list.append(self.test_enemy)
        self.time_elapsed = 0

        self.spawn_enemy()  # Initial enemy spawn

        # Setup stars
        for _ in range(STAR_COUNT):
            star = Star()
            self.star_list.append(star)


    def spawn_enemy(self):
        """Spawn an enemy that performs a loop swoop before settling into position."""
        target_x = random.randint(50, SCREEN_WIDTH - 50)
        target_y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 100)
        enemy = SwoopingEnemy("sources/enemies/json.jpeg", scale=1, target_x=target_x, target_y=target_y)
        self.enemy_list.append(enemy)


    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        # Draw stars on background
        for star in self.star_list:
            star.draw()
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
        self.enemy_list.update()

        # Keep the player on the screen
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH

        # Increment the time elapsed
        self.time_elapsed += delta_time

        # Update stars to appear as scrolling
        for star in self.star_list:
            star.update()

        # Check if 10 seconds have passed
        if self.time_elapsed >= ENEMY_SPAWN_INTERVAL:
            # Spawn a new enemy
            self.spawn_enemy()
            # Reset the timer
            self.time_elapsed = 0

        for bullet in self.bullet_list:

            enemies_hit = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if (len(enemies_hit) > 0):
                bullet.remove_from_sprite_lists()

            for enemy in enemies_hit:
                enemy.remove_from_sprite_lists()
                self.score += 1

                arcade.play_sound(self.hit_sound)

            if bullet.bottom > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()



def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()