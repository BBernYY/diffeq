from scipy.ndimage import laplace
import numpy as np
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
sw, sh = 800, 800
space = np.zeros((sw, sh))
space_dt = np.zeros((sw, sh))
space_dt_dt = np.zeros((sw, sh))
border_width = 50
amplitude = 100
t = 0
dt = 0.1
dx = dy = 0.5
v = 2
reflect = 0.1
frict = 0.9999
running = True
p = False
solid = np.zeros((800, 800), dtype=bool)
solid[:border_width, :] = True
solid[-border_width:, :] = True
solid[:, :border_width] = True
solid[:, -border_width:] = True
n = 0.85
wave_gen = np.zeros((800, 800), dtype=bool)
def add_disturbance(y, x, radius=5):
    global wave_gen
    y_indices, x_indices = np.ogrid[:800, :800]
    mask = (x_indices - x)**2 + (y_indices - y)**2 <= radius**2
    wave_gen |= mask
def add_goon(y, x, radius=10):
    global solid
    y_indices, x_indices = np.ogrid[:800, :800]
    mask = (x_indices - x)**2 + (y_indices - y)**2 <= radius**2
    solid |= mask
m = (0, 0)
st = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_pressed()[0]:
        add_disturbance(*pygame.mouse.get_pos())
    if pygame.mouse.get_pressed()[2]:
        add_goon(*pygame.mouse.get_pos())
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        space[wave_gen] = np.sin(2*t)*amplitude
    space_dt[solid] *= np.linalg.norm(n)
    space_dt_dt = v**2*laplace(space, mode='constant', cval=0.0)
    space_dt *= frict
    space_dt += space_dt_dt * dt
    space += space_dt * dt
    img = np.clip(space, -127, 127).astype(np.int8)
    rgb = np.zeros((*img.shape, 3), dtype=np.uint8)
    rgb[..., 0] = np.clip(-img, 0, 127) * 2  # negative → red
    rgb[..., 2] = np.clip(img, 0, 127) * 2   # positive → blue
    rgb[solid, :] += np.array([50, 50, 50], dtype=np.uint8)
    rgb[wave_gen, :] += np.array([50, 0, 50], dtype=np.uint8)
    pygame.surfarray.blit_array(screen, rgb)
    pygame.display.flip()
    t += dt