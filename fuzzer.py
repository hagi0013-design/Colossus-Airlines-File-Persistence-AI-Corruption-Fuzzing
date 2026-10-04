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
`