from PIL import Image


image = Image.open('final_map.png')
image = image.convert('RGB')
width, height = image.size

for x in range(width):
    for y in range(height):
        r, g, b = image.getpixel((x, y))
        '''
        if r == 0 and g == 0 and b == 0:
            image.putpixel((x, y), (170,170,170))
        '''
        if 1200 < x < 2600:
            if 0 < y < 320:
                if r == 255 and g == 149 and b == 0:
                    image.putpixel((x, y), (170,170,170))

image.save('final_map.png')
