import cairo

class BaseRenderer(object):

    def __init__(self, params):
        self.params = params

    def render_to_surface(self, surface, w, h):
        raise NotImplemented("Children must implement render_to_surface")

    def render_to_svg(self, filename, w, h):
        surf = cairo.SVGSurface(filename, w, h)
        self.render_to_surface(surf, w, h)
        surf.finish()

    def render_to_png(self, filename, w, h):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        self.render_to_surface(surf, w, h)
        surf.write_to_png(filename)
