# -*- encoding: utf-8 -*-
import os
from common import detect_language, read_header, write_file
from translations import *

Language = detect_language()
header = read_header()


txt01="""gap_x 15
gap_y  375
lua_load allcombined.lua

#${lua gradbar {5, 218 "${memperc}" ,100, 80, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}

TEXT
${image img/memory.png -p 0,0 -s 30x30}
${offset 35}${font DejaVu Sans:size=12}${color Tan1}"""+Memory[Language]+""" ${color}${hr 2}${font}
${color}"""+Ram[Language]+"""${color}${alignr}$memmax 
${membar 11,292}
${color}$mem """+UsedWord[Language]+"""${alignr}${memfree} """+FreeWord[Language]+"""
${color}"""+Swap[Language]+"""${alignr}${swapmax}
${swapbar 11,292}
${color}$swap """+UsedWord[Language]+"""${alignr}${swapfree} """+FreeWord[Language]+"""
#
"""


total=header+txt01
#print total

write_file('memfile', total)  # python will convert \n to os.linesep
