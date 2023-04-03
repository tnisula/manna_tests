import csv
import typer
from datetime import datetime, timedelta

"""
Usage: test_csv_generator.py [OPTIONS] COUNT INTERVAL 
                            RUUVI_INSIDE_TEMP_START RUUVI_INSIDE_HUM_START 
                            RUUVI_OUTSIDE_TEMP_START RUUVI_OUTSIDE_HUM_START 
                            HUM1000_TEMP_START HUM1000_HUM_START 
                            CO2_START 
                            FILENAME

Arguments:
  COUNT                     The count of the test value lines in csv.
                            [required]
  INTERVAL                  The time interval in seconds.  [required]
  RUUVI_INSIDE_TEMP_START   The start value of the ruuvi inside temperature.
                            [required]
  RUUVI_INSIDE_HUM_START    The start value of the ruuvi inside humidity.
                            [required]
  RUUVI_OUTSIDE_TEMP_START  The start value of the ruuvi outside temperature.
                            [required]
  RUUVI_OUTSIDE_HUM_START   The start value of the ruuvi outside humidity.
                            [required]
  HUM1000_TEMP_START        The start value of the hum1000 temperature.
                            [required]
  HUM1000_HUM_START         The start value of the hum1000 humidity.
                            [required]
  CO2_START                 The start value of the co2meter.  [required]
  FILENAME                  The filename of the csv file  [required]

Options:
  --ruuvi-inside-temp-end FLOAT   The end value of the ruuvi inside
                                  temperature.
  --ruuvi-inside-hum-end FLOAT    The end value of the ruuvi inside humidity.
  --ruuvi-outside-temp-end FLOAT  The end value of the ruuvi outside
                                  temperature.
  --ruuvi-outside-hum-end FLOAT   The end value of the ruuvi outside humidity.
  --hum1000-temp-end FLOAT        The end value of the hum1000 temperature.
  --hum1000-hum-end FLOAT         The end value of the hum1000 humidity.
  --co2-end FLOAT                 The end value of the co2meter.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
"""


def generate_data(count: int, interval: int, 
                  ruuvi_inside_temp_start: float, ruuvi_inside_temp_end: float,
                  ruuvi_inside_hum_start: float, ruuvi_inside_hum_end: float,
                  ruuvi_outside_temp_start: float, ruuvi_outside_temp_end: float,
                  ruuvi_outside_hum_start: float, ruuvi_outside_hum_end: float,
                  hum1000_temp_start: float, hum1000_temp_end: float,
                  hum1000_hum_start: float, hum1000_hum_end: float,
                  co2_start: float, co2_end: float):
                        
    """
    Generate time, temperature, humidity, and CO2 values
    """
    data = []
    new_time = datetime.now()
    ruuvi_inside_temp_step = round((ruuvi_inside_temp_end - ruuvi_inside_temp_start) / count, 1)
    ruuvi_inside_hum_step = round((ruuvi_inside_hum_end - ruuvi_inside_hum_start) / count, 1)
    ruuvi_outside_temp_step = round((ruuvi_outside_temp_end - ruuvi_outside_temp_start) / count, 1)
    ruuvi_outside_hum_step = round((ruuvi_outside_hum_end - ruuvi_outside_hum_start) / count, 1)
    
    hum1000_temp_step = round((hum1000_temp_end - hum1000_temp_start) / count, 1)
    hum1000_hum_step = round((hum1000_hum_end - hum1000_hum_start) / count, 1)
    co2_step = round((co2_end - co2_start) / count, 1)

    for i in range(count):
        ruuvi_inside_temperature = round(ruuvi_inside_temp_start + i * ruuvi_inside_temp_step, 2)
        ruuvi_inside_humidity = round(ruuvi_inside_hum_start + i * ruuvi_inside_hum_step, 2)
        ruuvi_outside_temperature = round(ruuvi_outside_temp_start + i * ruuvi_outside_temp_step, 2)
        ruuvi_outside_humidity = round(ruuvi_outside_hum_start + i * ruuvi_outside_hum_step, 2)
        hum1000_temperature = round(hum1000_temp_start + i * hum1000_temp_step, 1)
        hum1000_humidity = round(hum1000_hum_start + i * hum1000_hum_step, 1)
        co2 = round(co2_start + i * co2_step, 2)
        data.append((new_time.strftime("%Y-%m-%d %H:%M:%S"),
                    ruuvi_inside_temperature, ruuvi_inside_humidity,
                    ruuvi_outside_temperature, ruuvi_outside_humidity,
                    hum1000_temperature, hum1000_humidity,
                    co2))
        new_time = new_time + timedelta(seconds=interval)
    return data


