#!/usr/bin/python3

# iroiroclock - a simple clock for RaspberryPI + Unicorn HAT HD
#
# Copyright (c) 2023 Takashi Satou
# Released under the MIT License
#

import colorsys
import math
import random
import time
import datetime
import sys

import unicornhathd

import weather

unicornhathd.rotation(270)
unicornhathd.brightness(0.2)

width, height = unicornhathd.get_shape()

FONTS = {
    '0': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                1,0,1,
                1,0,1,     
                1,0,1,
                1,1,1),
    },
    '1': {
        'w': 1, 'h': 5,
        'buf': (1,
                1,
                1,    
                1,
                1),
    },
    '2': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                0,0,1,
                1,1,1,     
                1,0,0,
                1,1,1),
    },
    '3': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                0,0,1,
                1,1,1,
                0,0,1,
                1,1,1),
    },
    '4': {
        'w': 3, 'h': 5,
        'buf': (1,0,1,
                1,0,1,
                1,1,1,
                0,0,1,
                0,0,1),
    },
    '5': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                1,0,0,
                1,1,1,
                0,0,1,
                1,1,1),
    },
    '6': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                1,0,0,
                1,1,1,
                1,0,1,
                1,1,1),
    },
    '7': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                0,0,1,
                0,0,1,
                0,0,1,
                0,0,1),
    },
    '8': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                1,0,1,
                1,1,1,
                1,0,1,
                1,1,1),
    },
    '9': {
        'w': 3, 'h': 5,
        'buf': (1,1,1,
                1,0,1,
                1,1,1,
                0,0,1,
                1,1,1),
    },
    ':': {
        'w': 1, 'h': 5,
        'buf': (0,
                1,
                0,
                1,
                0),
    },
    ' ': {
        'w': 1, 'h': 5,
        'buf': (0,
                0,
                0,
                0,
                0),
    },
    'S': {
        'w': 4, 'h': 5,
        'buf': (0,1,1,1,
                1,0,0,0,
                0,1,1,0,
                0,0,0,1,
                1,1,1,0),
    },
    'u': {
        'w': 3, 'h': 5,
        'buf': (0,0,0,
                0,0,0,
                1,0,1,
                1,0,1,
                0,1,1),
    },
    'M': {
        'w': 5, 'h': 5,
        'buf': (1,0,0,0,1,
                1,1,0,1,1,
                1,0,1,0,1,
                1,0,0,0,1,
                1,0,0,0,1),
    },
    'o': {
        'w': 3, 'h': 5,
        'buf': (0,0,0,
                0,0,0,
                1,1,1,
                1,0,1,
                1,1,1),
    },
    'T': {
        'w': 5, 'h': 5,
        'buf': (1,1,1,1,1,
                0,0,1,0,0,
                0,0,1,0,0,
                0,0,1,0,0,
                0,0,1,0,0),
    },
    'h': {
        'w': 3, 'h': 5,
        'buf': (1,0,0,
                1,0,0,
                1,1,0,
                1,0,1,
                1,0,1),
    },
    'W': {
        'w': 5, 'h': 5,
        'buf': (1,0,0,0,1,
                1,0,0,0,1,
                1,0,1,0,1,
                1,1,0,1,1,
                1,0,0,0,1),
    },
    'F': {
        'w': 4, 'h': 5,
        'buf': (1,1,1,1,
                1,0,0,0,
                1,1,1,0,
                1,0,0,0,
                1,0,0,0),
    },
    'r': {
        'w': 3, 'h': 5,
        'buf': (0,0,0,
                0,0,0,
                1,1,1,
                1,0,0,
                1,0,0),
    },
    'a': {
        'w': 3, 'h': 5,
        'buf': (0,0,0,
                0,0,0,
                0,1,1,
                1,0,1,
                1,1,1),
    },
    '月': {
        'w': 7, 'h': 7,
        'buf': (0,1,1,1,1,1,0,
                0,1,0,0,0,1,0,
                0,1,1,1,1,1,0,
                0,1,0,0,0,1,0,
                0,1,1,1,1,1,0,
                0,1,0,0,0,1,0,
                1,0,0,0,1,1,0),
    },
    '火': {
        'w': 7, 'h': 7,
        'buf': (0,0,0,1,0,0,0,
                1,0,0,1,0,0,1,
                0,1,0,1,0,1,0,
                0,0,0,1,0,0,0,
                0,0,1,0,1,0,0,
                0,1,0,0,0,1,0,
                1,0,0,0,0,0,1),
    },
    '水': {
        'w': 7, 'h': 7,
        'buf': (0,0,0,1,0,0,0,
                0,0,0,1,0,0,1,
                1,1,1,1,0,1,0,
                0,0,1,1,1,0,0,
                0,1,0,1,0,1,0,
                1,0,0,1,0,0,1,
                0,0,1,1,0,0,0),
    },
    '木': {
        'w': 7, 'h': 7,
        'buf': (0,0,0,1,0,0,0,
                0,0,0,1,0,0,0,
                1,1,1,1,1,1,1,
                0,0,1,1,1,0,0,
                0,1,0,1,0,1,0,
                1,0,0,1,0,0,1,
                0,0,0,1,0,0,0),
    },
    '金': {
        'w': 7, 'h': 7,
        'buf': (0,0,0,1,0,0,0,
                0,0,1,0,1,0,0,
                0,1,1,1,1,1,0,
                1,0,0,1,0,0,1,
                0,1,1,1,1,1,0,
                0,0,1,1,1,0,0,
                1,1,1,1,1,1,1),
    },
    '土': {
        'w': 7, 'h': 7,
        'buf': (0,0,0,1,0,0,0,
                0,0,0,1,0,0,0,
                0,1,1,1,1,1,0,
                0,0,0,1,0,0,0,                
                0,0,0,1,0,0,0,
                0,0,0,1,0,0,0,                
                1,1,1,1,1,1,1),
    },
    '日': {
        'w': 7, 'h': 7,
        'buf': (0,1,1,1,1,1,0,
                0,1,0,0,0,1,0,
                0,1,0,0,0,1,0,
                0,1,1,1,1,1,0,
                0,1,0,0,0,1,0,
                0,1,0,0,0,1,0,
                0,1,1,1,1,1,0),
    },
}

