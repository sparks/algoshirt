import cairo

class BaseModule(object):

    def __init__(self, params):
        self.params = params

    def render(self, input_surfaces, input_shapes, output_surfaces):
        raise NotImplemented("Children must implement render")
