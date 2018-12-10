# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ProhdIPTV/lib/TSplayer.py
import Queue
import random
import os, re
from Screens.InfoBarGenerics import *
from Components.Pixmap import MovingPixmap, Pixmap
from enigma import eServiceReference, iServiceInformation, iPlayableService, getDesktop, gPixmapPtr
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.AVSwitch import AVSwitch
from ServiceReference import ServiceReference
from Screens.PVRState import PVRState, TimeshiftState
from Tools.Directories import copyfile
from skin import parseColor
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'

def getserviceinfo(sref):
    try:
        p = ServiceReference(sref)
        servicename = str(p.getServiceName())
        serviceurl = str(p.getPath())
        return (servicename, serviceurl)
    except:
        return (None, None)

    return (None, None)


def getrandom(cmax = 10, list1 = []):
    rand = 0
    try:
        rand = random.randrange(0, cmax)
        if rand in list1:
            rand = random.randrange(0, cmax)
    except:
        rand = 0

    return rand


from .pltools import log

class StatusScreen(Screen):

    def __init__(self, session):
        desktop = getDesktop(0)
        size = desktop.size()
        self.sc_width = size.width()
        self.sc_height = size.height()
        statusPositionX = 50
        statusPositionY = 100
        self.delayTimer = eTimer()
        try:
            self.delayTimer.callback.append(self.hideStatus)
        except:
            self.delayTimer_connect = self.delayTimer.timeout.connect(self.hideStatus)

        self.delayTimerDelay = 1500
        self.shown = True
        self.skin = '\n            <screen name="StatusScreen" position="%s,%s" size="%s,90" zPosition="0" backgroundColor="transparent" flags="wfNoBorder">\n                    <widget name="status" position="0,0" size="%s,70" valign="center" halign="left" font="Regular;22" transparent="1" foregroundColor="yellow" shadowColor="#40101010" shadowOffset="3,3" />\n            </screen>' % (str(statusPositionX),
         str(statusPositionY),
         str(self.sc_width),
         str(self.sc_width))
        Screen.__init__(self, session)
        self.stand_alone = True
        print 'initializing status display'
        self['status'] = Label('')
        self.onClose.append(self.__onClose)

    def setStatus(self, text, color = 'yellow'):
        self['status'].setText(text)
        self['status'].instance.setForegroundColor(parseColor(color))
        self.show()
        self.delayTimer.start(self.delayTimerDelay, True)

    def hideStatus(self):
        self.hide()
        self['status'].setText('')

    def __onClose(self):
        try:
            self.delayTimer.stop()
            del self.delayTimer
            try:
                self.delayTimer_connect
            except:
                pass

            self['status'].setText('')
        except:
            pass


