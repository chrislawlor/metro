import logging
from PIL import Image, ImageDraw, ImageFont
import random
from collections import defaultdict
from io import BytesIO
from base64 import b64encode

logger = logging.getLogger(__name__)

SIZE = 50
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


helvetica = ImageFont.truetype('/Users/stylecaster/Desktop/Helvetica-Bold.ttf', 70)


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
    "I": 30, "Ï": 30, "Í": 30, "Ī": 30, "Į": 30, "Ì": 30,
    "J": 10,
    "L": 10, "Ł": 10,
    "M": -10,
    "N": -4,
    "O": -6, "Ö": -6, "Ò": -6, "Ó": -6, "Œ": -24, "Ø": -6, "Ō": -6, "Õ": -6,
    "P": 6,
    "Q": -7,
    "T": 4,
    "U": -3, "Û": -3, "Ü": -6, "Ù": -3, "Ú": -3, "Ū": -3,
    "W": -18,
    "Z": 8,
})


def get_letter(letter, color=None, theme='nyc', background_color=BLACK):
    m = 3  # multiplier
    offset = letter_offsets[letter] // 2
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
        draw.ellipse((5*m, 5*m, 45*m, 45*m), fill=color)
        draw.text((17*m + offset, 15*m), letter, font=helvetica, fill=font_color)
        del draw
    image.thumbnail((SIZE, SIZE), Image.ANTIALIAS)
    return image


def combine_letters(images, background_color=BLACK):
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGBA', (total_width, max_height), color=background_color)

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    return new_im


def combine_rows(images, background_color=BLACK):
    logging.info(f"Combining {len(images)} rows")
    widths, heights = zip(*(i.size for i in images))

    total_width = max(widths)
    max_height = sum(heights)



    new_im = Image.new('RGBA', (total_width, max_height), color=background_color)

    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    return new_im


def render_row(row, theme):
    logger.info(f"Rendering row {row}")
    return combine_letters([get_letter(l.upper(), theme=theme) for l in row])


def text_to_rows(text, max_width):
    words = text.split()
    rows = []
    current_row = []
    spaces_remaining = max_width
    for word in words:
        logging.info(f"On word {word}")
        # if the word fits in the current row, add it
        if len(word) <= spaces_remaining:
            current_row += list(word)
            spaces_remaining -= len(word)
            # if we're not at the end of the row, add a space
            if spaces_remaining >= 1:
                current_row += [' ']
                spaces_remaining -= 1

            if spaces_remaining == 0:
                rows.append(current_row.copy())
                current_row = []
                spaces_remaining = max_width

        # else, go to the next row
        else:
            rows.append(current_row.copy())
            current_row = []
            spaces_remaining = max_width
    if current_row:
        rows.append(current_row)
    return rows


def render_rows(rows, theme):
    images = [render_row(row, theme) for row in rows]
    return combine_rows(images)


def to_img_tag(img):
    b = BytesIO()  
    img.save(b, format='png')
    tag = "<img src='data:image/png;base64,{0}'/>".format(b64encode(b.getvalue()).decode('utf-8'))
    return tag


def render_to_tag(text, theme='nyc'):
    rows = text_to_rows(text, 12)
    logger.info(rows)
    return to_img_tag(render_rows(rows, theme=theme))
