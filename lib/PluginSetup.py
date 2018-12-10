from Components.config import config, ConfigIP, ConfigInteger, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
class TuneinRadioSetup(Screen, ConfigListScreen):
    skin='''<screen
    name = "TuneinRadioSetup"
    position = "center,center"
    size = "920,560"
    backgroundColor = "#080000"
    title = "TuneinRadio Settings">
    <ePixmap
        position = "79,521"
        size = "25,25"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>
    <ePixmap
        position = "283,521"
        size = "25,25"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"
        zPosition = "3"
        transparent = "1"
        alphatest = "blend"/>
    <eLabel
        position = "86,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = "Cancel"/>
    <eLabel
        position = "295,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = "Save"/>
    <eLabel
        position = "495,523"
        zPosition = "4"
        size = "200,24"
        halign = "center"
        font = "Regular;25"
        transparent = "1"
        foregroundColor = "#ffffff"
        backgroundColor = "#41000000"
        text = " "/>
    <ePixmap
        position = "75,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <ePixmap
        position = "279,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <ePixmap
        position = "484,514"
        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"
        size = "204,37"
        zPosition = "2"
        backgroundColor = "#ffffff"
        alphatest = "blend"/>
    <widget
        name = "config"
        position = "20,50"
        size = "900,350"
        itemHeight = "35"
        scrollbarMode = "showOnDemand"
        transparent = "1"
        zPosition = "2"/>
</screen>'''
    def __init__(self, session):
        Screen.__init__(self, session)
        
        self.list = []
        
        self.list.append(getConfigListEntry(_('Show plugin in main menu(need e2 restart):'), config.TuneinRadio.menuplugin))
        

        ConfigListScreen.__init__(self, self.list, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.keySave,
         'cancel': self.keyClose,
         'blue': self.resetdefaults}, -2)
       
    def resetdefaults(self):
        pass



    def keySave(self):
       
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        self.close(True)
    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close(True)

    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)


