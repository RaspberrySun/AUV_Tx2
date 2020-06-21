import time


class PID:
    # Init
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time
        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0
        self.output = 0.0

    # Set Target Value
    def set_target(self, target):
        self.SetPoint = target

    """
    Calculate Value:
    u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
    """

    def calculate(self, feedback_value):
        error = self.SetPoint - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time
            if delta_time > 0:
                self.DTerm = delta_error / delta_time
            self.last_time = self.current_time
            self.last_error = error
            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    # Set Kp
    def set_kp(self, p_gain):
        self.Kp = p_gain

    # Set Ki
    def set_ki(self, i_gain):
        self.Ki = i_gain

    # Set Kd
    def set_kd(self, d_gain):
        self.Kd = d_gain

    # Set Sample Time
    def set_time(self, sample_time):
        self.sample_time = sample_time
