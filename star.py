import arcade
import random
import constant


# Creating star class for background
class Star():
    def __init__(self):
        # Randomly initialize the position and size of the star
        self.x = random.uniform(0, constant.SCREEN_WIDTH)
        self.y = random.uniform(0, constant.SCREEN_HEIGHT)
        self.size = random.uniform(1, 3)
        self.speed = random.uniform(1, constant.STAR_SPEED)
        self.alpha = random.uniform(100, 255)  # Alpha controls brightness (transparency)
        self.twinkle_direction = 1  # 1 for increasing brightness, -1 for decreasing

    def update(self):
        # Move the star downward
        self.y -= self.speed
        # If the star moves off the screen, reset it to the top
        if self.y < 0:
            self.y = constant.SCREEN_HEIGHT
            self.x = random.uniform(0, constant.SCREEN_WIDTH)

        self.alpha += self.twinkle_direction * random.uniform(0, constant.TWINKLE_SPEED) * 255

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

