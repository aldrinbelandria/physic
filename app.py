import pymunk, pymunk.batch
from pymunk.vec2d import Vec2d
import math
import pygame


space = pymunk.Space(threaded=True)
space.gravity = (0, 981)
space.threads = 1

# Piso y paredes
static_lines = [
    pymunk.Segment(space.static_body, ( -250, 150), ( 250, 150), 4),  # Piso
    pymunk.Segment(space.static_body, ( -250, -150), (-250,  150), 4),  # Pared izquierda
    pymunk.Segment(space.static_body, (  250, -150), ( 250,  150), 4),  # Pared derecha
    pymunk.Segment(space.static_body, (    -5, 145), (   5,  150), 4),  # Obstaculo centro
]
for line in static_lines:
    line.friction = 0.8
space.add(*static_lines)

image = pygame.image.load("Phone.png")

bodys = []

count_x = image.get_width()
count_y = image.get_height()
radio = 4
for x in range(count_x):
	for y in range(count_y):
		if image.get_at((x, y)).a == 0: continue
		
		b = pymunk.Body(1, 1)
		b.position = Vec2d(x*radio*2 - ((count_x * (radio*2)) / 2), y*radio*2 - 200)
		b.color = image.get_at((x, y))

		p = pymunk.Poly.create_box(b, (radio*2, radio*2))
		p.friction = .4
		p.elasticity = 0.0
		bodys.append(b)
		space.add(b, p)

data = pymunk.batch.Buffer()

DURATION = 3  # seconds
FPS = 60
FRAMES = DURATION * FPS

# import time

# time_start = time.time()
# for _ in range(FRAMES):
# 	for x in range(16):
# 		space.step(1/1024.0)
# 	print(_, time.time() - time_start)

# time_end = time.time()

# print("Time per step:", (time_end - time_start))


def run_pygame(space):
	import pygame
	import pymunk.pygame_util

	pygame.init()
	screen = pygame.display.set_mode((600, 400))
	# clock = pygame.time.Clock()
	# draw_options = pymunk.pygame_util.DrawOptions(screen)
	# draw_options.transform = pymunk.Transform.translation(x=300, y=200)
	
	running = True
	for _ in range(FRAMES):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((255, 255, 255))
		# space.debug_draw(draw_options)
		for body in bodys:
			pix = pygame.Surface((radio*2+1, radio*2+1), pygame.SRCALPHA)
			pix.fill(body.color)
			# Convierte radianes a grados y rota en sentido horario
			pix = pygame.transform.rotate(pix, -math.degrees(body.angle))
			# Ajusta la posición al centro de la ventana
			pos = (int(body.position.x + 300 - pix.get_width() // 2),
				int(200 + body.position.y - pix.get_height() // 2))
			screen.blit(pix, pos)
		
		pygame.display.flip()
		# clock.tick(60)
		for x in range(4):
			space.step(1.0/256.)

	pygame.quit()


def run_pygame_simple(space):
	import pygame
	import pymunk.pygame_util

	pygame.init()
	screen = pygame.display.set_mode((600, 400))
	draw_options = pymunk.pygame_util.DrawOptions(screen)
	draw_options.transform = pymunk.Transform.translation(x=300, y=200)

	running = True
	for _ in range(FRAMES):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill((255, 255, 255))
		space.debug_draw(draw_options)
		pygame.display.flip()
		for x in range(8):
			space.step(1.0/512.0)

	pygame.quit()


run_pygame(space)