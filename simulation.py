from car import Car
from car_loader import load_from_csv


class Simulation:
    n_angles = 1

    def __init__(self, cars_file) -> None:
        self.create_cars(cars_file)
        self.delta_time = 1 / 60

    def create_cars(self, cars_file):
        angles = []
        for i in range(self.n_angles):
            angles.append((i + 1) / self.n_angles)

        self.cars = {}

        for base_car in load_from_csv(cars_file):
            car_list = []
            for angle in angles:
                car = base_car.get_copy()
                car.current_input = angle
                car_list.append(car)
            self.cars[car.name] = car_list

    def update(self):
        for (name, cars) in self.cars.items():
            for car in cars:
                car.update(self.delta_time)

