# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/plugin.py

from Screens.Screen import Screen
from enigma import loadPNG, eTimer
from Components.ActionMap import ActionMap, NumberActionMap
from twisted.web.client import downloadPage, getPage
import urllib2


import os
from .lib.pltools import getversioninfo, gethostname, log
currversion, enigmaos, currpackage, currbuild = getversioninfo('TuneinRadio')##change
plugin_path='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'##change
class bootlogo(Screen):
    skin = '<screen name="bootlogo" position="center,center" size="900,550" title="" flags="wfNoBorder"><eLabel  position = "345,415"   zPosition = "4"   size = "100,25"  halign = "center"  font = "Regular;22"  transparent = "1" foregroundColor = "#ffffff" backgroundColor = "#41000000" text = "Loading.."/><ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/logo.png" position="0,0" size="900,550" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.active = False
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.disappear,
         'cancel': self.disappear}, -1)
        self.update_available = False
        self.plugin_name = 'TuneinRadio'####change
        self.systemlock = ''
        self.server_updatefile='http://tunisia-dreambox.info/TSplugins/TuneinRadio/TuneinRadio_updates.txt'##change
        self.server_softpath='http://tunisia-dreambox.info/TSplugins/TuneinRadio'##change
        self.timer1 = eTimer
        self.version = currversion
        self.currversion = currversion
        self.updateinfo = self.currversion + '_False_' + self.version
        if enigmaos == 'oe2.0':
            try:
                self.timer1.callback.append(self.checkupdates)
                self.timer2.start(100, False)
            except:
                self.onLayoutFinish.append(self.checkupdates)

        else:
            try:
                self.timer1_conn = self.timer.timeout.connect(self.checkupdates)
                self.timer2.start(100, False)
            except:
                self.onLayoutFinish.append(self.checkupdates)

    def back_close(self, result = None):
        if result:
            try:
                self.timer1.stop()
            except:
                pass

            try:
                if enigmaos == 'oe2.0':
                    self.timer1.callback.remove(self.disappear)
                else:
                    self.timer1_conn = None
            except:
                pass

            self.close()
        return

    def checkupdates(self):
        try:
            self.timer1.stop()
        except:
            pass

        
        
        getPage(self.server_updatefile, headers={'Content-Type': 'application/x-www-form-urlencoded'},timeout=20).addCallback(self.parseData).addErrback(self.addErrback)
        self.timer2 = eTimer()
        if enigmaos == 'oe2.0':
            self.timer2.callback.append(self.disappear)
        else:
            self.timer2_conn = self.timer2.timeout.connect(self.disappear)
        self.timer2.start(2000, False)

    def addErrback(self, result):
        if result:
            print "Twisted web failed:failed to download file "+str(result)
        #self.disappear()

    def parseData(self, data):
        debug = True
        try:##tmp
            updated_addons = ''
            new_addons = []
            version = '1.0'
            self.update_available = False         
            
            
            autoinstall = 'yes'
            try:##tmp
                for line in data.splitlines():
                    line = line.strip()
                    if line.startswith('name'):
                        self.plugin_name = line.split('=')[1].strip()
                    if line.startswith('software_version'):
                        version = line.split('=')[1].strip()
                        self.version = version
                    if line.startswith('software_fixupdate') and '=' in line:
                        new_update_file = line.split('=')[1]
                        print 'new_update_file', new_update_file
                        newupdate = True
                        try:
                            if new_update_file.strip() == '':
                                newupdate = False
                        except:
                                newupdate = False

                        debug = True
                        if newupdate == True:
                            try:
                                if new_update_file.endswith('.zip'):
                                    new_update_file = new_update_file[:-4]
                                uptype, upversion, update = new_update_file.split('_')
                                if float(upversion) == float(self.currversion):
                                    if not os.path.exists(plugin_path + '/updates/' + new_update_file):
                                        afile = open(plugin_path + '/updates/' + new_update_file, 'w')
                                        afile.close()
                                        url = self.server_softpath+'/' + new_update_file + '.zip'
                                       
                                        target = '/tmp/' + new_update_file + '.zip'
                                        if os.path.exists(target):
                                            os.remove(target)
                                        from .lib.tsdownload import startdownload
                                        startdownload(self.session, 'download', url, target, new_update_file, None, False)
                            except:
                                pass

            except:
                pass

            if float(self.version) > float(self.currversion):
                self.updateinfo = str(self.currversion) + '_' + 'True' + '_' + str(self.version)
            else:
                self.updateinfo = str(self.currversion) + '_' + 'False' + '_' + str(self.version)
            self.disappear()
        except:
            self.disappear()

        

    def disappear(self):
        try:
            self.timer2.stop()
            if enigmaos == 'oe2.0':
                self.timer2.callback.remove(self.disappear)
            else:
                self.timer2_conn = None
        except:
            pass

        if True:
            from .startmenu import StartMenuscrn #change
            self.session.openWithCallback(self.close, StartMenuscrn, self.updateinfo, self.plugin_name, self.back_close, self.active)#change
        return
