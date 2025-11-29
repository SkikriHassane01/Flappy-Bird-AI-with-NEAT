from pygame import transform, image
from os import path
BIRD_IMGS = [transform.scale2x(image.load(path.join("imgs", "bird1.png"))),
             transform.scale2x(image.load(path.join("imgs", "bird2.png"))),
             transform.scale2x(image.load(path.join("imgs", "bird3.png")))]
PIPE_IMG = transform.scale2x(image.load(path.join("imgs", "pipe.png")))
BG_IMG = transform.scale2x(image.load(path.join("imgs", "bg.png")))
BASE_IMG = transform.scale2x(image.load(path.join("imgs", "base.png")))