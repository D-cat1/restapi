#original code : https://www.learnpythonwithrune.org/automate-a-quotation-image-for-twitter-in-python-in-5-easy-steps/
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import requests
import io

# picture setup - it is set up for Twitter recommendations
WIDTH = 1080
HEIGHT = 1350
# the margin are set by my preferences
MARGIN = 60
MARGIN_TOP = 150
MARGIN_BOTTOM = 150
LOGO_MARGIN = 25

# font variables
FONT_SIZES = [40, 30, 20, 10, 5]
FONT_QUOTE = 'font-text'
FONT_QUOTED_BY = 'font-quoted-by'
FONT_SIZE = 'font-size'
FONT_QUOTED_BY_SIZE = 'font-quoted-by-size'

# Font colors
WHITE = 'rgb(255, 255, 255)'
GREY = 'rgb(200, 200, 200)'

# output text
OUTPUT_QUOTE = 'quote'
OUTPUT_QUOTED_BY = 'quoted-by'
OUTPUT_LINES = 'lines'


def text_wrap_and_font_size(output, font_style, max_width, max_height):
    for font_size in FONT_SIZES:
        output[OUTPUT_LINES] = []
        font = ImageFont.truetype(font_style[FONT_QUOTE], size=font_size, encoding="unic")
        output[OUTPUT_QUOTE] = " ".join(output[OUTPUT_QUOTE].split())
        if font.getsize(output[OUTPUT_QUOTE])[0] <= max_width:
            output[OUTPUT_LINES].append(output[OUTPUT_QUOTE])
        else:
            words = output[OUTPUT_QUOTE].split()
            line = ''
            for word in words:
                if font.getsize(line + " " + word)[0] <= max_width:
                    line +=  " " + word
                else:
                    output[OUTPUT_LINES].append(line)
                    line = word
            output[OUTPUT_LINES].append(line)
        line_height = font.getsize('lp')[1]

        quoted_by_font_size = font_size
        quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")
        while quoted_by_font.getsize(output[OUTPUT_QUOTED_BY])[0] > max_width//2:
            quoted_by_font_size -= 1
            quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")

        if line_height*len(output[OUTPUT_LINES]) + quoted_by_font.getsize('lp')[1] < max_height:
            font_style[FONT_SIZE] = font_size
            font_style[FONT_QUOTED_BY_SIZE] = quoted_by_font_size
            return True

    # we didn't succeed find a font size that would match within the block of text
    return False


def draw_text(image, output, font_style):

    draw = ImageDraw.Draw(image)
    lines = output[OUTPUT_LINES]
    font = ImageFont.truetype(font_style[FONT_QUOTE], size=font_style[FONT_SIZE], encoding="unic")
    line_height = font.getsize('lp')[1]

    y = MARGIN_TOP
    for line in lines:
        x =  (WIDTH - font.getsize(line)[0]) // 2
        draw.text((x, y), line.lstrip(), fill=WHITE, font=font)

        y = y + line_height

    quoted_by = output[OUTPUT_QUOTED_BY]
    quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=font_style[FONT_QUOTED_BY_SIZE], encoding="unic")
    # position the quoted_by in the far right, but within margin
    x = (WIDTH - quoted_by_font.getsize(quoted_by)[0]) // 2
    y += 20
    draw.text((x, y), quoted_by, fill=GREY, font=quoted_by_font)
    return image


def generate_image_with_quote(input_image, quote, quote_by, font_style):
    image = Image.open(input_image)

    # darken the image to make output more visible
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.5)

    # resize the image to fit Twitter
    image = image.resize((WIDTH, HEIGHT))

    # set logo on image


    output = {OUTPUT_QUOTE: quote, OUTPUT_QUOTED_BY: quote_by}

    # we should check if it returns true, but it is ignorred here
    text_wrap_and_font_size(output, font_style, WIDTH - 2*MARGIN, HEIGHT - MARGIN_TOP - MARGIN_BOTTOM)

    # now it is time to draw the quote on our image and save it
    image = draw_text(image, output, font_style)
    output = io.BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()


def genapimage(quote, nama, image):
    # setup input and output image
    input_image = requests.get(image, stream=True)#"image.jpg"


    # setup font type
    font_style = {FONT_QUOTE: "./module/font/Regular.ttf", FONT_QUOTED_BY: "./module/font/Italic.ttf"}
    quote_by = "- {} -".format(nama)
    
    # generates the quote image
    dataio = generate_image_with_quote(input_image.raw, quote, quote_by, font_style)
    print(dataio)
    return dataio

def unsplash():
   randimage = requests.head('https://source.unsplash.com/1080x1350/?minimalist')
   return randimage.headers["location"]