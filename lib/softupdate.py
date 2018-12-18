# soft and data updates unversal check ##changes for folders change,put plugin_updates.txt in server with the ipk
from os import popen, system, path, listdir, remove
import os
from Components.Label import Label
from Screens.Standby import TryQuitMainloop
from Screens.Screen import Screen
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap, NumberActionMap
from enigma import getDesktop, eConsoleAppContainer
sz_w = getDesktop(0).size().width()
from Screens.MessageBox import MessageBox
gLogFile = None
from .pltools import getversioninfo, gethostname, log as dlog
currversion, enigmaos, currpackage, currbuild = getversioninfo('TuneinRadio')
server_updatesfile='http://www.tunisia-dreambox.info/TSplugins/TuneinRadio/TuneinRadio_updates.txt'##change
server_updatespath='http://tunisia-dreambox.info/TSplugins/TuneinRadio' ##change
def dataupdates():
    version = None
    link = None
    updates = None
    builddate = ''
    try:
        import urllib2
        fp = urllib2.urlopen(server_updatesfile)
        count = 0
        lines = fp.readlines()
        link16 = ''
        link20 = ''
        builddate = ''
        for line in lines:
            if line.startswith('software_version'):
                version = line.split('=')[1].strip()
            if line.startswith('software_fixupdate'):
                builddate = line.split('=')[1].strip()
            if line.startswith('software_link2.0'):
                link20 = line.split('=')[1].strip()
            if line.startswith('software_updates'):
                updates = line.split('=')[1].strip()
            link = link20
            if not enigmaos == 'oe2.0':
                link = link.replace('.ipk', '.deb')

        return ('none',
         version,
         link,
         updates,
         builddate)
    except:
        return ('error',
         version,
         link,
         updates,
         builddate)

    return


