# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ProhdIPTV/lib/prohdplaylist.py

import os
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from enigma import getPrevAsciiCode, gPixmapPtr, eConsoleAppContainer, eSize, RT_WRAP, ePoint, eTimer, addFont, loadPNG, quitMainloop, eListbox, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceCenter, iServiceInformation, eServiceReference, iSeekableService, iPlayableService, iPlayableServicePtr, eDVBDB
sz_w = getDesktop(0).size().width()
from Plugins.Extensions.TuneinRadio.lib.pltools import log



class tsplaylist(Screen):
    if sz_w == 1280:
        skin = '''<screen name="tsplaylist" position="20,20" size="460,700" backgroundColor="#54111112" title=" " transparent="0"><widget name="info" position="280,280" zPosition="4" size="200,200" font="Regular;24" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" /><widget name="streamlist" position="20,20" size="400,600" itemHeight="60" backgroundColor="#54111112" foregroundColor="#9dc014" foregroundColorSelected="#ffffff" backgroundColorSelected="#41000000"  transparent="1" />

<widget name="programm" position="20,660" zPosition="4" size="480,60" font="Regular;20" foregroundColor="#ffffff" transparent="1" halign="left" valign="top" />
</screen> '''
    else:
        skin = '''<screen name="tsplaylist" position="30,30" size="660,1040" backgroundColor="#54111112" title=" " transparent="0">
<widget name="info" position="420,420" zPosition="4" size="300,300" font="Regular;36" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />

<widget name="streamlist" position="20,30" size="600,900" itemHeight="90" backgroundColor="#54111112" foregroundColor="#9dc014" foregroundColorSelected="#ffffff" backgroundColorSelected="#41000000"  transparent="1" />

<widget name="programm" position="20,970" zPosition="4" size="800,100" font="Regular;30" foregroundColor="#ffffff" transparent="1" halign="left" valign="top" />
</screen>

'''
    def __init__(self, session, playlist = [], playindex = 0, sendback = None):
        Screen.__init__(self, session)
        self.session = session
        self.playindex = playindex
        self.sendback = sendback
        
        self.playlist = playlist
        print self.playlist
       
        self.select_set = False
        self.lucent = 1
        self['info'] = Label(' ')
        self['programm']=Label(" ")
        self['actions'] = ActionMap(['ColorActions','OkCancelActions', 'WizardActions'], {'ok': self.keyOK,         
         'cancel': self.keyCancel}, -1)
        
        self['streamlist'] = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
       
        self.keyLocked = True
        self.page = 1
        self.currentlist = 'streamlist'
        self.timer2 = eTimer()
        try:
            self.timer2.callback.append(self.ListToMulticontent)
        except:
            self.timer2_conn = self.timer2.timeout.connect(self.ListToMulticontent)

        self.timer2.start(20, 1)

    def ListToMulticontent(self):
        cacolor = 16776960
        cbcolor = 16753920
        cccolor = 15657130
        cdcolor = 16711680
        cecolor = 16729344
        cfcolor = 65407
        cgcolor = 11403055
        chcolor = 13047173
        cicolor = 13789470
        scolor = cbcolor
        res = []
        theevents = []
        
        
        if sz_w == 1280:
            self['streamlist'].l.setItemHeight(60)
            self['streamlist'].l.setFont(0, gFont('Regular', 24))
        else:
            self['streamlist'].l.setItemHeight(90)
            self['streamlist'].l.setFont(0, gFont('Regular', 30))
        png = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/playlist.png'
        for i in range(0, len(self.playlist)):
            txt = self.playlist[i][0]
           
            scolor = cbcolor
            res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 0), size=(45, 45), png=loadPNG(png)))
            if sz_w == 1280:
                res.append(MultiContentEntryText(pos=(30, 1), size=(400, 60), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(txt), color=scolor, color_sel=cccolor, border_width=3, border_color=806544))
            else:
                res.append(MultiContentEntryText(pos=(40, 1), size=(600, 90), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER | RT_WRAP, text=str(txt), color=scolor, color_sel=cccolor, border_width=3, border_color=806544))
            theevents.append(res)
            res = []

        self['streamlist'].l.setList(theevents)
        self['streamlist'].show()
        self['streamlist'].moveToIndex(self.playindex)







    def keyOK(self):

        


            itemindex = self['streamlist'].getSelectionIndex()
            
            
            self.sendback(itemindex, self.playlist)
           
    def keyCancel(self):
        self.close(None, None)
        return
