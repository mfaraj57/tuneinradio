# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/resources/tsdownload.py
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Sources.List import List
from Components.Task import Task, Job, job_manager, Condition
from Components.config import config, ConfigSelection, ConfigSubsection, ConfigText, ConfigYesNo, getConfigListEntry, ConfigPassword
from Tools import Notifications, ASCIItranslit
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBarGenerics import InfoBarNotifications, InfoBarSeek
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction
from Tools.Directories import resolveFilename, SCOPE_HDD, SCOPE_CURRENT_PLUGIN
from Tools.Downloader import downloadWithProgress
from enigma import eConsoleAppContainer
from enigma import eTimer, ePoint, RT_HALIGN_LEFT, RT_VALIGN_CENTER, gFont, ePicLoad, eServiceReference, iPlayableService
from os import path as os_path, remove as os_remove, system as os_system
import os
from twisted.web import client
from Screens.Screen import Screen
from Screens.LocationBox import MovieLocationBox
from Components.config import config, ConfigText, getConfigListEntry
from Components.config import KEY_DELETE, KEY_BACKSPACE, KEY_ASCII, KEY_TIMEOUT
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText
from Components.Task import job_manager
from Tools.Directories import resolveFilename, SCOPE_HDD
from threading import Thread
from xml.etree.cElementTree import fromstring as cet_fromstring
from StringIO import StringIO
from urllib import FancyURLopener
total = 0
dlocation = '/media/hdd/'#config.plugins.AliSatSettings2.Downloadlocation.value
if not dlocation.endswith("/"):
   dlocation=dlocation+"/"
#from Plugins.Extensions.AliSatSettings.resources.functions import getenigmaos
#enigmaos=getenigmaos()
enigmaos='oe2.0'   
def freespace():
         downloadlocation=dlocation
         try:  
            diskSpace = os.statvfs(downloadlocation)
            #tspace=os.stat('/')
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            #used = diskSpace.f_bsize * (diskSpace.f_blocks -diskSpace.f_bavail)
            
            fspace=round(float((available) / (1024.0*1024.0)),2)        
	    tspace=round(float((capacity) / (1024.0 * 1024.0)),1)
            #self.freespace=nspace
            spacestr='Free space(' +str(fspace)+'MB) Total space(' + str(tspace)+'MB)'
	    #self["info1"].setText('Free space available:' +str(fspace)+'MB Total space:' + str(tspace)+' MB')
            return spacestr
         except:
            return ' '   

def stopdownload():
    cmd1 = 'killall -9 rtmpdump'
    cmd2 = 'killall -9 wget'
    os.system(cmd1)
    os.system(cmd2)
    self.close()

def getsize(site):
        import urllib,os
        try:
                            if os.path.exists("/tmp/filesize"):
                               os.remove("/tmp/filesize")
                            site = urllib.urlopen(site)
                            meta = site.info()
                            size= meta.getheaders("Content-Length")[0]

                           
                            afile=open("/tmp/filesize","w")
                            afile.write(str(size))
                            afile.close()
                            return size
        except:
                            pass
def getdownloadrtmp(url, filename):
    try:
        parts = []
        url = url.strip()
        parts = url.split(' ')
        if len(parts) < 1:
            link = "'" + url + "'"
            commandstr = 'rtmpdump -r ' + link + ' -o ' + filename
            return commandstr
        link = "'" + parts[0] + "'"
        print link
        playpath = ''
        swfUrl = ''
        pageUrl = ''
        live = ''
        for item in parts:
            if 'playpath' in item:
                parts2 = item.split('=')
                playpath = " --playpath='" + parts2[1] + "'"
            if 'swfUrl' in item:
                parts2 = item.split('=')
                swfUrl = " --swfUrl='" + parts2[1] + "'"
            if 'live' in item:
                parts2 = item.split('=')
                live = " --live='" + parts2[1] + "'"
            if 'pageUrl' in item:
                parts2 = item.split('=')
                pageUrl = " --pageUrl='" + parts2[1] + "'"
            commandstr = 'rtmpdump -r ' + link + playpath + swfUrl + pageUrl + ' -o ' + filename

        return commandstr
    except:
        link = "'" + url + "'"
        print 'error'
        commandstr = 'rtmpdump -r ' + link + ' -o ' + filename
        return commandstr


