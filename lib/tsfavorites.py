# 2016.03.14 10:37:05 Jerusalem Standard Time
#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/resources/TuneinRadiofavorites.py
import sys, os
import shutil
from enigma import loadPNG
from Components.config import config
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import ElementTree, dump, SubElement, Element
favlocation = "/etc/TuneinRadio"
xmlfile = favlocation + '/favorites2.xml'

PLUGIN_PATH='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'
def getfilename(backupRadioTuneinfolder):
    import datetime
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    for i in range(1, 100):
        filename = str(i) + '_' + day + month + year + '_favorites2.xml'
        if os.path.exists(backupRadioTuneinfolder + '/' + filename):
            continue
        else:
            return backupRadioTuneinfolder + '/' + filename


def getfavfiles(path):
    dirs = os.listdir(path)
    lines = []
    for file in dirs:
        if file.endswith('favorites2.xml'):
            lines.append((file, file))

    return lines


def copyfiles(src, dest):
    try:
        import os
        import shutil
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest)

        return True
    except:
        return False


def backupuserfiles():
    try:
        userfilesdir = '/etc/TuneinRadio'
        downloadfolder = config.TuneinRadio.downloadlocation.value
        backupRadioTuneinfolder = downloadfolder + '/TuneinRadio'
        result = shutil.copyfiles(userfilesdir, backupTuneinRadiofolder)
        return result
    except:
        print 'failed to backup favorites'
        return False


def restorefavorites():
    try:
        downloadfolder = config.TuneinRadio.downloadlocation.value
        favlocation = config.TuneinRadio.favlocation.value
        xmlfile = favlocation + '/favorites2.xml'
        backupTuneinRadiofolder = downloadfolder + '/TuneinRadio'
        backup_file = backupTuneinRadiofolder + '/favorites2.xml'
        tree = ElementTree()
        tree.parse(backup_file)
        root = tree.getroot()
        import shutil
        if not os.path.exists(backup_file):
            return False
        if os.path.exists(xmlfile):
            os.remove(xmlfile)
        shutil.copyfile(backup_file, xmlfile)
        return True
    except:
        print 'failed to restore favorites'
        return False


def restorefavorites2(session):
    try:
        downloadfolder = config.TuneinRadio.downloadlocation.value
        backupTuneinRadiofolder = downloadfolder + '/TuneinRadio'
        favlocation = config.TuneinRadio.favlocation.value
        nlines = []
        nlines = getfavfiles(backupTuneinRadiofolder)
        from Screens.ChoiceBox import ChoiceBox
        session.openWithCallback(stchoicesback, ChoiceBox, _('select favorites name'), nlines)
        return True
    except:
        return False


def stchoicesback(select):
    downloadfolder = config.TuneinRadio.downloadlocation.value
    backupTuneinRadiofolder = downloadfolder + '/TuneinRadio'
    try:
        if select:
            file = select[0]
            backup_file = backupTuneinRadiofolder + '/' + file
            tree = ElementTree()
            tree.parse(backup_file)
            root = tree.getroot()
            if not os.path.exists(backup_file):
                return False
            if os.path.exists(xmlfile):
                os.remove(xmlfile)
            shutil.copyfile(backup_file, xmlfile)
            return True
    except:
        print 'failed to restore favorites'
        return False


def backupfavorites2():
    try:
        favlocation = config.TuneinRadio.favlocation.value
        #xmlfile = favlocation + '/favorites2.xml'
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        downloadfolder = config.TuneinRadio.downloadlocation.value
        backupTuneinRadiofolder = downloadfolder + '/TuneinRadio'
        dst_file = getfilename(backupTuneinRadiofolder)
        import shutil
        shutil.copyfile(xmlfile, dst_file)
        return True
    except:
        print 'failed to backup favorites'
        return False


def backupfavorites():
    try:
        favlocation = config.TuneinRadio.favlocation.value
        xmlfile = favlocation + '/favorites2.xml'
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        downloadfolder = config.TuneinRadio.downloadlocation.value
        backupTuneinRadiofolder = downloadfolder + '/TuneinRadio'
        dst_file = backupTuneinRadiofolder + '/favorites2.xml'
        import shutil
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copyfile(xmlfile, dst_file)
        return True
    except:
        print 'failed to backup favorites'
        return False


def delfavorite(title, fav_id = None):
    try:
        favlocation = config.TuneinRadio.favlocation.value
        xmlfile = favlocation + '/favorites2.xml'
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        i = 0
        for addon in root.iter('addon'):
            for media in addon.iter('media'):
                media_title = media.get('title')
                media_url = media.text
                if fav_id is None:
                    if media_title == title:
                        addon.remove(media)
                        tree.write(xmlfile)
                        return True
                elif fav_id == i:
                    addon.remove(media)
                    tree.write(xmlfile)
                    try:
                        backupfavorites()
                    except:
                        pass

                    return True
                i = i + 1

        return False
    except:
        return False

    return
def favexists(title=None,param=None):
        if title is None or param is None:
            return False       
        if True:

            from xml.etree.ElementTree import ElementTree, dump, SubElement, Element        
            favlocation = config.TuneinRadio.favlocation.value
            xmlfile = favlocation + '/favorites2.xml'            
            tree = ElementTree()
            tree.parse(xmlfile)
            root = tree.getroot()
            i = 0
            print "title,paramxxx",title,param
            for addon in root.iter('addon'):
                    for media in addon.iter('media'):
                        print "mediaxxx",media
                        favtitle = str(media.attrib.get('title'))
                        favurl = str(media.text)
                        print "title,param,favtitle,favurlxxx",title,param,favtitle,favurl
                        if title==favtitle and param==favurl:
                            return True
            return False             
        else:
            return False

