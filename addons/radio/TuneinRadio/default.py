# -*- coding: utf8 -*-
#/*
# *
# * TuneIn Radio .
# *
# *Tunein api based on work of  2015 Brian Hornsby
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# */
import sys
import urllib, urllib2, re, os
module_path = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/addons/radio/TuneinRadio'
path = '/tmp/TuneinRadio'

################
import tunein
__partnerid__ = 'yvcOjvJP'
mac_address = None
__tunein__ = tunein.TuneIn('yvcOjvJP', 0, 'en-US', 'mp3,wma,wmpro,wmvideo,wmvoice', True, False)
############################################

####functions
from Plugins.Extensions.TuneinRadio.lib.pltools import log


def showmenu():
        
	addDir('Search',"/tag/",103,'img/search.png',1)
        addDir('Local','local',100,'img/local.png','',1)
       
         


			  
def search(url,searchtxt):
        
        
         
       
            
        
        
         
        
        
        searchtxt=searchtxt.replace(' ','+')    
        results = __tunein__.search(searchtxt, 'standard')
        stations=tunein.process_tunein_json(results)
        print "searchxx",searchtxt,stations        
        for station in stations:
                    addDir(station[0],station[1],station[2],station[3],station[4],station[5])    


                        
               
                  
                
        
def getlocalstations(namemain,urlmain,page):##movies
                print "page",page

                results = __tunein__.browse_local(
                username='', latlon='')
               
                stations=tunein.process_tunein_json(results)
                
                for station in stations:
                    addDir(station[0],station[1],station[2],station[3],station[4],station[5])    




                    
def getstreams(name,urlmain,page,image):##series

                 
        result = []
        
        result = __tunein__.tune(urlmain)
        if len(result) > 0:
            if len(result)== 1:
                print "stream",result[0]
                #playlink(result[0])
                #return
            print "result",result
            for stream in result:
                addDir(name,stream,10,image,'',1,link=True)
            
            
                                           
def get_params(action_param):
    param = []
    paramstring = action_param
    if paramstring is None or paramstring == '':
        paramstring = ''
    else:
        paramstring = '?' + action_param.split('?')[1]
    if len(paramstring) >= 2:
        params = paramstring
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]

    print 'input,output', paramstring, param
    return param



                    

	
list2 = []

def readnet(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
    except:
        return None

    return None
def addDir(name, url, mode, iconimage, desc = '', page = '',link=False):
    global list2
    image=iconimage
    try:name=name.encode("utf-8","ignore")
    except:pass
    if not page == '':
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page=' + str(page)+ '&image=' + urllib.quote_plus(image)
    else:
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page='+ '&image=' + urllib.quote_plus(image)
    if link == True:
        list2.append((name,
         url,
         iconimage,
         '',
         '',
         page))
    else:
        list2.append((name,
         u,
         iconimage,
         '',
         '',
         page))


def trace_error():
    import traceback
    try:
        traceback.print_exc(file=open('/tmp/ProhdIPTV_log', 'a'))
    except:
        pass








def process_mode(list1 = [], action_param = None,searchtxt=None):
    global list2
    if True:
        
        log(" ",'Start session####################################################')
        list2 = []
        log("action_param",action_param)
        params = get_params(action_param)
        log("params",params)    
        url = None
        name = None
        mode = None
        page = ''
        image = '/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/addons/radio/TuneinRadio/icon.png'
        try:
            url = urllib.unquote_plus(params['url'])
        except:
            pass

        try:
            name = urllib.unquote_plus(params['name'])
        except:
            pass
        try:
            image = urllib.unquote_plus(params['image'])
        except:
            pass
        try:
            mode = int(params['mode'])
        except:
            pass

        try:
            page = str(params['pageToken'])
        except:
            page = 1

        print 'Mode: ' + str(mode)
        print 'URL: ' + str(url)
        print 'Name: ' + str(name)
        print 'page: ' + str(page)
        if type(url) == type(str()):
            url = urllib.unquote_plus(url)
        if mode == None:
            
            getlocalstations(name,url,page)
        elif mode == 103:
             print '' + url
             search(url,searchtxt)  
        elif mode == 10:
            print '' + url
            getstreams(name,url,page,image)
        elif mode == 300:
            print '' + url
            getstreams(name,url,page,image)
    else:
        addDir('Error:script error [error 1050]', '', '', '', desc='', page='')
        trace_error()
    log(" ",'End session####################################################')
    return list2

#print "stations" ,process_mode(list1 = [], action_param = None)

    
   
