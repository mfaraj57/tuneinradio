from Components.config import config, ConfigIP, ConfigInteger, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from Screens.MessageBox import MessageBox
import os
mountedDevs = []
try:
    from Components.Harddisk import harddiskmanager
    for p in harddiskmanager.getMountedPartitions(True):
        mountedDevs.append((p.mountpoint, _(p.description) if p.description else ''))
except:
    pass
mounted_string = 'Nothing mounted at '

class TuneinRadioSetup(Screen, ConfigListScreen):
    skin='''<screen
    name = "TuneinRadioSetup"
    position = "center,center"
    size = "920,560"
    backgroundColor = "#080000"
    title = "TuneinRadio Settings">
    <ePixmap
        position = "79,521"
        size = "25,25"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>
    <ePixmap
        position = "283,521"
        size = "25,25"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>
    <eLabel
        position = "86,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = "Cancel"/>
    <eLabel
        position = "295,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = "Save"/>
    <eLabel
        position = "495,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = " "/>
    <ePixmap
        position = "75,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <ePixmap
        position = "279,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <ePixmap
        position = "484,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <widget
        name = "config"
        position = "20,50"
        size = "900,350"
        itemHeight = "35"
        scrollbarMode = "showOnDemand"
        transparent = "1"
        zPosition = "2"/>
</screen>'''
    def __init__(self, session):
        Screen.__init__(self, session)
        
        self.createSetup()
        ConfigListScreen.__init__(self, self.list, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.keySave,
         'cancel': self.keyClose,
         'ok': self.ok,                                                                   
         'blue': self.resetdefaults}, -2)
       

    def createSetup(self,result=None):

        self.list = []
        
        self.list.append(getConfigListEntry(_('Show plugin in main menu(need e2 restart):'), config.TuneinRadio.menuplugin))
        self.list.append(getConfigListEntry(_('Download directory # press ok to change:'), config.TuneinRadio.downloadlocation))
        self.list.append(getConfigListEntry(_('Slide show image source # press ok to change:'), config.TuneinRadio.images_source))

        

    def resetdefaults(self):
        pass

    
    def ok(self):
        if self['config'].getCurrent()[1] == config.TuneinRadio.downloadlocation:
            from downloadlocation import TuneinRadiodownloadlocation
            self.session.openWithCallback(self.createSetup,TuneinRadiodownloadlocation)
        

    def callbackd(self, result = False):
        if result:
            self.createSetup()
            return

    def keySave(self):
       
        for x in self['config'].list:
            x[1].save()

        configfile.save()


        from .pltools import getmDevices
        mount_devices=getmDevices()
        dlocation=config.TuneinRadio.downloadlocation.value
        foldermounted = self.checkmountDownloadPath(dlocation)
        if not foldermounted:
           self.session.open(MessageBox, mounted_string + str(dlocation), MessageBox.TYPE_ERROR,timeout=7)
            
        if config.TuneinRadio.images_source.value=="myphotos":        
           self.session.open( MessageBox, "Put your pictures in directory %s" %config.TuneinRadio.downloadlocation.value+"/myphtos",MessageBox.TYPE_INFO,timeout=7)


        self.close(True)


            
    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close(True)

    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)

    def checkmountDownloadPath(self, path):
        if path is None:
            self.session.open(MessageBox, _('nothing entered'), MessageBox.TYPE_ERROR)
            return False
        else:
            sp = []
            sp = path.split('/')
            print sp
            if len(sp) > 1:
                if sp[1] != 'media':
                   
                    return False
            mounted = False
            self.swappable = False
            sp2 = []
            f = open('/proc/mounts', 'r')
            m = f.readline()
            while m and not mounted:
                if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                    mounted = True
                    print m
                    sp2 = m.split(' ')
                    print sp2
                    if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                        print '[stFlash] swappable'
                        self.swappable = True
                m = f.readline()

            f.close()
            if not mounted:
                
                return False
            if os.path.exists(config.TuneinRadio.downloadlocation.value):
                try:
                    os.chmod(config.TuneinRadio.downloadlocation.value, 511)
                except:
                    pass

            return True
