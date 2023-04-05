import json
import csv
import time
import typer
from datetime import datetime, date, timedelta
from copy import deepcopy

from libraries.influxdb_handler import HandleInfluxDB

DEVICE_CONFIGURATION_FILE = \
    "/home/pi/mannasw/local_device_config_sync/device_config.json"

# DEVICE_CONFIGURATION_FILE = \
#     "device_config.json"

with open(DEVICE_CONFIGURATION_FILE, "r") as f:
    conf = json.load(f)

device_code = conf['DEVICE_CODE']
sensors = conf['SENSOR_CONFIGURATION']
# for sensor in sensors:
#    print(sensor)

inf_local = conf['INFLUXDB_LOCAL_CONFIGURATION']
handler = HandleInfluxDB(
    influxdb_local_host=inf_local['INFLUXDB_LOCAL_HOST'],
    influxdb_local_port=inf_local['INFLUXDB_LOCAL_PORT'],
    influxdb_local_measurement=inf_local['INFLUXDB_LOCAL_MEASUREMENT'],
    influxdb_local_database=inf_local['INFLUXDB_LOCAL_DATABASE'],
    influxdb_local_username=inf_local['INFLUXDB_LOCAL_USERNAME'],
    influxdb_local_password=inf_local['INFLUXDB_LOCAL_PASSWORD'])


class CsvHandler:

    def __init__(self, influx_handler=handler, device_code=device_code):
        self.influx_handler = influx_handler
        self.device_code = device_code
        self.influx_data = None

    def generate_influx_data(self, row):
        self.influx_data = None
        results = []

        for sensor in sensors:
            measurement_tags = {}
            measurement_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            # print(measurement_time)

            if sensor.get("SENSOR_MODEL") == "ruuvi"  and sensor.get("SENSOR_LOCATION") == "inside":
                fields = {'temperature': float(row['ruuvi_inside_temp'] if row['ruuvi_inside_temp'] else 0), 
                          'humidity': float(row['ruuvi_inside_hum'] if row['ruuvi_inside_hum'] else 0)}
            elif sensor.get("SENSOR_MODEL") == "ruuvi"  and sensor.get("SENSOR_LOCATION") == "outside":
                fields = {'temperature': float(row['ruuvi_outside_temp'] if row['ruuvi_outside_temp'] else 0), 
                          'humidity': float(row['ruuvi_outside_hum'] if row['ruuvi_outside_hum'] else 0)}
            elif sensor.get("SENSOR_MODEL") == "HUM1000":
                fields = {'temperature': float(row['hum1000_temperature'] if row['hum1000_temperature'] else 0),
                          'humidity': float(row['hum1000_humidity'] if row['hum1000_humidity'] else 0)}
            elif sensor.get("SENSOR_MODEL") == "co2meter":
                fields = {'co2': float(row['co2meter'] if row['co2meter'] else 0)}
            elif sensor.get("SENSOR_MODEL") == "ACC1000":
                fields = {'acc': float(row['acc1000'] if row['acc1000'] else 0)}

            # print(fields)
            measurement_tags.update({
                'SENSOR_MODEL': sensor['SENSOR_MODEL'],
                'SENSOR_CODE': sensor['SENSOR_CODE'],
                'SENSOR_LOCATION': sensor['SENSOR_LOCATION'],
                'SENSOR_ADD_INFO': sensor['SENSOR_ADD_INFO'],
                'DEVICE_CODE': self.device_code})

            result = {
                "time": measurement_time,
                "measurement": inf_local['INFLUXDB_LOCAL_MEASUREMENT'],
                "tags": measurement_tags,
                "fields": fields
            }
            # print(result)
            results.append(deepcopy(result))
            self.influx_data = results

    def write_csv_data_to_database(self):
        # check that data available
        if not self.influx_data:
            raise Exception("No CSV data available")

        # write data to database
        self.influx_handler.write_data_local_database(self.influx_data)


app = typer.Typer()


@app.command()
def write_to_influxdb(file_path: str, interval: float):
    # Initialize influx handler etc.
    csv_handler = CsvHandler()

    # Open CSV file and read data
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        # rows = list(reader)

        for row in reader:
            csv_handler.generate_influx_data(row)
            csv_handler.write_csv_data_to_database()

            # Sleep for the specified interval before writing next data point
            time.sleep(interval)


if __name__ == "__main__":
    app()
