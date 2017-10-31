from PIL import Image, ImageDraw, ImageFont
import random
from collections import defaultdict
from io import BytesIO
from base64 import b64encode


SIZE = 100
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

VIVID_BLUE = '#0039A6'
BRIGHT_ORANGE = '#FF6319'
LIME_GREEN = '#6CBE45'
LIGHT_SLATE_GRAY = '#A7A9AC'
TERRA_COTTA_BROWN = '#996633'
SUNFLOWER_YELLOW = '#FCCC0A'
TOMATO_RED = '#EE352E'
APPLE_GREEN = '#00933C'
RASPBERRY = '#B933AD'
DARK_SLATE_GRAY = '#808183'


PALLATES = {
    'nyc': [VIVID_BLUE, BRIGHT_ORANGE, LIME_GREEN, TERRA_COTTA_BROWN, LIGHT_SLATE_GRAY,
            SUNFLOWER_YELLOW, TOMATO_RED, APPLE_GREEN, RASPBERRY, DARK_SLATE_GRAY],
    'lirr': ['#00985F', '#4D5357', '#6E3219', '#CE8E00', BRIGHT_ORANGE, '#006983',
             '#00AF3F', VIVID_BLUE, '#C60C30', '#A626AA', '#00A1DE'],
    'nyc no grey': [VIVID_BLUE, BRIGHT_ORANGE, LIME_GREEN, TERRA_COTTA_BROWN,
                    SUNFLOWER_YELLOW, TOMATO_RED, APPLE_GREEN, RASPBERRY],
}

BLACK_FONT_COLORS = {SUNFLOWER_YELLOW}


helvetica = ImageFont.truetype('/Users/stylecaster/Desktop/Helvetica-Bold.ttf', 140)


letter_colors = {
    "A": VIVID_BLUE,
    "B": BRIGHT_ORANGE,
    "C": VIVID_BLUE,
    "D": BRIGHT_ORANGE,
    "E": VIVID_BLUE,
    "F": BRIGHT_ORANGE,
    "G": LIME_GREEN,
    "J": TERRA_COTTA_BROWN,
    "L": LIGHT_SLATE_GRAY,
    "N": SUNFLOWER_YELLOW,
    "Q": SUNFLOWER_YELLOW,
    "R": SUNFLOWER_YELLOW,
    "S": DARK_SLATE_GRAY,
    "W": SUNFLOWER_YELLOW,
    "Z": TERRA_COTTA_BROWN,
}


letter_offsets = defaultdict(lambda: 0)
letter_offsets.update({
    "!": 24,
    ";": 24,
    ":": 24,
    "F": 6,
    "G": -5,
    "H": -5,
    "I": 25, "Ï": 25, "Í": 25, "Ī": 25, "Į": 25, "Ì": 25,
    "J": 10,
    "L": 10, "Ł": 10,
    "M": -10,
    "O": -6, "Ö": -6, "Ò": -6, "Ó": -6, "Œ": -24, "Ø": -6, "Ō": -6, "Õ": -6,
    "P": 6,
    "Q": -7,
    "T": 4,
    "U": -3, "Û": -3, "Ü": -6, "Ù": -3, "Ú": -3, "Ū": -3,
    "W": -18,
})


def get_letter(letter, color=None, theme='nyc', background_color=BLACK):
    m = 3  # multiplier
    offset = letter_offsets[letter]
    font_color = WHITE
    if color is None:
        if letter in letter_colors:
            color = letter_colors[letter]
        else:
            color = random.choice(PALLATES[theme])
    if color in BLACK_FONT_COLORS:
        font_color = BLACK
    image = Image.new('RGBA', (SIZE*m, SIZE*m), color=background_color)
    if letter != " ":
        draw = ImageDraw.Draw(image)
        draw.ellipse((10*m, 10*m, 90*m, 90*m), fill=color)
        draw.text((34*m + offset, 30*m), letter, font=helvetica, fill=font_color)
        del draw
    image.thumbnail((SIZE, SIZE), Image.ANTIALIAS)
    return image


def combine_images(images):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    return new_im


def render_str(text, theme):
    return combine_images([get_letter(l, theme=theme) for l in text.upper()])


def to_img_tag(img):
    b = BytesIO()  
    img.save(b, format='png')
    tag = "<img src='data:image/png;base64,{0}'/>".format(b64encode(b.getvalue()).decode('utf-8'))
    return tag


def render_to_tag(text, theme='nyc'):
    return to_img_tag(render_str(text, theme=theme))
