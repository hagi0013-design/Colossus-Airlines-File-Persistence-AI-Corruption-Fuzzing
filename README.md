# Colossus-Airlines-File-Persistence-AI-Corruption-Fuzzing

# Colossus Airlines Reservation System



The original Colossus Airlines reservation system stored reservation data only in memory. Once the application was finished, all the reservation information was lost.

This project has the reservation system that implements persistent storage using C File I/O functions:

- fopen()
- fread()
- fwrite()
- fclose()

This is then saved to a binary file named:

flight_data.bin

When the program starts, it automatically attempts to load the flight information from the file.
If the file does not exist, both flight manifests are filled with empty seats.

When the user leaves the program, the complete flight state is automatically written back to disk.


The save file contains:

```c
typedef struct
{
    char magic[8];
    FlightData data;
} SaveFile;

The magic header stores COLAIR.
This allows the program to find corrupted files before attempting to use data.

File Validation & Error Recovery Analysis
The loading routine performs several validation checks before accepting saved data.

1. File Exists

flight_data.bin

If the file cannot be opened, the program makes the empty flight manifests.

2. File Size Verification

verify_File_Size(fp)

The actual file size needs to match
sizeof(SaveFile)
This detects
incomplete writes
oversized files
manually modified files

3. Header Validation

Verifies strcmp(save.magic, "COLAIR")

Files missing the correct header are rejected.

4. Fread Validation

readCount == 1

Partial reads caused by unexpected EOF are detected and rejected.

5. Seat Number Validation

Each seat number needs to be 
1 - 24

Invalid values mean there is corruption.

6. Reservation Flag Validation

Reservation status must be:

0 = available
1 = reserved


7. Passenger Name Validation

Passenger strings are forced to remain null-terminated:


s->passengername[name_len - 1] = '\0';


This prevents reading beyond array boundaries.

Recovery Strategy

If any validation fails:

Corrupted file rejected
Empty flight manifests created
Program continues running

This prevents crashes and undefined behavior caused by malformed files.

Pros & Cons
Pros
Very fast save and load operations
Compact storage
Not as complicated


Cons
Binary files are not human-readable
More difficult to debug manually
Binary vs Text Storage

Binary storage has excellent speed and efficiency but requires additional validation.

Text formats like CSV are easier to inspect and edit, but it needs more parsing code and larger file sizes.
