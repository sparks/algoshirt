import cairo
from algoshirt.algorithms import SurfaceBundle

class BaseRenderer(object):

    def __init__(self, params):
        self.params = params

    def render_to_surface(self, surface):
        raise NotImplemented("Children must implement render_to_surface")

    def render_to_svg(self, filename, w, h):
        surf = SurfaceBundle(cairo.SVGSurface(filename, w, h), w, h)
        self.render_to_surface(surf)
        surf.surface.finish()

    def render_to_png(self, filename, w, h):
        surf = SurfaceBundle(cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h), w, h)
        self.render_to_surface(surf)
        surf.surface.write_to_png(filename)
