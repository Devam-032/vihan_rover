
# International Rover Challenge 2023 - Autonomous Mars Rover Project

Our team participated in the International Rover Challenge 2023, where we developed an innovative, cost-effective Mars Rover prototype. The rover was recognized as the most economical rover in the competition. My primary responsibility was to develop the autonomous navigation system, focusing on arrow detection, obstacle avoidance, and maintaining the rover's heading without relying on encoders. Other team members worked on controlling a 5-DOF manipulator and scripting the soil connection and analysis module.

## Overview

This project involved developing a robust and economical autonomous Mars Rover capable of navigating rough and uneven terrains. The rover utilized a combination of sensors and computer vision techniques to detect directional cues, avoid obstacles, and maintain a steady course.

## Key Features

### 1. Arrow Detection

- **OpenCV Integration**: Implemented a Python node using OpenCV to detect directional arrows. The arrows served as waypoints for the rover, guiding its navigation.
- **Real-Time Processing**: The Python node processed images in real-time to detect the arrow's direction and adjust the rover's path accordingly.

### 2. Obstacle Avoidance and Distance Measurement

- **LiDAR Sensor**: Used a LiDAR sensor to measure the distance to detected arrows and nearby obstacles. The data from the LiDAR helped the rover navigate safely around obstacles.
- **Dynamic Path Adjustment**: Based on LiDAR readings, the rover dynamically adjusted its path to avoid collisions and follow the designated course.

### 3. Heading and Orientation Control

- **IMU Sensor**: The Inertial Measurement Unit (IMU) was utilized to determine the rover's heading relative to the detected arrow direction.
- **Closed-Loop System without Encoders**: Implemented a closed-loop control system that maintained the rover's heading and angular velocity. This approach eliminated the need for encoders, which can produce noisy data in rough terrains. By focusing on the IMU readings and maintaining a constant heading, the rover avoided deviations from its track.

### 4. Additional Features by Team Members

- **5-DOF Manipulator Control**: Other team members worked on developing and controlling a 5-DOF manipulator arm, allowing the rover to perform tasks such as picking up objects and interacting with the environment.
- **Soil Connection and Analysis Module**: A dedicated script was developed for the soil collection and analysis module, enabling the rover to gather soil samples and perform basic analysis for research purposes.

## Technologies Used

- **Languages**: Python
- **Frameworks/Tools**: ROS (Robot Operating System), OpenCV (for computer vision tasks)
- **Hardware**: LiDAR, IMU, Raspberry Pi, Jetson Nano
- **Sensors**: LiDAR, IMU

## Project Achievements

- **Most Economical Rover**: Our rover was recognized as the most economical solution at the International Rover Challenge 2023.
- **Autonomous Navigation and Stability**: Successfully demonstrated autonomous navigation capabilities, arrow detection, obstacle avoidance, and stable heading control without the use of encoders.
- **Team Contributions**: While my focus was on navigation, other team members contributed significantly to manipulator control and soil analysis, demonstrating a comprehensive skill set.

## How to Run the Project

1. **Set Up the Hardware**: Assemble the Mars Rover with the required sensors and controllers, including LiDAR, IMU, and a camera module for arrow detection.
2. **Install ROS and Dependencies**: Ensure ROS is installed on the onboard computer. Install necessary Python packages, such as OpenCV, and ROS dependencies.
3. **Launch the Rover's Navigation System**: Use the following command to start the rover's navigation system, including the arrow detection and obstacle avoidance components:

    ```bash
    roslaunch mars_rover_navigation arrow_detection_navigation.launch
    ```

4. **Monitor Navigation and Heading**: Use RViz or another ROS-compatible visualization tool to monitor the rover's navigation and heading in real-time.

## Future Work

- **Enhanced Vision Processing**: Improve the arrow detection algorithm to handle more complex visual cues and varying lighting conditions.
- **Advanced Terrain Adaptation**: Implement advanced terrain adaptation techniques to further improve stability and navigation in highly uneven terrains.
- **Manipulator Integration**: Integrate the 5-DOF manipulator control with the main navigation system for seamless multitasking.

## Conclusion

The project successfully demonstrated the ability to navigate rough terrains using a cost-effective and innovative approach. By eliminating the reliance on encoders and utilizing a combination of LiDAR, IMU, and computer vision, the rover maintained stability and navigational accuracy. The teamwork and integration of various modules showed the potential for future advancements in autonomous Mars exploration technology.
