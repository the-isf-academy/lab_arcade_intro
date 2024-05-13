############################################
# adapted from Python Aracde Example Games
#
# 💻 Experiment with the settings, see what you discover!
############################################


import arcade

class MyGame(arcade.Window):
    # Main application class

    def __init__(self):
        #Initializer

        self.screen_width = 400
        self.screen_height = 200

        super().__init__(
            width = self.screen_width, 
            height = self.screen_height, 
            title = "Game 1")


        # Physics
        self.MOVEMENT_SPEED = 5
        self.JUMP_SPEED = 25
        self.GRAVITY = 1.1

        self.game_over = False
        
     
        #Set up the game and initialize the variables.

        # Set up the player
        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(
            "assets/player_sprite.png",
            scale = 1,
            center_x = 196,
            center_y = 270
        )

        self.player_list.append(self.player_sprite)

        # sets up map
        map_name = ":resources:/tiled_maps/map.json"

        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
        }

        # map scaling
        self.TILE_SCALING = 0.5
        self.SPRITE_PIXEL_SIZE = 128
        self.GRID_PIXEL_SIZE = self.SPRITE_PIXEL_SIZE * self.TILE_SCALING

        # read in the tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, 
            layer_options=layer_options,
              scaling=self.TILE_SCALING
        )

        self.end_of_map = self.tile_map.width * self.GRID_PIXEL_SIZE

        # sets wall and coin SpriteLists
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]

  
        # sets the background color
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        # Keep player from running through the wall_list layer
        walls = [self.wall_list]

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls, gravity_constant=self.GRAVITY
        )

        # sets up camera 
        self.camera = arcade.Camera(self.screen_width, self.screen_height)

        # center camera on user
        self.pan_camera_to_user()


    def on_draw(self):
        # Render the screen.
        

        # These commands must happen before we start drawing
        self.camera.use()
        self.clear()

        # draw all the sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

  
        # draw game over text if condition met
        if self.game_over:
            arcade.draw_text(
                f"Game Over",
                self.player_sprite.center_x + 50,
                self.player_sprite.center_y + 100,
                arcade.color.BLACK,
                width=300,
                multiline=True,
            )

    def on_key_press(self, key, modifiers):
        # Called whenever a key is pressed.
        

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = self.JUMP_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.MOVEMENT_SPEED

        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        # Called when the user presses a mouse button.
        
        
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        #Movement and game logic

        if self.player_sprite.right >= self.end_of_map:
            self.game_over = True

        # Call update on all sprites
        if not self.game_over:
            self.physics_engine.update()

        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coins_hit:
            coin.remove_from_sprite_lists()

        # Pan to the user
        self.pan_camera_to_user(panning_fraction=0.12)

    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        # Manage Scrolling 

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width/2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height/2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)


# Create a Game object
window = MyGame()
# Run the game
arcade.run()