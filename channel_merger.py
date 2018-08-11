import sys
from PIL import Image

def load_channels(channels):
    for st in channels:
        print(st)
    red = Image.open('images/' + channels[0]).convert('L')
    green = Image.open('images/' + channels[1]).convert('L')
    blue = Image.open('images/' + channels[2]).convert('L')
    
    return (red, green, blue)

def merge_channels(channels):
    print(len(channels))
    merged = Image.merge('RGB', (channels[0], channels[1], channels[2]))
    
    return merged

def merge(channels, dest=''):
    print(len(channels))
    data = load_channels((channels[0], channels[1], channels[2]))
    image = merge_channels(data)
    
    if dest:
        image.save('static/results/' + str(dest) + '.png', 'PNG')
    return image
