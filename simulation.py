from car import Car


class Simulation:
    n_angles = 100

    def __init__(self) -> None:
        self.create_cars()
        self.delta_time = 1 / 60

    def create_cars(self):
        angles = []
        for i in range(self.n_angles):
            angles.append((i + 1) / self.n_angles)

        self.cars = {}
        car_list = []
        for angle in angles:
            car = Car()
            car.current_input = angle
            car_list.append(car)
        self.cars["ae86"] = car_list

    def update(self):
        for (name, cars) in self.cars.items():
            for car in cars:
                car.update(self.delta_time)