class TSRplayer(Screen, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide, InfoBarPVRState,InfoBarAudioSelection):
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    skin='''	    	<screen name ="TSRplayer" position="0,0" size="1280,720" backgroundColor="black" flags="wfNoBorder" title="Player">
	    
		<widget position="1160,557" halign="center" size="64,28" foregroundColor="#ffffff" zPosition="2" name="channel_number" transparent="1" font="Regular;32"/>
		
		
                
                
                
                <ePixmap position="80,620" size="117,550" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/pristavka.png" zPosition="10" transparent="1" alphatest="blend" />   	 
		   	 
                <widget name="cover" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/radio.png" position="0,0" size="1280,480" transparent="1" alphatest="blend" borderWidth="2" borderColor="#00555556" />
   		
                <widget name="plugin_icon" pixmap="~/spicons/radio.png" position="1160,640" size="65,65" transparent="1" alphatest="blend" borderWidth="2" borderColor="#00555556" />
   
                        
                <widget position="300,556" size="670,130" foregroundColor="#ffffff" backgroundColor="#41000000" zPosition="2" transparent="1" name="programm" halign="center" valign="center" font="Regular;24"/>
	
        
        
		 <widget source="global.CurrentTime" 	render="Label" position="1026,506" 	size="140,34" zPosition="2"	font="LCD;32" valign="top" halign="right" foregroundColor="white"	backgroundColor="transpBlack" transparent="1">
			<convert type="ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" 	render="Label" position="1123,508" 	size="70,22" zPosition="2"	font="LCD;20" valign="top" halign="right" foregroundColor="white"	backgroundColor="transpBlack" transparent="1">
			<convert type="ClockToText">Format::%S</convert>
		</widget>	
		<widget source="global.CurrentTime" render="Label" position="100,508" size="110,24" font="Regular;22" halign="left"  foregroundColor="white"	backgroundColor="transpBlack" transparent="1">
			<convert type="ClockToText">Format:%d.%m.%Y</convert>
		</widget>
		  <widget source="session.CurrentService" render="Label" position="240,485" size="800,30" zPosition="2" font="Regular;26" halign="center" noWrap="1" foregroundColor="white" transparent="1" backgroundColor="background">
		<convert type="ServiceName">Name</convert>
		</widget>
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_dolby_off.png" position="75,560" size="44,26" zPosition="1" alphatest="blend" />
		<widget source="session.CurrentService" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_dolby_on.png" position="75,560" size="44,26" zPosition="2" alphatest="blend">
			<convert type="ServiceInfo">IsMultichannel</convert>
			<convert type="ConditionalShowHide"/>
		</widget>
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_format_off.png"  position="123,560"  size="44,26" zPosition="1" alphatest="blend" />
		<widget source="session.CurrentService" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_format_on.png"	position="123,560"  size="44,26" zPosition="2" alphatest="blend">
			<convert type="ServiceInfo">IsWidescreen</convert>
			<convert type="ConditionalShowHide"/>
		</widget>
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_rec_off.png" 	position="171,560" size="44,26" zPosition="1" alphatest="blend" />
		<widget source="session.RecordState" render="Pixmap" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/ico_rec_on.png" 	position="171,560" size="44,26" zPosition="2" alphatest="blend">
			<convert type="ConditionalShowHide">Blink</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" font="Regular;20" position="1083,535" size="55,24" halign="right" foregroundColor="white" backgroundColor="transpBlack" transparent="1">
			<convert type="ServiceInfo">VideoWidth</convert>
		</widget>
		<eLabel text="x" font="Regular;20" position="1138,524" size="15,24" halign="center"  foregroundColor="white" backgroundColor="transpBlack" transparent="1"/>
		<widget source="session.CurrentService" render="Label" font="Regular;20" position="1153,535" size="55,24" halign="left" foregroundColor="white" backgroundColor="transpBlack" transparent="1">
			<convert type="ServiceInfo">VideoHeight</convert>
		</widget>		
		<widget source="session.CurrentService" render="Label" position="244,524" size="100,26" font="Regular;22" halign="right" foregroundColor="white" backgroundColor="transpBlack" transparent="1" >
			<convert type="ServicePosition">Position</convert>
		</widget>
		<ePixmap position="360,529" size="600,22" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/mpslider.png" zPosition="3" alphatest="blend" />
		<widget source="session.CurrentService" render="PositionGauge" position="385,533" size="552,14" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/pointer.png:13,3" >
			<convert type="ServicePosition">Gauge</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="980,524" size="100,26" font="Regular;22" halign="left" foregroundColor="white" backgroundColor="transpBlack" transparent="1" >
			<convert type="ServicePosition">Remaining</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="600,560" size="120,25" font="Regular;24" halign="center" foregroundColor="white" backgroundColor="transpBlack" transparent="1" >
			<convert type="ServicePosition">Length</convert>
		</widget>
		<ePixmap position="62,524" zPosition="1" size="168,34" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/TSplayer/mp_buttons.png" alphatest="on" transparent="1" />        
        
        
        
        </screen>   '''
    def __init__(self, session, serviceRef = None, serviceUrl = '', serviceName = '', serviceIcon = '', playlist = [], playindex = 0):
        Screen.__init__(self, session)
        self.session = session
        
        if serviceUrl == '' and serviceRef is not None:
            serviceName, serviceUrl = getserviceinfo(serviceRef)
        if playlist == []:
            playlist.append((serviceName, serviceUrl, serviceIcon))
       
        self.playlist = playlist
        self.playindex = playindex
        self.serviceRef = serviceRef
        self.serviceName = serviceName
        self.serviceUrl = serviceUrl
        self.serviceIcon = serviceIcon
        self.onPlayStateChanged = []
        InfoBarPVRState.__init__(self, screen=PVRState)
        self.pvrStateDialog = self.session.instantiateDialog(PVRState)
        try:
            self.lastservice = self.session.nav.getCurrentlyPlayingServiceReference()
        except:
            self.lastservice = None

        self.serviceName = serviceName
        self['programm'] = Label('playing stream..')
        self['channel_number'] = Label(str(playindex))
        self.onPlayStateChanged = []
        self.InfoBar_NabDialog = Label('')
        self.statusScreen = self.session.instantiateDialog(StatusScreen)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evUpdatedInfo: self.__evUpdatedInfo,
         iPlayableService.evUser + 10: self.__evAudioDecodeError,
         iPlayableService.evUser + 11: self.__evVideoDecodeError,
         iPlayableService.evUser + 12: self.__evPluginError})
        self['actions'] = ActionMap(['ColorActions',
         'WizardActions',
         'PiPSetupActions',
         'MediaPlayerSeekActions',
         'InfobarInstantRecord',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MoviePlayerActions',
         'ColorActions',
         'InfobarActions',
         'MenuActions',
         'NumberActions'], {'leavePlayer': self.leavePlayer,
         'info': self.openinfo,         
         'back': self.leavePlayer,
         'left': self.seekBack1,
         'down': self.showplaylistdown,
         'up': self.showplaylistup,
         'blue': self.seekFwdManual,
         'yellow':self.addfav,                   
         '0': self.resumeplay,
         'size-': self.av,
         'size+': self.av,
         'right': self.seekFwd1}, -1)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.audio = True
        self.new_aspect = self.init_aspect
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self)
        InfoBarShowHide.__init__(self)
        self['cover'] = Pixmap()    
        InfoBarAudioSelection.__init__(self)
        self.shown = False
        self.playstopped=False
        InfoBarSeek.__init__(self)
        self.onClose.append(self.playExit)
        self.onLayoutFinish.append(self.playService)
        return
 



    def addfav(self):
        
        from .tsfavorites import addfavorite,favexists
        result = False
        try:
            param = str(self.serviceUrl)
            title = str(self.serviceName)
            if favexists(title,param):
               self['programm'].setText('Channel already added to favorites.')
               
               return
               
            result = addfavorite('radio/TuneinRadio', title, param, 'radio')
        except:
            result = False

        if result == True:
            self['programm'].setText(title + ' added successfully to favorites.')
        else:
            self['programm'].setText('Failed to add to favorites.')
        



    def resumeplay(self):
            title = self.playlist[self.playindex][0]
            url = self.playlist[self.playindex][1]            
            self.playService(title,url)        
        

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
         1: _('4:3 PanScan'),
         2: _('16:9'),
         3: _('16:9 always'),
         4: _('16:10 Letterbox'),
         5: _('16:10 PanScan'),
         6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
         1: '4_3_panscan',
         2: '16_9',
         3: '16_9_always',
         4: '16_10_letterbox',
         5: '16_10_panscan',
         6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        print self.getAspectString(temp)
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)
        print self.getAspectString(temp)
        self.statusScreen.setStatus(self.getAspectString(temp))

    def ScreenSaverTimerStart(self):
        return
        try:
            time = int(config.usage.screen_saver.value)
            flag = self.seekstate[0]
            if not flag:
                ref = self.session.nav.getCurrentlyPlayingServiceOrGroup()
                if ref:
                    ref = ref.toString().split(':')
                    flag = ref[2] == '2' or os.path.splitext(ref[10])[1].lower() in AUDIO_EXTENSIONS
            if time and flag:
                self.screenSaverTimer.startLongTimer(time)
            else:
                self.screenSaverTimer.stop()
        except:
            pass

    def loadIcon(self):
        try:
            streamPic = self.playlist[self.playindex][2]
        except:
            streamPic = None

        if streamPic is None or streamPic == '':
            cover = plugin_path + '/icon.png'
            copyfile(cover, '/tmp/cover.jpg')
            self.ShowCover(streamPic)
        else:
            downloadPage(streamPic, '/tmp/cover.jpg').addCallback(self.ShowCover).addErrback(self.showerror)
        return

    def showerror(self, error):
        cover = plugin_path + '/icon.png'
        copyfile(cover, '/tmp/cover.jpg')
        self.ShowCover(None)
        return

    def ShowCover(self, picData):
        if fileExists('/tmp/cover.jpg'):
            try:
                self['cover'].instance.setPixmap(gPixmapPtr())
                self.scale = AVSwitch().getFramebufferScale()
                self.picload = ePicLoad()
                size = self['cover'].instance.size()
                self.picload.setPara((size.width(),
                 size.height(),
                 self.scale[0],
                 self.scale[1],
                 False,
                 1,
                 '#FF000000'))
                if self.picload.startDecode('/tmp/cover.jpg', 0, 0, False) == 0:
                    ptr = self.picload.getData()
                    if ptr != None:
                        self['cover'].instance.setPixmap(ptr)
                        self['cover'].show()
                        del self.picload
            except:
                pass

        return

       
        
    def bannershow(self):
        return
        self.hide()

    def _mayShow(self):
        print '244', self.audio
        if self.audio == True:
            try:
                p = InfoBarShowHide()
                if p.__state == p.STATE_SHOWN:
                    p.hideTimer.stop()
                elif p.__state == p.STATE_HIDDEN:
                    p.show()
            except:
                pass

        elif self.execing and self.seekstate != self.SEEK_STATE_PLAY:
            if self.pvrStateDialog is not None:
                self.pvrStateDialog.show()
        return
    def seekBack(self):
        self.seekBack1()

    def seekFwd(self):
        self.seekFwd1()

    def seekBack1(self):
        self.playindex = self.playindex - 1
        if self.playindex < 0:
            self.playindex = len(self.playlist) - 1
        title = self.playlist[self.playindex][0]
        url = self.playlist[self.playindex][1]
        self.playService(title=title, url=url)

    def seekFwd1(self):
        self.playindex = int(self.playindex) + 1
        if self.playindex == len(self.playlist):
            self.playindex = 0
        title = self.playlist[self.playindex][0]
        url = self.playlist[self.playindex][1]
        self.playService(title=title, url=url)

    def sendback(self, index = None, newplaylist = []):
        if newplaylist:
            self.newindex = index
            
            self.playlist = newplaylist
            self.playindex = index
            
            title = self.playlist[self.playindex][0]
            url = self.playlist[self.playindex][1]
            self.playService(title=title, url=url)

    def showplaylistdown(self):
        from .tsplaylist import tsplaylist
        newindex = self.playindex + 1
        if newindex == len(self.playlist):
            newindex = len(self.playlist) - 1
        self.session.openWithCallback(self.playlistback, tsplaylist, self.playlist, self.playindex, self.sendback)

    def showplaylistup(self):
        from .tsplaylist import tsplaylist
        newindex = self.playindex - 1
        if newindex < 0:
            newindex = 0
        self.session.openWithCallback(self.playlistback, tsplaylist, self.playlist, self.playindex, self.sendback)

    def playlistback(self, result = None, playlist = []):
        return
        if result:
            self.newindex = result
           
            self.playindex = result
            title = self.playlist[self.playindex][0]
            url = self.playlist[self.playindex][1]
            self.playService(title=title, url=url)

    def openinfo(self):

        if True:
            servicename, serviceurl = getserviceinfo(self.serviceRef)
            if servicename is not None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl is not None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec :' + str(sTagAudioCodec)

        else:
            return
            
        
        from .showinfo import showinfoscreen
        self.session.open(showinfoscreen,message,"TuneinRadio")
    def playService(self, title = None, url = None):
        try:
           
            self['programm'].setText('Playing stream..')
            if url is None:
                url = self.serviceUrl
            else:
                self.serviceUrl = url
            if title is None:
                title = self.serviceName
            else:
               self.serviceName = title 
            print "xxurl",url
            if url is None or not url.startswith('http') and not url.startswith('rtmp'):
                self['programm'].setText('invalid stream link1')
                return
            title=str(title)
            
            self.serviceRef = eServiceReference(4097, 0, str(url))
            self.serviceRef.setName(title)
            self.session.nav.stopService()
            self.session.nav.playService(self.serviceRef)
            self['channel_number'].setText(str(self.playindex))
            self['programm'].setText(' ')
        except:
            self['programm'].setText('invalid stream link2')

        return

    def leavePlayer(self):
        self.playExit()
        self.is_closing = True
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass

        self.close(self.playindex)

    def leavePlayerConfirmed(self, answer):
        self.is_closing = True

    def handleLeave(self, how = 'noask'):
        self.is_closing = True
        self.leavePlayerConfirmed([True, how])

    def doEofInternal(self, playing):
        currPlay = self.session.nav.getCurrentService()
        message = currPlay.info().getInfoString(iServiceInformation.sUser + 12)
        if message.find('Flash demuxer not available') != -1 or message.find('(AVI) demuxer not available') != -1:
            self['programm'].setText("Your box can't decode this video stream!\n%s") % message
        elif message.find('GStreamer plugin') != -1 and message.find('not available') != -1:
            self.__evPluginError()
        elif message.find('GStreamer') != -1 and message.find('missing a plug-in') != -1:
            self.__evPluginError()
        elif message.find('GStreamer error') != -1:
            print 'gsstreamer mah eroor', message
            self.__evPluginError()
        elif message.find('No decoder available') != -1:
            self.__evPluginError()
        else:
            if not self.execing:
               
                return None
            if not playing:
               
                return None
            #self.doSeek(0)
            #self.setSeekState(self.SEEK_STATE_PLAY)
            self.noexit = False
           
            self.playstopped=True
            title = self.playlist[self.playindex][0]
            url = self.playlist[self.playindex][1]            
            self.playService(title,url)
            #self.hide()
           
            return None
        return None

    def __evUpdatedInfo(self):
        sTitle = ''
        currPlay = self.session.nav.getCurrentService()
        if currPlay is not None:
            sTitle = currPlay.info().getInfoString(iServiceInformation.sTagTitle)
          
            try:
                sTitle = sTitle.strip()
            except:
                sTitle = ''

            if not sTitle == '':
                
                self.sTitle = sTitle
        try:
            self['programm'].setText(sTitle)
        except:
            self['programm'].setText('unknown')

        text = self['programm'].getText()
        return

    def __evAudioDecodeError(self):
        currPlay = self.session.nav.getCurrentService()
        sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
        print "[__evAudioDecodeError] audio-codec %s can't be decoded by hardware" % sTagAudioCodec
        if sTagAudioCodec is not None:
            self['programm'].setText(str(sTagAudioCodec))
            
            
        return

    def __evVideoDecodeError(self):
        currPlay = self.session.nav.getCurrentService()
        sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
        print "[__evVideoDecodeError] video-codec %s can't be decoded by hardware" % sTagVideoCodec
        if sTagVideoCodec is not None:
            self['programm'].setText(str(sTagVideoCodec))
            print '3showcodec,sTitle', str(sTagVideoCodec)
            
        return

    def __evPluginError(self):
        currPlay = self.session.nav.getCurrentService()
        message = currPlay.info().getInfoString(iServiceInformation.sUser + 12)
        print '[__evPluginError]', message
        if message is not None:
            self['programm'].setText(str(message))
            
        return

            
    def playExit(self):
        
        self.session.nav.stopService()
        if self.lastservice is not None:
            self.session.nav.playService(self.lastservice)
        return
