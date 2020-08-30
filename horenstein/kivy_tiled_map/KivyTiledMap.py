# KivyTiledMap.py

import itertools

from pytmx import TiledMap, TiledTileset

from kivy.core.image import Image


class KivyTiledMap(TiledMap):
    """Loads Kivy images. Make sure that there is an active OpenGL context
    (Kivy Window) before trying to load a map.
    """

    def __init__(self, *args, **kwargs):
        super(KivyTiledMap, self).__init__(*args, **kwargs)

        # call load tile images for each tileset
        for tileset in self.tilesets:
            self.loadTileImages(tileset)

    def loadTileImages(self, ts):
        """Loads the images in filename into Kivy Images.
        :type ts: TiledTileset
        """
        texture = Image(ts.source).texture

        ts.width, ts.height = texture.size

        # initialize the image array
        self.images = [0] * self.maxgid

        p = itertools.product(
            xrange(ts.margin, ts.height, ts.tileheight + ts.margin),
            xrange(ts.margin, ts.width, ts.tilewidth + ts.margin)
        )

        for real_gid, (y, x) in enumerate(p, ts.firstgid):
            if x + ts.tilewidth - ts.spacing > ts.width:
                continue

            gids = self.map_gid(real_gid)

            if gids:
                x = x - ts.spacing
                # convert the y coordinate to opengl (0 at bottom of texture)
                y = ts.height - y - ts.tileheight + ts.spacing

                tile = texture.get_region(x, y, ts.tilewidth, ts.tileheight)

                for gid, flags in gids:
                    self.images[gid] = tile


    def find_tile_with_property(self, property_name, layer_name='Meta'):
        layer = self.getTileLayerByName(layer_name)
        index = self.tilelayers.index(layer)
        for tile in layer:
            try:
                properties = self.getTileProperties((tile[0], tile[1], index))
                if properties.has_key(property_name):
                    return tile[0], tile[1]
            except:
                pass

        return None


    def tile_has_property(self, x, y, property_name, layer_name='Meta'):
        """Check if the tile coordinates passed in represent a collision.
        :return: Boolean representing whether or not there was a collision.
        """
        layer = self.getTileLayerByName(layer_name)
        index = self.tilelayers.index(layer)

        try:
            properties = self.getTileProperties((x, y, index))
            return properties.has_key(property_name)
        except:
            return False
