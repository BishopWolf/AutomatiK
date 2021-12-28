# -*- encoding: utf-8 -*-
import os
header = open('header.py', 'r').read()
from translations import *


# determine installed language
Language_installed=os.popen("locale | grep LANG").read()
if "fr" in Language_installed:
	Language="French"
elif "de" in Language_installed:
	Language="German"
elif "pt" in Language_installed:
	Language="Portuguese"
elif "it" in Language_installed:
	Language="Italian"
elif "jp" in Language_installed:
	Language="Italian"
else:
	Language="English"



txt01="""
#==============================================================================
#                               conkyrc_orange
#
#  author  : SLK
#  version : v2011011601
#  license : Distributed under the terms of GNU GPL version 2 or later
#
#==============================================================================



gap_x 15
gap_y 190

alignment top_right
update_interval 1
lua_load clock.lua
lua_draw_hook_post main

color1 white #Month color
color2 white #Year  color
color3 white #Weekdays color
color4 FFE3A0 #Current weekday color
color5 white  #Days of month color
color6 ff0000 #Current day color
double_buffer true


TEXT
${image img/calendar_clock.png -p 0,0 -s 30x30}#
${image img/calendar.png -p 10,40 -s 140x120}
${offset 35}${font Good Times:size=12}${color Tan1}"""+Time_Date[Language]+""" ${color}${hr 2}${font}

${goto 20}${voffset 0}${color}${font Rounded Elegance:size=12:weight=normal}${time %B}#
${alignr 180}${font Rounded Elegance:size=10:weight=normal}${time %Y}
${voffset 15}${alignc 80}${color 000000}${font Rounded Elegance:size=14}${time %A}
${alignc 80}${color FF0000}${font Rounded Elegance:size=45:weight=bold}${time %d}${font Rounded Elegance:size=10:weight=normal}

${voffset -105}
${font Liquid Crystal:size=25}${color FF0000}${goto 228}${time %H}${goto 263}${blink :}${goto 272}${time %M}${color}

${image img/unnamed.png -p 209,41 -s 110x110}
"""

total=header+txt01
#print total

f = open('clockfile', 'w')
f.write(total)  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it
