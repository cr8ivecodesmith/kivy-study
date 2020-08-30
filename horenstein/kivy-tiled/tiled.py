import os
import itertools
import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

import pytmx


class KivyTiledMap(pytmx.TiledMap):
    """
    Loads Kivy images. Make sure that there is an active OpenGL context
    (Kivy Window) before trying to load a map.
    """

    def __init__(self, map_file_path=None, *args, **kwargs):
        assert map_file_path, 'No map file provided, please provide the path to a .tmx file.'
        super(KivyTiledMap, self).__init__(map_file_path, *args, **kwargs)

        # pull out the directory containing the map file path
        self.map_dir = os.path.dirname(map_file_path)
        Logger.debug('KivyTiledMap: directory containing map file: "{}"'.format(self.map_dir))

        # call load tile images for each tileset
        for tileset in self.tilesets:
            self.loadTileImages(tileset)

    def loadTileImages(self, ts):
        """
        Loads the images in filename into Kivy Images.
        This is a port of the code here: https://github.com/bitcraft/PyTMX/blob/master/pytmx/tmxloader.py

        :type ts: pytmx.TiledTileset
        """
        tile_image_path = self.map_dir + '/' + ts.source
        Logger.debug('KivyTiledMap: loading tile image at {}'.format(tile_image_path))
        texture = CoreImage(tile_image_path).texture

        ts.width, ts.height = texture.size
        tilewidth = ts.tilewidth + ts.spacing
        tileheight = ts.tileheight + ts.spacing
        Logger.debug('KivyTiledMap: TiledTileSet: {}x{} with {}x{} tiles'.format(ts.width, ts.height, tilewidth, tileheight))

        # some tileset images may be slightly larger than the tile area
        # ie: may include a banner, copyright, ect.  this compensates for that
        width = int((((ts.width - ts.margin * 2 + ts.spacing) / tilewidth) * tilewidth) - ts.spacing)
        height = int((((ts.height - ts.margin * 2 + ts.spacing) / tileheight) * tileheight) - ts.spacing)
        Logger.debug('KivyTiledMap: TiledTileSet: true size: {}x{}'.format(width, height))

        # initialize the image array
        Logger.debug('KivyTiledMap: initializing image array')
        self.images = [0] * self.maxgid

        p = itertools.product(
            xrange(ts.margin, height + ts.margin, tileheight),
            xrange(ts.margin, width + ts.margin, tilewidth)
        )

        # trim off any pixels on the right side that isn't a tile
        # this happens if extra graphics are included on the left, but they are not actually part of the tileset
        width -= (ts.width - ts.margin) % tilewidth

        for real_gid, (y, x) in enumerate(p, ts.firstgid):
            if x + ts.tilewidth - ts.spacing > width:
                continue

            gids = self.map_gid(real_gid)

            if gids:
                # invert y for OpenGL coordinates
                y = ts.height - y - ts.tileheight

                tile = texture.get_region(x, y, ts.tilewidth, ts.tileheight)

                for gid, flags in gids:
                    self.images[gid] = tile

    def find_tile_with_property(self, property_name, layer_name='Meta'):
        layer = self.get_layer_by_name(layer_name)
        index = self.layers.index(layer)
        for tile in layer:
            properties = self.get_tile_properties(tile[0], tile[1], index)
            if properties and property_name in properties:
                return tile[0], tile[1]

        return None

    def find_tiles_with_property(self, property_name, layer_name='Meta'):
        tiles = []
        layer = self.get_layer_by_name(layer_name)
        index = self.layers.index(layer)
        for tile in layer:
            properties = self.get_tile_properties(tile[0], tile[1], index)
            if properties and property_name in properties:
                tiles.append((tile[0], tile[1]))

        return tiles

    def tile_has_property(self, x, y, property_name, layer_name='Meta'):
        """Check if the tile coordinates passed in represent a collision.
        :return: Boolean representing whether or not there was a collision.
        :rtype: bool
        """
        layer = self.get_layer_by_name(layer_name)
        layer_index = self.layers.index(layer)

        properties = self.get_tile_properties(x, y, layer_index)

        # if there are properties to look at, check whether the name is in them
        return property_name in properties if properties else False

    def valid_move(self, x, y, debug=False):
        # check if the tile is out of bounds
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            if debug:
                Logger.debug('KivyTiledMap: Move {},{} is out of bounds'.format(x, y))
            return False

        # check if the tile has the property 'Collidable'
        if self.tile_has_property(x, y, 'Collidable'):
            if debug:
                Logger.debug('KivyTiledMap: Move {},{} collides with map object'.format(x, y))
            return False

        return True

    def get_adjacent_tiles(self, x, y):
        """Get the tiles surrounding the north, south, east and west of x,y.
        :return: A list of coordinate tuples adjacent to x,y.
        :rtype: list
        """
        adjacent_tiles = []

        # try each direction and add to the list if they are valid_moves
        # up
        if self.valid_move(x, y - 1):
            adjacent_tiles.append((x, y - 1))

        # down
        if self.valid_move(x, y + 1):
            adjacent_tiles.append((x, y + 1))

        # left
        if self.valid_move(x - 1, y):
            adjacent_tiles.append((x - 1, y))

        # right
        if self.valid_move(x + 1, y):
            adjacent_tiles.append((x + 1, y))

        return adjacent_tiles