class downloadJobrtmp(Job):

    def __init__(self, cmdline, filename, filetitle):
        Job.__init__(self, 'Download: %s' % filetitle)
        self.filename = filename
        self.retrycount = 0
        print '63', filename
        downloadTaskrtmp(self, cmdline, filename)

    def retry(self):
        self.retrycount += 1
        self.restart()

    def cancel(self):
        stopdownload()
        self.abort()


class downloadTaskrtmp(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)

    def __init__(self, job, cmdline, filename):
        Task.__init__(self, job, _('Downloading ...'))
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filename = filename
        self.error = None
        self.lasterrormsg = None
        self.end = 300
        return

    def processOutput(self, data):
        if os.path.exists(self.filename):
            filesize = os.path.getsize(self.filename)
            currd = round(float(filesize / 1048576.0), 2)
            totald = 600
            recvbytes = filesize
            totalbytes = 629145600
            self.progress = int(currd)
        try:
            if data.endswith('%)'):
                startpos = data.rfind('sec (') + 5
                if startpos and startpos != -1:
                    self.progress = int(float(data[startpos:-4]))
            elif data.find('%') != -1:
                tmpvalue = data[:data.find('%')]
                tmpvalue = tmpvalue[tmpvalue.rfind(' '):].strip()
                tmpvalue = tmpvalue[tmpvalue.rfind('(') + 1:].strip()
                print '105', tmpvalue
            else:
                Task.processOutput(self, data)
        except Exception as errormsg:
            print 'Error processOutput: ' + str(errormsg)
            Task.processOutput(self, data)

    def processOutputLine(self, line):
        line = line[:-1]
        self.lasterrormsg = line
        if line.startswith('ERROR:'):
            if line.find('RTMP_ReadPacket') != -1:
                self.error = self.ERROR_RTMP_ReadPacket
                print '126', self.error
            elif line.find('corrupt file!') != -1:
                self.error = self.ERROR_CORRUPT_FILE
                os_system('rm -f %s' % self.filename)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith('wget:'):
            if line.find('server returned error') != -1:
                self.error = self.ERROR_SERVER
        elif line.find('Segmentation fault') != -1:
            self.error = self.ERROR_SEGFAULT

    def afterRun(self):
       
        if self.getProgress() == 0 or self.getProgress() == 100:
            pass


class downloadTaskPostcondition(Condition):
    RECOVERABLE = True

    def check(self, task):
        return True
        if task.returncode == 0 or task.error is None:
            return True
        else:
            return False
            return

    def getErrorMessage(self, task):
        return {task.ERROR_CORRUPT_FILE: _('Video Download Failed!\n\nCorrupted Download File:\n%s' % task.lasterrormsg),
         task.ERROR_RTMP_ReadPacket: _('Video Download Failed!\n\nCould not read RTMP-Packet:\n%s' % task.lasterrormsg),
         task.ERROR_SEGFAULT: _('Video Download Failed!\n\nSegmentation fault:\n%s' % task.lasterrormsg),
         task.ERROR_SERVER: _('Video Download Failed!\n\nServer returned error:\n%s' % task.lasterrormsg),
         task.ERROR_UNKNOWN: _('Video Download Failed!\n\nUnknown Error:\n%s' % task.lasterrormsg)}[task.error]


class downloadJob(Job):

    def __init__(self, url, file, title):
        Job.__init__(self, title)
        downloadTask(self, url, file)


