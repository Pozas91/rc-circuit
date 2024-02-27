from datetime import datetime
from threading import Timer

from RPi import GPIO
from pirc522 import RFID

from utils.database import insert_results

# Set up the GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Get instance of the RFID
rfid = RFID()

# Define a global variable to accumulate the data, and avoid send a request for each tag read
DATA = list()


def add_data(data: dict):
    global DATA
    DATA.append(data)


def clear_data():
    global DATA
    DATA.clear()


def main():
    # Initial call to send data
    send_data()

    while True:
        # Wait for tag
        rfid.wait_for_tag()

        # Request tag
        (error, tag_type) = rfid.request()

        if not error:
            # Try to avoid collision (several tags in the field)
            (error, uid) = rfid.anticoll()

            if not error:
                # Convert uid to string
                uid = ''.join(map(lambda s: str(s).rjust(3, '0'), uid))

                # Save this information into accumulated data
                add_data(data={
                    '_time': datetime.now().timestamp(),
                    'uid': uid,
                })

                # Print the uid
                print(f"Saving uid: {uid}")


def send_data():
    # Prepare a timer to send the data every 2 seconds
    Timer(10, send_data).start()

    if not DATA:
        return

    # Make a post request to the InfluxDB API using requests library
    try:
        # Get unique uid
        unique_ids = set(line['uid'] for line in DATA)

        # For each uid get min `_time` field
        relevant_data = [{
            'uid': uid,
            '_time': min(line['_time'] for line in DATA if line['uid'] == uid)
        } for uid in unique_ids]

        # Send the data
        insert_results(relevant_data)
        # Print information
        print("Data sent!")
    finally:
        # Clear the data list
        clear_data()


if __name__ == "__main__":
    main()
