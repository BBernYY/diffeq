import numpy as np
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

dt = 0.001
t = 0
k = 3
p = 3
g = 9.81
L = 1
s = np.array([0.0, 4, 0], dtype='f4')
quants = [s]
quants_data = [quants]
while True:
    quants[0][2] = p*k**2/L*np.cos(quants[0][0])*np.sin(k*t) - g/L*np.sin(quants[0][0])
    for i, val in enumerate(quants):
        for der in range(val.shape[0]-2, -1, -1):
            print(der)
            quants[i][der] += quants[i][der+1] * dt
    t += dt
    screen.fill((0,0,0))
    x = L * np.sin(quants[0][0])+p*np.sin(k*t)
    y = -L * np.cos(quants[0][0])
    pygame.draw.circle(screen, (255, 255, 0), (int(x*100 + 400), int(400 - y*100)), 10)

    pygame.draw.circle(screen, (0, 0, 255), (400+int(100*p*np.sin(k*t)), 400), 10)
    pygame.display.flip()
    quants_data.append(quants)
    print(t, quants[0][0])
