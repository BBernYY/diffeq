
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

dt = 0.001
t = 0
GM = 10
quants = []
s = np.array([[0,2], [2,0], [0,0]], dtype='f4')
quants = [s]
quants_data = [quants]
while True:
    quants[0][2] = -GM/(np.linalg.norm(quants[0][0])**3)*quants[0][0]
    for i, val in enumerate(quants):
        for der in range(val.shape[0]-2, -1, -1):
            print(der)
            quants[i][der] += quants[i][der+1] * dt
    t += dt
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255, 255, 0), (int(quants[0][0][0]*100+400), int(quants[0][0][1]*100+400)), 10)
    pygame.draw.circle(screen, (0, 0, 255), (400, 400), 10)
    pygame.display.flip()
    quants_data.append(quants)
    print(t, quants[0][0])
