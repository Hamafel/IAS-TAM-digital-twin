# Solar Panel Monitoring and Maintenance System

This project focuses on monitoring the status of solar panels, using both hardware and software components to ensure efficient operation and timely maintenance. Below is a summary of the components involved:

## 1. CNN Model for Solar Panel Classification

We developed a Convolutional Neural Network (CNN) model that classifies the condition of the solar panel based on images captured by the system. The model is capable of categorizing the panel status into three classes:
- **Dirty**
- **Clean**
- **Damaged**

This classification helps in automating the maintenance process by detecting when panels need cleaning or repairs.

## 2. API Endpoint for Sensor Data and BCF File Generation

We created an API endpoint that receives sensor data to continuously monitor the system. The sensors capture relevant environmental and operational parameters (described in the hardware section below). The API checks whether each sensor detects any issue or problem. When an issue is detected, the system generates a **BCF (Building Collaboration Format)** file, which includes a topic explaining the detected situation.

## 3. JSON File for Topic Descriptions

A JSON file is provided that contains descriptions of the topics used in generating the BCF files. These topics describe various scenarios related to solar panel issues, such as environmental factors affecting performance or physical damage. This structured approach ensures that every problem detected is well-documented for further analysis.

## 4. Hardware Code

In the `hardware` folder, you will find the code responsible for gathering sensor data. The system is built using the **ESP32** microcontroller, which is connected to several sensors, including:
- **CO2 Sensor**: Monitors the air quality around the solar panel.
- **Temperature Sensor**: Tracks the environmental temperature to assess heat exposure.
- **Water Level Sensor**: Measures water levels, especially useful for panels exposed to weather conditions.
- **Camera**: Captures real-time images of the solar panel to assess its physical status, used by the CNN model for classification.

Each sensor’s data is sent to the API endpoint for issue detection and BCF generation.

## Project Structure
-`software`: Contain the software code from endpoint,model and json template for the topics
-`Tpoics` : Contain the json templates for the topics
- `hardware/`: Contains the hardware code for ESP32, which collects data from CO2, temperature, water level sensors, and the camera.

