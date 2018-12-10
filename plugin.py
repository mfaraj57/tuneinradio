# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ImageDownLoader/plugin.py
from Plugins.Plugin import PluginDescriptor
from Components.config import config, ConfigIP, ConfigInteger, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
import os
config.TuneinRadio = ConfigSubsection()

config.TuneinRadio.menuplugin = ConfigEnableDisable(default=False)

config.TuneinRadio.autoupdate = ConfigEnableDisable(default=False)
config.TuneinRadio.downloadlocation = ConfigText(default='/media/hdd', fixed_size=False)
config.TuneinRadio.favlocation = ConfigText(default='/etc/TuneinRadio', fixed_size=False)
       

PLUGIN_PATH='/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio'
try:
    import socket
    timeout = 25
    socket.setdefaulttimeout(timeout)
except:
    pass

def main(session, **kwargs):
  ####
    import os
    if os.path.exists("/tmp/TuneinRadio/")==False:
        os.mkdir("/tmp/TuneinRadio/")
    if os.path.exists("/etc/TuneinRadio/")==False:
        os.mkdir("/etc/TuneinRadio/")
    if os.path.exists("/tmp/TuneinRadio/pics/")==False:
        os.mkdir("/tmp/TuneinRadio/pics/")
    if os.path.exists("/etc/TuneinRadio/")==False:
        os.mkdir("/etc/TuneinRadio/")
    if os.path.exists(PLUGIN_PATH + '/lib/defaults/favorites2.xml') and os.path.exists('/etc/TuneinRadio/favorites2.xml')==False:
            from Tools.Directories import copyfile
            copyfile(PLUGIN_PATH + '/lib/defaults/favorites2.xml',  '/etc/TuneinRadio/favorites2.xml')
    ####



    
    from .bootlogo import bootlogo
    session.open(bootlogo)


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('TuneinRadio'),
          main,
          'TuneinRadio_mainmenu',
          2)]
    return []


def Plugins(path, **kwargs):
    global plugin_path
    plugin_path = path
    list = []
    try:
        if config.TuneinRadio.menuplugin.value == True:
            list.append(PluginDescriptor(icon='plugin.png', name='Tunein Radio', description='Tunein Radio', where=PluginDescriptor.WHERE_MENU, fnc=menu))
    except:
        list.append(PluginDescriptor(icon='plugin.png', name='Tunein Radio', description='Tunein Radio', where=PluginDescriptor.WHERE_MENU, fnc=menu))

    list.append(PluginDescriptor(icon='plugin.png', name='Tunein Radio', description='Tunein Radio', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main))
    return list
