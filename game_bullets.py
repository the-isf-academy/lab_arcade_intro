############################################
# adapted from Python Aracde Example Games
#
# 💻 Experiment with the settings, see what you discover!
############################################

import random
import arcade
import os

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game Bullets Example"

BULLET_SPEED = 5
MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    def __init__(self):
        """ 
        Initializer set up the game and initialize the variables. 
        """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # sets up score
        self.score = 0

        # sets the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # sets up the player 
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/"
                                           "femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        # creates the coins
        self.coin_list = arcade.SpriteList()

        for i in range(COIN_COUNT):

            # Create the coin instance
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the coin to the list
            self.coin_list.append(coin)

        # sets up bullets
        self.bullet_list = arcade.SpriteList()


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        elif key == arcade.key.UP:
            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            # rotates image
            bullet.angle = 90

            # Give the bullet a speed
            bullet.change_y = BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate sprite list
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # updates player
        self.player_list.update()

        # updates on bullet 
        self.bullet_list.update()

        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()


if __name__ == "__main__":
    window = MyGame()   
    arcade.run()