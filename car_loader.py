import csv
from car import Car


def load_from_csv(filename):
    """ Get a list of the cars with stats set from the file """
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        header = rows[0]
        content = rows[1:]

        stat_indices = {}
        for i in range(len(header)):
            if header[i].strip() == "":
                continue
            stat_indices[header[i].lower().strip()] = i

        cars = []
        for car_row in content:
            car = Car()
            cars.append(car)
            car.name = car_row[stat_indices["name"]]
            car.steering_speed = float(car_row[stat_indices["maxsteeringspeed"]])
            car.constant_friction = float(car_row[stat_indices["constantfriction"]])
            car.linear_friction = float(car_row[stat_indices["frictionwithlinearslipangle"]])
            car.squared_friction = float(car_row[stat_indices["frictionwithslipanglesquared"]])
            car.max_speed = float(car_row[stat_indices["maxdrivetrainspeed"]])
            car.max_acceleration = float(car_row[stat_indices["maxacceleration"]])
            car.max_friction = float(car_row[stat_indices["maxfriction"]])

        return cars
