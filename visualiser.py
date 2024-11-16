
import math
import random
import pygame
from pygame import Vector2


class Visualiser:
    def __init__(self, simulation) -> None:
        self.pixels_per_game_unit = 6
        self.car_size = Vector2(1, 2)
        self.screen_size = Vector2(1000, 1000)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.font.init()
        self.font = pygame.font.SysFont('Courier New', 15, bold=True)
        self.running = True
        self.paused = False
        self.is_background_light = True
        self.simulation = simulation
        self.updates_per_render = 10

        self.colors = []
        for i in range(100):
            self.colors.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))


    def run(self):
        while self.running:
            if not self.paused:
                for i in range(self.updates_per_render):
                    self.simulation.update()
            self.update()
        self.print_scores()


    def update(self):
        self.run_event_loop()
        self.screen.fill((255, 255, 255) if self.is_background_light else (0, 0, 0))
        i = 0
        for car_name, car_list in self.simulation.cars.items():
            for car in car_list:
                self.draw_car(car, self.colors[i])
            i += 1
        self.draw_legend()
        pygame.display.flip()


    def draw_legend(self):
        i = 0
        scores = self.simulation.get_car_scores_sum()
        car_names = list(self.simulation.cars.keys())
        car_names.sort(key = lambda car_name: -scores[car_name])
        for car_name in car_names:
            text_surface = self.font.render(car_name.rjust(32, " ") + ": " + str(round(scores[car_name])), False, self.colors[i])
            self.screen.blit(text_surface, (0, 12 * i))
            i += 1


    def run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_f:
                    self.is_background_light = not self.is_background_light
                if event.key == pygame.K_s:
                    print()
                    self.print_scores()


    def print_scores(self):
        print("car_name, score_sum")
        for car_name, score in self.simulation.get_car_scores_sum().items():
            print(car_name + ", " + str(round(score)))
        

    def draw_car(self, car, color):
        car_size_pixels = self.car_size * self.pixels_per_game_unit 
        car_position_pixels = self.get_screen_position(car.position)
        self.draw_rectangle((car_position_pixels[0], car_position_pixels[1], car_size_pixels[0], car_size_pixels[1]), color, car.rotation_rads * 180 / math.pi)


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

