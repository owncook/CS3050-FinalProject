import arcade
import constant
from windows import StartView

def main():
    """ Main function """

    window = arcade.Window(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, constant.SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
  