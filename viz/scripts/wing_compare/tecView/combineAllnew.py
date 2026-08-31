import sys
from PIL import Image

images = [Image.open(x) for x in ['contour.png']]
widths, heights = zip(*(i.size for i in images))

xmargin = 2
ymargin = 2

total_width = max(widths)-2*xmargin
max_height = sum(heights)-4*ymargin

new_im = Image.new('RGB', (total_width, max_height),color=(255,255,255,0))

x_offset = 0
y_offset = 0
for im in images:
    im1 = im.crop((xmargin, ymargin, im.size[0]-xmargin, im.size[1]-ymargin)) 
    new_im.paste(im1, (x_offset,y_offset))
    y_offset += im.size[1]

new_im.save('contours.png')

# combine all

images = [Image.open(x) for x in ['contours.png', 'slices.png']]
widths, heights = zip(*(i.size for i in images))

total_width = max(widths)
max_height = sum(heights)

new_im = Image.new('RGB', (total_width, max_height),color=(255,255,255,0))

new_im.paste(images[0], (0,0))
new_im.paste(images[1], (0,heights[0]-20))
new_im.save('all.png')

