from RPi import GPIO
from pirc522 import RFID
from influxdb_client_3 import InfluxDBClient3, Point
import os

from dotenv import load_dotenv


# Load .env file variables
load_dotenv()

INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', '')
INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', '')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', '')

# Set up the GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Get instance of the RFID
rfid = RFID()

def main():
    client = InfluxDBClient3(host=INFLUXDB_HOST, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

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

                # Create a new point
                client.write(database=INFLUXDB_BUCKET, record=Point("rfid").tag("uid", uid))



if __name__ == "__main__":
    main()
