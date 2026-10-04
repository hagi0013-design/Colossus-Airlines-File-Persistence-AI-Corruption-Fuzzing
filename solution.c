

#define max_seats 24
#define name_len 50

typedef struct
{
    int seatnum;
    int reserved;
    char passengername[name_len];
} Seat;

typedef struct
{
    Seat outbound[max_seats];
    Seat inbound[max_seats];
} FlightData;

typedef struct
{
    char magic[8];
    FlightData data;
} SaveFile;


/* Set up all seats */
void set_up_Flights(FlightData *flights)
{
    for (int i = 0; i < max_seats; i++)
    {
        /* Outbound */
        flights->outbound[i].seatnum = i + 1;
        flights->outbound[i].reserved = 0;
        flights->outbound[i].passengername[0] = '\0';

        /* Inbound */
        flights->inbound[i].seatnum = i + 1;
        flights->inbound[i].reserved = 0;
        flights->inbound[i].passengername[0] = '\0';
    }
}


/* Validate one seat */
int validateseats(Seat *s)
{
    if (s == NULL)
        return 0;

    /* Check seat number */
    if (s->seatnum < 1 || s->seatnum > max_seats)
        return 0;

    /* Check reserved flag */
    if (s->reserved != 0 && s->reserved != 1)
        return 0;

    /*
     * Make sure passengername is null-terminated.
     * Since the array has 50 characters, force the
     * last character to '\0'.
     */
    s->passengername[name_len - 1] = '\0';

    /*
     * An unreserved seat should not have a passenger name.
     */
    if (s->reserved == 0 && strlen(s->passengername) > 0)
        return 0;

    /*
     * A reserved seat should have a passenger name.
     */
    if (s->reserved == 1 && strlen(s->passengername) == 0)
        return 0;

    return 1;
}


/* Verify file size */
int verify_File_Size(FILE *fp)
{
    long size;

    if (fp == NULL)
        return 0;

    if (fseek(fp, 0, SEEK_END) != 0)
        return 0;

    size = ftell(fp);

    if (size == -1)
        return 0;

    rewind(fp);

    if (size != (long)sizeof(SaveFile))
        return 0;

    return 1;
}


/* Load flight data */
int loadFlights(FlightData *flights)
{
    FILE *fp;
    SaveFile save;
    size_t readCount;

    fp = fopen("flight_data.bin", "rb");

    if (fp == NULL)
    {
        printf("No save file found. Starting fresh.\n");
        set_up_Flights(flights);
        return 0;
    }

    if (!verify_File_Size(fp))
    {
        printf("ERROR: Unexpected file size.\n");
        fclose(fp);

        set_up_Flights(flights);
        return -1;
    }

    readCount = fread(&save, sizeof(SaveFile), 1, fp);

    fclose(fp);

    if (readCount != 1)
    {
        printf("ERROR: File unreadable.\n");

        set_up_Flights(flights);
        return -1;
    }

    /*
     * Check file header.
     */
    if (strcmp(save.magic, "COLAIR") != 0)
    {
        printf("ERROR: Invalid file header.\n");

        set_up_Flights(flights);
        return -1;
    }

    /*
     * Validate every outbound and inbound seat.
     */
    for (int i = 0; i < max_seats; i++)
    {
        if (!validateseats(&save.data.outbound[i]))
        {
            printf("ERROR: Corrupted outbound seat data.\n");

            set_up_Flights(flights);
            return -1;
        }

        if (!validateseats(&save.data.inbound[i]))
        {
            printf("ERROR: Corrupted inbound seat data.\n");

            set_up_Flights(flights);
            return -1;
        }
    }

    /*
     * Copy loaded data into flights.
     */
    *flights = save.data;

    printf("Flight data loaded successfully.\n");

    return 1;
}


/* Save flight data */
int saveFlights(FlightData *flights)
{
    FILE *fp;
    SaveFile save;
    size_t written;

    fp = fopen("flight_data.bin", "wb");

    if (fp == NULL)
    {
        printf("ERROR: Cannot write save file.\n");
        return 0;
    }

    /*
     * Initialize the entire structure first.
     */
    memset(&save, 0, sizeof(SaveFile));

    /*
     * File header.
     */
    strcpy(save.magic, "COLAIR");

    /*
     * Copy flight data.
     */
    save.data = *flights;

    /*
     * Write the structure.
     */
    written = fwrite(&save, sizeof(SaveFile), 1, fp);

    fclose(fp);

    if (written != 1)
    {
        printf("ERROR: Save has failed.\n");
        return 0;
    }

    printf("Flight data saved.\n");

    return 1;
}