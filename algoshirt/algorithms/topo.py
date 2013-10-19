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
    def __init__(self, scale=50.0, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0):
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
    def __init__(self, wx = 0.025, wy =0.02):
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
        self.levels = self.params.get("levels", 10)
        self.xsamples = self.params.get("xsamples", 200)
        self.ysamples = self.params.get("ysamples", 200)


    def iso_points(self, ptstart, alpha=1.0, looptol=0.1, minsteps = 10, maxsteps = 100):
        points = []
        pt = ptstart
        z = self.height_func.z(pt)
        for step_i in xrange(maxsteps):
            print("pt: ({},{})".format(pt[0], pt[1]))
            grad = self.height_func.grad(pt)
            tangent = asarray([-grad[1], grad[0]])
            step = alpha if step_i < minsteps else min(alpha, norm(ptstart-pt))
            ptstep = pt + tangent*alpha

            pt = root(lambda p: self.height_func.z(p)-z, ptstep)
            if step_i > minsteps and norm(pt - pstart) < looptol:
                break
            points.append(pt)
        return points
        
    def render_to_surface(self, surface, w, h):
        cx = cairo.Context(surface)
        grid = np.zeros((self.xsamples, self.ysamples))
        for x in range(self.xsamples):
            for y in range(self.ysamples):
                grid[x,y] = self.height_func.z([x,y])
        gridmin = np.min(grid.flat)
        gridmax = np.max(grid.flat)
        grid[0,:] = gridmin-10
        grid[-1,:] = gridmin-10
        grid[:,0] = gridmin-10
        grid[:,-1] = gridmin-10
        levels = np.linspace(gridmin, gridmax, self.levels)
        def which_wall(pt):
            ''' Tells you which wall a point falls on. 0 is the right wall.
            the rest go anti-clockwise'''
            if pt[0] >= w-w/self.xsamples:
                return 0
            elif pt[1] <= h/self.ysamples:
                return 1
            elif pt[0] <= w/self.xsamples:
                return 2
            elif pt[1] >= h - h/self.ysamples:
                return 3
            else:
                return -1
        wall_corners = [[1,0], [0,0], [0,1], [1,1]]

        for level in levels[1:-1]:
            col = list(np.random.rand(3,1))
            contours = measure.find_contours(grid, level)
            for contour in contours:
                contour[:,0] = contour[:,0]/self.xsamples*w
                contour[:,1] = contour[:,1]/self.ysamples*h
                cx.move_to(contour[0,0], contour[0,1])
                for i in range(contour.shape[0]):
                    cx.line_to(contour[i,0], contour[i,1])
                '''
                if norm(contour[-1,:] - contour[1,:]) > 0.1:
                    # This ends at a wall. Need to do fancy
                    # path closing
                    # need to go in anti-clockwise order
                    from_wall = which_wall(contour[-1,:])
                    to_wall = which_wall(contour[0,:])
                    if from_wall >= 0 and to_wall >= 0:
                        print "=====", from_wall, to_wall
                        wall = from_wall
                        while wall != to_wall:
                            print wall
                            print wall_corners[wall]
                            cx.line_to(*(asarray(wall_corners[wall]) * [w, h]))
                            wall = (wall+1) % 4
                '''
                cx.set_source_rgb(0, 0, 0)
                cx.stroke_preserve()
                #cx.stroke()
                cx.set_source_rgb(col[0], col[1], col[2])
                cx.fill()

