import math
from pygame import Vector2


class Car:
    # game object things
    position: Vector2
    velocity = Vector2
    rotation_rads = 0
    rotational_velocity = 0
    # car handling stats
    steering_speed = 2
    constant_friction = 4
    linear_friction = 16
    squared_friction = 0
    max_speed = 30
    max_acceleration = 10
    max_friction = 30
    # other
    current_input = 0

    def __init__(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)

    def update(self, delta_time):
        self.apply_friction(delta_time)
        self.apply_acceleration(delta_time)
        self.rotational_velocity = self.steering_speed * self.current_input
        self.position += self.velocity * delta_time
        self.rotation_rads += self.rotational_velocity * delta_time

    def apply_friction(self, delta_time):
        slip_angle = self.get_signed_slip_angle_rads()
        unsigned_slip_angle = min(abs(slip_angle), math.pi / 2)

        friction_force_magnitude = (
            self.constant_friction + 
            self.linear_friction * unsigned_slip_angle + 
            self.squared_friction * unsigned_slip_angle * unsigned_slip_angle
        )
        friction_acceleration_magnitude = min(friction_force_magnitude, self.max_friction)
        friction_acceleration_unsigned = friction_acceleration_magnitude
        instant_friction_acceleration_unsigned = friction_acceleration_unsigned * delta_time

        # is_reverse_drift = abs(slip_angle) > 90 * (180 / math.pi)
        is_reverse_drift = False
        drift_direction = 1 if slip_angle > 0 else -1
        print(slip_angle)
        local_horizontal_velocity = self.velocity
        global_friction_direction = (local_horizontal_velocity * -1 if is_reverse_drift else self.right() * drift_direction).normalize()
        instant_friction_acceleration = global_friction_direction * instant_friction_acceleration_unsigned
        self.velocity += self.clamp_friction(instant_friction_acceleration)

    def get_signed_slip_angle_rads(self):
        if self.velocity.length() == 0: return 0
        angle = self.velocity.normalize().angle_to(self.forward())
        angle = angle * math.pi / 180
        if angle < -math.pi: angle += 2 * math.pi
        if angle > math.pi: angle -= 2 * math.pi
        return angle

    def clamp_friction(self, unclamped_friction):
        return Vector2(
            min(max(-abs(self.velocity.x), unclamped_friction.x), abs(self.velocity.x)),
            min(max(-abs(self.velocity.y), unclamped_friction.y), abs(self.velocity.y)),
        )

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
    
    def right(self) -> Vector2:
        return Vector2(-math.cos(self.rotation_rads), -math.sin(self.rotation_rads))

    def get_velocity_in_direction(self, direction):
        return self.velocity.project(direction)
