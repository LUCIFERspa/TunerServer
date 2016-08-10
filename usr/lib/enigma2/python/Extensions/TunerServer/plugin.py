# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TunerServer/plugin.py
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Network import iNetwork
from Tools.Directories import fileExists
from enigma import eServiceCenter, eServiceReference, eTimer
from shutil import rmtree, move, copy
import os

class TunerServer(Screen):
    skin = """
	<screen name="TunerServer" zPosition="2" position="0,0" size="1280,720" title="Plugins" flags="wfNoBorder" backgroundColor="#ff000000">
<ePixmap name="arriba" position="0,0" size="1280,720" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/windows-fs8.png" zPosition="-5" />
<widget source="key_red" render="Label" position="130,387" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
 <ePixmap name="botonrojo" position="89,383" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/botrojo-fs8.png" zPosition="20" />
<widget source="key_blue" render="Label" position="130,434" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonazul" position="89,430" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/botazul-fs8.png" zPosition="20" />
<widget source="key_yellow" render="Label" position="130,481" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonamarillo" position="89,477" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/botamarillo-fs8.png" zPosition="20" />
<widget source="key_green" render="Label" position="130,527" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonverde" position="89,524" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/botverde-fs8.png" zPosition="20" />
<ePixmap name="lateral" position="0,260" size="42,128" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/HasSub.png" zPosition="20" />
    <ePixmap name="fondoazul" position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/fondotv-fs8.png" zPosition="-35" alphatest="blend" />
    <ePixmap name="fondoarriba" position="0,0" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/infobararriba70-fs8.png" zPosition="-30" alphatest="blend" />
    <ePixmap name="fondoabajo" position="-2,603" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/fondopie-fs8.png" zPosition="-31" alphatest="blend" />
<ePixmap name="iconodescarga" position="50,28" size="40,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/icon_addons.png" zPosition="30" alphatest="blend" />
<ePixmap name="playpie" position="50,635" size="24,24" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/TunerServer/confluence/menu/tv24-fs8.png" zPosition="30" alphatest="blend" />
<widget source="global.CurrentTime" render="Label" position="900,18" size="251,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
<widget source="global.CurrentTime" render="Label" position="900,40" size="300,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Date</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" position="80,633" size="481,32" font="Bold; 20" transparent="1" valign="center" zPosition="11" backgroundColor="#10101010" noWrap="1" halign="left" foregroundColor="#007c8286">
      <convert type="ServiceName">Name</convert>
    </widget>
<widget source="Title" render="Label" position="481,96" size="717,32" font="Bold; 24" halign="center" foregroundColor="#00faa900" backgroundColor="#101a2024" transparent="1" noWrap="1" zPosition="12" />
    <eLabel name="marcopip" position="82,117" size="344,186" backgroundColor="#00373737" />
    <widget source="session.VideoPicture" render="Pig" position="83,118" size="342,184" zPosition="50" backgroundColor="#ff000000" />
	<widget name="lab1" position="491,138" size="700,420" font="Regular;15" transparent="0"/>
	<widget name="lab2" position="430,500" size="300,30" font="Regular;20" valign="center" halign="right" foregroundColor="white" transparent="1" zPosition="2"/>
	<widget name="labstop" position="740,500" size="260,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="red"/>
	<widget name="labrun" position="740,500" size="260,30" zPosition="1" font="Regular;20" valign="center" halign="center" backgroundColor="green"/>
      <widget font="Regular; 17" backgroundColor="dp_gris_barra_fondo" halign="right" position="484,640" render="Label" size="592,71" source="session.CurrentService" transparent="1" foregroundColor="dp_gris_barra" valign="top" borderColor="dp_gris_barra_sombra2" borderWidth="1">
      <convert type="spaSysInfo">DiskAllSleep</convert>
      </widget>
<widget name="homeinfo" position="100,40" size="500,30" zPosition="11" font="Regular; 21" halign="left" valign="center" backgroundColor="#140b1" foregroundColor="white" transparent="1" noWrap="1" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('Tuner Server setup'))
        mytext = '\nThis plugin implements the Tuner Server feature included. It will allow you to share the tuners of this box with another STB, PC and/or another compatible device in your home network.\nThe server will build a virtual channels list in the folder /media/hdd/tuner or /media/usb/tuner on this box.\nYou can access the tuner(s) of this box from clients on your internal lan using nfs, cifs, UPnP or any other network mountpoint.\nThe tuner of the server (this box) has to be avaliable. This means that if you have ony one tuner in your box you can only stream the channel you are viewing (or any channel you choose if your box is in standby).\nRemember to select the correct audio track in the audio menu if there is no audio or the wrong language is streaming.\nNOTE: The server is built, based on your current ip and the current channel list of this box. If you change your ip or your channel list is updated, you will need to rebuild the server database.\n\n\t\t'
        self['lab1'] = Label(_(mytext))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Server Disabled'))
        self['labrun'] = Label(_('Server Enabled'))
        self['key_red'] = Label(_('Build Server'))
        self['key_green'] = Label(_('Disable Server'))
        self['key_yellow'] = Label(_('Close'))
	self['key_blue'] = Label(_('Manage disk'))
	self['homeinfo'] = Label(_('Home Tuner Server'))
        self.my_serv_active = False
        self.ip = '0.0.0.0'
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.close,
         'back': self.close,
         'red': self.ServStart,
         'green': self.ServStop,
		 'blue': self.montar,
         'yellow': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.doServStart)
        self.onClose.append(self.delTimer)
        self.onLayoutFinish.append(self.updateServ)
		
    def montar(self):
		from Plugins.SystemPlugins.DeviceManager.HddSetup import HddSetup
		self.session.open(HddSetup)

    def ServStart(self):
        if os.path.ismount('/media/hdd'):
            self['lab1'].setText(_('Your server is now building hdd \nPlease wait ...'))
            self.activityTimer.start(10)
        elif os.path.ismount('/media/usb'):
            self['lab1'].setText(_('Your server is now building USB \nPlease wait ...'))
            self.activityTimer.start(10)
        else:
            self.session.open(MessageBox, _("Sorry, but you need to have a device mounted at '/media/hdd' or 'media/usb'"), MessageBox.TYPE_INFO)

    def doServStart(self):
        self.activityTimer.stop()

        if os.path.ismount('/media/hdd'):
            folder = '/media/hdd/tuner'
        elif os.path.ismount('/media/usb'):
            folder = '/media/usb/tuner'

        if os.path.exists(folder):
            rmtree(folder)
        ifaces = iNetwork.getConfiguredAdapters()
        for iface in ifaces:
            ip = iNetwork.getAdapterAttribute(iface, 'ip')
            ipm = '%d.%d.%d.%d' % (ip[0],
             ip[1],
             ip[2],
             ip[3])
            if ipm != '0.0.0.0':
                self.ip = ipm

        os.mkdir(folder, 0755)
        s_type = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'
        serviceHandler = eServiceCenter.getInstance()
        services = serviceHandler.list(eServiceReference('%s FROM BOUQUET "bouquets.tv" ORDER BY bouquet' % s_type))
        bouquets = services and services.getContent('SN', True)
        count = 1
        for bouquet in bouquets:
            self.poPulate(bouquet, count, folder)
            count += 1

        mytext = "Server avaliable on ip %s\nTo access this box's tuners you can connect via Lan or UPnP.\n\n1) To connect via lan you have to mount the /media/hdd or /media/usb folder of this box in the client /media/hdd folder. Then you can access the tuners server channel list from the client Media player -> Harddisk -> tuner.\n2) To connect via UPnP you need an UPnP server that can manage .m3u files like Mediatomb." % self.ip
        self['lab1'].setText(_(mytext))
        self.session.open(MessageBox, _('Build Complete!'), MessageBox.TYPE_INFO)
        self.updateServ()

    def poPulate(self, bouquet, count, folder):
        n = '%03d_' % count
        name = n + self.cleanName(bouquet[1])
        path = folder
        serviceHandler = eServiceCenter.getInstance()
        services = serviceHandler.list(eServiceReference(bouquet[0]))
        channels = services and services.getContent('SN', True)
        
        for channel in channels:
            if not int(channel[0].split(':')[1]) & 64:
                filename = path + "/" + n + self.cleanName(bouquet[1]) + ".m3u"
                try:
                    out = open(filename, 'a')
                except:
                    continue

                out.write('#EXTM3U\n')
                out.write('#EXTINF:-1,' + channel[1] + '\n')
                out.write('http://' + self.ip + ':8001/' + channel[0] + '\n\n')
                out.close()
                

    def cleanName(self, name):
        name = name.replace(' ', '_')
        name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
        name = name.replace('.', '_')
        name = name.replace('<', '')
        name = name.replace('<', '')
        name = name.replace('/', '')
        return name

    def ServStop(self):
        if self.my_serv_active == True:
            self['lab1'].setText(_('Your server is now being deleted\nPlease Wait ...'))
			
            if os.path.ismount('/media/hdd'):
                folder = '/media/hdd/tuner'
            elif os.path.ismount('/media/usb'):
                folder = '/media/usb/tuner'

            if os.path.exists(folder):
                rmtree(folder)
            mybox = self.session.open(MessageBox, _('Tuner Server Disabled.'), MessageBox.TYPE_INFO)
            mybox.setTitle(_('Info'))
            self.updateServ()
        self.session.open(MessageBox, _('Server now disabled!'), MessageBox.TYPE_INFO)

    def updateServ(self):
        self['labrun'].hide()
        self['labstop'].hide()
        self.my_serv_active = False
		
        if os.path.ismount('/media/hdd'):
            folder = '/media/hdd/tuner'
        elif os.path.ismount('/media/usb'):
            folder = '/media/usb/tuner'

        if os.path.isdir(folder):
            self.my_serv_active = True
            self['labstop'].hide()
            self['labrun'].show()
        else:
            self['labstop'].show()
            self['labrun'].hide()

    def delTimer(self):
        del self.activityTimer


def settings(menuid, **kwargs):
    if menuid == 'network':
        return [(_('Tuner Server setup'),
          main,
          'tuner_server_setup',
          None)]
    else:
        return []


def main(session, **kwargs):
    session.open(TunerServer)


def Plugins(**kwargs):
    return PluginDescriptor(name=_('Tuner Server'), description=_('Allow Streaming From Box Tuners'), where=PluginDescriptor.WHERE_PLUGINMENU, needsRestart=False, fnc=main)
