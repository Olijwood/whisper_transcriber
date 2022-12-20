import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import *
import os
import shutil
import splitclip


def transcribe(file):
    splitclip.main()
    dir_path = os.getcwd()
    base_path_to_temp_files = f"{dir_path}/temp_audio_holder/"
    if not os.path.isdir(base_path_to_temp_files):
        os.mkdir(base_path_to_temp_files)
    model = whisper.load_model("base")
    with open(f"transcription.txt", "w") as f:
        clips = splitclip.splitClip(file)
        print(f"Number of clips: {clips}")
        for num in range(1, clips):
            path_to_saved_file = os.path.join(
                base_path_to_temp_files, f"temp_{num}.mp3"
            )
            audio_clip = AudioFileClip(path_to_saved_file)
            audio_clip.close()

            print(f"{clips - (num)} clips left to be transcribed.")

            result = model.transcribe(path_to_saved_file)

            line = result["text"].split(" ")
            for word in line:
                f.write(word + " ")

        transcription_path = f"{dir_path}/transcription/"
        shutil.move(
            f"{dir_path}/transcription.txt", f"{transcription_path}transcription.txt"
        )


def delete_files():
    dir_path = os.getcwd()
    base_path_to_temp_files = f"{dir_path}/temp_audio_holder/"
    for temp_file in os.listdir(base_path_to_temp_files):
        os.remove(f"{base_path_to_temp_files}{temp_file}")

    base_path_to_time_files = f"{dir_path}/times/"
    for time_file in os.listdir(base_path_to_time_files):
        os.remove(f"{base_path_to_time_files}{time_file}")

    base_path_to_audio_files = f"{dir_path}/audio_files/"
    for audio_file in os.listdir(base_path_to_audio_files):
        os.remove(f"{base_path_to_audio_files}{audio_file}")


def main():
    dir_path = os.getcwd()
    path = f"{dir_path}/audio_files/"

    for file in os.listdir(path):
        suffix = ".mp3"
        if file.endswith(suffix):
            transcribe(os.path.join(path, file))

    delete_files()


main()
