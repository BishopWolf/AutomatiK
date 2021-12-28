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
#Lists_Of_Cards=os.popen("LC_ALL=C lshw -class display | grep -i product | egrep -i 'GK|GF|GP|GM' ").read() # find only the nvidia cards
Lists_Of_Cards=os.popen("LC_ALL=C lshw -class display | grep -i product | egrep -i 'GK|GF|GP|GM' ").read() # find only the nvidia cards
#Lists_Of_Cards=os.popen("LC_ALL=C lshw -class display" ).read() # find only the nvidia cards

#CardName=CardName.split(': ')[-1]
#CardName=CardName.rstrip()
#print ("CardName",CardName)



#*-display
#description: VGA compatible controller
#product: GP104 [GeForce GTX 1070]
#vendor: NVIDIA Corporation
#physical id: 0
#bus info: pci@0000:01:00.0
#version: a1
#width: 64 bits
#clock: 33MHz
#capabilities: pm msi pciexpress vga_controller bus_master cap_list rom
#configuration: driver=nvidia latency=0
#resources: irq:45 memory:f6000000-f6ffffff memory:e0000000-efffffff memory:f0000000-f1ffffff ioport:e000(size=128) memory:c0000-dffff
#*-display
#description: VGA compatible controller
#product: GP104 [GeForce GTX 1070]
#vendor: NVIDIA Corporation
#physical id: 0
#bus info: pci@0000:02:00.0
#version: a1
#width: 64 bits
#clock: 33MHz
#capabilities: pm msi pciexpress vga_controller bus_master cap_list rom
#configuration: driver=nvidia latency=0
#resources: irq:46 memory:f4000000-f4ffffff memory:c0000000-cfffffff memory:d0000000-d1ffffff ioport:d000(size=128) memory:f5000000-f507ffff
#"""

Lists_Of_Cards=Lists_Of_Cards.strip()
Lists_Of_Cards=Lists_Of_Cards.split('*-display')


#Lists_Of_Cards=["GTX660,GTX660"]
#Lists_Of_Cards=
#IsNvidiaSettingsInstalled=os.popen("which nvidia-settings").read()
#if IsNvidiaSettingsInstalled!="":
	# Num=0
	# for i in Lists_Of_Cards:
	# 		#s=os.popen("nvidia-settings -q Gpus | grep gpu:0").read()
	# 		#card=s[s.find("(")+1:s.find(")")] # extract only the card name

	# 		# detect Connetion type
	# 		ConnectorToDisplay=os.popen("nvidia-settings -q XineramaInfoOrder -t").read().rstrip()
	# 		if ConnectorToDisplay=="":
	# 			ConnectorToDisplay="N/A"

	# 		# detect if fan speed is available
	# 		FanDetector=os.popen("nvidia-settings -q [fan:0]/GPUCurrentFanSpeedRPM -t").read()
	# 		if FanDetector=="":
	# 			RPM="N/A"
	# 		else:
	# 			RPM="RPM"

	# 		# detect Maximum clock speed
	# 		MaximumClock=os.popen("nvidia-settings -q all -t  | grep GPUCurrentClockFreqs:").read().split(",")
	# 		MaximumClock=(MaximumClock[len(MaximumClock)-1:])
	# 		MaximumClock=MaximumClock[0].rstrip()
	# 		#print (MaximumClock)
	# 		# detect Screen Resolution
	# 		ScreenResolution=os.popen("nvidia-settings -q ScreenPosition -t").read()
	# 		ScreenResolution = ScreenResolution.replace(' ','').split(',')
	# 		Width=ScreenResolution[2].split('=')[1].rstrip()
	# 		Height=ScreenResolution[3].split('=')[1].rstrip()
	# 		RefreshRate=os.popen("nvidia-settings -q [dpy:1]/RefreshRate -t").read().rstrip()
	# 		DriverVersion=os.popen("nvidia-settings -q 0/NvidiaDriverVersion -t").read().rstrip()
	# 		#print (Width)
	# 		#print (Height)
	# 		TotalMemory=os.popen("nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t").read()
	# 		#print TotalMemory
	# 		Num=Num+1
	# else:
	# 			CardName=CardName+" - No nvidia drivers found !          "
	# 			ConnectorToDisplay=""
	# 			Width=os.popen("xrandr | grep '*' | awk '{ print $1}'").read().rstrip()
	# 			Height=""
	# 			RefreshRate=""
	# 			DriverVersion=""
	# 			MaximumClock=""
	# 			TotalMemory=""


