# TileGrid.py

class TileGrid(GridLayout):
    """Creates a Kivy grid and puts the tiles in a KivyTiledMap in it."""
    map_file = StringProperty('map.tmx')

    def __init__(self, **kwargs):
        self.map = KivyTiledMap(self.map_file)

        super(TileGrid, self).__init__(
            rows=self.map.height, cols=self.map.width,
            row_force_default=True,
            row_default_height=self.map.tileheight,
            col_force_default=True,
            col_default_width=self.map.tilewidth,
            **kwargs
        )

        tilelayer_index = 0
        for tile in self.map.getTileLayerByName('Ground'):
            texture = self.map.getTileImage(tile[0], tile[1], 0)
            self.add_widget(Image(texture=texture, size=texture.size))
            tilelayer_index += 1

    def get_tile_position(self, x, y):
        # invert the x and y to account for gridlayout's children
        x = self.map.width - x - 1
        y = self.map.height - y - 1

        # calculate the position in the array
        child_index = x + y * self.map.width
        child = self.children[child_index]
        return child.pos

    def valid_move(self, x, y):
        if x < 0 or x > self.map.width - 1 or y < 0 or y > self.map.height - 1:
            Logger.debug('TileGrid: Move {},{} is out of bounds'.format(x, y))
            return False

        if self.map.tile_has_property(x, y, 'Collidable'):
            Logger.debug('TileGrid: Move {},{} collides with something'.format(x, y))
            return False

        return True
