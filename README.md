# EcoRoby - Robotic Arm for Waste Sorting

![EcoRoby](https://github.com/user-attachments/assets/23b1f9e7-a739-43e0-afb0-4b9e1a267267)

EcoRoby is a 3D-printed robotic arm designed for automatic object recognition and sorting into designated bins (paper, plastic, glass). It integrates machine learning for classification and is controlled via Arduino. This project combines robotics, electronics, and AI for educational and practical applications in recycling.

## Features
- Automatic recognition of objects using a camera (originally OV7670, now laptop camera due to FIFO limitation)
- Servo-controlled robotic arm for moving and sorting items
- Machine Learning model integrated locally for object classification
- Compact and 3D-printable design

## Hardware
- 3D-printed robotic arm parts: base, shoulder, elbow, wrist, gripper
- 6 servo motors for movement
- Arduino board for servo control
- Laptop camera (used instead of OV7670 without FIFO)
- External power supply for servos

## Software
- Arduino IDE for controlling servos
- Python / ML model for object recognition
- Integration code between Arduino and ML model

## Demo Video
Watch EcoRoby in action: [YouTube Link](https://youtu.be/RZXt9ttduHs?si=dOiy6DUMeK1Ywf3U)
