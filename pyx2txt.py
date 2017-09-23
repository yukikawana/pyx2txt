#!/usr/bin/python
from PIL import Image, ImageDraw, ImageChops
import numpy as np
from numpy import linalg
import sys
import pdb
import os
from extra import colortrans
respb = 16
imgsnp = np.load('imgsnp.npy')
unicodes = [
'\u2588',
'\u2581',
'\u2582',
'\u2583',
'\u2584',
'\u2585',
'\u2586',
'\u2587',

'\u2588',
'\u2587',
'\u2586',
'\u2585',
'\u2584',
'\u2583',
'\u2582',
'\u2581',

'\u259f',
'\u2596',
'\u2599',
'\u2597',

'\u259a',
'\u259e',
'\u2596',
'\u2599',
'\u2597',
'\u259f',

'\u258f',
'\u258e',
'\u258d',
'\u258c',
'\u258b',
'\u258a',
'\u2589',

'\u2589',
'\u258a',
'\u258b',
'\u258c',
'\u258d',
'\u258e',
'\u258f'

]



def main():
    imagefile = sys.argv[1]
    if imagefile == 'check':
        check = True
        print len(unicodes)
        im = Image.open('images/test.jpg').quantize(256)
        draw(im, check=True)
    else:
        im = Image.open(imagefile).quantize(256,  kmeans=False)
        draw(im, check=False)

def draw(im, check=False, blockwidth=20, multi=1):
    width, height = im.size
    ratio = float(blockwidth) / float(width)
    blockheight = int(ratio * height)

    imr = im.resize((blockwidth * respb, blockheight * respb), Image.ANTIALIAS)
    checkcount = 0
    line = ''
    if multi > 1:
        from joblib import Parallel, delayed
        multiarg = []
        for hh in xrange(blockheight):
            for ww in xrange(blockwidth*2):
                part = imr.crop((ww*respb/2,hh*respb,(ww+1)*respb/2,(hh+1)*respb))
                multiarg.append((part.copy(), blockwidth))
        output = Parallel(n_jobs=multi)([delayed(wrapper)(i) for i in multiarg])
        line = ''
        for hhww in xrange(blockheight*blockwidth*2):
            line+=output[hhww]
            if hhww%(blockwidth*2) == 0:
                line += '\n'
        sys.stdout.write(line)
        sys.stdout.write('\n')
    else:
        for hhww in xrange(blockheight*blockwidth*2):
            hh = hhww/(blockwidth*2)
            ww = hhww - hh*blockwidth*2
            part = imr.crop((ww*respb/2,hh*respb,(ww+1)*respb/2,(hh+1)*respb))
            imgq = part.quantize(2, kmeans=True)
            default_palette =  getPaletteInRgb(imgq)
            bg = hex(default_palette[0])[2:4].zfill(2)+hex(default_palette[1])[2:4].zfill(2)+hex(default_palette[2])[2:4].zfill(2)
            fg = hex(default_palette[3])[2:4].zfill(2)+hex(default_palette[4])[2:4].zfill(2)+hex(default_palette[5])[2:4].zfill(2)
            ind = np.argmin(linalg.norm(np.asarray(imgq)-imgsnp,axis=(1,2)))
            if check:
                ind = checkcount
                checkcount += 1
                default_palette = [255, 0,0, 0,0,255]
                imgs = create_temp_imgs(0, default_palette)
                c = 0
                for img in imgs:
                    img.save(str(c)+'.png')
                    c+=1
                bg = hex(default_palette[0])[2:4].zfill(2)+hex(default_palette[1])[2:4].zfill(2)+hex(default_palette[2])[2:4].zfill(2)
                fg = hex(default_palette[3])[2:4].zfill(2)+hex(default_palette[4])[2:4].zfill(2)+hex(default_palette[5])[2:4].zfill(2)
            bgshort,rgb = colortrans.rgb2short(bg)
            fgshort,rgb = colortrans.rgb2short(fg)
            #if ind == 8+ad:
            if ind == len(unicodes):
                sys.stdout.write('\n')
                return
            if ind == 0:
                color1 = fgshort
                color2 = fgshort
                block = ' '
            elif ind == 8:
                color1 = bgshort
                color2 = bgshort
                block = ' '
            elif (32 < ind and ind <40) or (8 < ind and ind <16) or ind ==16 or ind == 18 or ind == 22 or ind == 24:
                color1 = bgshort
                color2 = fgshort
                block = unicodes[ind]
            else:
                color1 = fgshort
                color2 = bgshort
                block = unicodes[ind]
            line += '\033[38;5;{0};48;5;{1}m'.format(color1,color2)+block.encode('utf-8')+'\033[0;00m'
            #sys.stdout.write('\033[38;5;{0};48;5;{1}m'.format(color1,color2)+block+'\033[0;00m')
            if check:
                sys.stdout.write(' ')
        #sys.stdout.write(line + '\n')
            if hhww%(blockwidth*2) == 0:
                line += '\n'
        sys.stdout.write(line+'\n')



