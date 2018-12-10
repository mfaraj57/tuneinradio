# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ProhdIPTV/lib/Console3.py
from Screens.Screen import Screen
from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import copyfile, fileExists
from enigma import getDesktop
import os
from Screens.Standby import TryQuitMainloop
from .pltools import getversioninfo, gethostname
currversion, enigmaos, currpackage, currbuild = getversioninfo('ImagDownLoader') ##change

class Console3(Screen):
    global HD_Res
    try:
        sz_w = getDesktop(0).size().width()
        if sz_w == 1280:
            fullHD_Res = False
        elif sz_w == 1920:
            fullHD_Res = True
        else:
            fullHD_Res = False
    except:
        HD_Res = False

    if fullHD_Res == False:
        skin = '\n        \t\n                <screen name="Console3"  backgroundColor="#380038" position="center,center" size="920,600" title=""   >\n                \n\t\t<widget name="text" backgroundColor="#380038" position="30,30" size="865,570" font="Regular;22"   zPosition="2"  />\n                </screen>'
    else:
        skin = '\n        \t\n                <screen name="Console3" position="center,center" size="1380,675" title=""   >\n                \n\t\t<widget name="text" position="28,33" size="831,640" font="Regular;33"  transparent="1" zPosition="2"  />\n                </screen>'

    def __init__(self, session, title = 'Console', cmdlist = None, finishedCallback = None, closeOnSuccess = False, instr = None, endstr = None):
        Screen.__init__(self, session)
        self.color = '#800080'
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = False
        self.endstr = 'Press OK to exit or Blue to restart Enigma '
        instr = 'Installing please wait\n' + '\n*************************************\n'
        self['text'] = ScrollLabel(instr)
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'ColorActions'], {'blue': self.restartenigma,
         'ok': self.cancel,
         'back': self.cancel,
         'blue': self.restartenigma,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.newtitle = title
        self.onShown.append(self.updateTitle)
        self.container = eConsoleAppContainer()
        self.run = 0
        if enigmaos == 'oe2.0':
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
        else:
            self.contianer_closed = self.container.appClosed.connect(self.runFinished)
            self.contianer_dataAvail = self.container.dataAvail.connect(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def restartenigmold(self):
        os.system('killall -9 enigma2')

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.run += 1
        self.setTitle('Execution Finished')
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            str = self['text'].getText()
            str += '\n' + _('Execution finished!!-press blue to restart enigma')
            self['text'].setText(str)
            self['text'].lastPage()
            if self.finishedCallback is not None and not retval:
                self.finishedCallback()
            if not retval and self.closeOnSuccess == False:
                pass
            else:
                str += '\n' + _(self.endstr)
                self['text'].setText(str)
                self['text'].lastPage()
        return

    def cancel(self):
        try:
            if enigmaos == 'oe2.0':
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)
            else:
                self.contianer_closed = None
                self.contianer_dataAvail = None
            if self.run == len(self.cmdlist):
                self.close()
        except:
            pass

        return

    def dataAvail(self, str):
        self['text'].setText(self['text'].getText() + str)

    def restartenigma(self):

        self.session.open(TryQuitMainloop, 3)

