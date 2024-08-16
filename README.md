<div align="center"> 
<p style="width=150px;">
    <img src="https://github.com/btnrv/BeeRocketry_RocketGroundStation/blob/main/Assets/logo.png" width="150"/>
</p>

# BeeRocketry 2024 Rocket Ground Station
</div>

## Overview

BeeRocketry 2024 Rocket Ground Station is a ground station written in Python designed to work with Python 3.10+. This code is specifically written for the Teknofest Rocket Competition 2024. Note that Python 3.12 has not been tested and is probably not supported by most libraries used in this project.

## Features

- **Asynchronous Serial Communication:** Enables the receiving and sending of data over serial ports asynchronously with 0% lag.
- **Real-Time Data Visualization:** Provides immediate feedback on various rocket parameters through live Matplotlib graphs.
- **Formatted Communication:** Adheres to the communication standards outlined in the Teknofest 2024 rulebook for data exchange with the judging computer.
- **Enhanced Stability:** Implements measures to increase the reliability of serial communications, minimizing data loss and transmission errors.
- **Start, Stop, Reset Buttons:** Provides start, stop, and reset operations implemented as buttons.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Demonstrations](#demonstrations)
- [Known Limitations](#known-limitations)
- [License and Disclaimers](#license-and-disclaimers)

## Installation
```bash
# Check the python version by running the following
# Python 3.10.x is suggested
python
exit()

# Clone and navigate to the repository
git clone https://github.com/btnrv/BeeRocketry_RocketGroundStation.git

cd BeeRocketry_RocketGroundStation

# Run the installation script to install necessary libraries from requirements.txt
install.bat
```

## Usage

The ground station application requires customization before use.

First, customize the `.env` file according to your desired data update frequency and given `TEAM_ID` for the competition. 

Next, you have to set up the Serial widget according to your serial communication structure. We used an array of values embedded into a string such as **0,0,0,0,0,0,0,0,...** and later decoded it to extract values. In short, you **must modify the SerialWidget code to suit your specific packet format**, or data structure.

Once you have confirmed that your packet format is correct:

- Adjust your `Windows scaling settings to 100%`. See [Known Limitations](#known-limitations) for more details.
- Plug in your USB-TTL adapter and ground station COM device to receive data.
- Run the `main.py` file to start the application.
- In the application, select the appropriate COM devices from the dropdown menus as well as the respective baudrates.
- Press the `Start` button to begin communication and graph visualization.

## Demonstrations

<p align="center">
    <img src="https://github.com/btnrv/BeeRocketry_RocketGroundStation/blob/main/Assets/ss1.png" style="width:150px%; margin:5px;" />
    <img src="https://github.com/btnrv/BeeRocketry_RocketGroundStation/blob/main/Assets/ss2.png" style="width:150px%; margin:5px;" />
</p>
<p align="center">
    <img src="assets/demo.gif" alt="Demonstration GIF" style="width:70%; margin:5px;" />
</p>

## Known Limitations

The application may not display correctly if Windows scaling is not set to 100%. Please adjust your display settings accordingly. PySide6 does not allow forcing the scaling to the window in the latest versions.

Stop the serial communication by pressing `Stop` before closing the window, otherwise the serial communication keeps working. This is because I couldn't find a way to close it's thread properly alongside the window.

## License and Disclaimers
This project’s code is intended as a source of inspiration and should not be used by directly copying and pasting. If you decide to use any part of the code, please consider letting me know by emailing tanriverdiburak754@gmail.com. I would love to hear how my code have helped with your projects.

This project is licensed under the MIT License. For more details, please refer to the LICENSE file.