class downloadTask(Task):
    global total
    total = 0

    def __init__(self, job, url, file):
        Task.__init__(self, job, 'download task')
        self.end = 100
        self.url = url
        self.local = file

    def prepare(self):
        self.error = None
        return

    def run(self, callback):
        self.callback = callback
        getsize(self.url)
        self.download = downloadWithProgress(self.url, self.local)
        self.download.addProgress(self.http_progress)
        print "self.url, self.local",self.url, self.local
        self.download.start().addCallback(self.http_finished).addErrback(self.http_failed)

    def http_progress(self, recvbytes, totalbytes):
        currd = round(float(recvbytes / 1048576.0), 2)
        totald = round(float(totalbytes / 1048576.0), 1)
        info = _('%d of %d MB' % (currd, totald))
        total = totald
        self.progress = int(self.end * recvbytes / float(totalbytes))

    def http_finished(self, string = ''):
        print '[http_finished]' + str(string), self.local
        Task.processFinished(self, 0)
        
        
        try:
            filetitle = os_path.basename(self.local)
        except:
            filetile = ''
        if not '_update.zip'  in self.local:
           
           try:Notifications.AddNotification(MessageBox, _(filetitle+' successfully transfered to your HDD!'), MessageBox.TYPE_INFO, timeout=10)
           except:pass
        if '_plugin.' in self.local or '_update.zip' in self.local:
            self.deflatezip(self.local)
            return
       
        if self.local.endswith(".zip") and not "-et" in self.local and "-vu" not in self.local:
           self.deflatezip(self.local)

    def http_failed(self, failure_instance = None, error_message = ''):
        if error_message == '' and failure_instance is not None:
            error_message = failure_instance.getErrorMessage()
            print '[http_failed] ' + error_message
            Task.processFinished(self, 1)
            try:
                filetitle = os_path.basename(self.local)
            except:
                filetile = ''
        if  '_update.zip'  in self.local:
          return 
        try:Notifications.AddNotification(MessageBox, _('Failed to download '+filetitle), MessageBox.TYPE_INFO, timeout=10)
        except:pass
        return



    def deflatezip(self, filename):
        self.container = eConsoleAppContainer()
        if '_update.zip' in filename:
           self.destination="/"
        else:   
           self.destination = os.path.split(filename)[0]
        
        print "filenamets",filename
        fname=filename.replace('.zip', '')
        print "fnamets2",fname        
        cmd = "echo 'Configuring %s...' >> /tmp/ipkinstall.log" % fname
        cmd = cmd + '; unzip -o ' + filename + ' -d ' + self.destination + '  >> /tmp/filestall.log'

        if enigmaos=='oe2.0':
               self.container.appClosed.append(self.deflateOnClosed)
        else:    
              self.container_closed =self.container.appClosed.connect(self.deflateOnClosed)        
        
        self.container.execute(cmd)        
        
        info = 'Installing to root...'

    def deflateOnClosed(self, result):
        print 'result292', result
        try:
          if '_update.zip' in self.local:
              os.remove(self.local)
              return
          zipfilesize=  os.path.getsize(self.local)
          nfifilesize=os.path.getsize(self.local.replace(".zip",".nfi"))
          print 'zipfilesize,nfifilesize',zipfilesize,nfifilesize
         
          if nfifilesize==zipfilesize or nfifilesize > zipfilesize:
             os.remove(self.local)
             
        except:
           pass
           #Notifications.AddNotification(MessageBox, _('File successfully unzipeed to your HDD,you can flash your receiver now!'), MessageBox.TYPE_INFO, timeout=10)

    def afterRun(self):
        
        return
        if self.getProgress() == 0 or self.getProgress() == 100:
            Notifications.AddNotification(MessageBox, _(self.local+' successfully transfered to your HDD!'), MessageBox.TYPE_INFO, timeout=10)


PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings'

