# 2015.08.05 16:44:23 Arabic Standard Time
#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ALiSatSettings/restart.py
from Components.Label import Label
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
import os
from Screens.Standby import TryQuitMainloop
from Tools.Directories import copyfile, pathExists, createDir, removeDir
from Components.Pixmap import Pixmap
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor

class asettingsrestartScreen(Screen):
    skin = '\n                        <screen name="asettingsrestartScreen" position="center,center" size="580,300" title="Restart Enigma"  >\n                        \t\n\t\t        <widget name="tspace" position="0,5" zPosition="4" size="580,200" font="Regular;23" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />\n\t\t\t\n\n                        <ePixmap name="ButtonRed" position="100,200" zPosition="4" size="140,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ALiSatSettings/skin/ddbuttons/red.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_red" position="100,207" zPosition="5" size="140,30" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n        \t        <ePixmap name="ButtonGreen" position="350,200" zPosition="4" size="160,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ALiSatSettings/skin/ddbuttons/green.png" transparent="1" alphatest="on" />\n\t\t\t<widget name="key_green" position="340,207" zPosition="5" size="160,30" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n      \n                 \n                </screen>'

    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self['tspace'] = Label('Restart Enigma to load settings?')
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('OK'))
        self['shortcuts'] = ActionMap(['ShortcutActions', 'WizardActions', 'InfobarEPGActions'], {'ok': self.restartenigma,
         'back': self.close,
         'green': self.restartenigma,
         'red': self.close}, -1)

    def restartenigma(self):
        epgpath = '/media/hdd/epg.dat'
        epgbakpath = '/media/hdd/epg.dat.bak'
        if os.path.exists(epgbakpath):
            os.remove(epgbakpath)
        if os.path.exists(epgpath):
            copyfile(epgpath, epgbakpath)
        self.session.open(TryQuitMainloop, 3)
# okay decompyling I:\alisat\enigma2-plugin-extensions-ali-sat-settings-oe1.6_1.0_all\enigma2-plugin-extensions-ali-sat-settings-oe1.6_1.0_all\data\usr\lib\enigma2\python\Plugins\Extensions\ALiSatSettings\restart.pyo 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.08.05 16:44:23 Arabic Standard Time
