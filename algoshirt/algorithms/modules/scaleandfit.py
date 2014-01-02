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

    def __init__(self, params = default_params):
        super(ScaleAndFit, self).__init__(params)

    def render(self, surface_in, surface_out):
        cr = cairo.Context(surface_out.surface)

        corrected_ratio = 1

        if self.params["scale"]["value"] or surface_in.width > surface_out.width or surface_in.height > surface_out.height:
            ar_in = surface_in.width/surface_in.height
            ar_out = surface_out.width/surface_out.height

            if ar_out < ar_in:
                corrected_ratio = float(surface_out.width)/surface_in.width
            else:    
                corrected_ratio = float(surface_out.height)/surface_in.height

        cr.translate(surface_out.width/2-surface_in.width/2*corrected_ratio, surface_out.height/2-surface_in.height/2*corrected_ratio)
        cr.scale(corrected_ratio, corrected_ratio)

        cr.set_source_surface(surface_in.surface, 0, 0)
        cr.paint()
