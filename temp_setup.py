import csv
import random
import typer
from datetime import datetime, timedelta


def generate_data(count: int, interval: int, temp_start: float, temp_end: float, temp_step: float):
    """Generate time, temperature, humidity, and CO2 values"""
    data = []
    new_time = datetime.now()
    for i in range(count):
        temperature = round(temp_start + i * temp_step, 2)
        if temperature > temp_end:
            break
        humidity = round(random.uniform(20, 50), 2)
        co2 = round(random.uniform(600, 700), 2)
        data.append((new_time.strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity, co2))
        new_time = new_time + timedelta(seconds=interval)
    return data


def write_to_csv(filename: str, data):
    """Write data to CSV file"""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'temperature', 'humidity', 'co2'])
        writer.writerows(data)


app = typer.Typer()

@app.command()
def main(count: int, interval: int, temp_start: float, temp_end: float, temp_step: float, filename: str):
    """Generate and write data to CSV file"""
    data = generate_data(count, interval, temp_start, temp_end, temp_step)
    write_to_csv(filename, data)
    typer.echo(f"time, temperature, humidity and co2 values written to {filename}")

# Here is an example command to run the typer app:
# Interval value given in seconds
# Temperature values are floating point numbers
# python temp_setup.py main --count 20 --interval 10 --temp_start 0 --temp_end 50 --temp_step 0.5 --filename data.csv
# 
python temp_setup.py 20 10 0 50 0.5 data.csv 
if __name__ == "__main__":
    app()
