import pymunk, pymunk.batch
from pymunk.vec2d import Vec2d
import math
import pygame
import numpy as np
import cv2
from tqdm import tqdm

def create_space(bodys_count):
	space = pymunk.Space(threaded=True)
	space.gravity = (0, 981)
	space.threads = 2
	# space.iterations = 5
	space.use_spatial_hash(1.0, bodys_count*10)
	return space

def add_static_lines(space, viw_size=(600, 400)):
	static_lines = [
		pymunk.Segment(space.static_body, ( 0, viw_size[1]), ( viw_size[0], viw_size[1]), 4),  # Piso
		pymunk.Segment(space.static_body, ( 0, 0), ( 0,  viw_size[1]), 4),  # Pared izquierda
		pymunk.Segment(space.static_body, ( viw_size[0], 0), ( viw_size[0],  viw_size[1]), 4)#,  # Pared derecha
		# pymunk.Segment(space.static_body, ( 295, 400-5), (305,  400), 4),  # Obstaculo centro
	]
	for line in static_lines:
		line.friction = 0.8
	space.add(*static_lines)

def load_image(path):
	return pygame.image.load(path)

def create_bodies_and_colors_from_image(space, image, body_size=1, center=(0,0)):
	bodys = []
	colors = []
	count_x = image.get_width()
	count_y = image.get_height()
	for x in range(count_x):
		for y in range(count_y):
			color = image.get_at((x, y))
			if color.a == 0: continue # Saltar pixeles transparentes
			colors.append((color.r, color.g, color.b))
			b = pymunk.Body(4, 1)
			b.position = Vec2d(x*body_size - (body_size * count_x) / 2 + center[0], y*body_size + center[1])
			p = pymunk.Poly.create_box(b, (body_size, body_size))
			p.friction = .4
			p.elasticity = 0.0
			bodys.append(b)
			space.add(b, p)

	return bodys, colors

def get_simulation_data(space, bodys, frames):
	data = pymunk.batch.Buffer()

	simulation_data = np.array([], dtype=np.float64)

	for _ in tqdm(range(frames)):
		pymunk.batch.get_space_bodies(space, pymunk.batch.BodyFields.POSITION, data)
		simulation_data = np.append(simulation_data, np.array(memoryview(data.float_buf()).cast('d'))[:-2])
		data.clear()

		# space.step(1.0/60.)
		for x in range(8):
			space.step(1.0/1024.)

	return np.reshape(simulation_data, (frames, len(bodys), 2))


def create_image_from_frame(frame, colors, width=32, height=32, body_size=1):
	image = np.zeros((height, width, 3), dtype=np.uint8)
	for i in range(len(frame)):
		x, y = frame[i][0], frame[i][1] # Obtenemos la x y la y
		cv2.rectangle(image, (np.int32(x), np.int32(y)), (np.int32(x)+body_size-1, np.int32(y)+body_size-1), colors[i], -1)
		#cv2.circle(image, (np.int32(x), np.int32(y)), 0, colors[i], -1)

	return image

def create_video(data, colors, size, scale=1, fps=60, body_size=1):
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	out = cv2.VideoWriter('physic_video.mp4', fourcc, fps, (size[0]*scale, size[1]*scale))

	for frame in data:
		image = create_image_from_frame(frame, colors, size[0], size[1], body_size)
		image = cv2.resize(image, (size[0]*scale, size[1]*scale), interpolation=cv2.INTER_NEAREST)
		out.write(image)

	out.release()

def main():
	VIW_SIZE = 640, 360
	BODY_SIZE = 2
	image = load_image("img_64x64.png")

	space = create_space(image.get_width() * image.get_height())
	add_static_lines(space, VIW_SIZE)
	bodys, colors = create_bodies_and_colors_from_image(space, image, BODY_SIZE, (VIW_SIZE[0]/2, VIW_SIZE[1]/2))
	
	DURATION = 5  # seconds
	FPS = 60
	FRAMES = DURATION * FPS
	
	simulation_data = get_simulation_data(space, bodys, FRAMES)
	create_video(simulation_data, colors, VIW_SIZE, 2, FPS, BODY_SIZE)

	image_result = create_image_from_frame(simulation_data[110], colors, VIW_SIZE[0], VIW_SIZE[1], BODY_SIZE)

	cv2.imshow("Resultado", image_result)
	cv2.moveWindow("Resultado", 512, 100)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()