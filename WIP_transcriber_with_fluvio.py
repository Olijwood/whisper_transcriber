import whisper
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import *
import os
import shutil
import splitclip
from fluvio import Fluvio, Offset


def transcribe(file):
    TOPIC_NAME = "transcription"
    PARTITION = 0

    splitclip.main()

    base_path_to_saved_files = "/Users/Oli/audio-transcriber-3/temp_audio_holder/"
    model = whisper.load_model("base")
    clips = splitclip.splitClip(file)

    for num in range(1, clips):
        with open(f"transcription_{num}.txt", "w") as f:
            path_to_saved_file = os.path.join(
                base_path_to_saved_files, f"temp_{num}.mp3"
            )
            audio_clip = AudioFileClip(path_to_saved_file)
            audio_clip.close()

            print(f"{clips - (num)} clips left to be transcribed.")

            result = model.transcribe(path_to_saved_file)

            line = result["text"].split(" ")
            for word in line:
                f.write(word + " ")

            directory_path = "/Users/Oli/audio-transcriber-3"
            shutil.move(
                f"{directory_path}/transcription_{num}.txt",
                f"{directory_path}/transcription/transcription_{num}.txt",
            )

        TOPIC_NAME = "transcription"

        os.popen("fluvio topic create {}".format(TOPIC_NAME))

        fluvio = Fluvio.connect()

        producer = fluvio.topic_producer(TOPIC_NAME)

        transcription_path = "/Users/Oli/audio-transcriber-3/transcription/"

        with open(str(transcription_path + f"transcription_{num}.txt"), "r") as g:
            text = g.read()
            producer.send_string(text)

        consumer = fluvio.partition_consumer(TOPIC_NAME, PARTITION)
        for record in consumer.stream(Offset.from_end(0)):
            print("{}".format(record.value_string()))
            break


def delete_temp_files():
    base_path_to_temp_files = "/Users/Oli/audio-transcriber-3/temp_audio_holder/"
    for temp_file in os.listdir(base_path_to_temp_files):
        os.remove(f"{base_path_to_temp_files}{temp_file}")
    base_path_to_time_files = "/Users/Oli/audio-transcriber-3/times/"
    for time_file in os.listdir(base_path_to_time_files):
        os.remove(f"{base_path_to_time_files}{time_file}")


def delete_audio_files():
    base_path_to_audio_files = "/Users/Oli/audio-transcriber-3/audio_files/"
    for audio_file in os.listdir(base_path_to_audio_files):
        os.remove(f"{base_path_to_audio_files}{audio_file}")


def main():
    path = "/Users/Oli/audio-transcriber-3/audio_files/"
    for file in os.listdir(path):
        suffix = ".mp3"
        if file.endswith(suffix):
            transcribe(os.path.join(path, file))
    delete_temp_files()
    delete_audio_files()


main()
