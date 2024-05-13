############################################
# adapted from Python Aracde Example Games
#
# 💻 Experiment with the settings, see what you discover!
############################################

import random
import arcade
import os

class MyGame(arcade.Window):
    def __init__(self):
        # Initializer set up the game and initialize the variables. 
        

        # Call the parent class initializer
        self.screen_width = 800
        self.screen_height = 800

        super().__init__(
            width = self.screen_width,
            height = self.screen_height, 
            title = "Game Bullets Example")

        # sets the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # sets up the player 
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            filename = "assets/player_sprite.png", 
            center_x = 50,
            center_y = 70,
            scale = 0.5)
        
        self.movement_speed = 5

        self.player_list.append(self.player_sprite)

        # sets up the coins
        self.coin_list = arcade.SpriteList()

        for i in range(5):

            # Create the coin instance
            coin = arcade.Sprite(
                filename = "assets/coin_sprite.png", 
                scale =  0.005)

            # Position the coin
            coin.center_x = random.randrange(self.screen_width)
            coin.center_y = 500

            # Add the coin to the list
            self.coin_list.append(coin)

        # sets up lasers
        self.laser_list = arcade.SpriteList()

        self.laser_sprite_path = "assets/laser_sprite.png"
        self.laser_sprite_scale = 0.03
        self.laser_speed = 5

        self.laser_sound = arcade.load_sound(path = "assets/laser-gun.wav")

        # sets up score
        self.score = 0

    def on_draw(self):
        # Render the screen.
        

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()

        self.coin_list.draw()
        self.laser_list.draw()

        # Render the text
        arcade.draw_text(
            f"Score: {self.score}", 
            10, 
            20, 
            arcade.color.WHITE, 
            14)
    
    def on_key_press(self, key, modifiers):
        # Called whenever a key is pressed.
        

        if key == arcade.key.A:
            self.player_sprite.change_x = -self.movement_speed

        elif key == arcade.key.D:
            self.player_sprite.change_x = self.movement_speed

        elif key == arcade.key.SPACE:
            # Create a laser
            laser = arcade.Sprite(
                filename = self.laser_sprite_path,
                scale = self.laser_sprite_scale)

            # rotates image
            laser.angle = 90

            # Give the bullet a speed
            laser.change_y = self.laser_speed

            # Position the laser
            laser.center_x = self.player_sprite.center_x
            laser.bottom = self.player_sprite.top

            # Add the laser to the appropriate sprite list
            self.laser_list.append(laser)

            arcade.play_sound(self.laser_sound)
        
        

        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        # Called when the user presses a mouse button.
        

        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        

    def on_update(self, delta_time):
        # Movement and game logic 

        # updates player
        self.player_list.update()

        # updates on laser 
        self.laser_list.update()

        for laser in self.laser_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(laser, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if laser.bottom > self.screen_height:
                laser.remove_from_sprite_lists()


# Create a Game object
window = MyGame()
# Run the game
arcade.run()