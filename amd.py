import os
from common import detect_language, read_header, write_file
from translations import *

Language = detect_language()
header = read_header()


LOGO = "Ati_logo.png"
PathToLOGO = "${image img/"+LOGO+" -p 5,55 }"

# ------------- Card Name --------------------------
#CardName = os.popen(
#    "clinfo | grep -i '  Device Name'").readlines()[0].split()[-1].strip()  # find the cards

#CardName = CardName.split(': ')[-1].split('[')[0].strip()
CardName="gfx803"

BoardName = os.popen(
    "glxinfo | grep -i '  Device:'").readlines()[0].split(': ')[-1].strip()
CardSpecs = BoardName.split('(')
BoardName = CardSpecs[0].strip()
CardGPU = CardSpecs[1].strip().split(',')[1].strip()
#CardName = os.popen("rocm-smi | tail -n +1 | head -n 9 | tail -n 1 | awk '{ print $1}'").readlines()[0].strip()

CardMemory = os.popen(
    "glxinfo | grep -i '  Video Memory:'").readlines()[-1]
CardMemory = CardMemory.split(':')[1].strip()

print(CardSpecs)
print(CardGPU, CardName)


# ------------- Resolution --------------------------
Resolution = os.popen(r"xrandr | grep -E '^[^ ]|[0-9]\*\+' | grep *+").read()
Resolution = Resolution.rstrip()
Resolution = Resolution.split()
Resolution = Resolution[0]
print(Resolution)


# ------------- RefreshRate --------------------------
RefreshRate = os.popen(r"xrandr | grep -E '^[^ ]|[0-9]*\+' | grep *+").read()
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

# print ConnectorToDisplay
Connector_List = []
# ''.join(list).
for i,r in zip(Connectors, Resolutions):
    ConnectorToDisplay_TEXT = """${goto 80}""" + \
        """ :"""+i+"""${alignr} """+r+"\n"
    # print ConnectorToDisplay_TEXT
    Connector_List.append(ConnectorToDisplay_TEXT)

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

# dmesg | grep -E 'drm|radeon' | grep Detected
# """+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+MaximumClock+""" Mhz
txt01 = """
gap_x 380
gap_y 727

lua_load allcombined.lua

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font DejaVu Sans:size=12}${color Tan1}"""+'GPU INFORMATION'+""" ${color}${hr 2}${font}
${color yellow}${font DejaVu Sans:size=11}"""+BoardName+"""${font}${color}
"""+Total_Connector+"""
${goto 80}Driver :${alignr}"""+DriverVersion+"""
${goto 80}Card Name :${alignr}"""+CardName+"""
${goto 80}Card GPU :${alignr}"""+CardGPU+"""
${goto 80}Card Memory :${alignr}"""+CardMemory+"""
${goto 80}Free Memory :${alignr}${execi 10 glxinfo | grep -i 'Currently available dedicated video memory:' | awk '{ print $6}'} MB
${goto 80}fanspeed :${alignr}${execi 5 sensors | grep amdgpu -A 6 | grep fan | head -n 2 | tail -n 1 | awk '{ print $2}'} RPM
${goto 80}Temperature: ${alignr}${execi 5 sensors | grep amdgpu -A 6 | grep edge | awk '{ print $2}'}
${goto 80}Power: ${alignr}${execi 5 sensors | grep amdgpu -A 6 | grep PPT | awk '{ print $2 " " $3}'}
${goto 80}GPU use: ${alignr}${execi 5 cat /sys/class/drm/card*/device/gpu_busy_percent 2>/dev/null | head -n 1} %
${goto 80}${execigraph 5 "cat /sys/class/drm/card*/device/gpu_busy_percent 2>/dev/null | head -n 1"}"""
total = header+txt01+PathToLOGO
write_file('graphiccardfile', total)
