import csv
import typer
from datetime import datetime, timedelta


def generate_data(count: int, interval: int, 
                  temp_start: float, temp_end: float,
                  hum_start: float, hum_end: float,
                  co2_start: float, co2_end: float):
    """
    Generate time, temperature, humidity, and CO2 values
    """
    data = []
    new_time = datetime.now()
    temp_step = round((temp_end - temp_start) / count, 1)
    hum_step = round((hum_end - hum_start) / count, 1)
    co2_step = round((co2_end - co2_start) / count, 1)

    for i in range(count):
        temperature = round(temp_start + i * temp_step, 2)
        # if temperature > temp_end:
        #    break
        humidity = round(hum_start + i * hum_step, 1)
        co2 = round(co2_start + i * co2_step, 2)
        data.append((new_time.strftime("%Y-%m-%d %H:%M:%S"),
                    temperature, humidity, co2))
        new_time = new_time + timedelta(seconds=interval)
    return data


def write_to_csv(filename: str, data):
    """
    Write data to CSV file
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'temperature', 'humidity', 'co2'])
        writer.writerows(data)


app = typer.Typer()


@app.command()
def main(count: int = typer.Argument(..., help="The count of the lines in csv."),
         interval: int = typer.Argument(...,
                                        help="The time interval in seconds."),
         temp_start: float = typer.Argument(...,
                                            help="The start value of the temperature."),
         temp_end: float = typer.Option(None, help="The end value of the temperature."),
         hum_start: float = typer.Argument(...,
                                            help="The start value of the humidity."),
         hum_end: float = typer.Option(None, help="The end value of the humidity."),
         co2_start: float = typer.Argument(...,
                                            help="The start value of the co2."),
         co2_end: float = typer.Option(None, help="The end value of the co2."),
         filename: str = typer.Argument(..., help="The filename of the csv file")):
    """
    Generate and write data to CSV file
    """
    if not temp_end:
        temp_end = temp_start
    if not hum_end:
        hum_end = hum_start
    if not co2_end:
        co2_end = co2_start
    data = generate_data(count, interval, temp_start, 
                         temp_end, hum_start, hum_end, 
                         co2_start, co2_end)
    write_to_csv(filename, data)
    typer.echo(
        f"time, temperature, humidity and co2 values written to {filename}")


# Here is an example command to run the typer app:
# Interval value given in seconds
# Temperature values are floating point numbers
# python temp_setup2.py 20 10 21.5 --temp-end 50 60 --hum-end 80 4000 --co2-end 8000 data.csv

if __name__ == "__main__":
    app()