txt01="""
gap_x   1080
gap_y 50

lua_load allcombined.lua

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+""" ${color}${hr 2}${font}"""


Lists_Of_Cards=['product: GK106 [GeForce GTX 1080]','product: GK106 [GeForce GTX 780]','product: GK107 [GeForce GTX 1470]','product: GK108 [GeForce GTX 1080]']

List = []
Height_conky=115
g=len(Lists_Of_Cards)
#NumberOfCores=1
for Card in range(int(len(Lists_Of_Cards))):
	Comment="# Cardname"+str(Card+1)+"\n" 
	CardName=Lists_Of_Cards[Card].split('product:')[1]
	CardName="${color yellow}${font Ubuntu-Title:size=11}"+CardName+"${font}"
	Number_Of_Cores="${font}${color}${alignr}${exec nvidia-settings -q [gpu:0]/CUDACores -t} CUDA Cores"
	Speed_Of_Fan="${voffset 10}${goto 80}"+FanSpeed[Language]+": ${alignr}  ${exec nvidia-settings -q [fan:"+str(Card)+"]/GPUCurrentFanSpeedRPM -t} RPM"

	# detect Screen Resolution
	ScreenResolution=os.popen("nvidia-settings -q ScreenPosition -t").read()
	ScreenResolution = ScreenResolution.replace(' ','').split(',')
	Width=ScreenResolution[2].split('=')[1].rstrip()
	Height=ScreenResolution[3].split('=')[1].rstrip()
	RefreshRate=os.popen("nvidia-settings -q [dpy:1]/RefreshRate -t").read().rstrip()
	DriverVersion=os.popen("nvidia-settings -q 0/NvidiaDriverVersion -t").read().rstrip()
	Height_Width="${goto 80}"+str(DisplayResolution[Language])+" :${alignr}"+Width+" x "+Height+"-"+RefreshRate
	DriverVersion="${goto 80}Driver :${alignr}"""+DriverVersion
	
	# detect Maximum clock speed+title
	MaximumClock=os.popen("nvidia-settings -q all | grep -w GPUCurrentClockFreqs | grep gpu:0").read().strip()
	MaximumClock=MaximumClock.split(',')
	MaximumClock=MaximumClock[1]
	Frequency_Text=Frequency[Language]+"$alignr ${nvidia memfreq} / "+str(MaximumClock)+" Mhz"
	Frequency_Bar='${lua gradbar {6,'+str(Height_conky+40)+', "${nvidia memfreq}" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}	${image img/trans-bg240.png -p 3,'+str(Height_conky+35)+' -s 314x11}'
    #${lua gradbar {6, 190, "${nvidia memfreq}" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,136 -s 314x11}
	# detect Displays
	try:		
		Display_Brand="${goto 80}"+ScreenDisplay[Language]+" :${alignr} N/A"
	except:
		pass

	try:
		Screen_Detection=os.popen("cat /var/log/Xorg.0.log | grep -i -w connected | sed -e 's/([^()]*)//g'").read().split(':')[1]
		Display_Brand="${goto 80}"+ScreenDisplay[Language]+" :${alignr}"+str(Screen_Detection)
	except:
		pass


	try:
		Screen_Detection=os.popen("nvidia-xconfig --query-gpu-info | grep EDID").read().split(':')[1]
		Screen_Detection=Screen_Detection.rstrip()
		Display_Brand="${goto 80}"+ScreenDisplay[Language]+" :${alignr}"+str(Screen_Detection)
	except:
		pass
	# memory text + bar
	print Display_Brand
	Memory_Text=Ram[Language]+"${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB "
	Memory_Bar_List=[]
	M1="${lua gradbar {6, "+str(Height_conky+70)+" ,"
	M2='"${exec nvidia-settings -q [gpu:'
	M3="0"
	M4=']/UsedDedicatedGPUMemory -t}"'
	M5=",1996 , 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"
	M6=str(Height_conky+65)
	M7=' -s 314x11}'
	Memory_Bar_List.append(M1)
	Memory_Bar_List.append(M2)	
	Memory_Bar_List.append(M3)
	Memory_Bar_List.append(M4)
	Memory_Bar_List.append(M5)
	Memory_Bar_List.append(M6)
	Memory_Bar_List.append(M7)		
	Memory_Bar=''.join(Memory_Bar_List)
	#Memory_Bar="${lua gradbar {6, "+str(Height_conky+70)+" , "${exec nvidia-settings -q [gpu:"+str(Card)+ " # ]/UsedDedicatedGPUMemory -t}" ,1996, 105,2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"+str(Height_conky+65)+" -s 314x11}"
	#Memory_Bar="${lua gradbar {6, "+str(Height_conky+70)+", "${exec nvidia-settings -q [gpu:"+str(Card)+"]/UsedDedicatedGPUMemory -t}" ,1996, 105,2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"+str(Height_conky+65)+" -s 314x11}"
	#${lua gradbar {6, 190, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,1996 , 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,186 -s 314x11}


	#${lua gradbar {6,160, "${nvidia memfreq}" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}	${image img/trans-bg240.png -p 3,160 -s 314x11}
	#Mémoire vive${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB${image img/trans-bg240.png -p 3,166 -s 314x11} 


	#${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
	#"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
	#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}


	# detect Connetion type
	ConnectorToDisplay=os.popen("nvidia-settings -q XineramaInfoOrder -t").read().rstrip()
	if ConnectorToDisplay=="":
		ConnectorToDisplay="N/A"
	Connector_Type="${goto 80}Connector :${alignr}"+ConnectorToDisplay+"\n"

	# temperature bar + text
	Temperature_Text=Temperature[Language]+" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C"
	Temperature_Bar_List=[]
	T1="${lua gradbar {6, "+str(Height_conky+100)+" ,"
	T2='"${exec nvidia-settings -q [thermalsensor:'
	T3="0"
	T4=']/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,'
	T5=str(Height_conky+95)
	T6=" -s 314x11}"
	Temperature_Bar_List.append(T1)
	Temperature_Bar_List.append(T2)
	Temperature_Bar_List.append(T3)	
	Temperature_Bar_List.append(T4)
	Temperature_Bar_List.append(T5)
	Temperature_Bar_List.append(T6)	
	Temperature_Bar=''.join(Temperature_Bar_List)			
	#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}

	PathToLOGO="${image img/"+LOGO+" -p 5,"+str(Height_conky-55)+" }"

	Separator="${color}${hr 1}"



	List.append(Comment+"\n")
	List.append(CardName)	
	List.append(Number_Of_Cores+"\n")
	List.append(Speed_Of_Fan+"\n")
	List.append(Height_Width+"\n")
	List.append(DriverVersion+"\n")
	List.append(Display_Brand+"\n")		
	List.append(Connector_Type)				
    #List.append(BackgroundImage)
	List.append(Frequency_Text+"\n")
	List.append(Frequency_Bar+"\n")	
	List.append(Memory_Text+"\n")
	List.append(Memory_Bar+"\n")	
	List.append(Temperature_Text+"\n")
	List.append(Temperature_Bar+"\n")
	List.append(PathToLOGO)	
	List.append(Separator)

	Height_conky=Height_conky+207
TotalGPU=''.join(List)	

	#reste="""+Ram[Language]+"""${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB 
	#${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
	#"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
	#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}


	#    CpuName=""+Cpu[Language]+" "+str(Cores+1)
#	${color yellow}${font Ubuntu-Title:size=11}"""+CardName+"""${font}${color}${alignr}${exec nvidia-settings -q [gpu:0]/CUDACores -t} CUDA Cores
#	${voffset 10}${goto 80}"""+FanSpeed[Language]+""": ${alignr}  ${exec nvidia-settings -q [fan:0]/GPUCurrentFanSpeedRPM -t} """+RPM+"""
#	${goto 80}"""+ScreenDisplay[Language]+""" :${alignr}"""+Width+""" x """+Height+"""-"""+RefreshRate+"""
#	${goto 80}Connector :${alignr}"""+ConnectorToDisplay+"""
#	${goto 80}Driver :${alignr}"""+DriverVersion+"""
#	"""+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+MaximumClock+""" Mhz
#	${lua gradbar {6, 140, "${nvidia memfreq}" ,"""+MaximumClock+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,136 -s 314x11}
#	"""+Ram[Language]+"""${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB 
#	${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
#	"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
#	${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}
# 
 


total=header+txt01+TotalGPU
writefile( total)


