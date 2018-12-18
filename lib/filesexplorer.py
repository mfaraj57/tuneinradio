# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/lib/filesexplorer.py
from Plugins.Extensions.TuneinRadio.lib.gimports import *
from enigma import eConsoleAppContainer, eTimer, eListboxPythonMultiContent, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, getDesktop, loadPNG, loadPic, eServiceReference
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
size_w = reswidth
plugin_id = 'fileexplorer'
import datetime

def TuneinRadiofexplorer_filesexplorer(entry):
    if size_w == 1280:
        return [entry,
         (eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
          0,
          1,
          35,
          35,
          loadPNG('%s/spicons/%s' % (PLUGIN_PATH, 'movie.png'))),
         (eListboxPythonMultiContent.TYPE_TEXT,
          50,
          10,
          850,
          37,
          0,
          RT_HALIGN_LEFT,
          str(entry[0])),
         (eListboxPythonMultiContent.TYPE_TEXT,
          920,
          10,
          260,
          37,
          0,
          RT_HALIGN_LEFT,
          str(entry[1]))]
    else:
        return [entry,
         (eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
          0,
          1,
          52,
          52,
          loadPNG('%s/spicons/%s' % (PLUGIN_PATH, 'movie.png'))),
         (eListboxPythonMultiContent.TYPE_TEXT,
          82,
          15,
          1450,
          52,
          0,
          RT_HALIGN_LEFT,
          str(entry[0])),
         (eListboxPythonMultiContent.TYPE_TEXT,
          1540,
          15,
          420,
          52,
          0,
          RT_HALIGN_LEFT,
          str(entry[1]))]


def streamMenuList_youtube2font(streamMenuList):
    if size_w == 1280:
        streamMenuList.l.setFont(0, gFont('Regular', 20))
        streamMenuList.l.setFont(1, gFont('Regular', 18))
        streamMenuList.l.setFont(2, gFont('Regular', 12))
        streamMenuList.l.setFont(3, gFont('Regular', 10))
        streamMenuList.l.setItemHeight(37)
    else:
        streamMenuList.l.setFont(0, gFont('Regular', 35))
        streamMenuList.l.setFont(1, gFont('Regular', 30))
        streamMenuList.l.setFont(2, gFont('Regular', 25))
        streamMenuList.l.setFont(3, gFont('Regular', 20))
        streamMenuList.l.setItemHeight(50)


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def mkdir(backuppath):
    try:
        if os.path.exists(backuppath) == False:
            os.makedirs(backuppath)
    except:
        pass


def getDownloadPath():
    Downloadpath = str(config.TuneinRadio.downloadlocation.value)
    mkdir(Downloadpath)
    if Downloadpath.endswith('/'):
        return Downloadpath
    else:
        return Downloadpath + '/'


def freespace():
    downloadlocation = getDownloadPath()
    try:
        diskSpace = os.statvfs(downloadlocation)
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return fspace
    except:
        return 0


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
        if freespace < 60:
            return (False, 'Download is not allowed with freespace less than 60mb')
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


