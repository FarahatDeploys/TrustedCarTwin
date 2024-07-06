### this code provides the user with 4 screens (2 nodes)
 
import os
import cv2
import time
import carla
import numpy as np
import pygame
from queue import Queue

def initialize_carla_client():
    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('vehicle')[0]

    spawn_points = world.get_map().get_spawn_points()
    for spawn_point in spawn_points:
        try:
            vehicle = world.spawn_actor(vehicle_bp, spawn_point)
            vehicle.set_autopilot(False)
            return vehicle, world
        except RuntimeError as e:
            print(f"Spawn failed at {spawn_point.location}: {e}")
            continue
    raise RuntimeError("All spawn points are occupied.")

def create_camera(world, vehicle, transform):
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '800')
    camera_bp.set_attribute('image_size_y', '600')
    camera_bp.set_attribute('fov', '90')
    camera_bp.set_attribute('sensor_tick', '0.1')  # 10 FPS
    camera = world.spawn_actor(camera_bp, transform, attach_to=vehicle)
    return camera

def process_camera_image(image):
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]  # Remove alpha channel
    array = array[:, :, ::-1]  # Convert from BGRA to RGB
    return array.copy()  # Return a writable copy

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

    # Initialize Pygame for joystick
    pygame.init()
    pygame.joystick.init()

    # Check for joystick
    if pygame.joystick.get_count() < 1:
        print("No joystick found.")
        pygame.quit()
        exit()

    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    vehicle, world = initialize_carla_client()

    # Create four cameras and attach them to the vehicle
    camera1 = create_camera(world, vehicle, carla.Transform(carla.Location(x=2.5, z=0.7)))
    camera2 = create_camera(world, vehicle, carla.Transform(carla.Location(x=-2.5, z=0.7)))
    camera3 = create_camera(world, vehicle, carla.Transform(carla.Location(y=2.5, z=0.7)))
    camera4 = create_camera(world, vehicle, carla.Transform(carla.Location(y=-2.5, z=0.7)))

    camera_queue1 = Queue()
    camera_queue2 = Queue()
    camera_queue3 = Queue()
    camera_queue4 = Queue()
    camera1.listen(lambda image: camera_queue1.put(process_camera_image(image)))
    camera2.listen(lambda image: camera_queue2.put(process_camera_image(image)))
    camera3.listen(lambda image: camera_queue3.put(process_camera_image(image)))
    camera4.listen(lambda image: camera_queue4.put(process_camera_image(image)))

    try:
        while True:
            # Capture all axis values
            axis_values = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            raw_steer = joystick.get_axis(0)
            raw_throttle = joystick.get_axis(5)
            raw_brake = joystick.get_axis(4)

            # Adjust values as needed for CARLA (e.g., reversing the axis direction)
            throttle = max(0.0, (raw_throttle + 1) / 2)
            brake = max(0.0, (raw_brake + 1) / 2)
            steer = raw_steer

            # Print control values for debugging
            print(f"Control Values - Throttle: {throttle:.2f}, Steer: {steer:.2f}, Brake: {brake:.2f}")

            if joystick.get_button(0):
                print("Exit button pressed. Exiting...")
                raise KeyboardInterrupt

            control = carla.VehicleControl()
            control.throttle = throttle
            control.steer = steer
            control.brake = brake
            control.hand_brake = bool(joystick.get_button(1))

            # Print the control object for debugging
            print(f"Applying Control: {control}")

            vehicle.apply_control(control)

            if not camera_queue1.empty() and not camera_queue2.empty() and not camera_queue3.empty() and not camera_queue4.empty():
                camera_image1 = camera_queue1.get()
                camera_image2 = camera_queue2.get()
                camera_image3 = camera_queue3.get()
                camera_image4 = camera_queue4.get()

                # Combine the four camera images in a 1x4 grid
                combined_image = np.hstack((camera_image1, camera_image2, camera_image3, camera_image4))

                # Display control inputs on the combined camera image
                cv2.putText(combined_image, f"Steer: {steer:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(combined_image, f"Throttle: {throttle:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(combined_image, f"Brake: {brake:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                cv2.imshow('CARLA Cameras', combined_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera1.stop()
        camera2.stop()
        camera3.stop()
        camera4.stop()
        vehicle.destroy()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    main()
