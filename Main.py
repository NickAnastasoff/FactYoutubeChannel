#!/usr/bin/python3
import sys
import cv2
import random
import moviepy.editor as mp
import os
from gpt4allj import Model
model = Model(pathToGpt4all)
from youtube import upload
from constants import *

music = mp.AudioFileClip(f"{pathToMusic}/{(random.choice([f for f in os.listdir(pathToMusic) if not f.endswith('.DS_Store')]))}")


def textBox(text, fontsize, backOpacity, y, width, height, duration, startTime, w, h, Ratio):
        # Create a text clip
        text_clip = mp.TextClip(text, font='Amiri-regular', color='white', fontsize=fontsize * Ratio, size=((phonewidth-width) * Ratio, (height) * Ratio), method='caption')

        # Add a background color to the text clip
        text_clip = text_clip.on_color(size=(text_clip.w, text_clip.h+20), color=(0,0,0), pos=(0,'center'), col_opacity=backOpacity)

        # Move the text clip to the desired position
        text_clip = text_clip.set_pos(lambda t: ((w-text_clip.w)/2, (h-text_clip.h)/y))

        # Set the duration of the text clip
        text_clip = text_clip.set_duration(duration)

        # Set the start time of the text clip
        text_clip = text_clip.set_start(startTime)

        return text_clip

while True:
    with open('settings.json') as json_file:
        data = json.load(json_file)
        channel_topics = data['channel_topics'][0]
        random_topic = random.choice(list(channel_topics.keys()))
        array_data = channel_topics[random_topic]
        random_element = random.choice(array_data)

    musicDuration = music.duration
    start_time = random.uniform(0, musicDuration - videoLength)
    clip = music.subclip(start_time, start_time + videoLength)
    clip.write_audiofile("random_clip.wav")

    # get the video file
    videoFile = random.choice(os.listdir(pathToVideos))
    openingPrompt = 'Psychology Fact: Did you know that according to psychology, people who talk to themselves...STOP Sports fact: Only one sport has been played on the moon...STOP Productivity Fact: The most most productive day of the week is...STOP ' + str(random_topic) + ':'
    openingText = model.generate(openingPrompt,
               seed=-1,
               n_threads=-1,
               n_predict=50,
               top_k=40,
               top_p=0.9,
               temp=.7,
               n_batch=8)
    openingText = openingText[:openingText.find("STO")]
    endingPrompt = 'Psychology Fact: Did you know that according to psychology, people who talk to themselves...  ending text: are more likely to have a high IQ. Talking to yourself makes your brain work more efficiently, and can help control emotions!STOP Sports fact: Only one sport has been played on the moon... ending text: 50 years ago, Alan Shepardan, an Apollo 14 astronaut, played golf on the moon, and he hit over 10 miles!STOP Productivity Fact: The most most productive day of the week is... ending text: Thursday! After 40 hours of work per week, productivity decreases by 50%, and who really feels productive on Monday?STOP ' + str(random_topic) + ': ' + openingText + 'ending text:'
    endingText = model.generate(endingPrompt,
               seed=-1,
               n_threads=-1,
               n_predict=50,
               top_k=40,
               top_p=0.9,
               temp=.7,
               n_batch=8)
    Title = str(random_topic).upper()

    print("video title: " + Title)

    path = pathToVideos + random_element
    files = os.listdir(path)
    files = [f for f in files if not f.endswith('.DS_Store')]
    randomFile = random.choice(files)
    print("files in folder: " + str(files))
    print("chosen file: " + randomFile)

    clip = mp.VideoFileClip(pathToVideos + random_element + "/" + randomFile)
    videoDuration = clip.duration
    start_time = random.uniform(0, videoDuration - videoLength)
    subclip = clip.subclip(start_time, start_time + videoLength)
    subclip.write_videofile("clip.mp4")
    cap = cv2.VideoCapture("clip.mp4")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    my_video = mp.VideoFileClip(subclip.filename, audio=True)
    w,h = moviesize = my_video.size

    Ratio = int(w / phonewidth)

    print("screen ratio: "+str(Ratio))
    
    # Add the ending text
    end_txt_mov = textBox(endingText, 60, 0.5, 2, 100, 500, 5, 4, w, h, Ratio)

    # Add the opening text
    start_txt_mov = textBox(openingText, 60, 0.5, 2, 100, 500, 4, 0, w, h, Ratio)

    # Add the title
    title_mov = textBox(Title, 70, 1, 4, 150, 100, 10, 0, w, h, Ratio)

    final = mp.CompositeVideoClip([my_video, start_txt_mov, end_txt_mov, title_mov])
    final_clip = final.set_audio(music)
    final_clip.subclip(0,6).write_videofile("Short.mov",fps=30,codec='libx264')

    os.remove("clip.mp4")
    os.remove("random_clip.wav")

    upload(Title, videoDescription, "Short.mov", client_file)