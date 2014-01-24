import algoshirt.algorithms.modules as modules
from algoshirt.algorithms import SurfaceBundle
from base import BaseRenderer

class TilesRenderer(BaseRenderer):

    default_params = modules.Tiles.default_params
    
    def __init__(self, params = default_params):
        super(TilesRenderer, self).__init__(params)
    
    def render_to_surface(self, surface):
        tiles = modules.Tiles(self.params)
        print self.params
        tiles_sur = tiles.tiling()
        tiles_surB = SurfaceBundle(tiles_sur, tiles_sur.get_width(), tiles_sur.get_height())
        
        tiles_sur.write_to_png("./test.png")
        
        snf = modules.ScaleAndFit()
        snf.render(tiles_surB, surface)