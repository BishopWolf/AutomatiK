# -*- encoding: utf-8 -*-
import os
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
else:
	Language="English"


def writefile( str ):
	f = open('graphiccardfile', 'w')
	f.write(str)  # python will convert \n to os.linesep
	f.close()  # you can omit in most cases as the destructor will call it

header = open('header.py', 'r').read()
LOGO="Nvidia_logo.png"
PathToLOGO="${image img/"+LOGO+" -p 5,55 }"

# ------------- Card Name --------------------------
CardName=os.popen("LC_ALL=C lshw -class display | grep -i product | grep -E -i 'GK|GF|GP|GM' ").read() # find only the nvidia cards

CardName=CardName.split(': ')[-1]
CardName=CardName.rstrip()
#print ("CardName",CardName)

IsNvidiaSettingsInstalled=os.popen("which nvidia-settings").read()
if IsNvidiaSettingsInstalled!="":
			#s=os.popen("nvidia-settings -q Gpus | grep gpu:0").read()
			#card=s[s.find("(")+1:s.find(")")] # extract only the card name

			# detect Connetion type
			ConnectorToDisplay=os.popen("nvidia-settings -q XineramaInfoOrder -t").read().rstrip()
			if ConnectorToDisplay=="":
				ConnectorToDisplay="N/A"

			# detect if fan speed is available
			FanDetector=os.popen("nvidia-settings -q [fan:0]/GPUCurrentFanSpeedRPM -t").read()
			if FanDetector=="":
				RPM="N/A"
			else:
				RPM="RPM"

			# detect Maximum clock speed
			MaximumClock=os.popen("nvidia-settings -q all -t  | grep GPUCurrentClockFreqs:").read().split(",")
			MaximumClock=(MaximumClock[len(MaximumClock)-1:])
			MaximumClock=MaximumClock[0].rstrip()
			#print (MaximumClock)
			# detect Screen Resolution
			ScreenResolution=os.popen("nvidia-settings -q ScreenPosition -t").read()
			ScreenResolution = ScreenResolution.replace(' ','').split(',')
			Width=ScreenResolution[2].split('=')[1].rstrip()
			Height=ScreenResolution[3].split('=')[1].rstrip()
			RefreshRate=os.popen("nvidia-settings -q [dpy:1]/RefreshRate -t").read().rstrip()
			DriverVersion=os.popen("nvidia-settings -q 0/NvidiaDriverVersion -t").read().rstrip()
			#print (Width)
			#print (Height)
			TotalMemory=os.popen("nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t").read()
			#print TotalMemory
else:
			CardName=CardName+" - No nvidia drivers found !          "
			ConnectorToDisplay=""
			Width=os.popen("xrandr | grep '*' | awk '{ print $1}'").read().rstrip()
			Height=""
			RefreshRate=""
			DriverVersion=""
			MaximumClock=""
			TotalMemory=""


txt01="""
gap_x   1080
gap_y 50

lua_load allcombined.lua

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+""" ${color}${hr 2}${font}
${color yellow}${font Ubuntu-Title:size=11}"""+CardName+"""${font}${color}${alignr}${exec nvidia-settings -q [gpu:0]/CUDACores -t} CUDA Cores
${voffset 10}${goto 80}"""+FanSpeed[Language]+""": ${alignr}  ${exec nvidia-settings -q [fan:0]/GPUCurrentFanSpeedRPM -t} """+RPM+"""
${goto 80}"""+ScreenDisplay[Language]+""" :${alignr}"""+Width+""" x """+Height+"""-"""+RefreshRate+"""
${goto 80}Connector :${alignr}"""+ConnectorToDisplay+"""
${goto 80}Driver :${alignr}"""+DriverVersion+"""
"""+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+MaximumClock+""" Mhz
${lua gradbar {6, 140, "${nvidia memfreq}" ,"""+MaximumClock+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,136 -s 314x11}
"""+Ram[Language]+"""${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB 
${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}
"""

total=header+txt01+PathToLOGO
writefile( total)