class TileMap(Widget):
    """Creates a Kivy grid and puts the tiles in a KivyTiledMap in it."""
    scaled_tile_size = ListProperty()

    def __init__(self, map_file_path=None, **kwargs):
        assert map_file_path, 'No map file path provided to TileMap. Please pass in a path to a .tmx file.q'
        self.tiled_map = KivyTiledMap(map_file_path)
        super(TileMap, self).__init__(**kwargs)

        self._scale = 1.0
        self.tile_map_size = (self.tiled_map.width, self.tiled_map.height)
        self.tile_size = (self.tiled_map.tilewidth, self.tiled_map.tileheight)
        self.scaled_tile_size = self.tile_size
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.scaled_tile_size = (self.tile_size[0] * self.scale, self.tile_size[1] * self.scale)
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]
        self.on_size()

    def on_size(self, *args):
        Logger.debug('TileMap: Re-drawing')

        screen_tile_size = self.get_root_window().width / 8
        self.scaled_tile_size = (screen_tile_size, screen_tile_size)
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]

        self.canvas.clear()
        with self.canvas:
            layer_idx = 0
            for layer in self.tiled_map.layers:
                if not layer.visible:
                    continue  # skip the layer if it's not visible

                # set up the opacity of the tiled layer
                Color(1.0, 1.0, 1.0, layer.opacity)

                # iterate through the tiles in the layer
                for tile in layer:
                    tile_x = tile[0]
                    tile_y = tile[1]
                    try:
                        texture = self.tiled_map.get_tile_image(tile_x, tile_y, layer_idx)
                    except AttributeError:
                        continue  # keep going if the texture is empty

                    # calculate the drawing parameters of the tile
                    draw_pos = self._get_tile_pos(tile_x, tile_y)
                    draw_size = self.scaled_tile_size

                    # create a rectangle instruction for the gpu
                    Rectangle(texture=texture, pos=draw_pos, size=draw_size)
                layer_idx += 1

    def _get_tile_pos(self, x, y):
        """Get the tile position relative to the widget."""
        pos_x = x * self.scaled_tile_size[0]
        pos_y = (self.tile_map_size[1] - y - 1) * self.scaled_tile_size[1]
        return pos_x, pos_y

    def get_tile_position(self, x, y):
        """Get the tile position according to the window."""
        return self._get_tile_pos(x, y)

    def get_tile_at_position(self, pos):
        """Find out the tile coordinates of the position.
        :param pos: The screen position to get the tile of.
        :type pos: (float, float)
        :return: The tile position.
        :rtype: (int, int) | None
        """
        # convert the pos to local coords
        pos = self.to_local(*pos)
        Logger.debug('TileMap: Finding tile at position {}'.format(pos))

        found_x = False
        tile_x = 0
        while tile_x < self.tiled_map.width:
            tile_x_right = (tile_x + 1) * self.scaled_tile_size[0]
            if tile_x_right < pos[0]:
                tile_x += 1
            else:
                found_x = True
                break

        # start at the bottom of the map, same as kivy coords
        tile_y = self.tiled_map.height
        while tile_y != 0:
            # calculate how far up from the bottom of the widget the tile is
            tile_y_top = (self.tiled_map.height - tile_y) * self.scaled_tile_size[1]
            if tile_y_top < pos[1]:
                tile_y -= 1
            else:
                if found_x:
                    return tile_x, tile_y
                break

        return None