class updatesscreen(Screen):##change pngs path
    if sz_w == 1280:
        skin = '''<screen
    name = "updatesscreen"
    position = "center,center"
    size = "790,570"
    backgroundColor = "#080000">

       <ePixmap
            position = "220,540"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/yellow.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <widget
            name = "key_yellow"
            position = "200,537"
            zPosition = "4"
            size = "200,24"
            halign = "center"
            font = "Regular;20"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"/>
        <ePixmap
            position = "200,530"
            pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>


            
        <ePixmap
            position = "550,540"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/green.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <widget
            name = "key_green"
            position = "530,537"
            zPosition = "4"
            size = "200,24"
            halign = "center"
            font = "Regular;20"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"/>
        <ePixmap
            position = "530,530"
            pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>
       


        
    <widget
        name = "info"
        position = "20,50"
        zPosition = "2"
        size = "760,485"
        font = "Regular;22"
        foregroundColor = "#ffffff"
        transparent = "1"
        halign = "center"
        valign = "center"/>
</screen>
'''
    else:
        skin ='''<screen
    name = "updatesscreen"
    position = "center,center"
    size = "1165,855"
    backgroundColor = "#080000">


    <widget
        name = "key_green"
        position = "580,806"
        zPosition = "4"
        size = "390,36"
        halign = "center"
        font = "Regular;30"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"/>
    <ePixmap
        position = "645,795"
        pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "306,56"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <ePixmap
        position = "655,810"
        size = "38,38"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>


    <ePixmap
        position = "300,810"
        size = "25,25"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>
        
        
    <widget
        name = "key_yellow"
        position = "280,806"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;20"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"/>
    <ePixmap
        position = "280,795"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "200,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>




        
    <widget
        name = "info"
        position = "30,75"
        zPosition = "2"
        size = "1140,728"
        font = "Regular;33"
        foregroundColor = "#ffffff"
        transparent = "1"
        halign = "center"
        valign = "center"/>
</screen>'''
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['key_green'] = Label('Upgrade')
        self['key_yellow'] = Label('Settings')
        self.updatestring = ''
        self.xmlversion = ''
        self.xmlupdates = ''
        self.xmlupdate = False
        self.update = False
        self.removefirst = False
        self.builddate = ''
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close,
         'blue': self.installLastupdate,
         'yellow': self.showsetup,                                                                 
         'green': self.runsoftupdate}, -1)
        info = 'Checking software updates,please wait...'
        self['info'] = Label(_(info))
        self.onLayoutFinish.append(self.getupgradeinfo)
    def showsetup(self):
        from .PluginSetup import TuneinRadioSetup
        self.session.open(TuneinRadioSetup)
    def installLastupdate(self):
        if self.builddate.strip() == '':
            return
        else:
            self.builddate = self.builddate.replace('.zip', '')
            filename = '/tmp/' + self.builddate + '.zip'
            if True:
                url = server_updatespath+"/" + self.builddate + '.zip'
                cmdlist = []
                cmdlist.append("wget -O '" + filename + "' -c '" + url + "'")
                cmdlist.append('unzip -o ' + filename + ' -d ' + '/')
                cmdlist.append('rm ' + filename)
                from .Console3 import Console3
                self.session.open(Console3, title='_(Installing last update)', cmdlist=cmdlist, finishedCallback=None, closeOnSuccess=False, instr=None, endstr=None)
            return

    def getupgradeinfo(self):
        debug = True
        try:
            new_addons = ''
            
            error, version, link, updates, builddate =dataupdates()
            self.builddate = builddate
            
            if error == 'error':
                self['info'].setText(_('Error in getting updates data,internet or server down,try later'))
                return
            currbuild = builddate
            if error == 'error' or updates is None:
                self['info'].setText(_('Error getting data,check internet or server down'))
                self['key_green'].setText(' ')
                self.update = False
                return
            if updates is None:
                self['info'].setText(_('Sorry unable to get updates info,no internet or server down!'))
                self['key_green'].setText(' ')
                self.update = False
                return
            try:
                allupdates = updates.replace(':', '\n')
            except:
                self['info'].setText(_('Sorry unable to get updates info,no internet or server down!'))
                self['key_green'].setText(' ')
                self.update = False
                return

            self.link = link
            print 'version,currversion', version, currversion
            if version.strip() == currversion.strip():
                self['info'].setText(_('Plugin version: ' + currversion + '\nmfaraj57\n\n TuneinRadio is uptodate\n'))
                self.update = True
                self.removefirst = True
                self['key_green'].setText(_('re-install'))
                return
            if float(version) > float(currversion):
                updatestr = _('Plugin version: ' + currversion + '\n\nNew release ' + version + ' is available  \n updates:' + allupdates )
                self['key_green'].setText(_('Upgrade'))
                self.update = True
                self['info'].setText(updatestr)
            else:
                self['info'].setText(_('Plugin version: ' + currversion + '\n\n TuneinRadio is uptodate\n'))
        except:
            self.update = False
            self['info'].setText(_('unable to check for updates-No internet connection or server down-please check later'))

        return

    def runsoftupdate(self):
        if self.update == False:
            return
        
        cmdlist=[]
        cmdlist.append('echo upgrade started,please wait....&& wget "http://tunisia-dreambox.info/TSplugins/TuneinRadio/TuneinRadioInstaller.sh" -O - | /bin/sh')
        from .Console3 import Console3
        self.session.open(Console3, title=_('Installing last update'), cmdlist=cmdlist, finishedCallback=None, closeOnSuccess=False, instr=None, endstr=None)
        return

        