def write_to_csv(filename: str, data):
    """
    Write data to CSV file
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'ruuvi_inside_temp', 'ruuvi_inside_hum', 
                        'ruuvi_outside_temp', 'ruuvi_outside_hum', 
                        'hum1000_temperature', 'hum1000_humidity', 'co2meter'])
        writer.writerows(data)


app = typer.Typer()


@app.command()
def main(count: int = typer.Argument(..., help="The count of the test value lines in csv."),
        interval: int = typer.Argument(...,
                                    help="The time interval in seconds."),
        ruuvi_inside_temp_start: float = typer.Argument(...,
                                help="The start value of the ruuvi inside temperature."),
        ruuvi_inside_temp_end: float = typer.Option(None, 
                                help="The end value of the ruuvi inside temperature."),
        ruuvi_inside_hum_start: float = typer.Argument(...,
                                help="The start value of the ruuvi inside humidity."),
        ruuvi_inside_hum_end: float = typer.Option(None, 
                                help="The end value of the ruuvi inside humidity."),
        ruuvi_outside_temp_start: float = typer.Argument(...,
                                help="The start value of the ruuvi outside temperature."),
        ruuvi_outside_temp_end: float = typer.Option(None, 
                                help="The end value of the ruuvi outside temperature."),
        ruuvi_outside_hum_start: float = typer.Argument(...,
                                help="The start value of the ruuvi outside humidity."),
        ruuvi_outside_hum_end: float = typer.Option(None, 
                                help="The end value of the ruuvi outside humidity."),
        hum1000_temp_start: float = typer.Argument(...,
                                help="The start value of the hum1000 temperature."),
        hum1000_temp_end: float = typer.Option(None, 
                                help="The end value of the hum1000 temperature."),
        hum1000_hum_start: float = typer.Argument(...,
                                help="The start value of the hum1000 humidity."),
        hum1000_hum_end: float = typer.Option(None, 
                                help="The end value of the hum1000 humidity."),
        co2_start: float = typer.Argument(...,
                                help="The start value of the co2meter."),
        co2_end: float = typer.Option(None, help="The end value of the co2meter."),
        filename: str = typer.Argument(..., help="The filename of the csv file")):

    if not ruuvi_inside_temp_end:
        ruuvi_inside_temp_end = ruuvi_inside_temp_start
    if not ruuvi_inside_hum_end:
        ruuvi_inside_hum_end = ruuvi_inside_hum_start
    if not ruuvi_outside_temp_end:
        ruuvi_outside_temp_end = ruuvi_outside_temp_start
    if not ruuvi_outside_hum_end:
        ruuvi_outside_hum_end = ruuvi_outside_hum_start

    if not hum1000_temp_end:
        hum1000_temp_end = hum1000_temp_start
    if not hum1000_hum_end:
        hum1000_hum_end = hum1000_hum_start

    if not co2_end:
        co2_end = co2_start

    """
    Generate and write data to CSV file
    """
    data = generate_data(count, interval, 
                        ruuvi_inside_temp_start, ruuvi_inside_temp_end, 
                        ruuvi_inside_hum_start, ruuvi_inside_hum_end,
                        ruuvi_outside_temp_start, ruuvi_outside_temp_end, 
                        ruuvi_outside_hum_start, ruuvi_outside_hum_end,
                        hum1000_temp_start, hum1000_temp_end, 
                        hum1000_hum_start, hum1000_hum_end,
                        co2_start, co2_end)
    write_to_csv(filename, data)
    typer.echo(
        f"time, ruuvi inside, ruuvi outside, hum1000 and co2meter values written to {filename}")


# Here is an example command to run the typer app:
# Interval value given in seconds
# Temperature values are floating point numbers
# python test_csv_generator.py 20 10 21.5 --ruuvi-inside-temp-end 50                        
#                              4000 --ruuvi-inside-hum-end 5000
#                              11.5
#                              5500
#                              
# 60 --hum-end 80 4000 --co2-end 8000 data.csv
# python test_csv_generator.py 
# 20 10 21.5 --ruuvi-inside-temp-end 50                     
# 4000 --ruuvi-inside-hum-end 5000
# 11.5 5500 22 644

if __name__ == "__main__":
    app()
