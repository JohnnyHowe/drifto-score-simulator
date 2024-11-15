import math
import pygame
from pygame import Vector2
from car import Car

SCREEN_SIZE = Vector2(500, 500)
PIXELS_PER_GAME_UNIT = 10
CAR_SIZE = Vector2(1, 2)


def main():
    car = Car()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    car = Car()

        screen.fill((255, 255, 255))
        delta_time = clock.tick() / 1000
        if paused: delta_time = 0

        car_size_pixels = (CAR_SIZE[0] * PIXELS_PER_GAME_UNIT, CAR_SIZE[1] * PIXELS_PER_GAME_UNIT)
        car_position_pixels = get_screen_position(car.position)
        draw_rectangle(screen, (car_position_pixels[0], car_position_pixels[1], car_size_pixels[0], car_size_pixels[1]), (0, 0, 0), car.rotation_rads * 180 / math.pi)
        car.update(delta_time)

        car.current_input = 0
        if pygame.key.get_pressed()[pygame.K_a]: car.current_input -= 1
        if pygame.key.get_pressed()[pygame.K_d]: car.current_input += 1

        pygame.display.flip()


def get_screen_position(world_position):
    return SCREEN_SIZE / 2 + world_position * PIXELS_PER_GAME_UNIT


def draw_ray(screen, position, ray_dir, color=(0, 0, 0)):
    pygame.draw.line(screen, color, position, position + ray_dir)


def draw_rectangle(screen, rect, color, rotation=0):
    """Draw a rectangle, centered at x, y.
    https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    (x, y, width, height) = rect
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * -rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)


if __name__ == "__main__":
    main()
