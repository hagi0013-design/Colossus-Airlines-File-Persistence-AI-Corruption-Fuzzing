I told the AI to generate a python script named fuzzer.py that creates multiple corrupted
binary save files for a C airline reservation application.

The fuzzer should create:
2. Files with appended and  extra bytes.
3. Random non-printable binary data.
4. Invalid seat numbers.
5. Invalid reservation flags.
6. Corrupted passenger-name fields.

The goal is to stress test the file-loading code for
fread(), binary struct deserialization,
and also the corruption detection.


import os
import random

SAVE_FILE = "flight_data.bin"

def make_truncated_file():
    with open("corrupt_truncated.bin", "wb") as f:
        f.write(os.urandom(100))

    print("Created corrupt_truncated.bin")


def make_oversized_file():
    with open("corrupt_oversized.bin", "wb") as f:
        f.write(os.urandom(5000))

    print("Created corrupt_oversized.bin")


def make_garbage_data_file():
    with open("corrupt_garbage.bin", "wb") as f:
        data = bytearray(os.urandom(2000))

        for i in range(100):
            position = random.randint(0, len(data) - 1)

            data[position] = random.randint(128, 255)

        f.write(data)

    print("Created corrupt_garbage.bin")


def make_bad_seat_file():
    data = bytearray(os.urandom(2000))

    for i in range(25):
        position = random.randint(0, len(data) - 4)

        bad_seat = random.choice([0, -5, 99, 9999])

        data[position:position+4] = (
            int(bad_seat).to_bytes(
                4,
                byteorder="little",
                signed=True
            )
        )

    with open("corrupt_seatnums.bin", "wb") as f:
        f.write(data)

    print("Created corrupt_seatnums.bin")


def make_bad_flags_file():
    data = bytearray(os.urandom(2000))

    for i in range(25):
        position = random.randint(0, len(data) - 4)

        bad_flag = random.choice([
            2,
            3,
            10,
            999,
            -1
        ])

        data[position:position+4] = (
            int(bad_flag).to_bytes(
                4,
                byteorder="little",
                signed=True
            )
        )

    with open("corrupt_flags.bin", "wb") as f:
        f.write(data)

    print("Created corrupt_flags.bin")


def add_extra_bytes():
    with open("corrupt_extra_bytes.bin", "wb") as f:
        f.write(os.urandom(2000))

        f.write(b"THIS_SHOULD_NOT_BE_HERE")

    print("Created corrupt_extra_bytes.bin")


if __name__ == "__main__":
    make_truncated_file()
    make_oversized_file()
    make_garbage_data_file()
    make_bad_seat_file()
    make_bad_flags_file()
    add_extra_bytes()

    print("\nAll corrupted test files generated.")


    The AI-generated fuzzer created:

corrupt_truncated.bin
corrupt_oversized.bin
corrupt_garbage.bin
corrupt_seatnums.bin
corrupt_flags.bin
corrupt_extra_bytes.bin
Problems Discovered

Testing revealed lots of failures:

Invalid seat numbers
Invalid reservation flags
Unexpected EOF during reads
Random binary data in passenger records

Fixes Implemented



Magic header verification
Seat number validation
Reservation flag validation
Passenger-name sanitization
Recovery through reinitialization
']='

The final program that I made rejects corrupted files and rebuilds the clean flight manifests instead of crashing.