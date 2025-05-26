import random
import hashlib
import matplotlib.pyplot as plt
import time
import pandas as pd
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class Vehicle:
    def __init__(self, vehicle_id, speed, position):
        self.id = vehicle_id
        self.speed = speed
        self.position = position
        self.salt = "vanet" + str(random.random())  # Add a salt

        # Generate ECDSA private key for signing
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()

    def move(self, dt):
        self.position = (self.position[0] + self.speed * dt * random.uniform(-0.1, 1.1),
                         self.position[1] + self.speed * dt * random.uniform(-0.1, 1.1))

    def check_collision(self, other, threshold=1):
        distance = ((self.position[0] - other.position[0]) ** 2 +
                    (self.position[1] - other.position[1]) ** 2) ** 0.5
        return distance < threshold

    def hash_message(self, message):
        message_bytes = str(message).encode()
        hash_values = {}
        start_time = time.time()
        hash_values["sha256"] = hashlib.sha256(message_bytes + self.salt.encode()).hexdigest()
        hash_values["sha256_time"] = time.time() - start_time
        start_time = time.time()
        hash_values["md5"] = hashlib.md5(message_bytes + self.salt.encode()).hexdigest()
        hash_values["md5_time"] = time.time() - start_time
        start_time = time.time()
        hash_values["sha1"] = hashlib.sha1(message_bytes + self.salt.encode()).hexdigest()
        hash_values["sha1_time"] = time.time() - start_time
        start_time = time.time()
        hash_values["blake2b"] = hashlib.blake2b(message_bytes + self.salt.encode()).hexdigest()
        hash_values["blake2b_time"] = time.time() - start_time
        start_time = time.time()
        hash_values["sha3_256"] = hashlib.sha3_256(message_bytes + self.salt.encode()).hexdigest()
        hash_values["sha3_256_time"] = time.time() - start_time
        return hash_values

    def check_integrity(self, message, hashes):
        for hash_type, hash_value in hashes.items():
            if hash_type in ["sha256", "md5", "sha1", "blake2b", "sha3_256"]:
                if hash_value != self.hash_message(message)[hash_type]:
                    return False
        return True

    def sign_message(self, message):
        message_bytes = str(message).encode() + self.salt.encode()
        signature = self.private_key.sign(message_bytes, ec.ECDSA(hashes.SHA256()))
        return signature

    def verify_signature(self, message, signature, sender_public_key):
        message_bytes = str(message).encode() + self.salt.encode()
        try:
            sender_public_key.verify(signature, message_bytes, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    def generate_message(self):
        message = {
            "vehicle_id": self.id,
            "speed": self.speed,
            "position": self.position,
        }
        hash_values = self.hash_message(message)
        signature = self.sign_message(message)
        return message, hash_values, signature, self.public_key

    def receive_message(self, message, hashes, signature, sender_public_key):
        print(f"Vehicle {self.id} received message from {message['vehicle_id']}: {message}")
        print(f"Received hashes: {hashes}")
        if not self.check_integrity(message, hashes):
            print("Message integrity is NOT valid!")
            return
        if not self.verify_signature(message, signature, sender_public_key):
            print("Signature verification FAILED!")
            return
        print("Message integrity and signature are valid.")

def simulate(vehicles, dt, num_steps):
    hash_times = {"sha256": [], "md5": [], "sha1": [], "blake2b": [], "sha3_256": []}
    for _ in range(num_steps):
        for vehicle in vehicles:
            vehicle.move(dt)
            collisions = [other for other in vehicles if vehicle != other and vehicle.check_collision(other)]
            if collisions:
                print(f"Collision detected between vehicle {vehicle.id} and: {', '.join(other.id for other in collisions)}")

            message, hash_values, signature, pub_key = vehicle.generate_message()
            for other in vehicles:
                if hasattr(other, 'receive_message'):
                    other.receive_message(message.copy(), hash_values.copy(), signature, pub_key)
            for hash_type, hash_time in hash_values.items():
                if hash_type.endswith("_time"):
                    hash_times[hash_type[:-5]].append(hash_time)

    # Prepare data for Pandas boxplot
    hash_data = []
    for hash_type, times in hash_times.items():
        for time_val in times:
            hash_data.append({"hash_type": hash_type, "time": time_val})

    # Convert hash_data to a DataFrame
    hash_df = pd.DataFrame(hash_data)

    # Create a boxplot using Pandas
    hash_df.boxplot(column="time", by="hash_type", showmeans=True)
    plt.title("Hash Generation Times")
    plt.ylabel("Time (s)")
    plt.xlabel("Hash Function")
    plt.xticks(rotation=45)  # Rotate hash type labels for better readability
    plt.show()

def plot_speeds(vehicles, num_steps, dt):
    times = list(range(num_steps))
    speeds = {vehicle.id: [] for vehicle in vehicles}
    for i in range(num_steps):
        for vehicle in vehicles:
            vehicle.move(dt)
            speeds[vehicle.id].append(vehicle.speed)
        collisions = [other for other in vehicles if vehicle != other and vehicle.check_collision(other)]
        if collisions:
            print(f"Collision detected between vehicle {vehicle.id} and: {', '.join(other.id for other in collisions)}")

    # Create a pandas DataFrame
    speeds_df = pd.DataFrame(speeds, index=times)

    # Plot speeds using matplotlib
    speeds_df.plot(figsize=(10, 5), title="Vehicle Speeds Over Time", legend=True)
    plt.xlabel("Time")
    plt.ylabel("Speed")
    plt.show()

def plot_positions(vehicles, num_steps, dt):
    positions = {vehicle.id: [] for vehicle in vehicles}
    for i in range(num_steps):
        for vehicle in vehicles:
            vehicle.move(dt)
            positions[vehicle.id].append(vehicle.position)
        collisions = [other for other in vehicles if vehicle != other and vehicle.check_collision(other)]
        if collisions:
            print(f"Collision detected between vehicle {vehicle.id} and: {', '.join(other.id for other in collisions)}")

    # Create a pandas DataFrame
    positions_df = pd.DataFrame(positions)

    # Plot positions using matplotlib
    positions_df.apply(pd.Series.explode).plot.scatter(x=0, y=1, figsize=(10, 5), title="Vehicle Positions Over Time", legend=True)
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.show()

# Create vehicle instances
vehicle1 = Vehicle("V1", 65, (0, 0))
vehicle2 = Vehicle("V2", 50, (10, 20))
vehicle3 = Vehicle("V3", 35, (30, 50))
vehicle4 = Vehicle("V4", 20, (10, 50))
vehicle5 = Vehicle("V5", 95, (30, 10))
vehicle6 = Vehicle("V6", 70, (70, 10))

# Valid message test
message, hash_values, signature, pub_key = vehicle1.generate_message()
vehicle2.receive_message(message, hash_values.copy(), signature, pub_key)

# Invalid message test (tampered speed)
tampered_message = message.copy()
tampered_message["speed"] = 100
vehicle2.receive_message(tampered_message, hash_values.copy(), signature, pub_key)

# Simulate hash generation times
simulate([vehicle1, vehicle2], 0.1, 100)

# Plot speeds
plot_speeds([vehicle1, vehicle2], 100, 0.1)

# Plot positions
plot_positions([vehicle1, vehicle2], 100, 0.1)
