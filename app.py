import pymunk, pymunk.batch
from pymunk.vec2d import Vec2d
import math
import pygame
import numpy as np
import cv2
from tqdm import tqdm

def create_space():
	space = pymunk.Space(threaded=False)
	space.gravity = (0, 981)
	space.threads = 1
	return space

def add_static_lines(space):
	static_lines = [
		pymunk.Segment(space.static_body, ( 0, 400), ( 600, 400), 4),  # Piso
		pymunk.Segment(space.static_body, ( 0, 0), ( 0,  400), 4),  # Pared izquierda
		pymunk.Segment(space.static_body, ( 600, 0), ( 600,  400), 4),  # Pared derecha
		pymunk.Segment(space.static_body, ( 295, 400-5), (305,  400), 4),  # Obstaculo centro
	]
	for line in static_lines:
		line.friction = 0.8
	space.add(*static_lines)

def load_image(path):
	return pygame.image.load(path)

def create_bodies_from_image(space, image, radio=4):
	bodys = []
	count_x = image.get_width()
	count_y = image.get_height()
	for x in range(count_x):
		for y in range(count_y):
			if image.get_at((x, y)).a == 0: continue
			b = pymunk.Body(4, 1)
			b.position = Vec2d(x*radio*2 - (radio*2 * count_x) / 2 + 300, y*radio*2)
			b.color = image.get_at((x, y))
			p = pymunk.Poly.create_box(b, (radio*2, radio*2))
			p.friction = .4
			p.elasticity = 0.0
			bodys.append(b)
			space.add(b, p)
	return bodys, radio

def get_simulation_data(space, bodys, radio, frames):

	# pygame.init()
	# screen = pygame.display.set_mode((600, 400))

	data = pymunk.batch.Buffer()

	simulation_data = np.array([], dtype=np.float64)

	for _ in tqdm(range(frames)):
		# screen.fill((255, 255, 255))

		# for body in bodys:
		# 	pix = pygame.Surface((radio*2+1, radio*2+1), pygame.SRCALPHA)
		# 	pix.fill(body.color)
		# 	# Convierte radianes a grados y rota en sentido horario
		# 	pix = pygame.transform.rotate(pix, -math.degrees(body.angle))
		# 	# Ajusta la posición al centro de la ventana
		# 	pos = (int(body.position.x + 300 - pix.get_width() // 2),
		# 		int(200 + body.position.y - pix.get_height() // 2))
		# 	screen.blit(pix, pos)
		
		# pygame.display.flip()

		pymunk.batch.get_space_bodies(space, pymunk.batch.BodyFields.POSITION, data)
		simulation_data = np.append(simulation_data, np.array(memoryview(data.float_buf()).cast('d'))[:-2])
		data.clear()

		# space.step(1.0/60.)
		for x in range(8):
			space.step(1.0/1024.)

	return np.reshape(simulation_data, (frames, len(bodys), 2))


def create_image_from_data_frame(frame, width=32, height=32):
	image = np.zeros((height, width, 3), dtype=np.uint8)
	for coord in frame:
		x, y = coord[0], coord[1] # Obtenemos la x y la y
		cv2.circle(image, (np.int32(x), np.int32(y)), 1, (255, 255, 255), -1)

	return image

def main():
	space = create_space()
	add_static_lines(space)
	image = load_image("img.png")
	bodys, radio = create_bodies_from_image(space, image, 2)
	
	DURATION = 5  # seconds
	FPS = 60
	FRAMES = DURATION * FPS
	
	simulation_data = get_simulation_data(space, bodys, radio, FRAMES)

	image_result = create_image_from_data_frame(simulation_data[110], 600, 400)

	cv2.imshow("Resultado", image_result)
	cv2.moveWindow("Resultado", 512, 100)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()