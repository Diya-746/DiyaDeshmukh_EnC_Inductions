# Diya Deshmukh – Kratos EnC Inductions

## Repository Structure

```
src/
├── kratos_diya
├── kratos_diya_msgs
└── arm_humble
```

---

# Week 3 part 1

## Question 1

Implemented ROS2 publisher and subscriber nodes for rover monitoring.

Features:

- Publisher
- Subscriber
- Launch file
- Custom message
- ROS2 package

---

# Week 3 part 2

## Question 1

Solved Forward and Inverse Kinematics for the given planar manipulator.

## Question 2

Implemented an Inverse Kinematics controller for the provided robotic arm.

### Features

- Publishes `sensor_msgs/msg/JointState`
- Controls
  - base_yaw_joint
  - shoulder_joint
  - elbow_joint
- Computes inverse kinematics
- Rejects unreachable targets
- Maintains internal end-effector position

---

## Assumptions

- Wrist and gripper remain fixed.
- Link lengths taken from the provided URDF.

---

## Challenges

- ROS2 package setup
- Custom message creation
- RViz visualization
- ROS2 launch configuration
- Package dependency debugging

---

## Testing

Verified using:

- `ros2 topic echo /joint_states`
- RViz visualization
- Reachability checks
- Successful movement of robotic arm# DiyaDeshmukh_EnC_Inductions
