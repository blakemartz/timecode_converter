import csv
import math


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
    frames_2398 = timecode_to_frames(timecode, 23.976)  # Use the exact frame rate
    time_in_seconds = frames_2398 * (1001 / 24000)  # Convert to real-time (in seconds)

    # Convert real-time to frames at 29.97 fps drop-frame
    frames_2997 = time_in_seconds * (30000 / 1001)
    drop_frames = 2 * math.floor(frames_2997 / 1800) - math.floor(math.floor(frames_2997 / 1800) / 10)

    frames_2997_adjusted = round(frames_2997 - drop_frames)
    timecode_2997 = frames_to_timecode(frames_2997_adjusted, 30)

    return timecode_2997.replace(':', ';', 2)


input_csv = 'input_timecodes.csv'
output_csv = 'output_timecodes_accu.csv'

with open(input_csv, 'r') as infile, open(output_csv, 'w') as outfile:
    csv_reader = csv.reader(infile)
    csv_writer = csv.writer(outfile)

    for row in csv_reader:
        timecode_2398 = row[0]
        timecode_2997 = convert_timecode(timecode_2398)
        csv_writer.writerow([timecode_2398, timecode_2997])