class downloadTasksScreen(Screen):
    skin='''               <screen name="downloadTasksScreen" position="center,center" size="1070,580" backgroundColor="#00060606" >	
	
			
			<widget name="title" position="60,50" size="600,50" zPosition="5" valign="center" halign="left" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			<widget source="tasklist" render="Listbox" position="60,120" size="1010,370" zPosition="7" scrollbarMode="showOnDemand" transparent="1" >
				<convert type="TemplatedMultiContent">
					{"template": [
							MultiContentEntryText(pos = (0, 1), size = (400, 24), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 1 is the name
							MultiContentEntryText(pos = (410, 1), size = (200, 24), font=1, flags = RT_HALIGN_RIGHT, text = 2), # index 2 is the state
							MultiContentEntryProgress(pos = (620, 1), size = (200, 24), percent = -3), # index 3 should be progress
							MultiContentEntryText(pos = (830, 1), size = (300, 24), font=1, flags = RT_HALIGN_LEFT, text = 4), # index 4 is the percentage
						],
					"fonts": [gFont("Regular", 22),gFont("Regular", 18)],
					"itemHeight": 25
					}
				</convert>
			</widget>
			
		<ePixmap position="79,521" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/red.png"  zPosition="3" transparent="1" alphatest="blend" />	
		<ePixmap position="283,521" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/green.png"    zPosition="3" transparent="1" alphatest="blend" />                
		<ePixmap position="483,521" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/blue.png"    zPosition="3" transparent="1" alphatest="blend" /> 
                <eLabel position="86,523" zPosition="4" size="200,24" halign="center" font="Regular;22" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Stop" />
		<eLabel position="295,523" zPosition="4" size="200,24" halign="center" font="Regular;22" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text=" " />
                <eLabel position="504,523" zPosition="4" size="200,24" halign="center" font="Regular;22" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Local images" />
        	<ePixmap position="75,514" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		<ePixmap position="279,514" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		<ePixmap position="484,514" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/AliSatSettings/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                      
                </screen>'''
    def __init__(self, session, plugin_path, tasklist, filename = None):
        Screen.__init__(self, session)
        
        self.session = session
        self.tasklist = tasklist
        self.filename = filename


        
        self['tasklist'] = List(self.tasklist)
        self['shortcuts'] = ActionMap(['ColorActions',
         'ShortcutActions',
         'WizardActions',
         'MediaPlayerActions'], {'blue': self.showfiles,
         'ok': self.keyOK,         
         'back': self.keyCancel,
         'red': self.keyOK}, -1)
        self['title'] = Label()
        self.onLayoutFinish.append(self.layoutFinished)
        self.onShown.append(self.setWindowTitle)
        self.onClose.append(self.__onClose)
        self.Timer = eTimer()
        
        if enigmaos=='oe2.0':
               self.Timer.callback.append(self.TimerFire)
        else:    
               self.timer_connect=self.Timer.timeout.connect(self.TimerFire)

    def play(self):
        try:
            current = self['tasklist'].getCurrent()
        except:
            return

        if current is None:
            return
        else:
            print "current",current
            print current[1]
            try:
                title = str(current[1])
            except:
                return

            dlocation = config.plugins.tstube.downloadlocation.value + '/'
            filename = str(dlocation + title)
            print "filenamexx",filename
            sref = eServiceReference(4097, 0, filename)
            sref.setName(title)
            if sref is not None:
                from TSMplayer4 import TSMplayer4
                try:
                    player = config.TSmedia.mediaplayer.value
                except:
                    player = 'TSMplayer'

                if player == 'TSMplayer':
                    self.session.open(TSMplayer4, sref=sref, addon_params={}, plugin_id='plugin.program.filesexplorer', playlist=[], playindex=0, playall=False, noexit=True, referer='filesexplorer', serviceName=title, audio=False, mode='appversion4')
                else:
                    from Screens.InfoBar import MoviePlayer
                    self.session.open(MoviePlayer, sref)
            return
            return

    def showfiles(self):
                from Plugins.Extensions.AliSatSettings.main import AliSatSettingsFilesScreen
                self.session.open(AliSatSettingsFilesScreen)

    def __onClose(self):
        del self.Timer

    def layoutFinished(self):
        try:size=freespace()
        except:size=''
        sizestr=dlocation+" "+size
        print "sizestr",sizestr
        self['title'].setText(_(sizestr))
        self.Timer.startLongTimer(2)

    def TimerFire(self):
        self.Timer.stop()
        self.rebuildTaskList()

    def rebuildTaskList(self):
        size=''

            
        try:
            txt=open("/tmp/filesize").read()
            size=str(int(txt)/(1024*1024))+"MB"
           
        except:
            size=" "
        
        self.tasklist = []
        
        for job in job_manager.getPendingJobs():
            
            status=job.getStatustext()
            try:fsize=freespace()
            except:fsize=''
            sizestr=dlocation+" "+fsize
            self['title'].setText(_(sizestr))
            
            if 'progress' in status.lower():
               
                
                try:
                    filesize=os.path.getsize(dlocation+job.name)
                    filesize=str(int(filesize)/(1024*1024))+"MB"
                except:
                    filesize=''
                size=filesize+"/"+size    
                self.tasklist.append((job,
                 job.name,
                 status,
                 int(100 * job.progress / float(job.end)),
                 str(100 * job.progress / float(job.end)) + '%'+" "+size))
            else :
                self.tasklist.append((job,
                 job.name,
                 status,
                 int(100 * job.progress / float(job.end)),
                 str(100 * job.progress / float(job.end)) + '%'))
        self['tasklist'].setList(self.tasklist)
        self['tasklist'].updateList(self.tasklist)
        self.Timer.startLongTimer(2)

    def setWindowTitle(self):
        self.setTitle(_('Current downloads'))

    def keyOK(self):
        current = self['tasklist'].getCurrent()
        print current
        if current:
            job = current[0]
            self.job = job
            from TaskView2 import JobViewNew
            self.session.openWithCallback(self.JobViewCB, JobViewNew, job)

    def JobViewCB(self, why):
        print 'WHY---', why

    def keyCancel(self):
        self.close()

    def keySave(self):
        self.close()