def create_temp_imgs(count,default_palette):
    tempimgs = []
    temp = Image.new('P', (respb/2,respb), 0)
    temp.putpalette(default_palette)
    d = ImageDraw.ImageDraw(temp)
    d.rectangle([0, 0, respb/2-1, respb-1], fill=1)
    count+=1
    tempimgs.append(temp)

    for h in xrange(1,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, respb-1-h*2+1, respb/2-1, respb-1], fill=1)
        count+=1
        tempimgs.append(temp)

    temp = Image.new('P', (respb/2,respb), 0)
    temp.putpalette(default_palette)
    d = ImageDraw.ImageDraw(temp)
    count+=1
    tempimgs.append(temp)

    for h in xrange(1,respb/2):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 0, respb/2-1, h*2-1], fill=1)
        count+=1
        tempimgs.append(temp)

    #quarter blocks
    for qw in [0,respb/4]:
        for qh in [0,respb/2]:
            temp = Image.new('P', (respb/2,respb), 0)
            temp.putpalette(default_palette)
            d = ImageDraw.ImageDraw(temp)
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
            count+=1
            tempimgs.append(temp)

    #quarter diagonal two blocks
    for qwqh in [ [[0,0],[respb/4,respb/2]], [[0,respb/2],[respb/4,0]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)

    #three blocks
    for qwqh in [ [[0,0],[respb/4,respb/2],[respb/4,0]], [[0,0],[respb/4,respb/2],[0,respb/2]], [[0,respb/2],[respb/4,0],[0,0]],[[0,respb/2],[respb/4,0],[respb/4,respb/2]]]:
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        for qw, qh in qwqh:
            d.rectangle([qw, qh, qw+respb/4-1, respb/2-1+qh], fill=1)
        count+=1
        tempimgs.append(temp)

    for w in xrange(0,respb/2-1):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([0, 0, w, respb-1], fill=1)
        count+=1
        tempimgs.append(temp)

    for w in xrange(0,respb/2-1):
        temp = Image.new('P', (respb/2,respb), 0)
        temp.putpalette(default_palette)
        d = ImageDraw.ImageDraw(temp)
        d.rectangle([respb/2-1-w,0, respb/2-1, respb-1], fill=1)
        count+=1
        tempimgs.append(temp)

    return tempimgs

def multidraw(part, blockwidth):
    imgq = part.quantize(2,  kmeans=True)
    default_palette = getPaletteInRgb(imgq)
    bg = hex(default_palette[0])[2:4].zfill(2)+hex(default_palette[1])[2:4].zfill(2)+hex(default_palette[2])[2:4].zfill(2)
    fg = hex(default_palette[3])[2:4].zfill(2)+hex(default_palette[4])[2:4].zfill(2)+hex(default_palette[5])[2:4].zfill(2)
    ind = np.argmin(linalg.norm(np.asarray(imgq)-imgsnp,axis=(1,2)))
    bgshort,rgb = colortrans.rgb2short(bg)
    fgshort,rgb = colortrans.rgb2short(fg)
    if ind == 0:
        color1 = fgshort
        color2 = fgshort
        block = ' '
    elif ind == 8:
        color1 = bgshort
        color2 = bgshort
        block = ' '
    elif (32 < ind and ind <40) or (8 < ind and ind <16) or ind ==16 or ind == 18 or ind == 22 or ind == 24:
        color1 = bgshort
        color2 = fgshort
        block = unicodes[ind]
    else:
        color1 = fgshort
        color2 = bgshort
        block = unicodes[ind]
    char = '\033[38;5;{0};48;5;{1}m'.format(color1,color2)+block.encode('utf-8')+'\033[0;00m'

    return char
 


def wrapper(args):
    return multidraw(*args)


def getPaletteInRgb(img):
    assert img.mode == 'P', "image should be palette mode"
    pal = img.getpalette()
    color = pal[0:6]
    return color


if __name__ == '__main__':
    main()
