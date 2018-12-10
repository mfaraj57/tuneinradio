# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ProhdIPTV/lib/ProhdIPTVfunctions.py
import os, urllib
PLUGIN_PATH='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'

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
        afile = open('/tmp/tuneinradio_log', 'a')####change
    except:
        return

    afile.write('\n' + label + ':' + txt)
    afile.close()


