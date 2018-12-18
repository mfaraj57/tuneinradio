
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'

import os
import sys
import shutil

from twisted.web.client import downloadPage, getPage, error

from os import listdir as os_listdir
from Screens.Standby import TryQuitMainloop
#from twisted.web.client import downloadPage, getPage, error
from twisted.web import client
import re, urllib2, urllib, cookielib, socket
from urllib2 import Request, URLError, urlopen as urlopen2, build_opener, HTTPCookieProcessor, HTTPHandler, quote, unquote
from urllib import quote, unquote_plus, unquote, urlencode
from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
import httplib
from urlparse import urlparse, parse_qs
from xml.dom.minidom import parse
import StringIO
from random import randint
from xml.dom import Node, minidom
from Plugins.Plugin import PluginDescriptor
from enigma import getPrevAsciiCode,eDVBDB, gPixmapPtr, eConsoleAppContainer, eSize, ePoint, eTimer, addFont, loadPNG, quitMainloop, eListbox, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, eListboxPythonMultiContent, gFont, getDesktop, ePicLoad, eServiceCenter, iServiceInformation, eServiceReference, iSeekableService, iPlayableService, iPlayableServicePtr, eDVBDB
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from Screens.InfoBarGenerics import *
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Button import Button
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.AVSwitch import AVSwitch
from Components.ScrollLabel import ScrollLabel
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, pathExists, SCOPE_MEDIA, copyfile, fileExists, createDir,  SCOPE_PLUGINS, SCOPE_CURRENT_SKIN

import sys



from GlobalActions import globalActionMap

from Screens.InfoBarGenerics import InfoBarPlugins

InfoBar_instance = None
dwidth = getDesktop(0).size().width()
size_w = getDesktop(0).size().width()
size_h = getDesktop(0).size().height()
def getScale():
    return AVSwitch().getFramebufferScale()


from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
from Components.config import config, ConfigInteger, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from .lib.pltools import getversioninfo,log
currversion,enigmaos,currpackage,currbuild= getversioninfo("TuneinRadio")
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
       



T_INDEX = 0
T_FRAME_POS = 1
T_PAGE = 2
T_NAME = 3
T_FULL = 4


def startspinner():
                from Spinner import Spinner
                cursel = PLUGIN_PATH+"/skin/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                return Spinner(Bilder)             
def buildBilder():
                cursel = PLUGIN_PATH+"/skin/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                
                return Bilder
