import random
import moviepy.editor as mp
import json
import os
from Constants import *

def RandomClipAudio(file, duration):
    """
    Args:
        file: string of path to file
        time: float of length of clip in seconds
    Returns:
        Audio: mp audio clip of music
    """

    audio = mp.AudiofileClip(file)
    audioDuration = audio.duration
    start_time = random.uniform(0, audioDuration - duration)
    clip = audio.subclip(start_time, start_time + duration)
    return clip


def findTopicInJson(path_to_json_file):
    """
    Args:
        path_to_json_file: string of path to json file
    Returns:
        topic: string of topic
    """

    with open(path_to_json_file) as json_file:
        data = json.load(json_file)
        channel_topics = data['channel_topics'][0]
        random_topic = random.choice(list(channel_topics.keys()))
        array_data = channel_topics[random_topic]
        random_element = random.choice(array_data)
        print("video backround: " + random_element)
        return random_element
    
def findTopicVideo(randomTopic, pathToVideos):
    """
    Args:
        randomTopic: string of topic
        pathToVideos: string of path to videos
    Returns:
        randomFile: string of path to video
    """

    path = pathToVideos + randomTopic
    files = os.listdir(path)
    files = [f for f in files if not f.endswith('.DS_Store')]
    randomFile = random.choice(files)
    print("files in folder: " + str(files))
    print("chosen file: " + randomFile)
    return randomFile

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