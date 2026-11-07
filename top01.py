# -*- encoding: utf-8 -*-
import os
from common import detect_language, read_header, write_file
from translations import *

Language = detect_language()
header = read_header()


txt01="""gap_x 380
gap_y 19

TEXT
${image img/gearwheels.png -p 0,0 -s 30x30}
${offset 35}${font DejaVu Sans:size=12}${color Tan1}"""+TasksProcesses[Language]+""" ${color}${hr 2}${font}
${offset 5}${color}"""+Load[Language]+""" ${loadavg 1}
#${running_processes} ${running_threads} ${processes}
${hr 2}${font}
${color lightgrey}${font DejaVu Sans Mono:size=9}${goto 5}PROCESS${goto 140}CPU${goto 192}"""+Memory[Language]+"""${goto 300}PID
${hr 1}
${goto 5}${top name 1}${goto 120}${top cpu 1}%${goto 192}${top mem_res 1}${goto 270}${top pid 1}
${goto 5}${top name 2}${goto 120}${top cpu 2}%${goto 192}${top mem_res 2}${goto 270}${top pid 2}
${goto 5}${top name 3}${goto 120}${top cpu 3}%${goto 192}${top mem_res 3}${goto 270}${top pid 3}
${goto 5}${top name 4}${goto 120}${top cpu 4}%${goto 192}${top mem_res 4}${goto 270}${top pid 4}
${goto 5}${top name 5}${goto 120}${top cpu 5}%${goto 192}${top mem_res 5}${goto 270}${top pid 5}${font}"""
# ${offset 5}${image img/proc-box01.png -p 0,48 -s 320x115}
# ${top name 1} $alignr ${top mem 1} ${tab 10} ${top cpu 1} ${top pid 1}

total=header+txt01
#print total

write_file('topfile', total)  # python will convert \n to os.linesep