WEEKDAYS = [
    { 'name': 'Mo', 'color': (128,255,255) },
    { 'name': 'Tu', 'color': (128,255,255) },
    { 'name': 'We', 'color': (128,255,255) },
    { 'name': 'Th', 'color': (128,255,255) },
    { 'name': 'Fr', 'color': (128,255,255) },
    { 'name': 'Sa', 'color': (128,128,255) },
    { 'name': 'Su', 'color': (255,128,128) },    
]

JWEEKDAYS = [
    { 'name': '月', 'color': (128,255,255) },
    { 'name': '火', 'color': (128,255,255) },
    { 'name': '水', 'color': (128,255,255) },
    { 'name': '木', 'color': (128,255,255) },
    { 'name': '金', 'color': (128,255,255) },
    { 'name': '土', 'color': (128,128,255) },
    { 'name': '日', 'color': (255,128,128) },    
]

SMALL_FONTS = {
    '0': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                1,0,1,
                1,0,1,                
                1,1,1),
    },
    '1': {
        'w': 1, 'h': 4,
        'buf': (1,
                1,
                1,
                1),
    },
    '2': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                0,0,1,
                0,1,0,                     
                1,1,1),
    },
    '3': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                0,1,1,
                0,0,1,
                1,1,1),
    },
    '4': {
        'w': 3, 'h': 4,
        'buf': (1,0,1,
                1,0,1,
                1,1,1,
                0,0,1),
    },
    '5': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                1,1,0,
                0,0,1,
                1,1,1),
    },
    '6': {
        'w': 3, 'h': 4,
        'buf': (1,0,0,
                1,1,1,
                1,0,1,
                1,1,1),
    },
    '7': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                0,0,1,
                0,0,1,
                0,0,1),
    },
    '8': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                1,1,1,
                1,0,1,
                1,1,1),
    },
    '9': {
        'w': 3, 'h': 4,
        'buf': (1,1,1,
                1,0,1,
                1,1,1,
                0,0,1),
    },
    '/': {
        'w': 2, 'h': 4,
        'buf': (0,0,
                0,1,
                1,0,
                0,0),

    },
}


def draw_pattern(buf, x, y, w, h, color):
    r, g, b = color
    for j in range(h):
        for i in range(w):
            if buf[i + j * w]:
                unicornhathd.set_pixel(15 - (x + i), y + j, r, g, b)
                
def draw_string(s, x, y, color):
    for c in s:
        f = FONTS[c]
        draw_pattern(f['buf'], x, y, f['w'], f['h'], color)
        x += f['w'] + 1

        
def draw_small_pattern(buf, x, y, w, h, color):
    r, g, b = color
    for j in range(h):
        for i in range(w):
            if buf[i + j * w]:
                unicornhathd.set_pixel(15 - (x + i), y + j, r, g, b)

                
