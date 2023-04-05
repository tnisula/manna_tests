# manna_tests
Repository for delivering codes

test_csv_generator.py       Main app to generate csv-file.

test_csv_empty_values.py    App to write empty values to columns selected by the user.

test_csv_writer.py          Writes measurements points from csv-file to local db in Raspberry PI

# Usage
Usage: test_csv_generator.py [OPTIONS] COUNT INTERVAL RUUVI_INSIDE_TEMP_START RUUVI_INSIDE_HUM_START RUUVI_OUTSIDE_TEMP_START RUUVI_OUTSIDE_HUM_START HUM1000_TEMP_START HUM1000_HUM_START CO2_START FILENAME

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
  ACC1000_START             The start value for the ACC1000 sensor.
                            [required]
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
  --acc1000-end FLOAT             The end value for the ACC1000 sensor.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Here is an example command to run the typer app:
Interval value given in seconds
Temperature values are floating point numbers

# Example command:
python test_csv_generator.py --ruuvi-inside-temp-end 60 15 30 21.5 36 10 12 35 50 4000 0.01 data.csv

# Note: Negative temperatures!
python test_csv_generator.py 15 30 -- -21.5 36 10 12 35 50 4000 0.01 data.csv

# Writing empty values to the selected columns in csv file
python test_csv_empty_values.py data.csv output.csv --empty_columns=2,4,6,8

# Writing values from data.csv file to Raspberry using 30 seconds interval
python test_csv_writer.py data.csv 30