class TileMovement(Widget):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    initialized = BooleanProperty()
    moving = BooleanProperty(False)
    path = ListProperty()  # list of nodes to the destination tile

    def __init__(self, tile_map, **kwargs):
        super(TileMovement, self).__init__(**kwargs)

        # hold on to the tile map
        self.tile_map = tile_map

        # TODO: figure out why this as a class variable shares across instances
        self.current_tile = Vector(0, 0)
        self.destination_tile = Vector(0, 0)
        self.direction = 'down'  # the last direction that was moved in

        # necessary to deal with Kivy's non-instant initialization of properties
        self.initialized = False

        # dispatched when movements are complete
        self.register_event_type('on_complete')

        # debugging via rectangle drawing
        self._debug = False

    def on_complete(self):
        pass

    def on_animation_complete(self):
        # mark the moving variable in case anyone is watching
        self.moving = False

        # check if we're at the destination tile
        if self.path:
            # keep moving, not at the destination yet
            self._move_to_tile()
        elif self.current_tile == self.destination_tile:
            Logger.debug('TileMovement: Move complete')
            self.dispatch('on_complete')

    def move(self, direction):
        """
        Move up, down, left or right.

        :param direction: The direction to move in.
        :type direction: str
        :rtype: bool
        """
        Logger.debug('TileMovement: move({})'.format(direction))
        self.direction = direction
        new_x, new_y = self.get_tile_in_direction(self.direction)

        # move the destination tile to keep coherence
        if self.destination_tile == self.current_tile:
            self.destination_tile.x = new_x
            self.destination_tile.y = new_y

        self.current_tile.x = new_x
        self.current_tile.y = new_y

        coordinates = self.tile_map.get_tile_position(self.current_tile.x, self.current_tile.y)
        Logger.debug('TileMovement: Moving to {} at {}'.format(self.current_tile, coordinates))

        # mark moving variable in case anyone is watching it
        self.moving = True

        animation = Animation(pos=coordinates, duration=0.5)
        animation.bind(on_complete=lambda *args: self.on_animation_complete())
        animation.start(self)

    def _move_to_tile(self):
        if not self.path:
            self.move_to_tile(self.destination_tile)
            return

        next_tile_x, next_tile_y = self.path[0]
        # this inherently moves up/down before left/right
        x_differential = next_tile_x - self.current_tile.x
        y_differential = next_tile_y - self.current_tile.y

        move_succeeded = False
        if y_differential < 0 and not move_succeeded:
            move_succeeded = self.move(self.UP)
        if y_differential > 0 and not move_succeeded:
            move_succeeded = self.move(self.DOWN)
        if x_differential < 0 and not move_succeeded:
            move_succeeded = self.move(self.LEFT)
        if x_differential > 0 and not move_succeeded:
            move_succeeded = self.move(self.RIGHT)

        if not move_succeeded:
            Logger.debug('TileMovement: Move failed, finding a different path')
            self.path = []
            Clock.schedule_once(lambda *args: self._move_to_tile(), 1)
            return False
        else:
            self.path.pop(0)

    def move_to_tile(self, tile, retry=False):
        """Move to the specified tile, if possible.
        :param retry: Whether or not to keep attempting the move every second.
        :type retry: bool
        :return: Whether or not the move is possible.
        :rtype: bool
        """
        if self.current_tile.x == tile[0] and self.current_tile.y == tile[1]:
            Logger.debug('TileMovement: Move to current tile requested, bailing')
            return

        self.destination_tile.x = tile[0]
        self.destination_tile.y = tile[1]

        def move_to_tile(*args):
            self.move_to_tile(self.destination_tile)

        # find a path
        self.path = find_path(self.tile_map, self.current_tile.x, self.current_tile.y, tile[0], tile[1])

        if not self.path:
            Logger.debug('TileMovement: Move failed, no path')
            if retry:
                Logger.debug('TileMovement: Trying to move again in a second')
                Clock.schedule_once(move_to_tile, 1)
            return False

        # pop the first tile in the path, which is the current one
        if not self.moving:
            self.moving = True
            self.path.pop(0)
            self._move_to_tile()

    def get_tile_in_direction(self, direction):
        """Find out what the coordinates of the tile are in the specified
        direction.
        """
        tile_x = self.current_tile.x
        tile_y = self.current_tile.y

        if direction == self.UP:
            tile_y -= 1
        elif direction == self.DOWN:
            tile_y += 1
        elif direction == self.LEFT:
            tile_x -= 1
        elif direction == self.RIGHT:
            tile_x += 1

        return tile_x, tile_y

    def get_tile_in_current_direction(self):
        """Get the tile in the direction this component is facing.
        :return: tile coordinates
        :rtype: (int, int)
        """
        return self.get_tile_in_direction(self.direction)

    def set_current_tile(self, x, y):
        self.current_tile.x = x
        self.current_tile.y = y
        self.destination_tile.x = self.current_tile.x
        self.destination_tile.y = self.current_tile.y

        new_pos = self.tile_map.get_tile_position(self.current_tile.x, self.current_tile.y)
        Logger.debug('TileMovement: Setting current tile to {}'.format(new_pos))
        self.pos = new_pos

    def debug(self):
        self._debug = True

    def on_pos(self, *args):
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)


