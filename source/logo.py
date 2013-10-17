import os, sys
import Image
from config import logo_original, logo_resized

max_width = float(350)
max_height = float(150)


def original_logo(logo_name):
    return logo_original + "/" + logo_name

def resized_logo(logo_name):
    return logo_resized + "/" + logo_name

def resize_logo(logo_name):
   
    img = Image.open(original_logo(logo_name))
    width, height = img.size
    ratio = min((max_width / width), \
                (max_height / height))

    new_width = int(ratio * width)
    new_height = int(ratio * height)

    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    img.save(resized_logo(logo_name))

