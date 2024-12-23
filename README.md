# Smart Environmental Monitoring System

## Overview
This project demonstrates a **smart environmental monitoring system** using the **ESP32** and **Pico W**. The ESP32 acts as the **server**, receiving data from various sensors and sending it to the cloud. The Pico W functions as the **client**, requesting and displaying the sensor data on an **OLED screen**.

## Features

- **Real-time Monitoring:** Continuously monitors and displays environmental data.
- **Client-Server Architecture:** 
  - **ESP32** (Server): Collects sensor data and transmits it to the cloud.
  - **Pico W** (Client): Requests and displays sensor data on an OLED screen.
- **IoT Integration:** Connects sensors to an Internet of Things (IoT) platform for easy access to data.
- **Cloud Integration:** Sends sensor data via Wi-Fi to a cloud service (Adafruit IO) for remote access and storage.
- **Environmental Feedback:** Provides real-time feedback and visual indicators based on environmental conditions.

## How It Works

1. **Sensors:** Various sensors are connected to the ESP32, which collects environmental data (e.g., temperature, humidity, air quality).
2. **ESP32 as Server:** The ESP32 receives data from the sensors and sends it over a Wi-Fi network to the cloud-based platform (Adafruit IO).
3. **Pico W as Client:** The Pico W requests the data from the ESP32 and displays it on an OLED screen for real-time monitoring.
4. **Cloud Storage:** Data is sent to Adafruit IO for long-term storage, analysis, and remote access.
5. **Feedback Mechanism:** The system provides feedback based on the environmental data to indicate specific conditions (e.g., high temperature, low air quality).

## Getting Started

To get started with this project, follow these steps:

1. **Hardware Setup:** Connect the sensors to the ESP32 and Pico W.
2. **Software Setup:** Install the necessary libraries and set up the connection to Adafruit IO.
3. **Running the System:** Power up the devices and view real-time data on the OLED display.


