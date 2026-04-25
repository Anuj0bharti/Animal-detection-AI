"""
Drone Tracking System (Concept Implementation)

This module demonstrates how detected animals can be tracked using a drone.
It uses control theory (PID controller) and computer vision outputs.

NOTE: This is a conceptual module for demonstration.
"""

import math
import time
from dataclasses import dataclass


# ---------------- DATA STRUCTURES ----------------
@dataclass
class Detection:
    label: str
    confidence: float
    x_center: float
    y_center: float
    area: float


# ---------------- PID CONTROLLER ----------------
class PIDController:
    def __init__(self, kp=0.4, ki=0.0, kd=0.2):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / max(dt, 1e-6)
        self.prev_error = error

        return (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )


# ---------------- DRONE CONTROLLER ----------------
class DroneTracker:
    """
    Tracks a target object using bounding box data.
    Converts vision output → drone movement commands.
    """

    def __init__(self, frame_width, frame_height, target_label="cow"):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.target_label = target_label

        # PID controllers
        self.pid_x = PIDController()
        self.pid_y = PIDController()

        # Desired size of object (distance control)
        self.target_area = (frame_width * frame_height) * 0.08

        print("Drone Tracker Initialized")

    def select_target(self, detections):
        """
        Select highest confidence target
        """
        targets = [d for d in detections if d.label == self.target_label]
        if not targets:
            return None

        return max(targets, key=lambda d: d.confidence)

    def compute_control(self, detection, dt=0.05):
        """
        Convert detection → velocity commands
        """

        # Error from center
        error_x = detection.x_center - (self.frame_width / 2)
        error_y = detection.y_center - (self.frame_height / 2)

        # Normalize errors
        norm_x = error_x / (self.frame_width / 2)
        norm_y = error_y / (self.frame_height / 2)

        # PID output
        vx = -self.pid_y.compute(norm_y, dt)
        vy = -self.pid_x.compute(norm_x, dt)

        # Distance control using area
        area_error = (detection.area - self.target_area) / self.target_area
        vz = -0.5 * area_error

        # Yaw control (turn drone)
        yaw_rate = -0.3 * norm_x

        return vx, vy, vz, yaw_rate

    def send_command(self, vx, vy, vz, yaw_rate):
        """
        Simulated MAVLink-style command
        """

        print(f"""
        MAVLINK COMMAND:
        ----------------
        Velocity X: {vx:.2f}
        Velocity Y: {vy:.2f}
        Velocity Z: {vz:.2f}
        Yaw Rate : {yaw_rate:.2f}
        """)

    def track(self, detections):
        """
        Main tracking loop step
        """

        target = self.select_target(detections)

        if target is None:
            print("Searching for target...")
            self.send_command(0, 0, 0, 0.2)  # slow rotation
            return

        vx, vy, vz, yaw = self.compute_control(target)

        print(f"Tracking {target.label} (confidence: {target.confidence:.2f})")
        self.send_command(vx, vy, vz, yaw)


# ---------------- DEMO ----------------
if __name__ == "__main__":
    tracker = DroneTracker(640, 480, target_label="cow")

    # Fake detections
    detections = [
        Detection(label="cow", confidence=0.9, x_center=320, y_center=240, area=50000)
    ]

    for _ in range(10):
        tracker.track(detections)
        time.sleep(0.1)