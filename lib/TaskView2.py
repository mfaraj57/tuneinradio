# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/resources/TaskView2.py
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigSelection, getConfigListEntry
from Components.SystemInfo import SystemInfo
from Components.Task import job_manager
from Screens.InfoBarGenerics import InfoBarNotifications
import Screens.Standby
import os
from enigma import gPixmapPtr, getDesktop
from Tools import Notifications
from Components.Pixmap import Pixmap
THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/ImageDownLoader'

class JobViewNew(InfoBarNotifications, Screen, ConfigListScreen):
    try:
        sz_w = getDesktop(0).size().width()
        if sz_w == 1280:
            fullHD_Res = False
        elif sz_w == 1920:
            fullHD_Res = True
        else:
            fullHD_Res = False
    except:
        fullHD_Res = False

    if fullHD_Res == True:
        skin = '     <screen position="center,center" size="1920,1080" title="  " >        <widget name="pixmap" position="1413,558" size="300,300" zPosition="1" alphatest="on" />\n\n\t\t<widget source="job_name" render="Label" position="150,150" size="720,150" font="Regular;42" backgroundColor="#40000000" />\n\t\t<!--widget source="job_task" render="Label" position="150,225" size="720,75" font="Regular;36" backgroundColor="#40000000" /-->\n\t\t<widget source="job_progress" render="Progress" position="210,375" size="720,54" borderWidth="2" backgroundColor="#40000000" />\n\t\t<widget source="job_progress" render="Label" position="150,525" size="420,48" font="Regular;42" backgroundColor="#40000000" zPosition="2" halign="center" transparent="1"  >\n\t\t\t<convert type="ProgressToText" />\n\t\t</widget>\n\t\t<widget source="job_status" render="Label" position="150,600" size="720,45" font="Regular;34" backgroundColor="#40000000" />\n\t\t<widget name="config" position="150,725" size="775,60" foregroundColor="#cccccc" backgroundColor="#40000000" />            <eLabel position="225,1090" zPosition="1" size="300,45" backgroundColor="#f23d21" />     <eLabel position="226,993" zPosition="1" size="294,39" backgroundColor="#40000000" />     <eLabel position="525,990" zPosition="1" size="300,45" backgroundColor="#389416" />    <eLabel position="528,993" zPosition="1" size="294,39" backgroundColor="#40000000" />    <eLabel position="825,990" zPosition="1" size="600,45" backgroundColor="#0064c7" />    <eLabel position="828,993" zPosition="1" size="594,39" backgroundColor="#40000000" />    <widget source="cancelable" render="FixedLabel" text="Stop download" position="225,990" size="300,45" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" > <convert type="ConditionalShowHide" />\n\t</widget>\n\t<widget source="finished" render="FixedLabel" text="OK" position="525,990" size="300,45" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" > <convert type="ConditionalShowHide" />\n\t</widget>\n\t<widget source="backgroundable" render="FixedLabel" text="Continue in background" position="825,990" size="600,45" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" >\n\t\t\t<convert type="ConditionalShowHide" />\n\t</widget>            </screen>'

   
    else:
        skin = '\n    <screen position="center,center" size="1280,720" title="  " >\n    \n    <widget name="pixmap" position="942,372" size="200,200" zPosition="1" alphatest="on" />\n\n\t\t<widget source="job_name" render="Label" position="100,100" size="480,100" font="Regular;28" backgroundColor="#40000000" />\n\t\t<!--widget source="job_task" render="Label" position="100,150" size="480,50" font="Regular;23" backgroundColor="#40000000" /-->\n\t\t<widget source="job_progress" render="Progress" position="140,250" size="480,36" borderWidth="2" backgroundColor="#40000000" />\n\t\t<widget source="job_progress" render="Label" position="100,350" size="280,32" font="Regular;28" backgroundColor="#40000000" zPosition="2" halign="center" transparent="1"  >\n\t\t\t<convert type="ProgressToText" />\n\t\t</widget>\n\t\t<widget source="job_status" render="Label" position="100,400" size="480,30" font="Regular;23" backgroundColor="#40000000" />\n\t\t<widget name="config" position="100,500" size="550,40" foregroundColor="#cccccc" backgroundColor="#40000000" />\n\t\n        \n    <eLabel position="150,660" zPosition="1" size="200,30" backgroundColor="#f23d21" /> \n    <eLabel position="152,662" zPosition="1" size="196,26" backgroundColor="#40000000" /> \n    <eLabel position="350,660" zPosition="1" size="200,30" backgroundColor="#389416" />\n    <eLabel position="352,662" zPosition="1" size="196,26" backgroundColor="#40000000" />\n    <eLabel position="550,660" zPosition="1" size="400,30" backgroundColor="#0064c7" />\n    <eLabel position="552,662" zPosition="1" size="396,26" backgroundColor="#40000000" />\n\n    \t<widget source="cancelable" render="FixedLabel" text="Stop download" position="150,660" size="200,30" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" > \n\t\t\t<convert type="ConditionalShowHide" />\n\t</widget>\n\t<widget source="finished" render="FixedLabel" text="OK" position="350,660" size="200,30" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" > \n\t\t\t<convert type="ConditionalShowHide" />\n\t</widget>\n\t<widget source="backgroundable" render="FixedLabel" text="Continue in background" position="550,660" size="400,30" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" >\n\t\t\t<convert type="ConditionalShowHide" />\n\t</widget>    \n        \n\t</screen>'

    def __init__(self, session, job, parent = None, cancelable = True, backgroundable = True, afterEventChangeable = True):
        from Components.Sources.StaticText import StaticText
        from Components.Sources.Progress import Progress
        from Components.Sources.Boolean import Boolean
        from Components.ActionMap import ActionMap
        Screen.__init__(self, session, parent)
        InfoBarNotifications.__init__(self)
        ConfigListScreen.__init__(self, [])
        self.parent = parent
        self.session = session
        try:
            txt=open("/tmp/filesize").read()
            self.size="Size "+str(int(txt)/(1024*1024))+"MB"
           
        except:
            self.size="000"
           
        self.job = job
        self['pixmap'] = Pixmap()
        self['job_name'] = StaticText(job.name)
        self['job_progress'] = Progress()
        self['job_task'] = StaticText()
        self['summary_job_name'] = StaticText(job.name)
        self['summary_job_progress'] = Progress()
        self['summary_job_task'] = StaticText()
        self['job_status'] = StaticText(job.name)
        self['finished'] = Boolean()
        self['cancelable'] = Boolean(cancelable)
        self['cancelable'].boolean = True
        self['backgroundable'] = Boolean(backgroundable)
        self['key_blue'] = StaticText(_('Background'))
        
        self.onShow.append(self.windowShow)
        self.onHide.append(self.windowHide)
        self['setupActions'] = ActionMap(['ColorActions', 'SetupActions'], {'green': self.ok,
         'red': self.abort,
         'blue': self.background,
         'cancel': self.ok,
         'ok': self.ok}, -2)
        self.settings = ConfigSubsection()
        if SystemInfo['DeepstandbySupport']:
            shutdownString = _('go to standby')
        else:
            shutdownString = _('shut down')
        self.settings.afterEvent = ConfigSelection(choices=[('nothing', _('do nothing')),
         ('close', _('Close')),
         ('standby', _('go to idle mode')),
         ('deepstandby', shutdownString)], default=self.job.afterEvent or 'nothing')
        self.job.afterEvent = self.settings.afterEvent.getValue()
        self.afterEventChangeable = afterEventChangeable
        self.setupList()
        self.state_changed()

    def setupList(self):
        if self.afterEventChangeable:
            self['config'].setList([getConfigListEntry(_('After event'), self.settings.afterEvent)])
        else:
            self['config'].hide()
        self.job.afterEvent = self.settings.afterEvent.getValue()

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.setupList()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.setupList()

    def windowShow(self):
        pic1 = THISPLUG + '/skin/images/download.png'
        self['pixmap'].instance.setPixmapFromFile(pic1)
        self.job.state_changed.append(self.state_changed)

    def windowHide(self):
        if len(self.job.state_changed) > 0:
            self.job.state_changed.remove(self.state_changed)

    def state_changed(self):
        j = self.job
        self['job_progress'].range = j.end
        self['summary_job_progress'].range = j.end
        self['job_progress'].value = j.progress
        self['summary_job_progress'].value = j.progress
        self['job_status'].text = self.size +" "+j.getStatustext()
        if j.status == j.IN_PROGRESS:
            self['job_task'].text = j.tasks[j.current_task].name
            self['summary_job_task'].text = j.tasks[j.current_task].name
        else:
            self['job_task'].text = ''
            self['summary_job_task'].text = j.getStatustext()
        if j.status in (j.FINISHED, j.FAILED):
            self.performAfterEvent()
            self['backgroundable'].boolean = False
            if j.status == j.FINISHED:
                self['finished'].boolean = True
                self['cancelable'].boolean = False
            elif j.status == j.FAILED:
                self['cancelable'].boolean = True

    def background(self):
        if self['backgroundable'].boolean == True:
            self.close(False)

    def ok(self):
        if self.job.status in (self.job.FINISHED, self.job.FAILED):
            self.close(False)

    def abort(self):
        if self.job.status == self.job.NOT_STARTED:
            job_manager.active_jobs.remove(self.job)
            self.close(False)
        elif self.job.status == self.job.IN_PROGRESS and self['cancelable'].boolean == True:
            from Screens.MessageBox import MessageBox
            self.session.openWithCallback(self.stop_job, MessageBox, _('Stop download now,downloaded file will be deleted.'), MessageBox.TYPE_YESNO)
        else:
            self.close(False)

    def stop_job(self, result):
        if result:
            self.job.cancel()
            print '167', self.job.name
            downloadfolder = config.plugins.tstube.downloadlocation.value
            print '168', downloadfolder + '/' + self.job.name
            try:
                os.remove(downloadfolder + self.job.name)
                cmd1 = 'killall -9 rtmpdump'
                cmd2 = 'killall -9 wget'
                os.system(cmd1)
                os.system(cmd2)
            except:
                print 'failed to stop download'

            self.close(True)

    def performAfterEvent(self):
        self['config'].hide()
        if self.settings.afterEvent.getValue() == 'nothing':
            return
        if self.settings.afterEvent.getValue() == 'close' and self.job.status == self.job.FINISHED:
            self.close(False)
        from Screens.MessageBox import MessageBox
        if self.settings.afterEvent.getValue() == 'deepstandby':
            if not Screens.Standby.inTryQuitMainloop:
                Notifications.AddNotificationWithCallback(self.sendTryQuitMainloopNotification, MessageBox, _('A sleep timer wants to shut down\nyour Dreambox. Shutdown now?'), timeout=20, domain='JobManager')
        elif self.settings.afterEvent.getValue() == 'standby':
            if not Screens.Standby.inStandby:
                Notifications.AddNotificationWithCallback(self.sendStandbyNotification, MessageBox, _('A sleep timer wants to set your\nDreambox to standby. Do that now?'), timeout=20, domain='JobManager')

    def checkNotifications(self):
        self.close(False)

    def sendStandbyNotification(self, answer):
        if answer:
            Notifications.AddNotification(Screens.Standby.Standby, domain='JobManager')

    def sendTryQuitMainloopNotification(self, answer):
        if answer:
            Notifications.AddNotification(Screens.Standby.TryQuitMainloop, 1, domain='JobManager')
