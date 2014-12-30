#!usr/bin/python

import os

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
def main():
        diskStat = getDiskSpace()
	diskUse = diskStat[1]
        diskPerc = diskStat[3]
	diskTotal = diskStat[0]
	print "%s of %s (%s) Memory used" % (diskUse, diskTotal, diskPerc)

if __name__ == '__main__':
    main()