def viewdownloads(session, plugin_path = None):
    tasklist = []
    size=''
    try:
        txt=open("/tmp/filesize").read()
        size=str(int(txt)/(1024*1024))+"MB"
       
    except:
        size=" "

        
    for job in job_manager.getPendingJobs():        
        status=job.getStatustext()

        
        if 'progress' in status.lower():
          
             try:
                filesize=os.path.getsize(dlocation+job.name)
                filesize=str(int(filesize)/(1024*1024))+"MB"
             except:
                filesize=''
             size=filesize+"/"+size  
            
             tasklist.append((job,
             job.name,
             status,
             int(100 * job.progress / float(job.end)),
             str(100 * job.progress / float(job.end)) + '%'+" "+size))
        else :
             tasklist.append((job,
             job.name,
             status,
             int(100 * job.progress / float(job.end)),
             str(100 * job.progress / float(job.end)) + '%'))
    session.open(downloadTasksScreen, plugin_path, tasklist)


def startdownload(session, answer = 'download', myurl = None, filename = None, title = None, plugin_path = None, show = True):
    url = myurl
    print '365', url, filename
    if answer == 'download':
        fname = filename
        svfile = filename
        svf = svfile
        try:
            if title is None:
                title = os.path.split(svfile)[1]
        except:
            pass

        if 'rtmp' not in url:
            urtmp = "wget -O '" + svfile + "' -c '" + url + "'"
            job_manager.AddJob(downloadJob(url, svfile, title))
        else:
            params = url
            print 'params A=', params
            svfile = svfile.replace(' ', '').strip()
            params = params.replace(' swfVfy=', ' --swfVfy ')
            params = params.replace(' playpath=', ' --playpath ')
            params = params.replace(' app=', ' --app ')
            params = params.replace(' pageUrl=', ' --pageUrl ')
            params = params.replace(' tcUrl=', ' --tcUrl ')
            params = params.replace(' swfUrl=', ' --swfUrl ')
            print 'params B=', params
            cmd = 'rtmpdump -r ' + params + " -o '" + svfile + "'"
            print '384cmd', cmd
            job_manager.AddJob(downloadJobrtmp(cmd, svfile, title))
        if show == True:
                tasklist = []
                size=''
                try:
                    txt=open("/tmp/filesize").read()
                    size=str(int(txt)/(1024*1024))+"MB"
                   
                except:
                    size=" "

                    
                for job in job_manager.getPendingJobs():

                    
                    status=job.getStatustext()
                    if 'progress' in status.lower():
                         try:
                            filesize=os.path.getsize(dlocation+job.name)
                            filesize=str(int(filesize)/(1024*1024))+"MB"
                         except:
                            filesize=''
                         size=filesize+"/"+size                          
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'+" "+size))
                    else :
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'))
                session.open(downloadTasksScreen, plugin_path, tasklist)

    elif answer == 'view':
                tasklist = []
                size=''
                try:
                    txt=open("/tmp/filesize").read()
                    size=str(int(txt)/(1024*1024))+"MB"
                   
                except:
                    size=" "

                    
                for job in job_manager.getPendingJobs():                     
                    status=job.getStatustext()
                    if 'progress' in status.lower():
                         try:
                            filesize=os.path.getsize(dlocation+job.name)
                            filesize=str(int(filesize)/(1024*1024))+"MB"
                         except:
                            filesize=''
                         size=filesize+"/"+size  
                        
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'+" "+size))
                    else :
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'))
                session.open(downloadTasksScreen, plugin_path, tasklist)
                return True



