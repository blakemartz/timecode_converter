import csv
import math
import pandas as pd
from prettytable import PrettyTable


def timecode_to_frames(timecode, fps):
    hours, minutes, seconds, frames = map(int, timecode.split(':'))
    total_frames = (hours * 3600 + minutes * 60 + seconds) * fps + frames
    return total_frames


def frames_to_timecode(frames, fps):
    frames = int(round(frames))
    hours = frames // (3600 * fps)
    frames %= 3600 * fps
    minutes = frames // (60 * fps)
    frames %= 60 * fps
    seconds = frames // fps
    frames %= fps
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def convert_timecode(timecode):
    frames_2398 = timecode_to_frames(timecode, 23.98)
    frames_2997 = frames_2398 * (30000 / 1001) / (24000 / 1001)

    drop_frames = math.floor(frames_2997 / 17982) * 18 + math.floor((frames_2997 % 17982) / 1798)
    frames_2997_adjusted = frames_2997 + drop_frames
    timecode_2997 = frames_to_timecode(frames_2997_adjusted, 30)

    return timecode_2997.replace(':', ';', 2)


input_csv = 'input_timecodes.csv'
output_csv = 'output_timecodes.csv'

# Read the Adobe timecodes CSV file
adobe_timecodes = []
with open('adobe_timecodes.csv', 'r') as adobe_file:
    adobe_reader = csv.reader(adobe_file)
    for row in adobe_reader:
        adobe_timecodes.append(row[1])  # Assuming the second column contains the timecodes

# Process the input and output CSV files
with open(input_csv, 'r') as infile, open(output_csv, 'w') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    for index, row in enumerate(csv_reader):
        timecode_2398 = row[0]
        timecode_2997 = convert_timecode(timecode_2398)
        csv_writer.writerow([timecode_2398, timecode_2997, adobe_timecodes[index]])

# Read the output CSV file using pandas
df = pd.read_csv(output_csv, header=None, names=['Timecode 23.98', 'Timecode 29.97 Df', 'Adobe 29.97 Df'])

# Display the DataFrame
# print(df)

# Create a PrettyTable instance
table = PrettyTable()

# Set the field names of the table
table.field_names = ['23.98 fps', '29.97 Df', 'Adobe 29.97 DF']

# Add the rows to the table
for index, row in df.iterrows():
    table.add_row(row)

# Display the PrettyTable
print(table)
