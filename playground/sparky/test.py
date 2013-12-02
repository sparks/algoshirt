import numpy, math
from algoshirt.util import webscrapper
import cairo

def unit_vector(data, axis=None, out=None):
    if out is None:
        data = numpy.array(data, dtype=numpy.float64, copy=True)
        if data.ndim == 1:
            data /= math.sqrt(numpy.dot(data, data))
            return data
    else:
        if out is not data:
            out[:] = numpy.array(data, copy=False)
        data = out
    length = numpy.atleast_1d(numpy.sum(data*data, axis))
    numpy.sqrt(length, length)
    if axis is not None:
        length = numpy.expand_dims(length, axis)
    data /= length
    if out is None:
        return data

def reflection_matrix(point, normal):
    normal = unit_vector(normal[:2])
    M = numpy.identity(3)
    M[:2, :2] -= 2.0 * numpy.outer(normal, normal)
    M[:2, 2] = (2.0 * numpy.dot(point[:2], normal)) * normal
    return cairo.Matrix(M[0,0], M[1,0], M[0,1], M[1,1], M[0,2], M[1,2])

image = webscrapper.rss_to_image_surface()[0]
output = cairo.ImageSurface(cairo.FORMAT_ARGB32, image.get_width(), image.get_height())

cxt = cairo.Context(output)

point = (image.get_width()*0.8, image.get_height()*0.1)
vector = (1, 3)

cxt.set_source_surface(image, 0, 0)
cxt.paint()

cxt.set_matrix(reflection_matrix(point, vector))

cxt.set_source_surface(image, 0, 0)
cxt.paint()

output.write_to_png("test.png")

