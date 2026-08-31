import sys
from PIL import Image

images = [Image.open(x) for x in ['1.png', '2.png', '3.png','4.png', '5.png', '6.png']]
widths, heights = zip(*(i.size for i in images))

xmargin = 2
ymargin = 2

total_width = 3*(max(widths)-2*xmargin)
max_height = 2*(max(heights)-2*ymargin)

new_im = Image.new('RGB', (total_width, max_height),color=(255,255,255,0))

#im1 = im.crop((left, top, right, bottom)) 

x_offset = 0
for idex in range(len(images)):
    im = images[idex]
    x_offset = idex%3*im.size[0]
    y_offset = idex//3*im.size[1]
    im1 = im.crop((xmargin, ymargin, im.size[0]-xmargin, im.size[1]-ymargin)) 
    new_im.paste(im1, (x_offset,y_offset))

new_im.save('slices.png')