class MainScreen(Screen):                                                        
    
    def __init__(self, session,info={},action_params=None,source_data=[],nextrun=1,screens=[]):  
        self.action_params=action_params
        self.session = session
               
        self.param_title= info['name']
        self.action_params=action_params
        self.addon_id=info['addon_id']
       
        
        self.screens=screens
        self.screens.append(self)       
        self.info=info        
        self.transparent = True
        fanart_file=PLUGIN_PATH+"/skin/images/infopanel.png"
        self.searchtxt=None
        if os.path.exists(fanart_file):
           self.fanart=True
        else:
           self.fanart=False 
        
        textsize=20
        
        self.textcolor='#76addc'   
        fonttype='Regular'
        self.spinner_running=False
        
        self.color = '#080000'
       
        if dwidth == 1280:
            size_w = 1000
            size_h = 702
            textsize = 20
            self.spaceX = 100#130#35
            self.picX = 220#200#180
            self.spaceY = 20#50
            self.picY = 170
        elif dwidth == 1920:
            size_w = 1500
            size_h = 1050
            textsize = 45
            self.spaceX = 150#130#35
            self.picX = 330#200#180
            self.spaceY = 30#50
            self.picY = 255
        else:
            #textsize = 20
            self.spaceX = 75#30
            self.picX = 205#185
            self.spaceY = 40
            self.picY = 156
        self.thumbsX = 3
        self.thumbsY = 3
        self.thumbsC = self.thumbsX * self.thumbsY
        
        skincontent = ''
        posX = -1
        self.positionlist=[]
        if dwidth == 1920:
           if enigmaos=='oe2.0':
                  for x in range(self.thumbsC):
                      posY = x / self.thumbsX
                      posX += 1
                      if posX >= self.thumbsX:
                          posX = 0
                      absX = self.spaceX + posX * (self.spaceX + self.picX)
                      absY = 55 + posY * (30 + self.picY)
                      self.positionlist.append((absX, absY))##-125 -20
                      skincontent += '<widget source="label' + str(x) + '" render="Label" position="' + str(absX - 70) + ',' + str(absY + self.picY - 20) + '" size="' + str(self.picX + 120) + ',' + str(2*textsize) + '" font="Regular;30" zPosition="10" transparent="1"  halign="' + 'center' + '"  valign="' + 'center' + '"  foregroundColor="' + self.textcolor + '" />'
                      skincontent += '<widget name="thumb' + str(x) + '" position="' + str(absX + 7) + ',' + str(absY + 15) + '" size="' + str(self.picX - 45) + ',' + str(self.picY - 30) + '" zPosition="10"  alphatest="on" />'
                  skincontent +='<widget name="handlung" position="1536,680" size="330,513" backgroundColor="#080000" transparent="1" font="Regular;30" valign="top" halign="center" zPosition="1" />'
                  skincontent +='<widget name="info" position="1553,450" zPosition="4" size="330,225" font="Regular;30" foregroundColor="yellow" transparent="1" halign="left" valign="top" />'
                            
                  skincontent +='''
                      <ePixmap position="1530,625" size="410,42" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hsyoutubefhd.png"    alphatest="blend" />
                        
                      <ePixmap position="20,1050" size="1920,33" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutubefhd.png"    alphatest="blend" />
                      
                      <ePixmap position="20,20" size="1920,33" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutubefhd.png"    alphatest="blend" />
                                      
                      <ePixmap position="1900,20" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" />
                      <ePixmap position="20,20" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" /> 
                      <ePixmap position="1500,20" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" /> 
                      
                      
                       <ePixmap position="1545,77" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                      <ePixmap position="1545,172" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />                
                      <ePixmap position="1545,265" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                      <ePixmap position="1545,345" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                       
                      <ePixmap position="1557,97" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"    zPosition="3" transparent="1" alphatest="blend" />
                      <ePixmap position="1557,177" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"  zPosition="3" transparent="1" alphatest="blend" />	
                      <ePixmap position="1557,270" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"    zPosition="3" transparent="1" alphatest="blend" />
                      <ePixmap position="1557,350" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/blue.png"  zPosition="3" transparent="1" alphatest="blend" />                
                       
                      <ePixmap position="1600,980" size="65,65" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/TuneinRadio.png"  zPosition="3" transparent="1" alphatest="blend" />                
                       

                      <eLabel position="1500,97" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Menu" />
                      
                      <widget name="Key_green" position="1500,190" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="Key_yellow" position="1500,283" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="Key_blue" position="1500,363" zPosition="4" size="290,36"  halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="page" position="30,1010" zPosition="4" size="960,90" font="Regular;30" foregroundColor="yellow" transparent="1" halign="center" valign="top" />

                      '''
                      
                                  
         
         
              
                  
                     
                 
                  self.skin = '<screen position="center,center"    size="' + str(1920) + ',' + str(1070) + '" > \t\t\t<eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.color + '" /><widget name="frame" position="30,30" size="300,300" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/pic_frame2fhd.png" zPosition="10" alphatest="on" />' + skincontent + '</screen>'
                 
                 
           else:#enigmaos2.2
                  for x in range(self.thumbsC):
                      posY = x / self.thumbsX
                      posX += 1
                      if posX >= self.thumbsX:
                          posX = 0
                      absX = self.spaceX + posX * (self.spaceX + self.picX)
                      absY = 55 + posY * (30 + self.picY)
                      self.positionlist.append((absX, absY))##-90 -15
                      skincontent += '<widget source="label' + str(x) + '" render="Label" position="' + str(absX - 80) + ',' + str(absY + self.picY - 25) + '" size="' + str(self.picX + 120) + ',' + str(2*textsize) + '" font="Regular;30" zPosition="10" transparent="1"  halign="' + 'center' + '"  valign="' + 'center' + '"  foregroundColor="' + self.textcolor + '" />'
                      skincontent += '<widget name="thumb' + str(x) + '" position="' + str(absX + 7) + ',' + str(absY + 15) + '" size="' + str(self.picX - 45) + ',' + str(self.picY - 30) + '" zPosition="10"  alphatest="on" />'
                  skincontent +='<widget name="handlung" position="1536,680" size="330,513" backgroundColor="#080000" transparent="1" font="Regular;30" valign="top" halign="center" zPosition="1" />'
                  skincontent +='<widget name="info" position="1553,410" zPosition="4" size="330,225" font="Regular;30" foregroundColor="yellow" transparent="1" halign="left" valign="top" />'
                           
                  skincontent +='''<ePixmap position="1530,535" size="410,42" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hsyoutubefhd.png"    alphatest="blend" />
                  
                <ePixmap position="0,1065" size="1920,33" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutubefhd.png"    alphatest="blend" />
                
                <ePixmap position="0,10" size="1920,33" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutubefhd.png"    alphatest="blend" />
                                
                <ePixmap position="1900,0" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" />
                <ePixmap position="0,33" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" /> 
                <ePixmap position="1500,0" size="33,1065" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutubefhd.png"    alphatest="blend" /> 
		


               <ePixmap position="1600,980" size="65,65" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/TuneinRadio.png"  zPosition="3" transparent="1" alphatest="blend" />                
                       

              
               <ePixmap position="1545,77" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
              <ePixmap position="1545,172" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />                
              <ePixmap position="1545,265" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
              <ePixmap position="1545,345" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="306,55" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
               
              <ePixmap position="1557,97" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"    zPosition="3" transparent="1" alphatest="blend" />
              <ePixmap position="1557,177" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"  zPosition="3" transparent="1" alphatest="blend" />	
              <ePixmap position="1557,270" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"    zPosition="3" transparent="1" alphatest="blend" />
              <ePixmap position="1557,350" size="37,37" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/blue.png"  zPosition="3" transparent="1" alphatest="blend" />                
               
                      

                      <eLabel position="1602,97" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Menu" />
                      
                      <widget name="Key_green" position="1602,190" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="Key_yellow" position="1602,283" zPosition="4" size="290,36" halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="Key_blue" position="1602,363" zPosition="4" size="290,36"  halign="center" font="Regular;27" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                      <widget name="page" position="30,1010" zPosition="4" size="960,90" font="Regular;30" foregroundColor="yellow" transparent="1" halign="center" valign="top" />
                      '''
                      
                                  
         
         
              
                  if self.lock == True:
                      self.close()
                     
                 
                  self.skin = '<screen position="center,center"    size="' + str(1920) + ',' + str(1070) + '" > \t\t\t<eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.color + '" /><widget name="frame" position="30,30" size="290,240" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/pic_frame2fhd.png" zPosition="10" alphatest="on" />' + skincontent + '</screen>'
                 
        else:
          if enigmaos=='oe2.0':
            for x in range(self.thumbsC):
                posY = x / self.thumbsX
                posX += 1
                if posX >= self.thumbsX:
                    posX = 0
                absX = self.spaceX + posX * (self.spaceX + self.picX)
                absY = 55 + posY * (30 + self.picY)
                self.positionlist.append((absX, absY))
                skincontent += '<widget source="label' + str(x) + '" render="Label" position="' + str(absX - 70) + ',' + str(absY + self.picY-5) + '" size="' + str(self.picX + 90) + ',' + str(2*textsize) + '" font="'+fonttype+';'+str(textsize)+'" zPosition="10" transparent="0"  halign="' + 'center' + '"  valign="' + 'center' + '"  foregroundColor="' + self.textcolor + '" />'
                skincontent += '<widget name="thumb' + str(x) + '" position="' + str(absX + 5) + ',' + str(absY + 10) + '" size="' + str(self.picX - 30) + ',' + str(self.picY - 20) + '" zPosition="10"  alphatest="on" />'
                skincontent +='<widget name="handlung" position="1024,380" size="220,278" backgroundColor="#080000" transparent="1" font="Regular;20" valign="top" halign="center" zPosition="1" />'
                skincontent +='<widget name="info" position="1035,275" zPosition="4" size="220,150" font="Regular;20" foregroundColor="yellow" transparent="1" halign="left" valign="top" />'
                
                skincontent +='<ePixmap pixmap='+'"'+fanart_file+'"'+' position="0,0" size="1000,702"/>'	
                
            skincontent +='''
                <ePixmap position="1020,340" size="238,28" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hsyoutube.png"    alphatest="blend" />
                  
                <ePixmap position="0,700" size="1280,22" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutube.png"    alphatest="blend" />
                
                <ePixmap position="0,0" size="1280,22" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutube.png"    alphatest="blend" />
                                
                <ePixmap position="1260,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" />
                <ePixmap position="0,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" /> 
                <ePixmap position="1000,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" /> 
		<ePixmap position="1030,53" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                <ePixmap position="1030,115" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />                
                <ePixmap position="1030,177" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		<ePixmap position="1030,230" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		 
		<ePixmap position="1038,56" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"    zPosition="3" transparent="1" alphatest="blend" />
		<ePixmap position="1038,118" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"  zPosition="3" transparent="1" alphatest="blend" />	
		<ePixmap position="1038,180" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"    zPosition="3" transparent="1" alphatest="blend" />
		<ePixmap position="1038,233" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/blue.png"  zPosition="3" transparent="1" alphatest="blend" />                
		 
		<ePixmap position="1080,640" size="65,65" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/spicons/TuneinRadio.png"  zPosition="3" transparent="1" alphatest="blend" />                
                       

                <eLabel position="1068,65" zPosition="4" size="140,24" halign="center" font="Regular;20" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Menu" />
		
		<widget name="Key_green" position="1068,127" zPosition="4" size="160,24" halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                <widget name="Key_yellow" position="1068,189" zPosition="4" size="160,24" halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
		<widget name="Key_blue" position="1068,242" zPosition="4" size="160,24"  halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />'
                <widget name="page" position="20,680" zPosition="4" size="440,60" font="Regular;20" foregroundColor="yellow" transparent="1" halign="center" valign="top" />
                '''
                
            
            
            if True:
               
                    self.skin = '<screen position="center,center"    size="' + str(1280) + ',' + str(720) + '" > \t\t\t<eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.color + '" /><widget name="frame" position="20,20" size="200,156" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/pic_frame2.png" zPosition="10" alphatest="on" />' + skincontent + '</screen>'
          else:#oe2.2


            for x in range(self.thumbsC):
                posY = x / self.thumbsX
                posX += 1
                if posX >= self.thumbsX:
                    posX = 0
                absX = self.spaceX + posX * (self.spaceX + self.picX)
                absY = 55 + posY * (30 + self.picY)
                self.positionlist.append((absX, absY))
                skincontent += '<widget source="label' + str(x) + '" render="Label" position="' + str(absX - 50) + ',' + str(absY + self.picY-5) + '" size="' + str(self.picX + 90) + ',' + str(2*textsize) + '" font="'+fonttype+';'+str(textsize)+'" zPosition="10" transparent="0"  halign="' + 'center' + '"  valign="' + 'center' + '"  foregroundColor="' + self.textcolor + '" />'
                skincontent += '<widget name="thumb' + str(x) + '" position="' + str(absX + 5) + ',' + str(absY + 10) + '" size="' + str(self.picX - 30) + ',' + str(self.picY - 20) + '" zPosition="10"  alphatest="on" />'
                skincontent +='<widget name="handlung" position="1024,380" size="220,278" backgroundColor="#080000" transparent="1" font="Regular;20" valign="top" halign="center" zPosition="1" />'
                skincontent +='<widget name="info" position="1035,275" zPosition="4" size="220,150" font="Regular;20" foregroundColor="yellow" transparent="1" halign="left" valign="top" />'
                
                skincontent +='<ePixmap pixmap='+'"'+fanart_file+'"'+' position="0,0" size="1000,702"/>'	
                
            skincontent +='''
                <ePixmap position="1020,340" size="238,28" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hsyoutube.png"    alphatest="blend" />
                  
                <ePixmap position="0,700" size="1280,22" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutube.png"    alphatest="blend" />
                
                <ePixmap position="0,0" size="1280,22" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/hyoutube.png"    alphatest="blend" />
                                
                <ePixmap position="1260,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" />
                <ePixmap position="0,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" /> 
                <ePixmap position="1000,0" size="22,714" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/vyoutube.png"    alphatest="blend" /> 
		<ePixmap position="1030,53" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
                <ePixmap position="1030,115" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />                
                <ePixmap position="1030,177" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		<ePixmap position="1030,230" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png" size="204,37" zPosition="2" backgroundColor="#ffffff" alphatest="blend" />
		 
		<ePixmap position="1038,56" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"    zPosition="3" transparent="1" alphatest="blend" />
		<ePixmap position="1038,118" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"  zPosition="3" transparent="1" alphatest="blend" />	
		<ePixmap position="1038,180" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"    zPosition="3" transparent="1" alphatest="blend" />
		<ePixmap position="1038,233" size="25,25" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/blue.png"  zPosition="3" transparent="1" alphatest="blend" />                
		 
                <ePixmap position="1080,640" size="65,65" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/sicons/TuneinRadio.png"  zPosition="3" transparent="1" alphatest="blend" />                
                		

                <eLabel position="1068,65" zPosition="4" size="140,24" halign="center" font="Regular;20" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000" text="Menu" />
		
		<widget name="Key_green" position="1068,127" zPosition="4" size="160,24" halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
                <widget name="Key_yellow" position="1068,189" zPosition="4" size="160,24" halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />
		<widget name="Key_blue" position="1068,242" zPosition="4" size="160,24"  halign="center" font="Regular;18" transparent="1" foregroundColor="#ffffff" backgroundColor="#41000000"  />'
                <widget name="page" position="20,680" zPosition="4" size="440,60" font="Regular;20" foregroundColor="yellow" transparent="1" halign="center" valign="top" />
                '''
                
          
           
            if True:
                
                    self.skin = '<screen position="center,center"    size="' + str(1280) + ',' + str(720) + '" > \t\t\t<eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.color + '" /><widget name="frame" position="20,20" size="200,156" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/pic_frame2.png" zPosition="10" alphatest="on" />' + skincontent + '</screen>'
          







            
            
          
        Screen.__init__(self, session)
        self.onShow.append(self.refresh)
        ##plugin stuff
        
        self.nextrun=nextrun
        self.page=nextrun
        self.currPage=0
        self.favmode=False
        self.source_data=source_data
        self.predata_source=[]
        self.favplaylist=[]
        self.playlist=[]
        self.close_back=None		
        self.piclist=[]
        self['handlung'] = Label(_("Please wait... "))
        self.startSpinner()
        self['page']=Label()
        self['info'] = Label(str(self.page))
        
        self.pages=[]
        
        if not os.path.exists("/tmp/TuneinRadio/"):
             os.makedirs("/tmp/TuneinRadio/")
        self["Key_green"]=Label(_("Search"))
        self["Key_blue"]=Label(_("Download"))
        self["Key_blue"].hide()
        self.data1=[]
        self.data1.append(('',[]))
        self.index=0 
            
                
         
        self.favmode=False
        
        if self.param_title=='Favorites'  and self.page==1:
           self.sender='favorites'
           self["Key_yellow"]=Label(_("Delete"))
           
           
           
           self.favmode=True
           
        else:
        
                        
            self["Key_yellow"]=Label(_("+Favorite"))
        
       


           
        self.data=''
        self.rundef=None
        self.keyLocked=False
        self.resultsperpage=45
       
        self.showdownload=True          
        self.download=False
        
        ##
        self['actions'] = ActionMap(['TuneinRadioActions','ColorActions','OkCancelActions',
         'DirectionActions',
         'MovieSelectionActions','MenuActions',"EPGSelectActions",'WizardActions','PiPSetupActions'], {"red":self.closeall,			
         "addfav":self.savetofavorites,
         "blue":self.export2bq,
         "green":self.search ,#self.addfavorite,
         "ok": self.ok_clicked,         
         'cancel': self.exit,
         'left': self.key_left,
         'right': self.key_right,
       
         'size+': self.previouspage,
         'size-': self.nextpage,               
         'up': self.key_up,
         'down': self.key_down}, -1)

        self['frame'] = MovingPixmap()
        for x in range(self.thumbsC):
            self['label' + str(x)] = StaticText()
            self['thumb' + str(x)] = Pixmap()
        self.maxentry=12
        self.preindex=0
        self.bqupdate=False
       	self.keyLocked = True
       	self.timer = eTimer()
       	self.timer3 = eTimer()
       	if self.action_params is not None and  "mode=103" in self.action_params:
            try:
                self.timer3_connect=self.timer3.timeout.connect(self.search_ch)
            except:
                self.timer3.callback.append(self.search_ch)
            self.timer3.start(10, 1)             
             
        else:    
           self.onLayoutFinish.append(self.loaddata)
        
    def search(self):
                      param='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/addons/TuneinRadio/default.py?url=%2Ftag%2F&mode=103&name=Search&page=0&extra=1'

                   
                      self.info['name']="Search"
                      self.session.openWithCallback(self.updateinfo,MainScreen,info=self.info,action_params=param,source_data=[],nextrun=self.nextrun+1,screens=self.screens)

        
    def refresh(self):
        #self.stopSpinner()
        self.keyLocked = False
        #self.download=False
    def startdownload(self):

        return
        self.download=True
        self.ok_clicked()
    def update_bqs(self):
        return

        
    def load_bqs(self):
       
        
        return

    def showgensettings(self):
        return
        from Plugins.Extensions.TuneinRadio.plugin import TuneinRadioSetup1
        self.session.open(TuneinRadioSetup1)    
    
        
    def showinformation(self):
            return
            self.allow=True
            from Plugins.Extensions.TuneinRadio.lib.TuneinRadioinfo import TuneinRadioinfoscreen
            self.session.open(TuneinRadioinfoscreen,self.addon_id)  
        
    def startSpinner(self):
        return
        print "self.spinner_running",self.spinner_running
        if self.spinner_running==False:
          Bilder=buildBilder()
          self["bild"].start(Bilder)
          self.spinner_running=True
          return    
    def stopSpinner(self):
       return
       try:
         if self.spinner_running==True:
          self["bild"].stop()
          self.spinner_running=False                   
          self['bild'].instance.setPixmap(gPixmapPtr())     
          
          
          
   
         return 
       except:
         return             

    #self['bild']=None            
    def progress_callback(self,result):
          try:
            if result:
              if result.startswith("Error"):
               
                 self.keyLocked=False
                 self.stopSpinner()
                 self['handlung'].setText(_(str(result)))  
                 pass
              if result.startswith("Complete"):
                 self.keyLocked=False
                 self.stopSpinner()
                 self.updateinfo()
          except:
              
              pass   
           
    def exitpages(self):
       if self.spinner_running==True:
              self.stopSpinner()
              
           
       else:
           self.stopSpinner() 
         
       self.close()   
    def loaddata(self):
        try:self.timer.stop()
        except:pass

        
        self['handlung'].setText(_("Please wait.. "))
               
        try:
            self.timer_connect=self.timer.timeout.connect(self.startloaddata)
        except:
            self.timer.callback.append(self.startloaddata)
        self.timer.start(10, 1) 
    def datalist(self):
       
        self.data=[]
        
        if self.param_title.lower()=='favorites':

                from Plugins.Extensions.TuneinRadio.lib.tsfavorites import readfav
                self.data = readfav(mode='GFavorites', addon_id='radio/TuneinRadio', section='radio')
            
                
        
                self["Key_yellow"].setText(_("Remove"))
                self["Key_blue"].setText("Download")
                self.bouquet=True
                self.favmode=True
          
                 
        else:

            if len(self.source_data)<1 and not self.param_title=='Favorites' :
                                 #self['handlung'].setText('please wait..')
                                 pass
                                 self.lock=True
                                 self['handlung'].setText(_('Please wait..')) 
                                 
                                 
                                 
                                
                                 from Plugins.Extensions.TuneinRadio.addons.radio.TuneinRadio.default import process_mode
                                
                                 #log("self.action_params",self.action_params)
                                 self.source_data =process_mode([],self.action_params,searchtxt=self.searchtxt)


            print 'self.source_data',self.source_data 
            self.data=self.source_data#process_request(self.action_params)
            self["Key_yellow"].setText(_(" + Favorite"))
                                     
        try:self.totalresults=len(self.data)         
        except:self.totalresults=0         
        if self.data is None or len(self.data)<1 :
           if self.data is None:
              self.data=[]
           if self.favmode==False:
               
              self.data.append(("Error:no result founds",'',1,PLUGIN_PATH+'/skin/images/error.png','','',9,'',1))
           else:
             self['handlung'].setText(_('Favorites is empty'))   
	   self.totalresults=1 
        if len(self.data)==1 and (self.data[0][0].startswith("Error") or self.data[0][0].startswith("Message")):
           name=self.data[0][0]
           
           param_url=""
           self.data=[]
           self.data.append((name,param_url,1,PLUGIN_PATH+'/skin/images/error.png','','',9,param_url,1)) 
           self.totalresults=1 
        
            
        
        if self.totalresults>0:       
           self["info"].setText('page   :'+str(self.page)+"/"+str(self.currPage+1)+'\nresults:'+str(self.totalresults))
        else:
           self["info"].setText('page   :'+str(self.page)+"/"+str(self.currPage+1)+'\nresults:'+str(self.totalresults))
           
        self.keyLocked=False
        
        try:self.resultsperpage=self.data[0][8]
	except:self.resultsperpage=45
        self.positionlist = []
        
        posX = -1
        lastindex = 0
        self.Thumbnaillist = []
        self.filelist = []
        self.currPage = -1
        self.dirlistcount = 0
        
        index = 0
        framePos = 0
        Page = 0
        i = 1
        path="/tmp/"
        print "self.dataxx",self.data
        for x in self.data:
            
            if i > 45:
                break
            if x:
               try:
                self.filelist.append((index,
                 framePos,
                 Page,
                 x[0],
                 x[2]))
                index += 1
                framePos += 1
                if framePos > self.thumbsC - 1:
                    framePos = 0
                    Page += 1
                    
               except:
                  continue     
                    
            else:
                self.dirlistcount += 1

                       
        
        self.maxentry = len(self.filelist) - 1

        self.index =0# lastindex - self.dirlistcount
        
        
        
    def startloaddata(self):
        self.datalist()

                  
        self.setPicloadConf()
    def setPicloadConf(self):
        sc = getScale()
        self.picload = ePicLoad() 
        self.picload.setPara([self['thumb0'].instance.size().width(),
         self['thumb0'].instance.size().height(),
         sc[0],
         sc[1],
         True,
         1,
         self.color])
        self.initFrame()
        self.paintFrame()

    def initFrame(self):
        self.positionlist = []
        for x in range(self.thumbsC):
            frame_pos = self['thumb' + str(x)].getPosition()
            self.positionlist.append((frame_pos[0] - 5, frame_pos[1] - 5))

        frame_pos = self['thumb0'].getPosition()
        self['frame'].setPosition(frame_pos[0] - 5, frame_pos[1] - 5)

    def paintFrame(self):
        if self.maxentry < self.index or self.index < 0:
            return
        pos = self.positionlist[self.filelist[self.index][T_FRAME_POS]]
        self['frame'].moveTo(pos[0], pos[1], 1)
        self['frame'].startMoving()
        if self.currPage != self.filelist[self.index][T_PAGE]:
            self.currPage = self.filelist[self.index][T_PAGE]
            
            self.newPage()
      
        self.updateinfo()
    def newPage(self):
        #try:
            
            self.Thumbnaillist = []
            for x in range(self.thumbsC):
                self['label' + str(x)].setText('')
                self['thumb' + str(x)].hide()
            self["info"].setText('page   :'+str(self.page)+"/"+str(self.currPage+1)+'\nresults:'+str(self.totalresults))
           
            for x in self.filelist:
                
                if x[T_PAGE] == self.currPage:
                    try:title=x[T_NAME][:60]
                    except:title=x[T_NAME]
                    self['label' + str(x[T_FRAME_POS])].setText(str(title))
                    self.Thumbnaillist.append([0, x[T_FRAME_POS], x[T_FULL]])
                    
                    
                    webpic= str(x[T_FULL])
                    index=x[T_FRAME_POS]
                  
                    try:webpic=webpic.replace("ExQ","=")
                    except:pass
                    defpic='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/micons/TuneinRadio.png'
                    download=False
                    pic=defpic
                    localpic="/tmp/TuneinRadio/pics/pic.png"
                    if webpic is None or webpic=='':
                        print "xxxlog webpic is not validstr(webpic)",str(webpic)
                        download=False
                        localpic=defpic
                    if webpic is not None and  webpic.startswith("/usr") and os.path.exists(webpic):
                         localpic=webpic
                         download=False
                         print "xxxlog webpic starts with/usr"+webpic
                    
                    
                    if webpic is not None and not  webpic.strip()=='' and  not webpic.startswith("/usr") and   webpic.startswith("http") :
                        webpic_base=os.path.basename(webpic)
                        localpic="/tmp/TuneinRadio/pics/"+webpic_base
                        if os.path.exists(localpic):  
                           
                           download=False
                        else:
                            
                            download=True
                        print "xxxlog webpic starts httpwebpic ,str(download) ",webpic ,str(download) ,localpic   
                    if title.startswith('Error') or title.startswith('Message:'):
                          localpic='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/micons/error.png'
                          download=False
                          print "xxxlog webpic starts errorwebpic ,str(download)",webpic ,str(download)
                    if download==True:
                       print "xxxlog download truewebpic ,localfile",webpic 
                       self.downloadimage(localpic,webpic,index) 
                    else:    
                       self.downloadback(True,x[T_FRAME_POS],localpic)     
    def downloadimage(self,localfile,webfile,index):
        
           print "webfile,localfile",webfile,localfile
      
           client.downloadPage(str(webfile),localfile).addCallback(self.downloadback,index,localfile).addErrback(self.downloaderror,index)
				
    def downloadback(self,data,index,localfile):
        
        picobject= self['thumb' + str(self.Thumbnaillist[index][1])]
        
        self.showPic(picobject,localfile)
    def downloaderror(self,data,index):
                       
                       localfile='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/micons/TuneinRadio.png'
                       self.downloadback(True,index,localfile)
    def showPic(self,pic_object=None,localfile=None):
    

	         
                     print "localfile",localfile,pic_object
                     self.piclist.append(localfile)
                     if os.path.exists(str(localfile))==False:
                        localfile='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/micons/TuneinRadio.png' 
		     try:   
			pic_object.instance.setPixmap(gPixmapPtr())
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = pic_object.instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if enigmaos=='oe2.2':
                            value=self.picload.startDecode(str(localfile),  False)
			else:
                            value=self.picload.startDecode(str(localfile), 0, 0, False)
			if value == 0:
				ptr = self.picload.getData()
				
				if ptr != None:
					pic_object.instance.setPixmap(ptr)
					pic_object.show()
					del self.picload

		     except:
                         pass
                 
    
    def updateinfo(self):

       
       title=''           
       param=''
       action=0
     
       self.keyLocked = False
       self['handlung'].setText( " " )
       try:title=str(self.data[self.index][0])
       except:pass           
       try:param=str(self.data[self.index][1]).strip()
       except:pass
       if param is not None and  param.startswith("http"):
             self.bouquet=True
             self['Key_blue'].setText("+Bouquet")
             self['Key_blue'].show()
                           
       else:
           
             self.bouquet=False
             self['Key_blue'].hide()       
      
       if self.data is None or len(self.data)<1 :
          self['handlung'].setText(_("No items available "))
          
          return
       
       if len(self.data)==0 and self.data[0][0].startswith('Error') :
          self['handlung'].setText(_("Error :check details by info button"))
          
          return
       elif len(self.data)==0 and self.data[0][0].startswith('Message:'):    
            self['handlung'].setText(_(str(self.data[0][0])))
            return
       if self.bqupdate==True:
          title="Bouquets updated successfully"
          
          self['handlung'].setText(_(str(title)))
          self.closeall()
          return
       try:title=title.encode('utf-8', 'ignore')
       except:pass        
       self['handlung'].setText(_(str(title)))
      
       
    def previouspage(self):
        self.bqupdate=False 
        if self.keyLocked==True :
           return
        try:   
           self.preindex=self.index
           self.index -= 9 
           
           if self.index <0:
                   
                   self.index=0
                   self.exit()
                   
                        
              
           
        except:
          self.index=self.preindex-1 
          if self.index <0:
                   
                   self.index=0
                   self.exit()            
        self.paintFrame()   
    def nextpage(self):      
       self.bqupdate=False  
       try: 
        if self.keyLocked==True :
           return
        self.preindex=self.index
        self.index += 9   
        if self.index > self.maxentry:
                   

                   self.index =self.preindex
                   param_url=str(self.data[self.index][7])
                   self.action_params=param_url

                   
                   
                                    
                   self.newscreen(self.action_params) 
                   return
        
                              
               
       except:
          self.index = self.maxentry
       self.paintFrame()      
    def key_left(self):
        self.bqupdate=False 
        if self.keyLocked==True :
           return
        
        self.index -= 1
                
        if self.index < 0 :
              self.index=self.maxentry
              
        self.paintFrame()
        
    def key_right(self):
        self.bqupdate=False 
        if self.keyLocked==True :
           return
        self.preindex=self.index
        self.index += 1
        if self.index > self.maxentry and len(self.data)==45 :
                   

                   self.index =self.preindex
                   param_url=str(self.data[self.index][7])
                   self.action_params=param_url

                   
                   
                                    
                   self.newscreen(self.action_params) 
                   return
                  
                       
        else:
        
          if self.index > self.maxentry:
              self.index = 0
        print "selfindex',maxentery", self.index , self.maxentry      
        self.paintFrame()
       
    def key_up(self):
        self.bqupdate=False 
        if self.keyLocked==True:
           return
        
        self.index -= self.thumbsX
        
        if self.index < 0  :

                   self.index=self.maxentry
                       
        else:
        
          pass  
        
        
        self.paintFrame()
       
    def key_down(self):
        self.bqupdate=False
        if self.keyLocked==True :
           return
        self.preindex=self.index
        self.index += self.thumbsX
        if self.index > self.maxentry and len(self.data)==45:
                   
                   self.index = self.preindex
                   
                  
                  
                      
                   param_url=str(self.data[self.index][7])
                   self.action_params=param_url
                   
                   
                   
                                     
                                   
                   
                                      
                   #self.loaddata()
                   self.newscreen(self.action_params) 
                   
                   return
                       
        else:
        
          if self.index > self.maxentry:
              self.index = 0
        self.paintFrame()
       
        
       
    
    def exit(self):


          i=0
          for screen in self.screens:
              
              if screen==self:
                 del self.screens[i]
                 break
              i=i+1

          try:
              os.remove("/tmp/TuneinRadio/pics/")
          except:
              pass
          self.close()








        


        
    def delfav(self):
        try:
            title = self.data[self.index][0]
            url = self.data[self.index][1]
        except:
            self['handlung'].setText(_('Failed to delete from favorites-1'))
            return

        from Plugins.Extensions.TuneinRadio.lib.tsfavorites import delfavorite
        result = delfavorite(title, url)
        if result == True:
            from Plugins.Extensions.TuneinRadio.lib.tsfavorites import readfav
            self.source_data = readfav(mode='GFavorites', addon_id='radio/TuneinRadio', section='radio')
            self.index = self.index - 1
            self.loaddata()
            
            self['handlung'].setText(_('Item deleted successfully from favorites'))
        else:
            self['handlung'].setText(_('Failed to delete from favorites'))


    def savetofavorites(self):
        if self.keyLocked == True:
            return
        
        self.bqupdate=False 
        if self.favmode:
            self.delfav()
            return
        from Plugins.Extensions.TuneinRadio.lib.tsfavorites import addfavorite
        import sys
        result = False
        if True:
            param = str(self.data[self.index][1])
            title = str(self.data[self.index][0])
            try:
                picture = str(self.data[self.index][2])
            except:
                picture = PLUGIN_PATH + '/addons/radio/TuneinRadio/icon.png'

            url = param
            title = title
            pic = picture
            success, error = addfavorite("TuneinRadio", title, param, picture, 'radio')
            if success == True:
                self['handlung'].setText(_('Item added successfully to favorites.'))
            elif success == False:
                self['handlung'].setText(_('Item is already in favorites'))
            else:
                self['handlung'].setText(_(error))


             
          
            
 
