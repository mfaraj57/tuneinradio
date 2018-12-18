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


from Plugins.Extensions.TuneinRadio.lib.pltools import trace_error, log

def delfavorite(media_title, media_url):
    try:
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        i = 0
        for addon in root.iter('addon'):
            for media in addon.iter('media'):
                title = media.get('title')
                url = media.get('url')
                if media_title == title and media_url == url:
                    addon.remove(media)
                    tree.write(xmlfile)
                    return True

        return False
    except:
        trace_error()
        return False


def addfavorite(addon_id, media_title, media_url, media_picture, section = ''):
    debug = True
    if favexists(media_title, media_url) == True:
        return (False, True)
    try:
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        added = False
        if added == False:
            addon = SubElement(root, 'addon')
            addon.set('id', addon_id)
            addon.set('section', section)
            media = SubElement(addon, 'media')
            media.set('title', media_title)
            media.set('url', media_url)
            media.set('picture', media_picture)
            tree = ET.ElementTree(root)
            tree.write(xmlfile)
            return (True, False)
    except:
        trace_error()
        return ('Error', 'Error:favorites2.xml corrupted or not exists')


def favexists(media_title, media_url):
    list1 = []
    debug = True
    try:
        tree = ElementTree()
        tree.parse(xmlfile)
        root = tree.getroot()
        i = 0
        for addon in root.iter('addon'):
            for media in addon.iter('media'):
                title = str(media.attrib.get('title'))
                url = str(media.attrib.get('url'))
                if title == media_title and url == media_url:
                    return True

        return False
    except:
        trace_error()
        return False


def readfav(mode = 'GFavorites', addon_id = None, section = None):
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

            if True:
                for media in addon.iter('media'):
                    title = str(media.attrib.get('title'))
                    url = str(media.attrib.get('url'))
                    picture = str(media.attrib.get('picture'))
                    list1.append((title,
                     url,
                     picture,
                     id,
                     section_id))
                    i = i + 1

        return list1
    except:
        trace_error()
        list1.append(('Error:favorites2.xml corrupted or not exists', '', '', '', 1))
        print 'error in reading favorite xml file'
        return list1

    return
