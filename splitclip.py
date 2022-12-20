from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
import os
import time
import shutil

def generateTimeCodes(filename):
    dir_path = os.getcwd()
    target = f"{dir_path}/audio_files/"
    if not os.path.isdir(target):
        os.mkdir(target)
    for i in os.listdir(target):
        file = i
    audio = AudioFileClip(str(target + file))
    length = round(audio.duration)
    print(f"{length} seconds")

    time_codes = []
    prev_num = 0
    for num in range(length):
        if num % 30 == 0 and num != 0:
            time_codes.append((prev_num, num))
            prev_num = num

    remainder = length - time_codes[-1][-1]
    time_codes.append((time_codes[-1][-1], time_codes[-1][-1] + remainder))

    with open(f"{filename}_time.txt", "w") as f:
        for index in time_codes:
            f.write(f"{index[0]}-{index[1]}\n")

    times_target = f"{dir_path}/times/"
    if not os.path.isdir(times_target):
        os.mkdir(times_target)
    shutil.move(f"{filename}_time.txt", f"{times_target}{file}_time.txt")


def splitClip(filename):
    dir_path = os.getcwd()
    target = f"{dir_path}/audio_files/"
    for i in os.listdir(target):
        file = i
    required_video_file = "{}".format(filename)
    counter = 1
    times_target = f"{dir_path}/times/"
    with open(f"{times_target}{file}_time.txt", "r") as f:
        times = f.readlines()
    times = [x.strip() for x in times]
    for t in times:
        start_time = int(t.split("-")[0])
        end_time = int(t.split("-")[1])
        temp_target = f"{dir_path}/temp_audio_holder/"
        if not os.path.isdir(temp_target):
            os.mkdir(temp_target)
        temp_saving_location = f"{temp_target}temp_{counter}.mp3"
        counter += 1
        ffmpeg_extract_subclip(
            required_video_file, start_time, end_time, targetname=temp_saving_location
        )
        num_of_clips = times.index(t) + 1
    return num_of_clips


def main():
    dir_path = os.getcwd()
    target = f"{dir_path}/audio_files/"
    for filename in os.listdir(target):
        generateTimeCodes(os.path.join(target, filename))
        time.sleep(2)
        splitClip(os.path.join(target, filename))


if __name__ == "__main__":
    main()
