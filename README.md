# Vehicle-Simulation-with-Cryptographic-Messaging
Vehicle Simulation with Cryptographic Messaging
## Overview

This project simulates a network of vehicles that communicate with each other using cryptographic techniques to ensure message integrity and authenticity. Each vehicle can move, generate messages containing its state, and verify the integrity of received messages using hashing and digital signatures.
Features

    Vehicle movement simulation with random speed variations.
    Cryptographic signing of messages using ECDSA (Elliptic Curve Digital Signature Algorithm).
    Hashing of messages using multiple algorithms (SHA-256, MD5, SHA-1, BLAKE2b, SHA3-256).
    Collision detection between vehicles.
    Visualization of vehicle speeds and positions over time.

## Dependencies
To run this simulation, you need the following Python packages:

    random (standard library)
    hashlib (standard library)
    matplotlib (for plotting)
    pandas (for data manipulation)
    cryptography (for cryptographic operations)

You can install the required packages using pip:

```bash

pip install matplotlib pandas cryptography
```

## How to Run the Simulation

    Clone the Repository (if applicable):

```bash
git clone https://github.com/DinooBose/Vehicle-Simulation-with-Cryptographic-Messaging.git
cd Vehicle-Simulation-with-Cryptographic-Messaging
```
## Run the Simulation:
You can run the simulation by executing the Python script. Make sure you have Python 3.x installed.

```bash

    python vehicle_simulation.py
```
    Replace vehicle_simulation.py with the name of your Python file if it's different.

    View the Results:
    After running the simulation, you will see printed output in the console indicating message exchanges, integrity checks, and any detected collisions. Additionally, plots will be generated showing the hash generation times, vehicle speeds, and positions over time.

## Code Structure

    Vehicle Class: Represents a vehicle with attributes for ID, speed, position, and cryptographic keys. It includes methods for movement, message generation, signing, and verification.
    Simulation Functions: Functions to simulate vehicle movement, plot speeds, and plot positions.
    Main Execution: Creates instances of vehicles, runs the simulation, and visualizes the results.

## Example Output

When you run the simulation, you will see output similar to the following:

```Code

Vehicle V1 received message from V2: {'vehicle_id': 'V2', 'speed': 50, 'position': (10, 20)}
Received hashes: {'sha256': '...', 'md5': '...', ...}
Message integrity and signature are valid.
Collision detected between vehicle V1 and: V2
```
## License

This project is licensed under the MIT License - see the LICENSE file for details.
