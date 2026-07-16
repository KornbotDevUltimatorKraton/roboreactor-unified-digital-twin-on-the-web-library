# roboreactor

Official Python client library for connecting edge devices, emulators, and robot controls directly to the RoboReactor ecosystem.

---

# Installation

```bash
pip install roboreactor
```

---

# Create RoboReactor Account

To use the SDK:

1. Sign up at https://roboreactor.com/
2. Create a project
3. Generate your `secret_token`

You will need:

- Email
- Project Name
- Secret Token

---

# Initialize Client

```python
from roboreactor import RoboReactor

client = RoboReactor(
    email="your_email@example.com",
    project_name="Your_Project",
    secret_token="YOUR_SECRET_TOKEN"
)
```

---

# Verify Authentication Token

Verify your API connection before starting your robot system.

```python
from roboreactor import RoboReactor

client = RoboReactor(
    email="your_email@example.com",
    project_name="Robot_Project",
    secret_token="YOUR_SECRET_TOKEN"
)

status = client.verify_token()

if status:
    print("Connection verified!")
    print(status)
else:
    print("Authentication failed.")
```

---

# Send Joint Feedback Sensors

Upload robot joint sensor feedback to RoboReactor cloud.

```python
from roboreactor import RoboReactor 
client = RoboReactor( 
    email="your_email@example.com", 
    project_name="Robot_Project", 
    secret_token="YOUR_SECRET_TOKEN" ) 
    joint_feedback = { "joint_1": { 
        "angle_deg": 35.5 
        }, 
    "joint_2": { 
        "angle_deg": 12.8 
        }, 
    "joint_3": {
         "angle_deg": -8.2 
         } 
    }  
response = client.update_feedback_sensors(joint_feedback) 
print(response)

```

---

# Send Navigation Control

Send target coordinates, robot orientation, and joint targets.

```python
import math
from roboreactor import RoboReactor
client = RoboReactor( 
    email="your_email@example.com", 
    project_name="Robot_Project", 
    secret_token="YOUR_SECRET_TOKEN" ) 

# 2. Define your joint targets in DEGREES
# The client will automatically convert these to radians before sending
my_joint_targets = {
    "base": 90.0,    # Was 1.57 rad
    "shoulder": 180.0,    # Was 0.785 rad
    "wrist": -30.0    # Was -0.523 rad
}

# 3. Send the navigation control
# Orientation (roll, pitch, yaw) is also expected in degrees
response = client.send_navigation_control(
    x=2.5, 
    y=0.0, 
    z=1.5, 
    roll_deg=0.0, 
    pitch_deg=0.0, 
    yaw_deg=0.0, 
    joint_targets_deg=my_joint_targets, # Pass degrees here
    robot_name="Robot_arm_01"
)

# 4. Handle the response
if response:
    print("Navigation command sent successfully!")
else:
    print("Failed to send navigation command.")
```

---

# Convert Euler Angles to Quaternion

Utility function for converting Euler angles into quaternion format.

```python
from roboreactor import RoboReactor

quaternion = RoboReactor.euler_to_quaternion(
    roll_deg=0,
    pitch_deg=45,
    yaw_deg=90
)

print(quaternion)
```

---

# Send Generic Sensor Telemetry

Upload custom sensor payloads such as IMU, GPS, battery, and telemetry data.

```python
from roboreactor import RoboReactor

client = RoboReactor(
    email="your_email@example.com",
    project_name="Robot_Project",
    secret_token="YOUR_SECRET_TOKEN"
)

# 2. Prepare your sensor data
# The structure should match what the API expects for the 'sensor_payload'
my_sensor_data = {
    "BMS_sensor": {
        "main_pack": 60.5,
        "temp_sensor_5": 35.5
    },
    "Motion_sensor": {
        "imu_1": {"x": 1.05, "y": -0.02, "z": 1.0}
    }
}

# 3. Post the data
response = client.post_sensor_data(my_sensor_data)

# 4. Handle the response
if response:
    print("Data sent successfully:", response)
else:
    print("Failed to send sensor data.")
```

---

# Fetch IoT Remote Commands

Retrieve IoT control commands from RoboReactor cloud.

```python
from roboreactor import RoboReactor

client = RoboReactor(
    email="your_email@example.com",
    project_name="Robot_Project",
    secret_token="YOUR_SECRET_TOKEN"
)

commands = client.fetch_iot_control()

print(commands)
```

---

# Robot Edge Loop Example

Example continuous runtime telemetry loop for robotics edge devices.

```python
import time
from roboreactor import RoboReactor

client = RoboReactor(
    email="your_email@example.com",
    project_name="Robot_Project",
    secret_token="YOUR_SECRET_TOKEN"
)

while True:

    telemetry_payload = {
        "runtime": {
            "cpu_temp": 48.2,
            "loop_rate_hz": 120
        }
    }

    client.post_sensor_data(telemetry_payload)

    commands = client.fetch_iot_control()

    if commands:
        print("Received Commands:", commands)

    time.sleep(1)
```

---

# Features

- Secure cloud authentication
- Real-time robotics telemetry
- Navigation target streaming
- Joint control streaming
- Quaternion utilities
- Generic telemetry upload
- IoT remote command retrieval
- Edge-device architecture support

---

# Example Architecture

```text
Robot / MCU / SBC
        │
        ▼
RoboReactor Python SDK
        │
        ▼
RoboReactor Cloud API
        │
        ├── Telemetry Dashboard
        ├── Motion Streaming
        ├── IoT Remote Control
        └── Multi-Robot Coordination
```
