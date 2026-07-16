import math
import time
import requests
from typing import Dict, Any, Optional

class RoboReactor:
    """
    A unified production-ready Python client for the RoboReactor API.
    Handles motion control, navigation telemetry, and streaming multi-category sensor structures.
    """
    
    # Base URL encapsulated as a class constant
    _BASE_URL = "https://roboreactor.com"

    def __init__(self, email: str, project_name: str, secret_token: str):
        self.email = email
        self.project_name = project_name
        self.secret_token = secret_token

    def verify_token(self) -> Optional[str]:
        """
        Verifies the secret_token against the RoboReactor API.
        Returns the 'status' string if successful, or None if the request fails.
        """
        endpoint = f"/verify_token/{self.email}/{self.project_name}/{self.secret_token}"
        url = f"{self._BASE_URL}{endpoint}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('status')
        except requests.exceptions.RequestException as e:
            print(f"Verification error communicating with {url}: {e}")
            return None

    @staticmethod
    def euler_to_quaternion(roll_deg: float, pitch_deg: float, yaw_deg: float) -> Dict[str, float]:
        """Converts Euler angles (in degrees) to a Quaternion dictionary format."""
        roll = math.radians(roll_deg)
        pitch = math.radians(pitch_deg)
        yaw = math.radians(yaw_deg)

        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        return {
            "x": sr * cp * cy - cr * sp * sy,
            "y": cr * sp * cy + sr * cp * sy,
            "z": cr * cp * sy - sr * sp * cy,
            "w": cr * cp * cy + sr * sp * sy
        }

    def _send_post(self, endpoint: str, json_payload: Dict[str, Any], timeout: int = 5) -> Optional[Dict[str, Any]]:
        url = f"{self._BASE_URL}{endpoint}"
        try:
            response = requests.post(url, json=json_payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response body: {e.response.text}")
            return None

    def update_feedback_sensors(self, joints_data: Dict[str, Dict[str, float]]) -> Optional[Dict[str, Any]]:
        """
        Sends analog angular reading feedback for joint arrays.
        Endpoint: /feedback_sensor
        """
        payload = {self.email: {self.project_name: joints_data}}
        return self._send_post("/feedback_sensor", payload)

    def send_navigation_control(
        self, 
        x: float, 
        y: float, 
        z: float, 
        roll_deg: float, 
        pitch_deg: float, 
        yaw_deg: float, 
        joint_targets_deg: Dict[str, float], 
        steering_angle_deg: Optional[float] = None,
        robot_name: str = "Robot_arm_01"
    ) -> Optional[Dict[str, Any]]:
        """
        Sends absolute target coordinates, orientations, and target joint arrays.
        Accepts joint targets in degrees and converts them to radians for the API.
        Endpoint: /api/sim3/input
        """
        if steering_angle_deg is None:
            steering_angle_deg = math.degrees(x / z) if z != 0 else 0.0

        # Convert input degrees to radians for the API payload
        joint_targets_rad = {k: math.radians(v) for k, v in joint_targets_deg.items()}

        payload = {
            self.email: {
                self.project_name: {
                    "target_position": {"x": x, "y": y, "z": z},
                    "target_quaternion": self.euler_to_quaternion(roll_deg, pitch_deg, yaw_deg),
                    "joint_targets": joint_targets_rad,
                    "steering_angle_deg": steering_angle_deg,
                    "timestamp": int(time.time() * 1000),
                    "robot_name": robot_name
                }
            }
        }
        return self._send_post("/api/sim3/input", payload)

    def post_sensor_data(self, category_payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generic telemetry gateway routing specific structured sensor category payloads.
        Endpoint: /sensor_postdata
        """
        payload = {
            "email": self.email,
            "project_name": self.project_name,
            "sensor_payload": category_payload
        }
        return self._send_post("/sensor_postdata", payload)

    def fetch_iot_control(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves remote structural commands sent back down to the target package edge loop.
        Endpoint: /package_iot_control
        """
        payload = {self.email: {}}
        return self._send_post("/package_iot_control", payload)
