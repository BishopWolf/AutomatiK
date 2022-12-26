# -*- encoding: utf-8 -*-
import os
import re
import platform


CardVendor = os.popen(
    "clinfo | grep -i 'Platform Vendor:'").read().rstrip().lower().split("\n")

if len(CardVendor) > 1:
    for i in range(len(CardVendor)):
        # print "boucle",i,CardVendor[i]
        if CardVendor[i].find('intel') != -1:
            CardVendor[i] = ""

# print "apres",CardVendor
#CardVendor=CardVendor.rsplit(':', 1)[1]

# CardVendor=CardVendor.rstrip()
# CardVendor=CardVendor.lower()
# usage ${execi 5 radeontop -d- -l1 | grep -o 'gpu [0-9]\{1,3\}' | cut -c 5-7 }%
# ${execi 5 radeontop -d- -l1 }%
# mem${execi 5 radeontop -d- -l1 | grep -o 'vram [0-9]\{1,3\}' | cut -c 5-7 }%


# CardName=os.popen("LC_ALL=C lshw -class display | grep -i product | grep -E -i 'GK|GF|GP|GM' ").read() # find only the nvidia cards


# T="fdslfjlkm[jfsglm]fjsdklf[12345]fdsf"
#total=re.findall(r'\[([^]]*)\]', T)
# CardName=""
# for i in total:
#	CardName=i+" "+CardName


# detect if nvidia-settings is installed

# nvidia-settings -q all -t  >> nvidiaOptions.txt

# nvidia-settings -q XineramaInfoOrder -t 			DVI
# nvidia-settings -q ScreenPosition -t				x=0, y=0, width=1920, height=1080
# nvi./st	'*'")[3:12]

# nvidia-settings -q [gpu:0]/GPUMemoryInterface -t

# print t.find('amd')
# chown root.root radeontop; chmod u+s radeontop
if CardVendor[0].find('amd') != -1:
    import amd


elif CardVendor[0].find('nvidia') != -1:
    import nvidia


elif CardVendor[0].find('intel') != -1:
    txt01 = """
gap_x   380
gap_y 450

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+""" ${color}${hr 2}${font}
${color yellow}${font Ubuntu-Title:size=11}"""+CardName+"""


"""
# else:
#		LOGO="Question-mark.png" # question mark
#		txt01="""
# gap_x   1080
# gap_y 50

# lua_load allcombined.lua

# TEXT
# ${image img/graphic_card.png -p 0,0 -s 30x30}
# ${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+""" ${color}${hr 2}${font}
# ${color yellow}${font Ubuntu-Title:size=11}"""+CardName+"""${font}${color}
# """
