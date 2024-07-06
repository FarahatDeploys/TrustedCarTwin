# TrustedCarTwin
Welcome to the TrustworthyAutonomousTwin repository! This project aims to develop a digital twin for trustworthy autonomous vehicles (AVs). Our goal is to create a robust and ethical framework for AVs that ensures safety, reliability, and ethical decision-making in real-time traffic scenarios.


# CARLA Client
## CARLA Python Client

This repository contains a Python client for the CARLA simulator, which demonstrates how to control a vehicle using a joystick and capture images from multiple cameras attached to the vehicle.

### Features

- Connects to a running CARLA simulator instance.
- Spawns a vehicle and attaches four cameras to it.
- Captures and processes images from the cameras.
- Uses a joystick for controlling the vehicle.
- Displays combined camera images with control inputs overlaid.

### Requirements

- CARLA simulator (tested with version 0.9.x)
- Python 3.6 or later
- OpenCV
- Pygame
- NumPy

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/carla-python-client.git
    cd carla-python-client
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Ensure that the CARLA simulator is running on your machine.

### Usage

1. Run the CARLA simulator. Make sure it is listening on the default port (`localhost:2000`).

2. Execute the Python client script:

    ```bash
    python CAVE.py
    ```

3. Use a joystick to control the vehicle. The control inputs (steering, throttle, brake) will be displayed on the combined camera images in a 1x4 grid.

### File Structure

- `CAVE.py`: Main script that initializes the CARLA client, spawns a vehicle, attaches cameras, and processes joystick inputs.
- `requirements.txt`: List of required Python packages.

### Code Explanation

#### `initialize_carla_client()`

Initializes the connection to the CARLA simulator, retrieves the world and blueprint library, and attempts to spawn a vehicle at one of the available spawn points.

#### `create_camera()`

Creates a camera sensor, sets its attributes, and attaches it to the vehicle.

#### `process_camera_image()`

Processes the image data from the camera, converting it from BGRA to RGB format.

#### `main()`

Sets up the environment, initializes Pygame for joystick input, initializes the CARLA client, creates cameras, processes joystick inputs, and combines camera images.

#### Example Output

The combined camera images with control inputs overlaid will be displayed in a window. Press the 'q' key to exit the application.

## Acknowledgements

- [CARLA Simulator](https://carla.org/)
- [OpenCV](https://opencv.org/)
- [Pygame](https://www.pygame.org/)

## Contact

For any questions or suggestions, feel free to open an issue or contact the repository owner.