def draw_small_string(s, x, y, color):
    for c in s:
        f = SMALL_FONTS[c]
        draw_small_pattern(f['buf'], x, y, f['w'], f['h'], color)
        x += f['w'] + 1

BRIGHTNESS = 64
counter = 0        
xys = []
for i in range(16):
    xys.append([random.randint(0,15), random.randint(-15,0)])

def draw_sun():
    for y in range(0, 16):
        for x in range(0, 16):
            dx = x - 7.5
            dy = y - 7.5
            tt = (1.0 + math.sin(counter / 30.0)) * 5
            th = math.atan2(dy, dx)
            h = (72 - math.sqrt(dx * dx + dy * dy)
                 + math.sin(th * tt) / 4
                 + math.sin(counter / 10)
                 ) / 64.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)            
            r *= BRIGHTNESS
            g *= BRIGHTNESS
            b *= BRIGHTNESS
            unicornhathd.set_pixel(x, y, r, g, b)

            
def draw_cloud():
    for y in range(0, 16):
        for x in range(0, 16):
            dx = x + 7 * math.sin(counter / 20) - 7.5
            dy = (y + counter / 5) % 16 - 7.5
            i = (16 - math.sqrt(dx * dx + dy * dy)) / 16.0
            i *= BRIGHTNESS
            unicornhathd.set_pixel(x, y, i, i, i)
           

def draw_rain():
    for xy in xys:
        for i in range(8):
            x = xy[0]
            y = xy[1] - i
            if 0 <= y <= 15:
                r, g, b = colorsys.hsv_to_rgb(0.6, 1, (8 - i) / 8.0)
                r *= BRIGHTNESS
                g *= BRIGHTNESS
                b *= BRIGHTNESS
                unicornhathd.set_pixel(x, y, r, g, b)
        if xy[1] < 24:
            xy[1] += 1
        else:
            xy[0] = random.randint(0, 15)
            xy[1] = random.randint(-15, 0)

            
def draw_snow():
    for xy in xys:
        x = xy[0]
        y = xy[1]
        if 0 <= y <= 15:
            i = BRIGHTNESS
            unicornhathd.set_pixel(x, y, i, i, i)

        if counter % 10 != 0: continue

        if xy[1] < 15:
            xy[0] = (xy[0] + random.randint(-1, 1)) % 16
            xy[1] += 1
        else:
            xy[0] = random.randint(0, 15)
            xy[1] = random.randint(-15, 0)

DRAW_FUNCS = {
    weather.CLEAR: draw_sun,
    weather.CLOUDY: draw_cloud,
    weather.RAIN: draw_rain,
    weather.SNOW: draw_snow
}


def draw_weather(w, s):
    w1, conj, w2 = w
    if conj == weather.NONE:
        DRAW_FUNCS[w1]()
    elif conj == weather.LATER:
        if s % 10 < 4:
            DRAW_FUNCS[w1]()
        elif s % 10 < 8:
            DRAW_FUNCS[w2]()
    else: # weather.PARTLY
        if s % 10 < 7:
            DRAW_FUNCS[w1]()
        else:
            DRAW_FUNCS[w2]()
            
#cur_weather = (weather.CLEAR, weather.LATER, weather.CLOUDY)
cur_weather = (weather.RAIN, weather.PARTLY, weather.SNOW)
last_weather_time = None

try:
    while True:
        unicornhathd.clear()

        t = datetime.datetime.now()
        if (last_weather_time == None or
            t - last_weather_time > datetime.timedelta(hours=1)):
            cur_weather = weather.get_weather()
            last_weather_time = t
        
        h = t.hour
        if h >= 13:
            h -= 12
        m = t.minute
        s = t.second

        counter += 1
        draw_weather(cur_weather, s)
        
        ts = f'{h}:{m:02}'
        draw_string(ts, 0, 2, (255, 255, 255))

        ts = f'{s:02}'
        draw_string(ts, 0, 9, (255, 255, 255))

        wd = JWEEKDAYS[t.weekday()]
        if s % 10 < 3:
            draw_small_string(f'{t.month}/', 8, 10, wd['color'])
        elif s % 10 < 7:
            draw_small_string(f'{t.day}', 9, 10, wd['color'])
        else:
            draw_string(wd['name'], 8, 8, wd['color'])
        
        unicornhathd.show()

except KeyboardInterrupt:
    unicornhathd.off()

finally:
    unicornhathd.off()