def addfavorite(addon_id, media_title, media_url,section = ''):
    debug = True
    section=addon_id.split("/")[0]
    addon_id=addon_id.replace("/",".")
    
    if True:
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        if 'filesexplorer' in addon_id or 'favorites' in addon_id:
            return False
        added = False
        for addon in root.iter('addon'):
            id = addon.get('id')
            section_id = addon.get('section')
            print id
            if id == addon_id and section_id == section:
                addon.set('section', section)
                media = SubElement(addon, 'media')
                media.set('title', media_title)
                media.text = media_url
                tree = ET.ElementTree(root)
                tree.write(xmlfile)
                added = True
                print 'addfavorites-added', media_title
                break
        print "section,addon_id",section,addon_id
        if added == False:
            addon = SubElement(root, 'addon')
            addon.set('id', addon_id)
            addon.set('section', section)
            media = SubElement(addon, 'media')
            media.set('title', media_title)
            media.text = media_url
            tree = ET.ElementTree(root)
            tree.write(xmlfile)

        return True
    else:
        return False


print '***********************'

def getfav_datalist(addon_id = None, section = None,mode='section'):
    favlocation = config.TuneinRadio.favlocation.value
    favorites_xml = xmlfile
    #section=addon_id.split("/")[0]
    if not os.path.exists(favorites_xml):
        return []
    favlist = getfavorites(addon_id, section,mode)
    print "favlist",favlist
    names2 = []
    urls2 = []
    source_data = []
    for fav in favlist:
        if os.path.exists(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/sicon.png'):
            png_small = loadPNG(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/sicon.png')
        else:
            png_small = loadPNG(PLUGIN_PATH + '/skin/spicons/favorites.png')
        if os.path.exists(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/icon.png'):
            png_large = loadPNG(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/icon.png')
        else:
            png_large = loadPNG(PLUGIN_PATH + '/skin/micons/favorites.png')
        print '642', png_large
        source_data.append((fav[0],
         fav[1],
         fav[2],
         fav[3],
         fav[4],
         png_large,
         png_small))

    print 'source_data', source_data
    return source_data
def getfav_datalisttube(addon_id = None, section = None,mode='section'):
    favlocation = config.TuneinRadio.favlocation.value
    favorites_xml = tubexml
    #section=addon_id.split("/")[0]
    if not os.path.exists(favorites_xml):
        return []
    favlist = getfavoritestube(addon_id, section,mode)
    print "favlist",favlist
    names2 = []
    urls2 = []
    source_data = []
    for fav in favlist:
        if os.path.exists(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/sicon.png'):
            png_small = loadPNG(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/sicon.png')
        else:
            png_small = loadPNG(PLUGIN_PATH + '/interface/spicons/favorites.png')
        if os.path.exists(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/icon.png'):
            png_large = loadPNG(PLUGIN_PATH + '/addons/' + fav[3] + '/' + fav[2] + '/icon.png')
        else:
            png_large = loadPNG(PLUGIN_PATH + '/skin/micons/favorites.png')
        print '642', png_large
        source_data.append((fav[0],
         fav[1],
         fav[2],
         fav[3],
         fav[4],
         png_large,
         png_small))

    print 'source_data', source_data
    return source_data

def getplaylist():
    list1 = []
    debug = True
    try:
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        i = 0
        for addon in root.iter('addon'):
            try:
                id = str(addon.get('id'))
            except:
                id = None

            try:
                section_id = str(addon.get('section'))
            except:
                section_id = None

            for media in addon.iter('media'):
                title = str(media.attrib.get('title'))
                url = str(media.text)
                print 'beofre75playlist,section_id', id, section_id
                if not section_id.endswith('_playlist'):
                    i = i + 1
                    print 'not passed75playlist,section_id', id, section_id
                    continue
                print 'passed75playlist,section_id', id, section_id
                section = section_id.split('_')[0]
                list1.append((title,
                 url,
                 id,
                 section,
                 i))
                i = i + 1

        print 'list1', list1
        return list1
    except:
        list1.append(('Error reading playlist,repair favorites from Tools', '', '', '', 1))
        print 'error in reading favorite xml file'
        return list1

    return


def getfavorites(addon_id = None, section = None,mode='section'):
    list1 = []
    debug = True
    print "addon_id,section",addon_id,section
    
    if debug:
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        i = 0
        for addon in root.iter('addon'):
            try:
                id = str(addon.get('id'))
            except:
                id = None

            try:
                section_id = str(addon.get('section'))
            except:
                section_id = None

            
            section_id = section_id.replace('_playlist', '')
            print "addon_id,section,section_id",addon_id,section,section_id
            if mode == 'desktop':
                    try:id=id.replace(".","/")
                    except:continue
                    for media in addon.iter('media'):
                        title = str(media.attrib.get('title'))
                        url = str(media.text)
                        print '75id,section_id', id, section_id
                        list1.append((title,
                         url,
                         id,
                         section_id,
                         i))
                        i = i + 1

            elif mode=='addon':
                  if id == addon_id:
                    for media in addon.iter('media'):
                        title = str(media.attrib.get('title'))
                        url = str(media.text)
                        print '75id,section_id', id, section_id
                        list1.append((title,
                         url,
                         id,
                         section_id,
                         i))
                        i = i + 1

            elif mode=='section':
                
                for media in addon.iter('media'):
                    title = str(media.attrib.get('title'))
                    url = str(media.text)
                    print '94id,section_id', id, section_id
                    list1.append((title,
                     url,
                     id,
                     section_id,
                     i))
                    i = i + 1

        print 'list1', list1
        return list1
    else:
        list1.append(('Error reading favorites,repair favorites from Tools', '', '', '', 1))
        print 'error in reading favorite xml file'
        return list1

    return
