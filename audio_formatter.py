from pydub import AudioSegment
import os
import time

def audioFormatter():
    cwd = os.getcwd()
    unformatted_dir = f'{cwd}/unformatted_audio/'
    formatted_dir = f'{cwd}/audio_files/'
    formatted_wav_dir = f'{cwd}/formatted_wav_file/'
    if not os.path.isdir(unformatted_dir):
        os.mkdir(unformatted_dir)
    if not os.path.isdir(formatted_wav_dir):
        os.mkdir(formatted_wav_dir)
    for file in os.listdir(unformatted_dir):
        if file.endswith('.wav'):
            given_audio = AudioSegment.from_file(f'{unformatted_dir}{file}', format='wav')
            given_audio.export(f'{formatted_wav_dir}{file.rstrip(".wav") + "_processed.wav"}', format="wav", codec="pcm_s16le", parameters=["-ac", "1", '-ar', '16000', '-b:a', '256k'])
            for wav_file in os.listdir(formatted_wav_dir):
                if file.endswith('.wav'):
                    formatted_audio = AudioSegment.from_file(f'{formatted_wav_dir}{wav_file}', format='wav')
                    formatted_audio.export(f'{formatted_dir}{wav_file.rstrip(".wav")+".mp3"}', format='mp3')
                    time.sleep(3)
                    for i in os.listdir(unformatted_dir):
                        os.remove(f'{unformatted_dir}{i}')
                    for i in os.listdir(formatted_wav_dir):
                        os.remove(f'{formatted_wav_dir}{i}')
            
        elif file.endswith('.mp4'):
            given_audio = AudioSegment.from_file(f'{unformatted_dir}{file}', format='mp4')
            given_audio.export(f'{formatted_dir}{file.rstrip(".mp4")}.mp3', format="mp3")

audioFormatter()
