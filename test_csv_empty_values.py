import argparse
import csv

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate CSV file with empty values')
    parser.add_argument('input_file', type=str, help='Input CSV file')
    parser.add_argument('output_file', type=str, help='Output CSV file')
    parser.add_argument('--empty_columns', type=str, help='Comma-separated list of columns to empty', default='')

    args = parser.parse_args()

    # Read input file
    with open(args.input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read header row
        data = list(reader)    # Read remaining rows

    # Get indices of columns to empty
    empty_cols = []
    if args.empty_columns:
        empty_cols = [int(x) for x in args.empty_columns.split(',')]

    # Write output file with empty values in selected columns
    with open(args.output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in data:
            for i, value in enumerate(row):
                if i in empty_cols:
                    row[i] = ''
            writer.writerow(row)

if __name__ == '__main__':
    main()

# python test_csv_empty_values.py input.csv output.csv --empty_columns=1,2

