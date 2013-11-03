from algoshirt.algorithms import TopoRenderer
import cairo

t = TopoRenderer({})

t.render_to_png("test.png", 600, 600)
t.render_to_svg("test.svg", 600, 600)
