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
LOGO="Intel_HD_logo.png"
PathToLOGO="${image img/"+LOGO+" -p 5,55 }"

# ------------- Card Name --------------------------
CardName=os.popen("LC_ALL=C lshw -class display | grep -i product").read() # find the cards

CardName=CardName.split(': ')[-1]
CardName=CardName.rstrip()


# ------------- Resolution --------------------------
Resolution=os.popen("xrandr | grep -E '^[^ ]|[0-9]\*\+' | grep *+").read() 
Resolution=Resolution.rstrip()
Resolution=Resolution.split()
Resolution=Resolution[0]
print (Resolution)




# ------------- RefreshRate --------------------------
RefreshRate=os.popen("xrandr | grep -E '^[^ ]|[0-9]\*\+' | grep *+").read() 
RefreshRate=RefreshRate.rstrip()
RefreshRate=RefreshRate.split()
RefreshRate=RefreshRate[1][:-2]
#print (Frequency)


# ------------- Connector --------------------------
ConnectorList=os.popen("xrandr | grep connected | grep -v disconnected").readlines()
Connectors=[]
print ("test1",ConnectorList)
for i in ConnectorList:
	i=i.rstrip()
	i=i.split()
	print (i[0])
	Connectors.append(i[0])
#	for a in i:
#		if 

ResolutionList=os.popen("xrandr | grep *+").readlines()
Resolutions=[]
print (ResolutionList)
for i in ResolutionList:
	i=i.rstrip()
	i=i.split()
	print (i[0])
	Resolutions.append(i[0])
#{print Connectors
#print Resolutions

#print Connector
ConnectorToDisplay=os.popen("xrandr | grep 0+0").readlines() 
#print "0   ",ConnectorToDisplay


number=0
for i in ConnectorToDisplay:
	ConnectorToDisplay[number]=ConnectorToDisplay[number].rstrip()
	#print "a   ",ConnectorToDisplay[number]
	ConnectorToDisplay[number]=ConnectorToDisplay[number].split(' ', 1)[0]
	#print "b   ",ConnectorToDisplay[number]
	number=number+1
	#print 

number=0

#print ConnectorToDisplay
Connector_List = []
#''.join(list).
for i in Connectors:
	ConnectorToDisplay_TEXT="""${goto 80}"""+ScreenDisplay[Language]+""" :"""+i+"""${alignr} """+Resolutions[number]+"\n"
	#print ConnectorToDisplay_TEXT
	Connector_List.append(ConnectorToDisplay_TEXT)
	number=number+1
Total_Connector=''.join(Connector_List)
#print "fdsfd",Total_Connector

#TotalCpu=''.join(List)
#print 

# ------------- Drivers --------------------------
DriverVersion=os.popen("""LC_ALL=C lspci -v -s $(lspci | grep ' VGA ' | cut -d" " -f 1) | grep driver""").read() 
if DriverVersion!="":
    DriverVersion=DriverVersion.rstrip()
    try:
        DriverVersion=DriverVersion.split(': ')
    except:
        pass
    try:
        DriverVersion=DriverVersion[1]
    except:
        pass
else:
    DriverVersion="Unknown"
#print (DriverVersion)

# ------------- InstalledVram --------------------------
InstalledVram=os.popen("""RAM=$(cardid=$(lspci | grep VGA |cut -d " " -f1);lspci -v -s $cardid | grep " prefetchable"| cut -d "=" -f2);echo $RAM""").read() 
#InstalledVram=os.popen('lspci -v -s $cardid | grep " prefetchable"| cut -d "=" -f2).read() 
InstalledVram=InstalledVram.rstrip()
#InstalledVram=InstalledVram.split()
#for i in InstalledVram:
#	if "RAM=" in i:
#		InstalledVram=i[4:]
#InstalledVram=InstalledVram[1]
#print (InstalledVram)

#dmesg | grep -E 'drm|radeon' | grep Detected
#"""+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+MaximumClock+""" Mhz


txt01="""
gap_x   1080
gap_y 50

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+""" ${color}${hr 2}${font}
${color yellow}${font Ubuntu-Title:size=11}"""+CardName+"""





"""

total=header+txt01+PathToLOGO
writefile( total)