class TiledNode(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None
        self.previous = None

    def __eq__(self, other):
        """Compare based on x and y."""
        if other is None:
            return False

        if self.x == other.x:
            if self.y == other.y:
                return True

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<TiledNode: {},{}>'.format(self.x, self.y)

    def __hash__(self):
        return hash(self.__repr__())


def build_path(node):
    """
    :param node: The node at the end of a path.
    :type node: TiledNode
    :return: A list of coordinate tuples.
    :rtype: list
    """
    path = []
    while node is not None:
        path.insert(0, (node.x, node.y))
        node = node.previous
    return path


def find_path(tiled_map, start_x, start_y, dest_x, dest_y):
    """Find a path from the start position to the destination.
    :param tiled_map: The tile map to find a path in.
    :type tiled_map: TiledMap
    :return: List of tiles in the path found.
    :rtype: list
    """

    start_node = TiledNode(start_x, start_y)
    end_node = TiledNode(dest_x, dest_y)

    reachable = set([start_node])
    explored = set()

    while reachable:  # while reachable is not empty
        # choose some node we know how to reach
        # casting to list to be able to
        node = random.sample(reachable, 1)[0]

        # if the node is the end node, build and return the path
        if node == end_node:
            return build_path(node)

        # don't repeat ourselves
        reachable.remove(node)
        explored.add(node)

        # find out possible moves from this point
        adjacent_tiles = set([TiledNode(*tile) for tile in tiled_map.get_adjacent_tiles(node.x, node.y)])
        new_reachable = adjacent_tiles - explored
        for adjacent in new_reachable:
            if adjacent not in reachable:
                adjacent.previous = node  # remember how we got there
                reachable.add(adjacent)

    # if we got here no path was found
    return []


if __name__ == '__main__':
    from kivy.app import App
    from kivy.config import Config
    from kivy.uix.scatterlayout import ScatterLayout

    class TiledApp(App):

        def build(self):
            main_widget = ScatterLayout()
            map_file_path = 'test/assets/testmap.tmx'

            def add_widgets():
                Logger.debug('TiledApp: creating tile map using map file: {}'.format(map_file_path))
                tile_map = TileMap(map_file_path)

                Logger.debug('TiledApp: adding tile map to main widget')
                main_widget.add_widget(tile_map)

                Logger.debug('TiledApp: creating TileMovement widget')
                tile_movement = TileMovement(tile_map)
                tile_movement.debug()
                tile_movement.size_hint = 0.1, 0.1
                #main_widget.add_widget(tile_movement)

                def move_demo():
                    direction = tile_movement.RIGHT
                    Logger.debug('move_demo: moving {}'.format(direction))
                    tile_movement.move(direction)

                #Clock.schedule_interval(lambda *args: move_demo(), 2)

            Clock.schedule_once(lambda *args: add_widgets())
            return main_widget

    Config.set('kivy', 'log_level', 'debug')

    # print out the version of pytmx
    Logger.debug('TiledApp: pytmx version: {}'.format(pytmx.__version__))

    TiledApp().run()
