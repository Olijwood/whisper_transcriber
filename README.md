This is my code for audio transcription. When you run App.py it runs a server on Flask that you can access on the internet with '127.0.0.1:5000'. This IP Address takes you to the landing page which consists of a ‘choose file’ and ‘upload’ button. Currently this transcription service only works with '.mp3' files. I originally chose '.wav' but they tend to take up more storage and aren't as common as '.mp3' files. The upload works via Javascript and Flask, saving the file to the 'audio_files' directory.

Once you upload a file it is stored in the 'audio_files' directory and 'splitClip.py' is first run on that file. It generates time-codes of (currently) 30s chunks of the duration of the audio-file + remainder (I may wish to change this to something shorter so that the transcription can be sent to the Fluvio Topic in smaller chunks). These time codes break the audio file down into temp-files (or chunks) that are stored temporarily in 'temp_audio_holder'.

The Whisper model is then loaded in, I chose 'base' for the sake of speed/accuracy. 
(More on Whisper documentation here: https://github.com/openai/whisper if you wish to looking into more accurate models provided by Whisper). The code then cycles through each temp-file and transcribes that file to 'transcription.txt'. Once it starts transcribing, you can see how many clips you have left to be transcribed in the terminal. Once the transcription is finished, some admin functions are run to delete the original audio-file, the temporary audio-files and the 'times.txt'.

I've been testing the code with a 10.2MB podcast and this 'base' Whisper Model seems to be accurate enough. I don't reccomend changing splitClip to make your temp-files any longer than 60s as the Whisper model may struggle past this point.

Currently the transcription is returned to the user via JSON, I haven't figured out a way to simply display the txt file without also showing {response: (transcription) }.


(WIP) IMPLEMENTING FLUVIO:

  Fluvio provides low-latency, high-performance programmable streaming on cloud-native                   architecture. I would like to transcribe the file as it's being uploaded. Currently in my '(WIP)transcriber with fluvio.py' I have implemented Fluvio to some extent. When run, after transcribing the first clip of the audio-file the function creates the topic 'Transcription', reads the 'transcription_{x}.txt' file and produces that chunk of the transcription to the topic. 
  
Currently I am unclear as to how I could return these chunks of the transcription to the user, live, as the transcription is taking place. I also wonder if it's slightly cheating as it isn't taking place as the audio-file is being uploaded, rather as the audio-file is being transcribed. However, this does provide the possibility to watch your audio-file be transcribed (allbeit in chunks) as the file is being transcribed.

(WIP) IMPLEMENTING DEEP SPEECH (MOZILLA)

 I am currently working on trying another transcription library (Deep Speech) to see if it is faster than Whisper whilst still being accurate and providing punctuation.