###########################################################end process paramaeters         
#######################    
  

    def ok_clicked(self):         
              try:itemindex=self.index
              except:return
            
              try:title=str(self.data[self.index][0])                
              except:return                   
               
               
              try:param=str(self.data[self.index][1])
              except:return
              
                                             
              
              
              self.keyLocked=False
             
              self.playlist=[]
   
              
            
                    
                                    
              self.playlist=self.createplaylist()
              
              self.preindex=self.index 
                               
               
              if title.strip().startswith("Error") or title.strip().startswith("Message"):
                    self.keyLocked=False
                    
                    self.exit()
                    return              
                            
              if True:
                 self.action_params=param
                
                 
                 
                 

                 self.newscreen(self.action_params)                                   
                 
             
                 

    def createplaylist(self):
      if True:
        playlist=[]
        self.favplaylist=[]

        i=0
        
        for item in self.data:
            print "itemmainxx",str(item[0]),str(item[1])
            try:title=str(item[0])
            except:continue
            try:param=str(item[1])
            except:continue
            try:
                        webpic=item[2]
                        webpic_base=os.path.basename(webpic)
                        image="/tmp/TuneinRadio/pics/"+webpic_base
                
            except:
                image='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/micons/TuneinRadio.png'
            
            self.favplaylist.append((title,param,str(image)))
            
            playlist.append((title,param,str(image)))
            i=i+1
        print "playlistmain",playlist 
        return playlist        
      else:
        return []    


  
  

    def export2bq(self):

         
          
          
        if self.bouquet==False:
         
            return
  
            
            
        try:
            channelname = str(self.data[self.index][0])
        except:
            self['handlung'].setText(_("Failed to export to bouquet[erro:601]"))
            return

        try:
           url = str(self.data[self.index][1])
        except:
           self['handlung'].setText("Failed to export to bouquet[erro:602]")
           return 
        if True:
            
            from Plugins.Extensions.TuneinRadio.lib.pltools import addstream   
            error = addstream(url, channelname, 'TuneinRadio')
            if error == 'none':
                self['handlung'].setText('Stream added to ' + 'radio TuneinRadio bouquet' )

                eDVBDB.getInstance().reloadServicelist()
                eDVBDB.getInstance().reloadBouquets()
                
            else:
                self['handlung'].setText(error)
        else:
            self['handlung'].setText('Failed to add to bouquets')
       





        
    def newscreen(self,params):
       try:self.timer.stop()
       except:pass    
       self['handlung'].setText(_("Please wait.. "))
       self.loadscreen()        

    def begindownload(self,name,param):
                       
                       from .lib.tsdownload import startdownload
                       startdownload(self.session, 'download', str(param), str(name)+".mp3", str(name), None, True)
        
        
    def loadscreen(self):
       try:title=str(self.data[self.index][0])
       except:title=self.group_title
       param=self.data[self.index][1]

       
       
       self.lock=True
       self.keyLocked=True
       
   
       
       self.preindex=self.index
       if 'mode=' in param:
          
          
          if 'mode=9' in param:
              self.close()
              return
          from .addons.radio.TuneinRadio.default import process_mode
          self.source_data=process_mode([],param)
       
          try:name=self.source_data[0][0]
          except: name=None
          try:param=self.source_data[0][1]
          except: param=None                                      
          if len(self.source_data)==1 and name is not None and not name.startswith("Error") and  param is not None and param.startswith("http"):

                      if self.download==True:
                          self.download=False
                          self.begindownload(name,param)
                          return

                      from .lib.TSplayer import TSRadioplayer

                      log("selfplaylistmain",self.playlist)
                      self.session.openWithCallback(self.updateindex,TSRadioplayer, serviceRef=None,serviceUrl=str(param),serviceName=name,serviceIcon='', playlist = self.playlist, playindex =self.index,process_item=self.process_item)    			
	              self['handlung'].setText(_(str(name)))
                      return                
          if name is not None and  name.startswith("Error"):
             self['handlung'].setText(_('Error:,check /tmp/TuneinRadio_log for more details 1'))
             self.lock=False
             self.keyLocked=False
             
             return
          elif name is not None  and name.startswith("Message"):
               try:name=name.encode('utf-8', 'ignore')
               except:pass
               self['handlung'].setText(_(str(name)))

               self.lock=False
               self.keyLocked=False               
               return
          elif name is None:
              self['handlung'].setText(_('Error:,no data,check /tmp/TuneinRadio_log for more details 1'))
              self.lock=False
              self.keyLocked=False               
              return
              
            
          player=False
          
          self.index=0
       else:
          self.source_data=self.data
          player=True

      
       print "xxx",self.index,len(self.source_data)
       if self.source_data is not None:
           if len(self.source_data)>0:
               name=self.source_data[self.index][0]
               
               
               param=self.source_data[self.index][1]
               
              
               if not 'Error:' in name and not 'Error:' in param and not "Message:" in param and not "Message:" in param:
                   
                  if param.startswith("http") and player==True:
                      
                      if self.download==True:
                          self.download=False
                          self.begindownload(name,param)
                          return                     
                                      
                     
                      from .lib.TSplayer import TSRadioplayer
                      self.session.openWithCallback(self.updateindex,TSRadioplayer, serviceRef=None,serviceUrl=str(param),serviceName=name,serviceIcon='', playlist = self.playlist, playindex =self.index,process_item=self.process_item)    			
                      try:name=name.encode('utf-8', 'ignore')
                      except:pass
	              self['handlung'].setText(_(str(name)))                   

                  
                  else:
                     
                      self.info['name']=name
                      self.session.openWithCallback(self.updateinfo,MainScreen,info=self.info,action_params=param,source_data=self.source_data,nextrun=self.nextrun+1,screens=self.screens)
               else:
                  if 'Message:' in param:
                     self['handlung'].setText(_( str(param)))
                  else:   
                     self['handlung'].setText(_('Error:,check /tmp/TuneinRadio_log for more details 1'))      
           else:
                  self['handlung'].setText(_('No data returned,check /tmp/TuneinRadio_log for more details 2'))
       else:
                  self['handlung'].setText(_('No data returned,check /tmp/TuneinRadio_log for more details 3'))
                  self.index=self.preindex 
    def process_item(self,param,playindex):
           
          from .addons.radio.TuneinRadio.default import process_mode
          data=process_mode([],param)
          print "dataffff",data
          try:url=data[0]
          except:url=' '
          try:title=data[0][0]
          except:title="tuneinradio"         
          return url,title
    def updateindex(self,playindex=0):
        if self.favmode==True :
            return
            
        elif not playindex==self.index:
             self.index=playindex
             self.paintFrame() 
    def updateinfo2(self):

        pass
                  
    def closeall(self):
          if self.spinner_running==True:
          
            self.stopSpinner()   
                     
          try:self.stopSpinner()
          except:pass
          for screen in self.screens:
                try:screen.close()
                except:continue
          self.screens=[]

