
import sys
import time
import base64
import random
import grpc

import lab6_pb2
import lab6_pb2_grpc

IMAGE_FILE = "Flatirons_Winter_Sunrise_edit_2.jpg"


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 grpc-client.py HOST COMMAND REPS")
        print("Commands: add, dotProduct, rawImage, jsonImage")
        sys.exit(1)

    host = sys.argv[1]
    command = sys.argv[2]
    reps = int(sys.argv[3])

    if reps <= 0:
        print("REPS must be a positive integer")
        sys.exit(1)

    address = f"{host}:50051"
    print(f"Running {reps} reps against {address}")

    # Create a connection and client stub.
    with grpc.insecure_channel(address) as channel:
        stub = lab6_pb2_grpc.Lab6Stub(channel)

        # Prepare the request data before timing repeated calls.
        if command == "add":
            operation = lambda: stub.add(
                lab6_pb2.addMsg(a=5, b=10)
            )

        elif command == "dotProduct":
            a = [random.random() for _ in range(100)]
            b = [random.random() for _ in range(100)]
            request = lab6_pb2.dotProductMsg(a=a, b=b)
            operation = lambda: stub.dotproduct(request)

        elif command == "rawImage":
            with open(IMAGE_FILE, "rb") as f:
                image_bytes = f.read()
            request = lab6_pb2.rawImageMsg(img=image_bytes)
            operation = lambda: stub.rawimage(request)

        elif command == "jsonImage":
            with open(IMAGE_FILE, "rb") as f:
                image_bytes = f.read()
            encoded_image = base64.b64encode(
                image_bytes
            ).decode("ascii")
            request = lab6_pb2.jsonImageMsg(img=encoded_image)
            operation = lambda: stub.jsonimage(request)

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

        # Warm up once so connection setup is excluded from the timing.
        result = operation()

        start = time.perf_counter()
        for _ in range(reps):
            result = operation()
        elapsed = time.perf_counter() - start

        print(f"Last response: {result}")
        print(f"Took {elapsed * 1000 / reps:.3f} ms per operation")


if __name__ == "__main__":
    main()
