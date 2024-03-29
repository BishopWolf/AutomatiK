# -*- encoding: utf-8 -*-
import os,time
header = open('header.py', 'r').read()
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



List_Of_Devices=[]
#time.sleep(5)
#  /dev/sda1
Partition_Name=os.popen("df -Th 2>/dev/null | grep -E 'dev|media' | grep -E -v '^.*(tmp|lib|proc|sys|pts|daemon|root|gvfs|efi).*$'| awk '{ print $1}'").read().split() 

#new line ? : df -Th | grep dev| grep -E -v '^.*(tmp|proc|sys|var|pts|daemon|root|gvfs|efi).*$'



# ext4
File_Type=os.popen("df -PTh 2>/dev/null | grep -E 'dev|media' | grep -E -v '^.*(tmp|lib|proc|sys|pts|daemon|root|gvfs|efi).*$'| awk '{ print $2}'").read().split()


# Size
Partition_Size=os.popen("df -PTh 2>/dev/null | grep -E 'dev|media' | grep -E -v '^.*(tmp|lib|proc|sys|pts|daemon|root|gvfs|efi).*$'| awk '{ print $3}'").read().split()

#  /media/data_zalman
Mount_Point=os.popen("df -PTh 2>/dev/null | grep -E 'dev|media' | grep -E -v '^.*(tmp|lib|proc|sys|pts|daemon|root|gvfs|efi).*$' |  awk '{ print $7}'").read().split()
#print Mount_Point, len(Mount_Point)

	


#  print Mount_Point

#for dev in List_Of_Mounted_Partitions:
#	dev=dev.replace('\\040'," ")
#	List_Of_Mounted_Partitions[i]=dev
#	i=i+1




txt01="""
gap_x 745
gap_y 50

lua_load allcombined.lua

TEXT
${image img/hard_drive.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+DiskUsage[Language]+""" ${color}${hr 2}${font}
"""

List = []
Height=70
for name, point, size in zip(Partition_Name, Mount_Point, Partition_Size):
	if len (point)>35:
		Truncated=point[0:35]+"~"
		Mount=" ${color}"+Truncated+"\n"
	else:
		Mount=" ${color}"+point+"\n"
	Graph=f'${{fs_bar 11,230 {point}}}'
	PercentUsed="${alignr}${offset -5}${fs_used_perc "+point+"}% "+UsedWord[Language]+"\n"
	if len (name)>18:
		Truncated=name[0:18]+"~"		
		DriveName=" "+Truncated+" = "+size+" (${fs_type "+point+"})"
	else:		
		DriveName=" "+name+" = "+size+" (${fs_type "+point+"})"
	FreeSpace="${color}${alignr}${offset -5}${fs_free "+point+"} "+FreeWord[Language]+"\n"
	Separator="${color}${hr 1}"+"\n\n"
	BackgroundImage="${image img/trans-bg240.png -p 4,"+str(Height-3)+" -s 226x11}"

	List.append(Mount)
	List.append(Graph)
	List.append(PercentUsed)
	List.append(DriveName)
	List.append(FreeSpace)
	List.append(Separator)
	List.append(BackgroundImage)
	Height=Height+75
TotalDisk=''.join(List)
#print "TotalDisk",TotalDisk

#${lua gradbar {6, 70, "${fs_used_perc /}" ,100, 75, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${alignr}${offset -5}${fs_used_perc /}% utilisés

txt02="""${color lightgrey}"""+DiskReading[Language]+""": $color${diskio_read}${alignr}${color lightgrey}"""+DiskWriting[Language]+""": ${color}${diskio_write}
${color #000000}${diskiograph_read 12,145 000000 EEEEEE}${alignr}${color #000000}${diskiograph_write 12,145 000000 EEEEEE}
"""




total=header+"\n"+txt01+"\n"+TotalDisk+"\n"+txt02
#print total

f = open('diskfile', 'w')
f.write(total)  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it
