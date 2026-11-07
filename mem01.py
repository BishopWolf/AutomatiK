# -*- encoding: utf-8 -*-
import os
from common import detect_language, read_header, write_file
from translations import *

Language = detect_language()
header = read_header()


zram_max = r"""${execi 10 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1~/zram/{s+=$3} END{print f(s)}' /proc/swaps}"""
zram_bar = r"""${execbar 11,292 LC_ALL=C awk 'NR>1&&$1~/zram/{s+=$3;u+=$4} END{print (s>0?int(u*100/s):0)}' /proc/swaps}"""
zram_used = r"""${execi 2 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1~/zram/{u+=$4} END{print f(u)}' /proc/swaps}"""
zram_free = r"""${execi 2 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1~/zram/{s+=$3;u+=$4} END{print f(s-u)}' /proc/swaps}"""

swap_max = r"""${execi 10 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1!~/zram/{s+=$3} END{print f(s)}' /proc/swaps}"""
swap_bar = r"""${execbar 11,292 LC_ALL=C awk 'NR>1&&$1!~/zram/{s+=$3;u+=$4} END{print (s>0?int(u*100/s):0)}' /proc/swaps}"""
swap_used = r"""${execi 2 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1!~/zram/{u+=$4} END{print f(u)}' /proc/swaps}"""
swap_free = r"""${execi 2 LC_ALL=C awk 'function f(k){return k<=0?"0B":k>=1048576?sprintf("%.2fGiB",k/1048576):k>=1024?sprintf("%.2fMiB",k/1024):sprintf("%dKiB",k)} NR>1&&$1!~/zram/{s+=$3;u+=$4} END{print f(s-u)}' /proc/swaps}"""

txt01="""gap_x 15
gap_y  378
lua_load allcombined.lua

#${lua gradbar {5, 218 "${memperc}" ,100, 80, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}

TEXT
${image img/memory.png -p 0,0 -s 30x30}
${offset 35}${font DejaVu Sans:size=12}${color Tan1}"""+Memory[Language]+""" ${color}${hr 2}${font}
${color}"""+Ram[Language]+"""${color}${alignr}$memmax 
${membar 11,292}
${color}$mem """+UsedWord[Language]+"""${alignr}${memfree} """+FreeWord[Language]+"""
${color}"""+Zram[Language]+"""${alignr}"""+zram_max+"""
"""+zram_bar+"""
${color}"""+zram_used+""" """+UsedWord[Language]+"""${alignr}"""+zram_free+""" """+FreeWord[Language]+"""
${color}"""+Swap[Language]+"""${alignr}"""+swap_max+"""
"""+swap_bar+"""
${color}"""+swap_used+""" """+UsedWord[Language]+"""${alignr}"""+swap_free+""" """+FreeWord[Language]+"""
#
"""


total=header+txt01
#print total

write_file('memfile', total)  # python will convert \n to os.linesep
