
import math
import pygame
from pygame import Vector2


class Visualiser:
    def __init__(self, simulation) -> None:
        self.pixels_per_game_unit = 6
        self.car_size = Vector2(1, 2)
        self.screen_size = Vector2(1000, 1000)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 10)
        self.running = True
        self.paused = False
        self.simulation = simulation

    def run(self):
        while self.running:
            if not self.paused: self.simulation.update()
            self.update(self.simulation.cars)

    def update(self, cars):
        self.run_event_loop()
        self.screen.fill((255, 255, 255))
        for car_name, car_list in cars.items():
            for car in car_list:
                self.draw_car(car)
        pygame.display.flip()

    def run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def draw_car(self, car):
        car_size_pixels = self.car_size * self.pixels_per_game_unit 
        car_position_pixels = self.get_screen_position(car.position)
        self.draw_rectangle((car_position_pixels[0], car_position_pixels[1], car_size_pixels[0], car_size_pixels[1]), (0, 0, 0), car.rotation_rads * 180 / math.pi)
        text_surface = self.font.render(str((car.name)), False, (0, 0, 0))
        self.screen.blit(text_surface, self.get_screen_position(car.position))

    def get_screen_position(self, world_position):
        return self.screen_size / 2 + world_position * self.pixels_per_game_unit

    def draw_rectangle(self, rect, color, rotation=0):
        """https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame"""
        (x, y, width, height) = rect
        points = []
        radius = math.sqrt((height / 2)**2 + (width / 2)**2)
        angle = math.atan2(height / 2, width / 2)
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        rot_radians = (math.pi / 180) * -rotation
        for angle in angles:
            y_offset = -1 * radius * math.sin(angle + rot_radians)
            x_offset = radius * math.cos(angle + rot_radians)
            points.append((x + x_offset, y + y_offset))
        pygame.draw.polygon(self.screen, color, points)

