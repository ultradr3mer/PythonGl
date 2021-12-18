from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (256, 256), color=(0, 0, 0))

fnt = ImageFont.truetype('C:/Windows/Fonts/SourceCodePro-Regular.ttf', 40)
d = ImageDraw.Draw(img)

letters = ['1234567890',
           'ABCDEFGHIJ',
           'KLMNOPQRST',
           'UVWXYZ.,!?']

for i in range(len(letters)):
    group = letters[i]
    d.text(xy=(0, -11 + i * 32), text=group, font=fnt, fill=(255, 255, 255))

img.save('numbers.png')



