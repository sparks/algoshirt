from base import BaseRenderer
import noise
import cairo
from math import sin, floor, ceil
import numpy as np
from numpy import asarray
from numpy.linalg import norm
from scipy.optimize import brentq, newton, root
from skimage import measure

eps = 0.00001

class HeightFunc(object):
    def z(self, pt):
        return NotImplemented("Children must implement z")

    def grad(self, pt, delta=eps):
        xa = pt[0] - delta
        xb = pt[0] + delta
        
        ya = pt[1] - delta
        yb = pt[1] + delta
        ddx = (self.z([xb,pt[1]]) - self.z([xa,pt[1]])) / (2*delta)
        ddy = (self.z([pt[0],yb]) - self.z([pt[0],ya])) / (2*delta)
        return asarray([ddx, ddy])

class PerlinFunc(HeightFunc):
    def __init__(self, scale=20.0, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0):
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.repeatx = repeatx
        self.repeaty = repeaty
        self.base = base

    def z(self, pt):
        #return noise.pnoise2(pt[0], pt[1], self.octaves, self.persistence, self.lacunarity, self.repeatx, self.repeaty, self.base)
        return noise.pnoise2(pt[0]/self.scale, pt[1]/self.scale)

class SinFunc(HeightFunc):
    def __init__(self, wx = 0.05, wy =0.08):
        self.wx = wx
        self.wy = wy

    def z(self, pt):
        return sin(pt[0]*self.wx) + sin(pt[1]*self.wy)

height_funcs = [PerlinFunc, SinFunc]

class TopoRenderer(BaseRenderer):
    def __init__(self, params):
        super(TopoRenderer, self).__init__(params)
        height_func_key = self.params.get("height_func", 0)
        self.height_func = height_funcs[height_func_key]()
        self.levels = self.params.get("levels", 5)
        self.xsamples = self.params.get("xsamples", 200)
        self.ysamples = self.params.get("ysamples", 200)
        self.alpha = self.params.get("alpha", 0.5)

    def render_to_surface(self, surface, w, h):
        cx = cairo.Context(surface)
        grid = np.zeros((self.xsamples, self.ysamples))
        for x in range(self.xsamples):
            for y in range(self.ysamples):
                grid[x,y] = self.height_func.z([x,y])

        # Now window it to 0
        Xv, Yv = np.meshgrid(np.linspace(0,1,self.xsamples), np.linspace(0,1,self.ysamples))
        #window = 0.5*(1 - np.cos(Xv*2*np.pi)) * 0.5*(1 - np.cos(Yv*2*np.pi))
        window = 0.5*np.cos(np.pi*Xv - np.pi/2)**self.alpha * 0.5*np.cos(np.pi*Yv - np.pi/2)**self.alpha
        grid = grid*window
        gridmin = np.min(grid.flat)
        gridmax = np.max(grid.flat)
        levels = np.linspace(gridmin, gridmax, self.levels+2)
        np.random.seed(0)

        contour_levels = [measure.find_contours(grid, level, positive_orientation="low") for level in levels[1:-1]]
        # Scale everything appropriately
        for contours in contour_levels:
            for contour in contours:
                contour[:,0] = contour[:,0]/self.xsamples*w
                contour[:,1] = contour[:,1]/self.ysamples*h

        for level in range(len(contour_levels)-1):
            col = list(np.random.rand(3,1))
            for contour in contour_levels[level]:
                summed = 0
                cx.move_to(contour[0,0], contour[0,1])
                for i in range(1,contour.shape[0]):
                    #summed += (contour[i,0] - contour[i-1,0])*(contour[i,1] + contour[i-1,1])
                    cx.line_to(contour[i,0], contour[i,1])
                #if (summed < 0):
                    # counter-clockwise. We need to put an outer square
                    #cx.move_to(0,0)
                    #cx.line_to(0,h)
                    #cx.line_to(w,h)
                    #cx.line_to(w,0)
                cx.set_source_rgb(0, 0, 0)
                #cx.stroke_preserve()
            for contour in contour_levels[level+1]:
                cx.move_to(contour[0,0], contour[0,1])
                for i in range(-1, -contour.shape[0], -1):
                    #summed += (contour[i,0] - contour[i-1,0])*(contour[i,1] + contour[i-1,1])
                    cx.line_to(contour[i,0], contour[i,1])

            #cx.stroke()
            cx.set_source_rgb(col[0], col[1], col[2])
            cx.fill()

        for contours in contour_levels:
            for contour in contours:
                cx.move_to(contour[0,0], contour[0,1])
                for i in range(1,contour.shape[0]):
                    #summed += (contour[i,0] - contour[i-1,0])*(contour[i,1] + contour[i-1,1])
                    cx.line_to(contour[i,0], contour[i,1])
        cx.set_source_rgb(0,0,0)
        cx.stroke()


