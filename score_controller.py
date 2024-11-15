class ScoreController:
    base_score_multiplier = 0.2864789
    max_multiplier = 9
    min_progress_for_multiplier_decrease = -.25
    multiplier_progress_increase_speed = 0.06
    multiplier_effect_on_decrease = 0.05
    max_multiplier_decrease_per_second = -0.75
    max_multiplier_increase_per_second = 1
    car_surface_type_multiplier = 3.266666667
    multiplier_decrease_multiplier = 3

    def __init__(self) -> None:
        self.score = 0
        self.multiplier = 1
        self.multiplier_progress = 0

    def update(self, delta_time, angle, speed):
        self.score += self.get_base_score_increase_this_frame(delta_time, angle, speed) * self.multiplier
        self.update_multiplier(delta_time, angle, speed)

    def get_base_score_increase_this_frame(self, delta_time, angle, speed):
        return abs(angle) * speed * delta_time * self.base_score_multiplier * self.car_surface_type_multiplier

    def update_multiplier(self, delta_time, angle, speed):
        self.update_multiplier_progress(delta_time, angle, speed)
        # increase multiplier
        if self.multiplier_progress > 1 and self.multiplier < self.max_multiplier:
            self.multiplier_progress -= 1
            self.multiplier += 1
        # decrease multiplier
        if self.multiplier_progress <= self.min_progress_for_multiplier_decrease and self.multiplier > 1:
            self.multiplier_progress += 1 - self.min_progress_for_multiplier_decrease
            self.multiplier -= 1
        
        self.multiplier = min(max(1, self.multiplier), self.max_multiplier)
        self.multiplier_progress = max(self.min_progress_for_multiplier_decrease, self.multiplier_progress)
        if self.multiplier == self.max_multiplier:
            self.multiplier_progress = min(1, self.multiplier_progress)

    def update_multiplier_progress(self, delta_time, angle, speed):
        base_score_increase = self.get_base_score_increase_this_frame(delta_time, angle, speed)

        # increase
        multiplier_progress_change = base_score_increase * self.multiplier_progress_increase_speed

        # decrease
        multiplier_decrease_factor = self.multiplier * self.multiplier_effect_on_decrease
        multiplier_decrease = self.multiplier_decrease_multiplier * multiplier_decrease_factor * delta_time
        multiplier_progress_change -= multiplier_decrease

        multiplier_progress_change = max(multiplier_progress_change, self.max_multiplier_decrease_per_second * delta_time)
        multiplier_progress_change = min(multiplier_progress_change, self.max_multiplier_increase_per_second * delta_time)

        self.multiplier_progress += multiplier_progress_change
