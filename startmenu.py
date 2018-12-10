# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/startmenu.py
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap, NumberActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
import os
from Screens.MessageBox import MessageBox
from Components.Button import Button
from Tools.Directories import fileExists
from enigma import eTimer, eListboxPythonMultiContent, getDesktop, gFont, loadPNG
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Label import Label
from Tools.LoadPixmap import LoadPixmap
from Components.ConfigList import ConfigList, ConfigListScreen
from  .lib.pltools import getversioninfo, gethostname, log
currversion, enigmaos, currpackage, currbuild = getversioninfo('TuneinRadio')
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'
swidth = getDesktop(0).size().width()


def cMenuListEntry(name, idx):
    
    res = [name]
 
    png = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/icons/%s.png' % str(name)
   
    if fileExists(png):
        if enigmaos == 'oe2.0':
            res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 15), size=(278, 78), png=loadPNG(png)))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(2, 15), size=(278, 78), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(10, 3), size=(278, 90), font=0, text=' '))
    return res




class StartMenuscrn(Screen):
    if True:
        

        skin = '''<screen  name="StartMenuscrn" position="center,center" size="900,550" title=""  flags="wfNoBorder" >
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/logo.png" position="0,0" size="900,550" transparent="1"/>	


		<widget name="list" position="10,20" size="280,440" scrollbarMode="showOnDemand" itemHeight="110" transparent="1" zPosition="2" />
	        
                 
            <widget
            name = "info"
            position = "300,400"
            zPosition = "2"
            size = "600,250"
            font = "Regular;25"
            foregroundColor = "yellow"
            transparent = "1"
            halign = "center"
            valign = "center"/>

       
 

            
        </screen>'''



        
    def __init__(self, session,updateinfo='', plugin_name='',back_close=None, active=False):
    
        Screen.__init__(self, session)
        updatetxt=''
        currversion=''
        try:
            currversion=updateinfo.split("_")[0]
        except:
            pass
        if "True" in updateinfo:##updateinfo
            try:
                new_version=updateinfo.split("_")[2]
                currversion=updateinfo.split("_")[0]
                updatetxt="New version "+str(new_version) +" is available press blue to upgrade."
            except:
                new_version=''
                updatetxt=''
                currversion=''
        if not updatetxt=='':
           self['info'] = Label(updatetxt)
        else:   
           self['info'] = Label('Version: '+currversion)
        
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
            'cancel': self.close}, -2)
        self.ListToMulticontent()

    def ListToMulticontent(self):
        res = []
        theevents = []
        
       
        self['list'].l.setItemHeight(110)
        self['list'].l.setFont(0, gFont('Regular', 25))
                    
       
        self.data=[]
        self.data.append(("favorites",0))        
        self.data.append(("search",1))
        self.data.append(("local",2))
        self.data.append(("about",3))
        for item in self.data:
           res=cMenuListEntry(str(item[0]), item[1])
           theevents.append(res)
           res = []
        self['list'].l.setList(theevents)
        self['list'].show()
    
        

  

    def okClicked(self):

        idx=self['list'].getSelectedIndex()
        sel = self.data[idx][0]
        if True:
            if sel == 'favorites':
                    self.section = 'radio'
                    addons_path = PLUGIN_PATH + '/addons/' + self.section + '/'
                    addon_id = 'radio/TuneinRadio'
                    from .main import MainScreen
                    info={'name':'TuneinRadio','addon_id':"radio/TuneinRadio"} 
                    info['name'] = 'favorites'
                    self.session.open(MainScreen, info=info, action_params=None, source_data=[], nextrun=1, screens=[])
               
            elif sel == 'search':
                param='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/addons/TuneinRadio/default.py?url=%2Ftag%2F&mode=103&name=Search&page=0&extra=1'
                self.section = 'radio'
                addons_path = PLUGIN_PATH + '/addons/' + self.section + '/'
                addon_id = 'radio/TuneinRadio'
                from .main import MainScreen 
                info={'name':'TuneinRadio','addon_id':"radio/TuneinRadio"} 
                self.session.open(MainScreen, info=info, action_params=param, source_data=[], nextrun=1, screens=[])

            elif sel == 'local':
           
                self.section = 'radio'
                addons_path = PLUGIN_PATH + '/addons/' + self.section + '/'
                addon_id = 'radio/TuneinRadio'
                from .main import MainScreen 
                info={'name':'TuneinRadio','addon_id':"radio/TuneinRadio"} 
                self.session.open(MainScreen, info=info, action_params=None, source_data=[], nextrun=1, screens=[])
            elif sel == 'about':
                    from .lib.softupdate import updatesscreen
                    self.session.open(updatesscreen)

                
        else:
            return
