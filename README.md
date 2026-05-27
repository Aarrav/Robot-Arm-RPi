# 5-DOF Robot Arm: High-Level ROS 2 Control (Raspberry Pi)

This repository contains the high-level ROS 2 workspace developed for the 5XEB0 5-DOF robotic manipulator. Deployed on a Raspberry Pi, this software acts as the central "brain" of the system, handling trajectory generation, graphical user interfaces, and telemetry logging.

It serves as the companion to the low-level microcontroller firmware, demonstrating the ability to build scalable, distributed robotic systems using the ROS 2 ecosystem.

## 🧠 High-Level Architecture

The software is structured around a decentralized node architecture, allowing distinct processes to handle different aspects of the robot's operation:

* **Trajectory Generation:** Python-based ROS 2 nodes calculate smooth kinematic paths (e.g., polynomial trajectories) and publish target velocities/positions.
* **micro-ROS Agent:** The Raspberry Pi hosts the micro-ROS agent, bridging the ROS 2 graph with the Teensy 4.0 hardware over a UART serial connection.
* **Graphical Interfaces:** Custom Python GUIs allow for real-time manual jogging, node initialization, and system diagnostics without interacting directly with the terminal.
* **Telemetry & Logging:** Native `rosbag2` integration records high-frequency joint states and control efforts for offline MATLAB analysis and system identification.

## 📁 Repository Structure

The workspace is organized into standard `colcon` packages and standalone scripts:

* **ROS 2 Packages:**
  * `/base_motor_control` & `/dual_motor_control`: Nodes dedicated to publishing synchronized movement commands for single and multiple axes.
  * `/simple_trajectory`: Contains the `main.py` node responsible for executing complex, multi-joint trajectory profiles.
* **Standalone Applications:**
  * `Initial_app_GUI.py` & `Jogger.py`: Interactive tools for manual arm articulation and rapid prototyping.
* **Data Logging:**
  * `/logged_data`: Contains `.db3` ROS bag databases with recorded execution data used for the 5XEB0 academic paper.
* **Build Artifacts:** `/build`, `/install`, and `/log` directories managed by the Colcon build system.

## 🚀 Setup & Execution Overview

To deploy this workspace on the Raspberry Pi:

1. **Build the Workspace:** Navigate to the repository root and compile the Python packages using `colcon build`.
2. **Source the Environment:** Overlay the built packages onto your ROS 2 installation by running `source install/setup.bash`.
3. **Establish Hardware Bridge:** Launch the micro-ROS agent to connect with the Teensy microcontroller.
4. **Launch Nodes:** Run the desired control interface or trajectory script (e.g., `ros2 run simple_trajectory main` or launch the GUI script directly).
