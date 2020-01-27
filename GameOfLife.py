import pygame
import os
import random
import time

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

width = 80
height = 80
scale = 10

fadeolds = False
paused = False

matrix = [[random.randint(0,1) for y in range(height)] for x in range (width)]
age = [[0 for y in range(height)] for x in range (width)]

screen = pygame.display.set_mode((width*scale, height*scale))
clock = pygame.time.Clock()
FPS = 20  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).

image = pygame.Surface((32, 32))
image .fill(WHITE)  

def processFrame(source):
	processedMatrix = [[0 for y in range(height)] for x in range (width)]
	liveNeighbors = 0;
	cellsToCheck = [[-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]]

	for x in range(width):
		for y in range(height):
			liveNeighbors = 0;
			for coordinate in cellsToCheck:
				try:
					if source[x + coordinate[0]][y + coordinate[1]] == 1:
						liveNeighbors += 1
				except:
					liveNeighbors = liveNeighbors
			#print(liveNeighbors)


			if liveNeighbors < 2: #underpopulation
				processedMatrix[x][y] = 0
				age[x][y] = 0

			if source[x][y] == 1 and liveNeighbors > 3: #overpopulation
				processedMatrix[x][y] = 0
				age[x][y] = 0

			if source[x][y] == 1 and liveNeighbors == 2: #stasis
				processedMatrix[x][y] = 1
				age[x][y] += 10
				
			if source[x][y] == 1 and liveNeighbors == 3: #stasis
				processedMatrix[x][y] = 1
				age[x][y] += 10
			
			if source[x][y] == 0 and liveNeighbors == 3: #reproduction
				processedMatrix[x][y] = 1
				age[x][y] = 1

			if age[x][y] > 255:
				age[x][y] = 255

	return processedMatrix

def updateDisplay():
	for x in range(width):
		for y in range(height):
			if matrix[x][y] == 1:
				if fadeolds:
					pygame.draw.rect(screen, (255 - age[x][y],255 - age[x][y],255 - age[x][y]), pygame.Rect(x*scale,y*scale,scale,scale))
				else:
					pygame.draw.rect(screen, WHITE, pygame.Rect(x*scale,y*scale,scale,scale))

	pygame.display.update()  # Or pygame.display.flip()

def drawPixel(mouseX, mouseY):
	mouseX = mouseX // scale
	mouseY = mouseY // scale
	matrix[mouseX][mouseY] = 1
	if paused:
		for x in range(width):
			for y in range(height):
				if matrix[x][y] == 1:
					pygame.draw.rect(screen, WHITE, pygame.Rect(x*scale,y*scale,scale,scale))
		pygame.display.update()

def deletePixel(mouseX, mouseY):
	mouseX = mouseX // scale
	mouseY = mouseY // scale
	matrix[mouseX][mouseY] = 0
	if paused:
		for x in range(width):
			for y in range(height):
				if matrix[x][y] == 0:
					pygame.draw.rect(screen, BLACK, pygame.Rect(x*scale,y*scale,scale,scale))
		pygame.display.update()

print("PyGame Of Life\n------------\nR: Randomize\nC: Clear\nU: Speed up\nD: Slow down\nP: Pause\nClick and drag to draw (works when paused)\n--------------------")

updateDisplay()

while True:
	clock.tick(FPS)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				print("Randomize")
				matrix = [[random.randint(0,1) for y in range(height)] for x in range (width)]
			if event.key == pygame.K_c:
				matrix = [[0 for y in range(height)] for x in range (width)]
				updateDisplay()
				print("Clear")
			if event.key == pygame.K_u:
				FPS += 1
				print("Speed up - " + str(FPS) + "FPS")
			if event.key == pygame.K_d:
				FPS -= 1
				if FPS < 1:
					FPS = 1
				print("Slow down - " + str(FPS) + "FPS")
			if event.key == pygame.K_p:
				paused = not paused
				if paused:
					print("Paused")
				if not paused:
					print("Unpaused")
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				drawPixel(event.pos[0], event.pos[1])
		elif event.type == pygame.MOUSEMOTION:
			if event.buttons[0]:
				drawPixel(event.pos[0], event.pos[1])
			elif event.buttons[2]:
				deletePixel(event.pos[0], event.pos[1]) #get right button to actually kill cells
	

	screen.fill(BLACK)

	if not paused:
		matrix = processFrame(matrix)
		updateDisplay()
