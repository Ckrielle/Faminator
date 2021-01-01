from moviepy.video.fx import resize
from moviepy.editor import *
from pyfiglet import Figlet
import argparse


def logo():
    print(Figlet(font="catwalk").renderText("Faminator"))
    print("Made by Machina\ncurl -sL https://bit.ly/2ZGnLC5 | sh\n")


def time_to_sec(s, e):
    return (e[0] - s[0]) * 3600 + (e[1] - s[1]) * 60 + e[2] - s[2]


def time_frames(times):
    h, m, s = (times.split(':'))
    return (int(h), int(m), int(s))


def just_images(start, end, images, audio, out):
    time = [time_to_sec(i, j) for i, j in zip(start, end)]
    clips = [ImageClip(j).set_duration(i) for i, j in zip(time, images)]
    video = concatenate_videoclips(clips, method="compose")
    if audio:
        video = video.set_audio(AudioFileClip(audio))
    video.write_videofile(out, fps=24)


def just_videos(videos, audio, out):
    video = [VideoFileClip(i) for i in videos]
    for i in range(len(video)):
        video[i] = video[i].resize((1920, 1080))
    video = concatenate_videoclips(video)
    if audio:
        video = video.set_audio(AudioFileClip(audio))
    video.write_videofile(out, fps=24)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Easily Make Videos & Become Famous",
        epilog="Hack The Planet!"
    )
    parser.add_argument(
        '-i',
        '--input',
        action = 'store',
        help = 'Specify the input file',
        default = 'files.txt'
    )
    parser.add_argument(
        '-t',
        '--video_type',
        action = 'store',
        choices = ['img', 'vid'],
        help = 'Choose what kind of video you want to make',
        required = True
    )
    parser.add_argument(
        '-a',
        '--audio',
        action = 'store',
        help = 'Choose whether to set audio or not'
    )
    parser.add_argument(
        '-o',
        '--output',
        action = 'store',
        help = 'Specify the name of the output file',
        default = 'output.mp4'
    )

    args = parser.parse_args()
    return args

def main():

    logo()
    args = parse_args()

    choice = args.video_type
    audio = args.audio
    output = args.output
    with open(args.input, 'r') as f:
        data = [line.strip() for line in f]
        if choice == "img":
            time = [i.split('\t')[0] for i in data]
            start = [time_frames(i.split('-')[0]) for i in time]
            end = [time_frames(i.split('-')[1]) for i in time]
            media = [i.split('\t')[1] for i in data]
            just_images(start, end, media, audio, output)
        elif choice == "vid":
            just_videos(data, audio, output)

main()