class TuneinRadioFiles(Screen):
    skin='''    <screen
        name = "TuneinRadiofexplorer"
        position = "center,center"
        size = "1280,720"
        backgroundColor = "#080000"
        flags = "wfNoBorder"
        title = "Playlist">
        <widget
            name = "feedlist"
            position = "40,60"
            size = "1200,445"
            foregroundColorSelected = "#ffffff"
            backgroundColor = "#080000"
            foregroundColor = "yellow"
            backgroundColorSelected = "#41000000"
            selectionPixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/x37ltube.png"
            enableWrapAround = "1"
            zPosition = "1"
            scrollbarMode = "showOnDemand"
            transparent = "0"/>
        <ePixmap
            position = "center,700"
            size = "1280,11"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_line.png"
            zPosition = "1"
            transparent = "1"
            alphatest = "blend"/>
        <widget
            name = "plugin_icon"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/iptv.png"
            position = "1200,632"
            size = "65,65"
            transparent = "1"
            alphatest = "blend"
            borderWidth = "2"
            borderColor = "#005f5f"/>
        <widget
            name = "infoload"
            position = "20,30"
            zPosition = "4"
            size = "790,592"
            font = "Regular;23"
            foregroundColor = "yellow"
            transparent = "1"
            halign = "center"
            valign = "center"/>
        <widget
            name = "handlung"
            position = "30,580"
            size = "760,84"
            backgroundColor = "#080000"
            transparent = "1"
            font = "Regular;20"
            valign = "top"
            halign = "center"
            zPosition = "1"/>
        <widget
            name = "info"
            position = "820,600"
            zPosition = "4"
            size = "440,360"
            font = "Regular;22"
            foregroundColor = "yellow"
            transparent = "1"
            halign = "center"
            valign = "top"/>
        <eLabel
            position = "30,673"
            zPosition = "4"
            size = "170,24"
            halign = "left"
            font = "Regular;20"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"
            text = " "/>
        <widget
            name = "page"
            position = "30,20"
            zPosition = "4"
            size = "760,30"
            font = "Regular;22"
            foregroundColor = "yellow"
            transparent = "1"
            halign = "center"
            valign = "top"/>
        <ePixmap
            position = "167,664"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>
        <ePixmap
            position = "371,664"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>
        <ePixmap
            position = "575,664"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>
        <ePixmap
            position = "779,664"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
            size = "204,37"
            zPosition = "2"
            backgroundColor = "#ffffff"
            alphatest = "blend"/>
        <ePixmap
            position = "175,671"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <ePixmap
            position = "379,671"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <ePixmap
            position = "583,671"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <ePixmap
            position = "787,671"
            size = "25,25"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/blue.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <ePixmap
            position = "1000,671"
            size = "35,24"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/info.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <ePixmap
            position = "1060,671"
            size = "35,24"
            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/menu.png"
            zPosition = "3"
            transparent = "1"
            alphatest = "blend"/>
        <widget
            name = "Key_red"
            position = "207,673"
            zPosition = "4"
            size = "140,24"
            halign = "center"
            font = "Regular;20"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"
            text = "Delete"/>
        <widget
            name = "Key_green"
            position = "421,673"
            zPosition = "4"
            size = "140,24"
            halign = "center"
            font = "Regular;18"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"/>
        <widget
            name = "Key_yellow"
            position = "610,673"
            zPosition = "4"
            size = "145,24"
            halign = "left"
            font = "Regular;18"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"/>
        <widget
            name = "Key_blue"
            position = "819,673"
            zPosition = "4"
            size = "140,24"
            halign = "center"
            font = "Regular;18"
            transparent = "1"
            foregroundColor = "#ffffff"
            backgroundColor = "#41000000"/>
        <!--<widget backgroundColor="#41000000" foregroundColor="#ffffff" position="826,55" size="380,30"  name="pr_time" font="Regular;22" />  -->
        <!--<widget backgroundColor="#41000000" foregroundColor="#ffffff" position="826,92" size="380,552" name="program" font="Regular;22" /> -->
    </screen>'''
    def __init__(self, session, mode = 'movie', streamGenreLink = None, searchData = None):
        self.session = session
        Screen.__init__(self, session)
       
        self['Key_red'] = Label('Delete')
        self['Key_green'] = Label('Sort ')
        self['Key_yellow'] = Label('Refresh')
        self['Key_blue'] = Label('Rename')
        self.mode = mode
        self.streamGenreLink = streamGenreLink
        self.searchData = searchData
        self.chicon = mode + '.png'
        downloadlocation = config.TuneinRadio.downloadlocation.value
        self['info'] = Label('Download Path: ' + downloadlocation)
        self['infoload'] = Label('Loading files..')
        self['handlung'] = Label('')
        self['coverArt'] = Pixmap()
        self['plugin_icon'] = Pixmap()
        self['page'] = Label(' ')
        self.movies = []
        self.onShow.append(self.refreshindex)
        self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        streamMenuList_youtube2font(self.streamMenuList)
        self['feedlist'] = self.streamMenuList
        self.sort = 'sort_default'
        self.movie_list = []
        self.searchstr = None
        self.searchagain = 'titanic'
        self.filmliste = []
        self.page = 1
        self.onShow.append(self.getlocalmedia)
        self.streamMenuList.onSelectionChanged.append(self.moviesselectionchanged)
        self['actions'] = ActionMap(['ColorActions',
         'SetupActions',
         'DirectionActions',
         'PiPSetupActions',
         'WizardActions',
         'NumberActions',
         'EPGSelectActions',
         'MenuActions'], {'red': self.deletefile,
         'green': self.sortfiles,
         'info': self.showinformation,
         'blue': self.renamefile,
         'yellow': self.getlocalmedia,
         'ok': self.keyOK,
         'menu': self.changepath,
         'cancel': self.exit,
         'up': self['feedlist'].up,
         'down': self['feedlist'].down,
         'left': self['feedlist'].pageUp,
         'right': self['feedlist'].pageDown}, -1)
        self.pages = []
        cat_movies = []
        self.movies = []
        self.pagemovies = []
        self.desc = ''
        self.keyLocked = False
        self.page = 1
        self.download = False
        self.searchstr = None
        self.page = 1
        return

    def showinformation(self):
        from Plugins.Extensions.TuneinRadio.screens.imdb import imdbupdates
        try:
            itemtitle = str(self['feedlist'].getCurrent()[0][0])
        except:
            return

        if itemtitle is None:
            return
        else:
            if '(' in itemtitle:
                itemtitle = itemtitle.split('(')[0].strip()
            self.session.open(imdbupdates, itemtitle)
            return

    def sortfiles(self):
        if self.sort == 'alphabet':
            self.sort = 'alphabet_reverse'
            self.getlocalmedia()
            return
        if self.sort == 'alphabet_reverse':
            self.sort = 'date_reverse'
            self.getlocalmedia()
            return
        if self.sort == 'date_reverse':
            self.sort = 'sort_default'
            self.getlocalmedia()
            return
        if self.sort == 'sort_default':
            self.sort = 'alphabet'
            self.getlocalmedia()

    def progress_callback(self, data):
        pass

    def renamefile(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        try:
            filename = self['feedlist'].getCurrent()[0][0]
        except:
            self['info'].setText('Failed to rename file')
            return

        self.session.openWithCallback(self.renameCallback, VirtualKeyBoard, title=_('Enter new file name'), text=filename)

    def renameCallback(self, newfilename):
        try:
            filepath = str(self['feedlist'].getCurrent()[0][2])
            filename = str(self['feedlist'].getCurrent()[0][0])
        except:
            self['info'].setText('Failed to rename file')
            return

        if newfilename:
            try:
                newfilepath = filepath.replace(str(filename), str(newfilename))
                os.rename(filepath, newfilepath)
                self['info'].setText('file renamed successfuly')
                self.getlocalmedia()
            except:
                self['info'].setText('Failed to rename file')

    def ShowPlugin_icon(self):
        micon = '%s/interface/micons/%s' % (PLUGIN_PATH, 'tv.png')
        import os
        if os.path.exists(micon):
            self['plugin_icon'].instance.setPixmapFromFile(micon)

    def getlocalmedia(self, result = None):
        self.ShowPlugin_icon()
        folder = getDownloadPath()
        if freespace() == 0:
            self['info'].setText(folder + ' Free space: zero or invalid location')
            return
        fspace = str(freespace())
        self['info'].setText(folder + ' Free space: ' + fspace)
        if folder.endswith('/'):
            self.folder = folder
        else:
            self.folder = folder + '/'
        try:
            self.mediafiles = []
            for x in os.listdir(self.folder):
                fullpath = self.folder + x
                if os.path.isfile(fullpath):
                    msize = os.path.getsize(fullpath)
                    localimagesize = str(round(float(msize / 1048576.0), 2)) + 'MB'
                    filedate = modification_date(fullpath)
                    x = x.strip()
                    if x.endswith('.mp3') :
                        try:
                            parts = x.split('.')
                            title = x.split('.')[len(parts) - 2]
                        except:
                            pass

                        self.mediafiles.append((title,
                         localimagesize,
                         fullpath,
                         filedate))

            from operator import itemgetter
            if self.sort == 'alphabet':
                self.mediafiles.sort(key=itemgetter(0), reverse=False)
            elif self.sort == 'alphabet_reverse':
                self.mediafiles.sort(key=itemgetter(0), reverse=True)
            elif self.sort == 'date_reverse':
                self.mediafiles.sort(key=lambda s: os.path.getmtime(s[2]), reverse=False)
            elif self.sort == 'sort_default':
                self.mediafiles.sort(key=lambda s: os.path.getmtime(s[2]), reverse=True)
            self.streamMenuList.setList(map(TuneinRadiofexplorer_filesexplorer, self.mediafiles))
            self['infoload'].setText(' ')
        except:
            self.mediafiles.append(('Invalid download path', ''))
            self.streamMenuList.setList(map(TuneinRadiofexplorer_filesexplorer, self.mediafiles))
            self['infoload'].setText(' ')

    def changepath(self):
        from downloadlocation import TuneinRadiodownloadlocation
        try:
            self.session.openWithCallback(self.backuplocation_choosen, TuneinRadiodownloadlocation)
        except:
            return

    def backuplocation_choosen(self, option):
        pass

    def deletefile(self):
        try:
            downloadlocation = getDownloadPath()
            self.filename = self['feedlist'].getCurrent()[0][2]
            self.session.openWithCallback(self.removefile, MessageBox, _(self.filename + ' will be removed,are you sure?'), MessageBox.TYPE_YESNO)
            return
        except:
            self['info'].setText('No files deleted ')

    def removefile(self, result):
        if result:
            try:
                os.remove(self.filename)
                self.getlocalmedia()
                self['info'].setText(self.fname + ' deleted!')
            except:
                self['info'].setText('sorry unable to delete file! ')

    def keyOK(self):
        downloadlocation = getDownloadPath()
        try:
            self.filename = self['feedlist'].getCurrent()[0][2]
        except:
            return

        try:
            title = self['feedlist'].getCurrent()[0][0]
        except:
            return
        filename=os.path.join( str(config.TuneinRadio.downloadlocation.value),self.filename)
        sref = eServiceReference(4097, 0, filename)
        sref.setName(title)
        if sref is not None:
            self.channel_list = self.mediafiles
            cindex = self['feedlist'].getSelectionIndex()
            playlist = []
            for i in range(0, len(self.channel_list) - 1):
                try:
                    name = self.channel_list[i][0]
                    url = self.channel_list[i][2]
                except:
                    continue

                playlist.append((name, url))

            self.saveindex(cindex)
            from Plugins.Extensions.TuneinRadio.lib.TSplayer import TSRadioplayer


            if True:
                addon_params = {'Plugin_id:plugin.program.fexplorer', 'sectin:programs'}
                self.session.open( TSRadioplayer, serviceRef = sref, serviceUrl = filename, serviceName = title, serviceIcon = '', playlist = [], playindex = 0,process_item=None)
             
        return

    def saveindex(self, index):
        try:
            afile = open('/tmp/TuneinRadio/index.txt', 'w')
            afile.write(str(index))
            afile.close()
        except:
            pass

    def refreshindex(self):
        self.download = False
        self.lock = False
        index = 0
        try:
            if os.path.exists('/tmp/TuneinRadio/index.txt'):
                try:
                    index = int(open('/tmp/TuneinRadio/index.txt', 'r').read())
                    os.remove('/tmp/TuneinRadio/index.txt')
                except:
                    return

                if index < 0 or index > len(self.itemslist) or index < 0:
                    self.streamMenuList.moveToIndex(0)
                else:
                    self.streamMenuList.moveToIndex(index)
        except:
            pass

    def backplayer(self, result = None):
        return
        if result is None:
            return
        else:
            try:
                self.mlist.moveToIndex(result)
            except:
                pass

            return
            return

    def refreshlists(self, result = False):
        if result == True:
            self.close

    def moviesselectionchanged(self):
        try:
            cindex = self['feedlist'].getSelectionIndex()
        except:
            return

        folder = getDownloadPath()
        if freespace() == 0:
            self['info'].setText(folder + ' Free space: zero or invalid location')
            return
        fspace = str(freespace()) + 'MB'
        self['info'].setText(folder + ' Free space: ' + fspace + 'MB')
        try:
            data = str(self.mediafiles[cindex][0]) + '\n' + str(self.mediafiles[cindex][1]) + '\n' + str(self.mediafiles[cindex][3])
            self['handlung'].setText(data)
        except:
            pass

    def exit(self):
        self.close()

    def exitplugin(self):
        self.close()
