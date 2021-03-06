#!/usr/bin/python

"""
ver 1.0.150831
"""

import sys
import re
import os
import urllib2
import datetime

DAT="gled1.dat"
LOG="gled1.log"
inst0=0
inst1=0
ipad0=""
ipad1=""
LOGLEN=15
zviz=""

if os.path.isfile(LOG) is True:
    with open(LOG, 'r') as logdt:
        line = logdt.readlines()
        loglen = len(line)

    #print("br.lin: %s" % loglen)
    logdt.close()

else:
    loglen=0
    line=""

with open(LOG, 'w') as logdt:
    for i in range(max(loglen-LOGLEN, 0), loglen):
        #print(" %d: %s" % (i, line[i].rstrip()))
        logdt.write(line[i].rstrip() + "\n")

    dt1=datetime.datetime.now()
    dt2=dt1.strftime("%d.%m %H:%M: ")
    logdt.write(dt2)

    if os.path.isfile(DAT) is True:
        #print("vratilo istinu")
        with open(DAT, 'r') as dato:
            line = dato.readlines()

        for li1 in line:
            m1=re.search(r'INET=(?P<stri>\d+)', li1)
            if m1 is not None:
                #print(str(m1.groupdict()))
                inst0=int(m1.group('stri'))

            m1=re.search(r'IPAD=(?P<stri>(\d+\.*)+)', li1)
            if m1 is not None:
                ipad0=m1.group('stri')

        dato.close()

    resp=os.system("ping -c 1 -W 2 195.29.150.3 > /dev/null")
    if resp == 0:
        inst1=1
        req=urllib2.Request("http://kek0.net/ip.php")
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            print("%s %s" % (e.code, e.read()))
        else:
            ipad2=resp.read().rstrip()
            m2=re.search(r'(?P<stri>^(\d+\.*)+)$', ipad2)
            if m2 is not None:
                ipad1=m2.group('stri')
            
    
    if inst1 != inst0 or ipad1 != ipad0:
        with open(DAT, 'w') as dato:
            dato.write("INET=%d\nIPAD=%s" % (inst1, ipad1))
            dato.close()
    
    if inst1 == 1 and inst0 == 0 or ipad1 != ipad0:
        zviz=" ("+ipad0+") *"
        if ipad1 != "":
            #print(" ** service restart! **")
            os.system("service noip2 restart > /dev/null")

    #print("ovo: %d - %d, ono: %s%s" % (inst0, inst1, ipad1, zviz))
    logdt.write(" %s-%s : %s%s" % (inst0, inst1, ipad1, zviz))
    logdt.close()
