import pygame
from math import pi, cos, sin, sqrt, floor, ceil
running = True
mapArr = [
    [1,1,1,1,1,1],
    [1,0,1,0,0,1],
    [1,0,0,0,0,1],
    [1,0,0,0,0,1],
    [1,0,0,0,0,1],
    [1,1,1,1,1,1]
]
screen = pygame.display.set_mode((512,512))
x, y = 256, 256
speed = 5
clock = pygame.time.Clock()
keyDown = 0
ratioSize = 512 / len(mapArr)
def rayCast(originX, originY, directionX, directionY, maxDist, mapArr):
    dist = 0
    dirVecDist = sqrt(directionX ** 2 + directionY ** 2)
    originX /= ratioSize
    originY /= ratioSize
    normDirX = directionX / dirVecDist
    normDirY = directionY / dirVecDist
    checkX = floor(originX)
    checkY = floor(originY)
    deltaX = (1 / 1e30) if normDirX == 0 else abs(1 / normDirX)
    deltaY = (1 / 1e30) if normDirY == 0 else abs(1 / normDirY)
    side = 0
    if normDirX > 0:
        stepX = 1
        distX = (1.0 - (originX - floor(originX))) * deltaX
    else:
        stepX = -1
        distX = (originX - floor(originX)) * deltaX
    if normDirY > 0:
        distY = (1.0 - (originY - floor(originY))) * deltaY
        stepY = 1
    else:
        distY = (originY - floor(originY)) * deltaY
        stepY = -1
    wallFound = False
    while not wallFound:
        if distX < distY:
            distX += deltaX
            checkX += stepX
            side = 0
            pygame.draw.rect(screen, (255, 255, 100), (checkX * ratioSize, checkY * ratioSize, ratioSize, ratioSize))
            if checkX >= 0 and checkX < len(mapArr) and mapArr[checkY][checkX] == 1:
                wallFound = True
                dist = distX - deltaX
                pygame.draw.rect(screen, (0, 255, 0), (checkX * ratioSize, checkY * ratioSize, ratioSize, ratioSize))
                return dist, side
        else:
            distY += deltaY
            checkY += stepY
            side = 1
            pygame.draw.rect(screen, (255, 255, 100), (checkX * ratioSize, checkY * ratioSize, ratioSize, ratioSize))
            if checkY >= 0 and checkY < len(mapArr) and mapArr[checkY][checkX] == 1:
                wallFound = True
                dist = distY - deltaY
                pygame.draw.rect(screen, (0, 255, 0), (checkX * ratioSize, checkY * ratioSize, ratioSize, ratioSize))
                return dist, side




while running:
    fps = clock.get_fps()
    dt = 1 / 60
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif e.type == pygame.KEYDOWN:
            keyDown = e.key
        elif e.type == pygame.KEYUP and keyDown == e.key:
            keyDown = 0
    if keyDown == 122:
        y -= speed * dt
    elif keyDown == 115:
        y += speed * dt
    elif keyDown == 113:
        x -= speed * dt
    elif keyDown == 100:
        x += speed * dt
    screen.fill((255, 255, 255))
    for i in range(len(mapArr)):
        for j in range(len(mapArr[i])):
            pygame.draw.line(screen, (0, 0, 0), (j * ratioSize, 0), (j * ratioSize, 512))
            pygame.draw.line(screen, (0, 0, 0), (0, i * ratioSize), (512, i * ratioSize))
            if mapArr[i][j] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (j * ratioSize, i * ratioSize, ratioSize, ratioSize))
    pygame.draw.line(screen, (255, 255, 0), (x, y), (pygame.mouse.get_pos()))
    dirX, dirY = pygame.mouse.get_pos()[0] - x, pygame.mouse.get_pos()[1] - y
    dist, side = rayCast(x, y, dirX, dirY, 20, mapArr)
    dirVecDist = sqrt(dirX ** 2 + dirY ** 2)
    dirX = dirX / dirVecDist
    dirY = dirY / dirVecDist
    pygame.draw.line(screen, (255, 0, 0), (x, y), (x + dist * dirX * ratioSize, y + dist * dirY * ratioSize))
    pygame.draw.circle(screen, (0, 0, 0), (int(x),int(y)), 15)
    pygame.draw.circle(screen, (255, 0, 0), (x + dist * dirX * ratioSize, y + dist * dirY * ratioSize), 5)
    pygame.display.flip()
    clock.tick()