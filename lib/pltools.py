# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ProhdIPTV/lib/ProhdIPTVfunctions.py
import os, urllib
PLUGIN_PATH='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'
logfile='/tmp/TuneinRadio.log'

from Tools.Directories import fileExists
def getmDevices():
        myusb = myusb1 = myhdd = myhdd2 = mysdcard = mysd = myuniverse = myba = ''
        mdevices = []
        myusb=None
        myusb1=None
        myhdd=None
        myhdd2=None
        mysdcard=None
        mysd=None
        myuniverse=None
        myba=None
        if fileExists('/proc/mounts'):
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/backup'
                    if not os.path.exists('/media/usb/backup'):
                       os.system('mkdir -p /media/usb/backup')
                elif line.find('/media/usb1') != -1:
                    myusb1 = '/media/usb1/backup'
                    if not os.path.exists('/media/usb1/backup'):
                       os.system('mkdir -p /media/usb1/backup')
                elif line.find('/media/hdd') != -1:
                    myhdd = '/media/hdd/backup'
                    if not os.path.exists('/media/hdd/backup'):
                       os.system('mkdir -p /media/hdd/backup')
                elif line.find('/media/hdd2') != -1:
                    myhdd2 = '/media/hdd2/backup'
                    if not os.path.exists('/media/hdd2/backup'):
                       os.system('mkdir -p /media/hdd2/backup')
                elif line.find('/media/sdcard') != -1:
                    mysdcard = '/media/sdcard/backup'
                    if not os.path.exists('/media/sdcard/backup'):
                       os.system('mkdir -p /media/sdcard/backup')
                elif line.find('/media/sd') != -1:
                    mysd = '/media/sd/backup'
                    if not os.path.exists('/media/sd/backup'):
                       os.system('mkdir -p /media/sd/backup')
                elif line.find('/universe') != -1:
                    myuniverse = '/universe/backup'
                    if not os.path.exists('/universe/backup'):
                       os.system('mkdir -p /universe/backup')
                elif line.find('/media/ba') != -1:
                    myba = '/media/ba/backup'
                    if not os.path.exists('/media/ba/backup'):
                       os.system('mkdir -p /media/ba/backup')
            f.close()
        if myusb:
            mdevices.append((myusb, myusb))
        if myusb1:
            mdevices.append((myusb1, myusb1))
        if myhdd:
            mdevices.append((myhdd, myhdd))
        if myhdd2:
            mdevices.append((myhdd2, myhdd2))
        if mysdcard:
            mdevices.append((mysdcard, mysdcard))
        if mysd:
            mdevices.append((mysd, mysd))
        if myuniverse:
            mdevices.append((myuniverse, myuniverse))
        if myba:
            mdevices.append((myba, myba))
        return mdevices


def trace_error():
    import sys
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        if os.path.exists(logfile):
            logfile = 'logfile'
        else:
            return
        traceback.print_exc(file=open(logfile, 'a'))
    except:
        pass


def dellog():
    try:
        if os.path.exists(logfile):
            os.remove(logfile)
    except:
        pass

def getversioninfo(plugin_folder):
    currversion = '1.6'
    enigmaos = 'oe2.0'
    currpackage = 'full'
    currbuild = '01012016'
   
    version_file='/usr/lib/enigma2/python/Plugins/Extensions/'+plugin_folder + '/version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split(':')[1].strip()
                if 'kernel' in line:
                    enigmaos = line.split(':')[1].strip()
                if 'package' in line:
                    currpackage = line.split(':')[1].strip()
                if 'build' in line:
                    currbuild = line.split(':')[1].strip()

        except:
            pass

    return (currversion,
     enigmaos,
     currpackage,
     currbuild)


def gethostname():
    path = '/etc/hostname'
    hostname = 'None'
    if os.path.exists(path):
        f = open(path, 'r')
        hostname = f.read()
        f.close()
        if 'dm800se' in hostname:
            return 'dm800se'
        if 'dm8000' in hostname:
            return 'dm8000'
        if 'dm800' in hostname:
            return 'dm800hd'
        if 'dm500' in hostname:
            return 'dm500hd'
        if 'dm7020' in hostname:
            return 'dm7020hd'
        if 'dm820' in hostname:
            return 'dm820'
        if 'dm520' in hostname:
            return 'dm520'
        if 'dm7080' in hostname:
            return 'dm7080'
        if 'dm900' in hostname:
            return 'dm900'
        
        else:
            if "vu" in hostname:
                hostname=hostname.replace("vu","")
            return hostname
        return 'None'
    return 'None'

def IsValidFileName(name, NAME_MAX=255):
    prohibited_characters = ['/', "\000", '\\', ':', '*', '<', '>', '|', '"']
    if isinstance(name, basestring) and (1 <= len(name) <= NAME_MAX):
        for it in name:
            if it in prohibited_characters:
                return False
        return True
    return False
    
def RemoveDisallowedFilenameChars(name, replacment='.'):
    prohibited_characters = ['/', "\000", '\\', ':', '*', '<', '>', '|', '"']
    for item in prohibited_characters:
        name = name.replace(item, replacment).replace(replacment+replacment, replacment)
    return name
def log(label, txt):
    txt = str(txt)
    label = str(label)
    try:
        afile = open(logfile, 'a')####change
    except:
        return

    afile.write('\n' + label + ':' + txt)
    afile.close()
def addstreamboq(bouquetname=None):
    boqfile = '/etc/enigma2/bouquets.radio'
    if not os.path.exists(boqfile):
        pass
    else:
        fp = open(boqfile, 'r')
        lines = fp.readlines()
        fp.close()
        add = True
        for line in lines:
            if 'userbouquet.' + bouquetname + '.tv' in line:
                add = False
                break

    if add == True:
        fp = open(boqfile, 'a')
        fp.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.%s.tv" ORDER BY bouquet\n' % bouquetname)
        fp.close()
        add = True


def addstream(url=None, name=None, bouquetname=None):
    error = 'none'
    bouquetname = 'TuneinRadio'
    import urllib


    fileName = '/etc/enigma2/userbouquet.%s.radio' % bouquetname
    out = '#SERVICE 4097:0:0:0:0:0:0:0:0:0:%s:%s\r\n' % (urllib.quote(url), urllib.quote(name))
    try:
        addstreamboq(bouquetname)
        if not os.path.exists(fileName):
            fp = open(fileName, 'w')
            fp.write('#NAME %s\n' % bouquetname)
            fp.close()
            fp = open(fileName, 'a')
            fp.write(out)
        else:
            fp = open(fileName, 'r')
            lines = fp.readlines()
            fp.close()
            for line in lines:
                if out in line:
                    error = 'Stream already added to bouquet'
                    return error

            fp = open(fileName, 'a')
            fp.write(out)
        fp.write('')
        fp.close()
    except:
        error = 'Adding to bouquet failed'

    return error


