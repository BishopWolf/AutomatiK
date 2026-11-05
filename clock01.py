# -*- encoding: utf-8 -*-
import os
from common import detect_language, read_header, write_file
from translations import *

Language = detect_language()
header = read_header()



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
#lua_load clock.lua
#lua_draw_hook_post main

color1 white #Month color
color2 white #Year  color
color3 white #Weekdays color
color4 FFE3A0 #Current weekday color
color5 white  #Days of month color
color6 ff0000 #Current day color
double_buffer true


TEXT
${image img/calendar_clock.png -p 0,0 -s 30x30}#
${image img/calendar.png -p 10,40 -s 160x120}
${offset 35}${font DejaVu Sans:size=12}${color Tan1}"""+Time_Date[Language]+""" ${color}${hr 2}${font}

${goto 20}${voffset 0}${color}${font DejaVu Sans:size=12}${time %B}#
${alignr 160}${font DejaVu Sans:size=10}${time %Y}
${voffset 15}${alignc 70}${color 000000}${font DejaVu Sans:size=14}${time %A}
${alignc 70}${color FF0000}${font DejaVu Sans:size=45}${time %d}${font DejaVu Sans:size=10}

${voffset -105}
${font DejaVu Sans:size=25}${color FFFFFF}${goto 228}${time %H}${goto 263}${blink :}${goto 272}${time %M}${color}

#${image img/unnamed.png -p 209,41 -s 110x110}
"""

total=header+txt01
#print total
themed_clock = open('themed_clock', 'r').read()

write_file('clockfile', total)  # python will convert \n to os.linesep