####search stuff
    def search_ch(self):
      
                     try:self.timer3.stop()
                     except:pass
                     try:
                                 
                                       from Screens.VirtualKeyBoard import VirtualKeyBoard              
                            
                     except:
                            from Screens.VirtualKeyBoard import VirtualKeyBoard
                     import os
                     try:
                        txt=open("/etc/TuneinRadio/TuneinRadio_search.txt",'r').read()
                        #os.remove("/tmp/xbmc_search.txt") 
                     except:
       
                        txt=''
                          
                     self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Enter your search term(s)")), text = txt)           
           
                            
  
        
                                       
    def searchCallback(self,search_txt): 
        
                
        
          if search_txt:
             if True:
               search_txt=str(search_txt)
               file=open("/etc/TuneinRadio/TuneinRadio_search.txt",'w')
               file.write(search_txt)
               file.close()
                                 
               #self['handlung'].setText('please wait..')
               self['handlung'].setText(_('Please wait..'))
               
               self.searchtxt=search_txt
               self.loaddata()
               return
              
	     else:
               self['handlung'].setText(_("Error in searching for "+str(search_txt)))
	
          else:
            self['handlung'].setText(" ")

          
def removeFiles(folder_path):
   try:
      import os
      for file_object in os.listdir(folder_path):
          file_object_path = os.path.join(folder_path, file_object)
          if os.path.isfile(file_object_path):
              os.remove(file_object_path)
          
   except:
          pass
####search stuff
  

 
