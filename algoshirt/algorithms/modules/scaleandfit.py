#!/usr/bin/env python
from base import BaseModule
import cairo

class ScaleAndFit(BaseModule):

	default_params = {
		"scale":
			{
				"value": False,
				"type": "bool",
				"automate": False
			}
	}

	def __init__(self, params):
	    super(ScaleAndFit, self).__init__(params)

    def render(self, input_surfaces, input_shapes, output_surfaces):

    	# output = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image.get_width(), self.image.get_height())

    	# cr = cairo.Context(output)
    	# cr.set_source_surface(self.image, 0, 0)
    	# cr.paint()

    	# ar_shirt = self.w/self.h
    	# ar_design = surface.get_width()/surface.get_height()

    	# corrected_ratio = 1

    	# if ar_shirt < ar_design:
    	# 	corrected_ratio = self.w/surface.get_width()
    	# 	cr.translate(self.x, self.y+(self.h-surface.get_height()*corrected_ratio)/2)
    	# else:
    	# 	corrected_ratio = self.h/surface.get_height()
    	# 	cr.translate(self.x+(self.w-surface.get_width()*corrected_ratio)/2, self.y)

    	# cr.scale(corrected_ratio, corrected_ratio)

    	# cr.set_source_surface(surface, 0, 0)
    	# cr.paint()

    	# return output
