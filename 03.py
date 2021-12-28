#!/usr/bin/python
import calendar
import locale

calobject = calendar.LocaleTextCalendar(calendar.MONDAY, 'de_DE')
calobject.formatmonth(2012, 10)
print calobject
#c = calendar.LocaleTextCalendar(locale=locale.getdefaultlocale())
#cal = calendar.month(2016, 2)
#test=cal.split('\n')
#for g in test:
#	print g
#print (test)

#f = open('test', 'w')
#f.write(test)  # python will convert \n to os.linesep
#f.close()  # you can omit in most cases as the destructor will call it
