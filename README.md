# International Rover Challenge 2023 – Autonomous Mars Rover Project 🌐🚀


*The most economical and innovative Mars Rover at the International Rover Challenge 2023.*

---

## Overview

Our team participated in the **International Rover Challenge 2023**, where we developed an innovative, cost-effective Mars Rover prototype. The rover was recognized as the **most economical rover** in the competition.

My primary responsibility was to design the **autonomous navigation system**, focusing on:

- 🛰 Arrow detection
- ⚡ Obstacle avoidance
- 🛠️ Maintaining heading without encoders

Other team members contributed significantly by working on:

- 🤖 A 5-DOF manipulator
- 🌍 Soil collection and analysis modules

---

## Key Features

### 1. Arrow Detection 🔹

- **OpenCV Integration**: Implemented a Python node using OpenCV to detect directional arrows that served as waypoints.
- **Real-Time Processing**: Enabled the rover to adjust its path dynamically based on arrow directions.

### 2. Obstacle Avoidance 🌲

- **LiDAR Sensor**: Used to measure distances to obstacles and directional cues.
- **Dynamic Path Adjustment**: Helped the rover navigate safely around obstacles while following the course.

### 3. Heading and Orientation Control 🌌

- **IMU Sensor**: Utilized to maintain the rover’s heading and angular velocity.
- **Encoder-Free Control**: A closed-loop system eliminated the need for encoders, ensuring stability on rough terrains.

### 4. Team Contributions 🔧🔬

- **5-DOF Manipulator Control**: Enabled tasks like object interaction and handling.
- **Soil Collection and Analysis**: Automated soil sample collection and basic analysis.

---

## Technologies Used 🧰

| **Category**   | **Details**                           |
| -------------- | ------------------------------------- |
| **Languages**  | Python                                |
| **Frameworks** | ROS (Robot Operating System), OpenCV  |
| **Hardware**   | Raspberry Pi, Jetson Nano, LiDAR, IMU |
| **Sensors**    | LiDAR, IMU, Camera Module             |

---

## Project Achievements 🏆

- **Most Economical Rover**: Recognized as the most cost-effective prototype at IRC 2023.
- **Autonomous Stability**: Demonstrated stable navigation without relying on encoders.
- **Comprehensive Design**: Successfully integrated navigation, manipulation, and soil analysis capabilities.

---

## How to Run the Project 🚪

1. **Set Up the Hardware**

   - Assemble the Mars Rover with required sensors, controllers, and the camera module.

2. **Install ROS and Dependencies**

   - Install ROS and Python packages like OpenCV:
     ```bash
     sudo apt install ros-noetic-desktop-full
     pip install opencv-python
     ```

3. **Launch the Navigation System**

   - Start the arrow detection and obstacle avoidance components:
     ```bash
     rosrun autex arrow_detection.py
     ```

4. **Monitor in Real-Time**

   - Use RViz or similar tools to monitor the rover’s navigation and heading.

---

## Future Work 🔄

- **Enhanced Vision Processing**: Improve arrow detection for more complex visual cues.
- **Advanced Terrain Adaptation**: Enhance stability and navigation in uneven terrains.
- **Manipulator Integration**: Seamlessly integrate the 5-DOF manipulator with the main navigation system.

---

## Conclusion ✅

This project showcased the potential of a cost-effective Mars Rover capable of:

- Navigating rough terrains with precision
- Performing essential manipulative and analytical tasks

By leveraging LiDAR, IMU, and computer vision, the rover maintained stability and navigational accuracy without encoders, proving itself as a promising innovation for future Mars exploration.

---

*Developed with passion and ingenuity by a dedicated team of innovators.*

