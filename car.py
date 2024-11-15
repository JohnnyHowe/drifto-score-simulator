import math
from pygame import Vector2


class Car:
    # game object things
    position = Vector2(0, 0)
    velocity = Vector2(0, 0)
    rotation_rads = 0
    rotational_velocity = 0
    # car handling stats
    steering_speed = 2
    constant_friction = 4
    linear_friction = 16
    squared_friction = 0
    max_speed = 30
    max_acceleration = 10
    # other
    current_input = 0

    def update(self, delta_time):
        self.update_friction()
        self.apply_acceleration(delta_time)
        self.rotational_velocity = self.steering_speed * self.current_input
        self.position += self.velocity * delta_time
        self.rotation_rads += self.rotational_velocity * delta_time

    def update_friction(self):
        pass

    def apply_acceleration(self, delta_time):
        acceleration = self.get_max_acceleration_for_current_speed()
        instant_acceleration = acceleration * self.forward() * delta_time
        self.velocity += instant_acceleration

    def get_max_acceleration_for_current_speed(self):
        forwards_speed = self.get_velocity_in_direction(self.forward()).magnitude()
        return self.get_max_acceleration(forwards_speed)

    def get_max_acceleration(self, forwards_speed):
        return self.max_acceleration * min(max(0, 1 - (forwards_speed / self.max_speed) * (forwards_speed / self.max_speed)), 1)

    def forward(self) -> Vector2:
        return Vector2(-math.sin(self.rotation_rads), math.cos(self.rotation_rads))

    def get_velocity_in_direction(self, direction):
        return self.velocity.project(direction)
