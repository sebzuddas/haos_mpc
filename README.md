# NOTE: THIS IS A WORK IN PROGRESS!

# Introduction
In looking to develop my own custom automation systems that close the loop between sensors and actuators in HomeAssistant OS (HAOS), I saw the need to develop my own scripts that would enable me to access live HAOS sensor data in near-real-time. The ![websocket](https://developers.home-assistant.io/docs/api/websocket/#validate-config) API available shows the `.json` format for communicating with HAOS, but there didn't seem to be anything for doing this using Python. 

## Control Systems
HAOS offers very basic automations regarding turning switches on and off, or if the device supports it, tuning a specific variable (such as light intensity). These automations, although user friendly and fairly effective, have only the capabilities to implement hysteresis-based control systems. To develop a true 'intelligent' home, the home needs to be able to automatically control actuators based on **goals** and **constraints** set by the user. The overall mission of this project is to implement advanced control techniques to make the *intelligent* home a reality. 

# Intended Use
To be able to effectively interact with HAOS via Python scripts for advanced automation procedures. Although `.yaml` files can be used to create useful automations, it may be that more advanced automations should be developed, and for the processing to occur outside of HAOS. This set of scripts is intended to make the interplay between HAOS and some other techniques easier.

# Managing Credentials

Done via `python-dotenv`. Example file:
```
HASS_IO_AUTH_TOKEN = YOUR AUTH KEY
HASS_IO_HOSTNAME = ws://homeassistant.local:8123/api/websocket
YAML_NAME = subscriptions.yaml
```

# TODO:
- Sensor class
    - Create virtual sensors for testing
    - 

- Actuator Class
    - Send commands to HAOS via the websocket/api.

- DatabaseManager class
    - ~~pull data from TimescaleDB~~
    - Get list of database components from TimescaleDB

- Signal Processing
    - ~~Implement simple filtering techinques~~
    - Implement more filtering techniques
    - Functions for optimising filters

- Real-time data
    - Use the websocket functionality of HAOS to allow the system to function live
    - Making the sensor class be able to collect real-time data

