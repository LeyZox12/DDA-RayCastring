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
    normalizedDirectionX = directionX / dirVecDist
    normalizedDirectionY = directionY / dirVecDist
    checkX = int(originX)
    checkY = int(originY)
    distX = ceil(originX) - originX
    distY = ceil(originY) - originY
    wallFound = False
    while not wallFound:
        while distX >= distY:
            distY += ceil(originX + distX) - (originX + distX)
            checkY += 1
            if checkY >= 0 and checkY < len(mapArr) and mapArr[checkY][checkX] == 1:  
                wallFound = True
                dist = sqrt(distX ** 2 + distY ** 2)
                return dist
        while distY > distX:
            distX += ceil(originX + distX) - (originX + distX)
            checkX += 1
            if checkX >= 0 and checkX < len(mapArr) and mapArr[checkY][checkX] == 1:
                wallFound = True
                dist = sqrt(distX ** 2 + distY ** 2)
                return dist
            


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
    screen.fill("white")
    for i in range(len(mapArr)):
        for j in range(len(mapArr[i])):
            pygame.draw.line(screen, "black", (j * ratioSize, 0), (j * ratioSize, 512))
            pygame.draw.line(screen, "black", (0, i * ratioSize), (512, i * ratioSize))
            if mapArr[i][j] == 1:
                pygame.draw.rect(screen, "black", (j * ratioSize, i * ratioSize, ratioSize, ratioSize))        
    pygame.draw.line(screen, "yellow", (x, y), (pygame.mouse.get_pos()))
    dirX, dirY = pygame.mouse.get_pos()[0] - x, pygame.mouse.get_pos()[1] - y
    dist = rayCast(x, y, dirX, dirY, 20, mapArr)
    dirVecDist = sqrt(dirX ** 2 + dirY ** 2)

    dirX = dirX / dirVecDist
    dirY = dirY / dirVecDist
    print(dist)
    pygame.draw.line(screen, "red", (x, y), (x + dist * dirX, y + dist * dirY))
    
    pygame.draw.circle(screen, "black", (x,y), 15) 
    pygame.display.flip()
    clock.tick()