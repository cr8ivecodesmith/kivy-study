# Character.py

class Character(Widget):
    map_grid = ObjectProperty(None)
    current_tile = Vector(0, 0)
    speed = NumericProperty(0)
    destination = Vector(0, 0)

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.keyboard = Window.request_keyboard(self.on_keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_key_down)

    def update(self, delta):
        self.move()
        #Logger.debug('Test: {}'.format(self.parent.map_grid))

    def move(self):
        """Move to the specified tile coordinates."""
        pass
        #Logger.debug('Position: {}'.format(self.pos))

    def on_touch_down(self, touch):
        Logger.debug('Input: touch')

    def on_key_down(self, keyboard, keycode, text, modifiers):
        value, key_name = keycode
        Logger.debug('Input: {}'.format(key_name))

        if key_name in ['up', 'down', 'left', 'right']:
            new_x = self.current_tile.x
            new_y = self.current_tile.y

            if key_name == 'up':
                new_y -= 1
            elif key_name == 'down':
                new_y += 1
            elif key_name == 'left':
                new_x -= 1
            elif key_name == 'right':
                new_x += 1


            if self.map_grid.valid_move(new_x, new_y):
                self.current_tile.x = new_x
                self.current_tile.y = new_y

                Logger.debug('Character: Moving to {}'.format(self.current_tile))
                coords = self.map_grid.get_tile_position(self.current_tile.x, self.current_tile.y)
                anim = Animation(x=coords[0], y=coords[1])
                anim.start(self)

    def on_keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def set_current_tile(self, x, y):
        self.current_tile.x = x
        self.current_tile.y = y
        self.pos = self.map_grid.get_tile_position(self.current_tile.x, self.current_tile.y)
