# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/ImageDownLoader/Mytexte.py
from Screens.Screen import Screen
from enigma import getDesktop
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.ScrollLabel import ScrollLabel

class showinfoscreen(Screen):
    skin = '\n\t<screen position="0,0" size="920,600" title="TuneinRadio" backgroundColor="#70000000">\n\t<ePixmap position="0,0" size="920,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/infopanel.png" alphatest="blend" transparent="1" backgroundColor="transparent"/>\n  <widget font="Regular;30" position="400,40" render="Label" size="800,40" source="Title" halign="center" valign="center" foregroundColor="yellow" transparent="1" zPosition="2"/>\n  <ePixmap position="400,80" size="800,5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/slider.png" alphatest="blend" transparent="1" backgroundColor="transparent"/>\n\t<widget name="text" position="300,90" size="900,560" font="Regular;24" transparent="0" foregroundColor="yellow" backgroundColor="black" zPosition="1"/>\n\t\t<!--widget source="text" render="Label" position="100,100" size="900,540" font="Regular;20" /-->\n\t</screen>'

    def __init__(self, session, text = '', title = ''):
        Screen.__init__(self, session)
        self.text = text
        self.newtitle = title
        self['text'] = ScrollLabel(self.text)
        self['actions'] = ActionMap(['OkCancelActions', 'DirectionActions'], {'cancel': self.cancel,
         'ok': self.ok,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self['title'] = StaticText()
        self.onShown.append(self.updateTitle)

    def updateTitle(self):
        self.setTitle(self.newtitle)
        self['title'].setText(self.newtitle)

    def ok(self):
        self.close()

    def cancel(self):
        self.close()
