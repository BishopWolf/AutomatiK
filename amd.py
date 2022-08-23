import os
from translations import *

# determine installed language
Language_installed = os.popen("locale | grep LANG").read()
if "fr" in Language_installed:
    Language = "French"
elif "de" in Language_installed:
    Language = "German"
elif "pt" in Language_installed:
    Language = "Portuguese"
elif "it" in Language_installed:
    Language = "Italian"
else:
    Language = "English"


def writefile(str):
    f = open('graphiccardfile', 'w')
    f.write(str)  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it


header = open('header.py', 'r').read()
LOGO = "Ati_logo.png"
PathToLOGO = "${image img/"+LOGO+" -p 5,55 }"

# ------------- Card Name --------------------------
BoardName = os.popen(
    "clinfo | grep -i 'Board name:'").readlines()[-1]  # find the cards

BoardName = BoardName.split(': ')[-1].strip()

CardSpecs = os.popen(
    "clinfo | grep -i '  Name:'").readlines()
CardName = CardSpecs[0].split(':')[1].strip()
CardGPU = CardSpecs[1].split('(')[1].split(',')[0].strip()

CardMemory = os.popen(
    "glxinfo | grep -i '  Video Memory:'").readlines()[-1]
CardMemory = CardMemory.split(':')[1].strip()

print(CardSpecs)
print(CardGPU, CardName)


# ------------- Resolution --------------------------
Resolution = os.popen("xrandr | egrep '^[^ ]|[0-9]\*\+' | grep *+").read()
Resolution = Resolution.rstrip()
Resolution = Resolution.split()
Resolution = Resolution[0]
print(Resolution)


# ------------- RefreshRate --------------------------
RefreshRate = os.popen("xrandr | egrep '^[^ ]|[0-9]\*\+' | grep *+").read()
RefreshRate = RefreshRate.rstrip()
RefreshRate = RefreshRate.split()
RefreshRate = RefreshRate[1][:-2]
#print (Frequency)


# ------------- Connector --------------------------
ConnectorList = os.popen(
    "xrandr | grep connected | grep -v disconnected").readlines()
Connectors = []
# print "test1",ConnectorList
for i in ConnectorList:
    i = i.rstrip()
    i = i.split()
    # print i[0]
    Connectors.append(i[0])
#	for a in i:
#		if

ResolutionList = os.popen("xrandr | grep *+").readlines()
Resolutions = []
# print ResolutionList
for i in ResolutionList:
    i = i.rstrip()
    i = i.split()
    # print i[0]
    Resolutions.append(i[0])
# print Connectors
print(Resolutions)

# print Connector
ConnectorToDisplay = os.popen("xrandr | grep 0+0").readlines()
# print "0   ",ConnectorToDisplay


number = 0
for i in ConnectorToDisplay:
    ConnectorToDisplay[number] = ConnectorToDisplay[number].rstrip()
    # print "a   ",ConnectorToDisplay[number]
    ConnectorToDisplay[number] = ConnectorToDisplay[number].split(' ', 1)[0]
    # print "b   ",ConnectorToDisplay[number]
    number = number+1
    # print

number = 0

# print ConnectorToDisplay
Connector_List = []
# ''.join(list).
for i,r in zip(Connectors, Resolutions):
    ConnectorToDisplay_TEXT = """${goto 80}""" + \
        """ :"""+i+"""${alignr} """+r+"\n"
    # print ConnectorToDisplay_TEXT
    Connector_List.append(ConnectorToDisplay_TEXT)
    number = number+1
Total_Connector = ''.join(Connector_List)
print("fdsfd", Total_Connector)

# TotalCpu=''.join(List)
# print

# ------------- Drivers --------------------------
DriverVersion = os.popen(
    """LC_ALL=C lspci -v -s $(lspci | grep ' VGA ' | cut -d" " -f 1) | grep driver """).read()
DriverVersion = DriverVersion.rstrip()
DriverVersion = DriverVersion.split(': ')
DriverVersion = DriverVersion[1]
print(DriverVersion)

# dmesg | egrep 'drm|radeon' | grep Detected
# """+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+MaximumClock+""" Mhz
txt01 = """
gap_x 380
gap_y 670

lua_load allcombined.lua

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+'GPU INFORMATION'+""" ${color}${hr 2}${font}
${color yellow}${font Ubuntu-Title:size=11}"""+BoardName+"""${font}${color}
"""+Total_Connector+"""
${goto 80}Driver :${alignr}"""+DriverVersion+"""
${goto 80}Card Name :${alignr}"""+CardName+"""
${goto 80}Card GPU :${alignr}"""+CardGPU+"""
${goto 80}Card Memory :${alignr}"""+CardMemory+"""
${goto 80}Free Memory :${alignr}${execi 10 glxinfo | grep -i 'Currently available dedicated video memory:' | awk '{ print $6}'} MB
${goto 80}fanspeed :${alignr}${execi 5 sensors | grep fan1 | head -n 2 | tail -n 1 | awk '{ print $2}'} RPM
${goto 80}Temperature: ${alignr}${execi 5 rocm-smi | head -n 6 | tail -n 1 | awk '{ print $2}'}
${goto 80}Power: ${alignr}${execi 5 rocm-smi | head -n 6 | tail -n 1 | awk '{ print $3}'}
${goto 80}GPU use: ${alignr}${execi 5 rocm-smi | head -n 6 | tail -n 1 | awk '{print $10}'}
${image img/Ati_logo.png -p 5,55 }
"""
total = header+txt01+PathToLOGO
writefile(total)
