
from Screens.Screen import Screen
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
from Components.config import config
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'
def makevalid_filename(s):
    import re
    badchars = re.compile('[^A-Za-z0-9_. ]+|^\\.|\\.$|^ | $|^$')
    badnames = re.compile('(aux|com[1-9]|con|lpt[1-9]|prn)(\\.|$)')
    try:
        name = badchars.sub('_', s)
        if badnames.match(name):
            name = '_' + name
        try:
            name = name.split('_')[0]
        except:
            pass

        return name
    except:
        try:
            name = s.split('_')[0]
        except:
            pass

        return name


def IsValidFileName(name, NAME_MAX = 255):
    prohibited_characters = ['/',
     '\x00',
     '\\',
     ':',
     '*',
     '<',
     '>',
     '|',
     '"']
    if isinstance(name, basestring) and 1 <= len(name) <= NAME_MAX:
        for it in name:
            if it in prohibited_characters:
                return False

        return True
    return False


def RemoveDisallowedFilenameChars(name, replacment = '.'):
    prohibited_characters = ['/',
     '\x00',
     '\\',
     ':',
     '*',
     '<',
     '>',
     '|',
     '"']
    for item in prohibited_characters:
        name = name.replace(item, replacment).replace(replacment + replacment, replacment)

    return name


def checkdownloadPath(path = None):
    try:
        if os.path.exists(path) == False:
            return (False, 'Download direcotry is not available')
        if path is None:
            return (False, 'No Download direcotry given')
        sp = []
        sp = path.split('/')
        print sp
        if len(sp) > 1:
            if sp[1] != 'media':
                return (False, mounted_string % path)
        mounted = False
        swappable = False
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
                    swappable = True
            m = f.readline()

        f.close()
        if not mounted:
            return (False, mounted_string + str(path))
        freespace, spacestr = getfreespace(path)
        if freespace < 50:
            return (False, 'Download is not allowed with freespace less than 50mb')
        return (True, 'success')
    except:
        return (False, 'invalid download folder ')

    return


def getfreespace(downloadlocation = None):
    if os.path.exists(downloadlocation) == False:
        return (0, 'Download location is not available')
    else:
        try:
            diskSpace = os.statvfs(downloadlocation)
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            fspace = round(float(available / 1048576.0), 2)
            tspace = round(float(capacity / 1048576.0), 1)
            spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
            return (fspace, spacestr)
        except:
            return (None, None)

        return None
        return None


class TuneinRadiodownload(Screen):
    skin=''' <screen
            name = "TuneinRadiodownload"
            position = "center,center"
            size = "700,300"
            title = "Download menu">
            <widget
                name = "text"
                position = "70,8"
                size = "700,80"
                font = "Regular;22"
                transparent = "1"/>
            <widget
                name = "list"
                position = "15,100"
                size = "650,180"
                transparent = "1"/>
        </screen>'''
    def __init__(self, session, url = None, name = None,menu=False):
        self.session = session

        self.url = url
        self.name = name
        self.menu=menu
        Screen.__init__(self, session)
        if self.menu==True:

            self.list = [(_('Downloading'), 1),
             (_('Select Download location'), 2),
             (_('Downloads'), 3),                         
             (_('Settings'), 34)]

        else:     
            self.list = [(_('Download'), 0),
             (_('Downloading'), 1),
             (_('Select Download location'), 2),
             (_('Downloads'), 3),
             (_('Settings'), 34)]
            
        text = _('Download location:') + config.TuneinRadio.downloadlocation.value + '\nFreespace:' + self.calfreespace()
        self['text'] = Label(text)
        self.lines = []
        print '102', self.url
        self['list'] = MenuList(self.list)
        self['actions'] = ActionMap(['MsgBoxActions', 'DirectionActions'], {'cancel': self.cancel,
         'ok': self.ok,
         'alwaysOK': self.alwaysOK,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'upRepeated': self.up,
         'downRepeated': self.down,
         'leftRepeated': self.left,
         'rightRepeated': self.right}, -1)
    def showsetup(self):
        from .PluginSetup import TuneinRadioSetup
        self.session.open(TuneinRadioSetup)
    def refresh(self, result = None):
        text = _('Download location:') + config.TuneinRadio.downloadlocation.value + '\nFreespace:' + self.calfreespace()
        self['text'].setText(text)

    def progress_callback(self, data):
        print data

    def startdownload(self, action = 'download'):
        if action == 'view':
            from Plugins.Extensions.TuneinRadio.lib.tsdownload import startdownload
            startdownload(self.session, 'view', '', '', '', PLUGIN_PATH)
            return

        else:
            self.begindownload(self.name)

    def choicesback(self, select):
        if select:
            if select[0] == 'User input':
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                import os
                self.session.openWithCallback(self.begindownload, VirtualKeyBoard, title=_('Enter your movie title(s)'), text='')
            else:
                self.begindownload(select[0])

    def begindownload(self, select):
        if select:
            
            dlocation = config.TuneinRadio.downloadlocation.value
            success, txt = checkdownloadPath(dlocation)
            if success == False:
                self.session.open(MessageBox, txt, MessageBox.TYPE_ERROR)
                return
            self.name = str(select)
            if '/' in self.name:
                self.name.replace('/', '_')
            extension = '.mp3'
            import datetime
            now = datetime.datetime.now()
            DATETIME = now.strftime('%Y-%m-%d-%H-%M-%S')            
            
            name = '%s-%s.mp3 ' % ( self.name, DATETIME)
            target = os.path.join(dlocation , name)
            
            title = name
            try:
                if IsValidFileName(name) == False:
                    name = RemoveDisallowedFilenameChars(name)
                    title = name
                    target = os.path.join(dlocation , name)
            except:
                pass

            from Plugins.Extensions.TuneinRadio.lib.tsdownload import startdownload
            val = startdownload(self.session, 'download', self.url, target, title, PLUGIN_PATH)
            if val == True:
                self.close()
            return

    def calfreespace(self):
        freespace, freespacestr = getfreespace(config.TuneinRadio.downloadlocation.value)
        if freespace is not None:
            return freespacestr
        else:
            return 'Free space unknown'
            return

    def ok(self):
        if self['list'].getCurrent()[1] == 0:
            self.startdownload('download')
        elif self['list'].getCurrent()[1] == 1:
            self.startdownload('view')
        elif self['list'].getCurrent()[1] == 2:
            from downloadlocation import TuneinRadiodownloadlocation
            self.session.openWithCallback(self.refresh, TuneinRadiodownloadlocation)
        elif self['list'].getCurrent()[1] == 3:
            from filesexplorer import TuneinRadioFiles
            self.session.open(TuneinRadioFiles)
        else:
            self.showsetup()

    def cancel(self):
        self.close(False)

    def alwaysOK(self):
        self.close(True)

    def up(self):
        self.move(self['list'].instance.moveUp)

    def down(self):
        self.move(self['list'].instance.moveDown)

    def left(self):
        self.move(self['list'].instance.pageUp)

    def right(self):
        self.move(self['list'].instance.pageDown)

    def move(self, direction):
        self['list'].instance.moveSelection(direction)
