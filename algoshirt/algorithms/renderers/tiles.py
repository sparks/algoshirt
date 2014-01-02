import algoshirt.algorithms.modules as modules
from base import BaseRenderer

class TilesRenderer(BaseRenderer):

	default_params = modules.Tiles.default_params
	
	def __init__(self, params = default_params):
		super(TilesRenderer, self).__init__(params)
	
	def render_to_surface(self, surface):
		tiles = modules.Tiles(self.params)
		tiles_sur = tiles.tiling()

		snf = modules.ScaleAndFit()
		snf.render(tiles_sur, surface)