class ConsoleUpdateScreen(Screen):##change plugin path
    skin_1280 ='''    <screen
        name = "ConsoleUpdateScreen"
        position = "center,center"
        size = "790,570"
        title = "Plugin Update"
        backgroundColor = "#00060606"
        flags = "wfNoBorder">
        <ePixmap
            position = "15,5"
            size = "65,65"
            zPosition = "0"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/updates.png"
            alphatest = "on"/>
        <widget
            name = "tslog"
            position = "15,70"
            size = "730,500"
            font = "Regular;22"
            valign = "top"
            halign = "left"
            backgroundColor = "#00000000"
            transparent = "1"
            zPosition = "1"/>
    </screen>'''

    skin_1920 ='''<screen
    name = "UpdateScreen"
    position = "center,center"
    size = "1185,855"
    title = "Plugin Update"
    backgroundColor = "#00060606"
    flags = "wfNoBorder">
    <ePixmap
        position = "22,8"
        size = "98,98"
        zPosition = "0"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/updates.png"
        alphatest = "on"/>
    <widget
        name = "tslog"
        position = "22,105"
        size = "1095,750"
        font = "Regular;33"
        valign = "top"
        halign = "left"
        backgroundColor = "#00000000"
        transparent = "1"
        zPosition = "1"/>
</screen>
'''
    if sz_w == 1280:
        skin = skin_1280
    else:
        skin = skin_1920

    def __init__(self, session, updateurl):
        self.session = session
        self.updateurl = updateurl
        
        self['tslog'] = ScrollLabel()
        Screen.__init__(self, session)
        self.finsished = False
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.keyClose}, -2)
        self.onLayoutFinish.append(self.__onLayoutFinished)

    def __onLayoutFinished(self):
        sl = self['tslog']
        sl.instance.setZPosition(1)
        self['tslog'].setText(_('Starting update, please wait...'))
        self.startPluginUpdate()

    def startPluginUpdate(self):##change
       

        self.container = eConsoleAppContainer()
        if enigmaos == 'oe2.0':
           
            self.container.appClosed.append(self.finishedPluginUpdate)
            self.container.stdoutAvail.append(self.mplog)
            ##change plugin path
            self.container.execute('wget "http://tunisia-dreambox.info/TSplugins/TuneinRadio/TuneinRadioInstaller.sh" -O - | /bin/sh')
        else:
            self.container.appClosed_conn = self.container.appClosed.connect(self.finishedPluginUpdate)
            self.container.stdoutAvail_conn = self.container.stdoutAvail.connect(self.mplog)
            self.container.execute('dpkg -r enigma2-plugin-extensions-tuneinradio ;  dpkg -i --force-depends --force-overwrite /tmp/tmp.pac; apt-get -f -y install')

    def finishedPluginUpdate(self, retval):
        self.finished = True
        try:
            self.container.kill()
        except:
            pass

        if retval == 0:
            self.restartGUI()
            #self.session.openWithCallback(self.restartGUI, MessageBox, _('Plugin successfully updated!\nDo you want to restart the Enigma2 GUI now?'), MessageBox.TYPE_YESNO)

    def restartGUI(self, answer):
        self.finished = True
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def keyClose(self):
        self.close()

    def restartGUI2(self, answer):
        self.session.open(TryQuitMainloop, 3)

    def returnGUI(self, answer):
        pass

    def mplog(self, str1):
        print 'st', str1
        str2=self['tslog'].getText()
        str3=str2+"\n"+str1
        self['tslog'].setText(str3)
        self.writeToLog(str1)

    def writeToLog(self, log):
        global gLogFile
        if gLogFile is None:
            self.openLogFile()
        gLogFile.write(str(log) + '\n')
        gLogFile.flush()
        return

    def openLogFile(self):
        global gLogFile
        try:os.remove("/tmp/tmp.pac")
        except:pass
        baseDir = '/tmp'
        logDir = baseDir + '/'
        import datetime
        try:
            now = datetime.datetime.now()
        except:
            pass

        try:
            os.makedirs(baseDir)
        except OSError as e:
            pass

        try:
            os.makedirs(logDir)
        except OSError as e:
            pass

        try:
            gLogFile = open(logDir + '/plugin_update_%04d%02d%02d_%02d%02d.log' % (now.year,
             now.month,
             now.day,
             now.hour,
             now.minute), 'w')
        except:
            gLogFile = open(logDir + '/plugin_update', 'w')


def downloadurl(url):
    localf = '/tmp/tmp.pac'
    import urllib
    a, b = urllib.urlretrieve(url, localf)
