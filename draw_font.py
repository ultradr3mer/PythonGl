from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (512, 512), color=(0, 0, 0))

fnt = ImageFont.truetype('C:/Windows/Fonts/SourceCodePro-Regular.ttf', 58)
d = ImageDraw.Draw(img)

characters = ' !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
line_length = 12

line_number = 0
while len(characters) > 0:
    line, characters = characters[:line_length], characters[line_length:]
    y_pos = -11 + line_number * 64

    # d.text(xy=(0, y_pos), text=line, font=fnt, fill=(255, 255, 255))

    character_number = 0
    for c in line:
        d.text(xy=(36*character_number, y_pos), text=c, font=fnt, fill=(255, 255, 255))
        character_number += 1

    line_number += 1

img.save('numbers.png')
