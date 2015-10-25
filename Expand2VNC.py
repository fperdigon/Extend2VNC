#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fco'
import Expand2VNC_UI
from PyQt4 import QtCore, QtGui

class EVUI(Expand2VNC_UI.Ui_MainWindow):
    def __init__(self):
        super(EVUI, self).__init__()
    def setupUi(self, MainWindow):
        super(EVUI, self).setupUi(MainWindow)
        self.popen = object()
        self.start = False

        self.customres_lineEdit.setVisible(False)
        self.start_pushButton.clicked.connect(self.startfunc)
        self.resolution_comboBox.currentIndexChanged.connect(self.comboboxChangefunc)

        self.actionMain_help.triggered.connect(self.helpfunc)
        self.actionAbout_Qt.triggered.connect(QtGui.qApp.aboutQt)
        self.actionAbout_Expand2VNC.triggered.connect(self.Aboutfunc)

    def startfunc(self):
        if (self.start == False):
            self.start_pushButton.setText('Stop')
            resolutionList = ['640 480 60','800 480 60','1024 600 60','1024 768 60', '1366 768 60']
            i = self.resolution_comboBox.currentIndex()
            if (i < 4):
                resolution = resolutionList[i]
            else:
                if(self.customres_lineEdit.text() != ''):
                    resolution = self.customres_lineEdit.text().__str__()
                    resolution =  resolution.split('x')[0] + ' ' + resolution.split('x')[1] + ' 60'
                    print(resolution)
                else:
                    resolutionList[1]

            utils.generateVirtualScreen(resolution)
            self.popen = utils.vncStart(resolution)
            nIP = utils.obtainIP()
            self.status_label.setText('status: Virtual screen active in ' + nIP + ':5900 connect using a vnc client')
            self.start = True

        else:
            self.start_pushButton.setText('Star')
            self.popen.kill()
            utils.closeVirtualScreen()
            self.status_label.setText('status: Virtual screen stoped')
            self.start = False

    def comboboxChangefunc(self):
        if(self.resolution_comboBox.currentIndex() == 5):
            self.customres_lineEdit.setVisible(True)
        else:
            self.customres_lineEdit.setVisible(False)

    def Aboutfunc(self):

        QtGui.QMessageBox.about(QtGui.QMainWindow(), "About Expand2VNC",
                "<b>Expand2VNC v0.1</b> is an aplication to expand your screen using a virtual video interface and vncserver in Linux. Licence GPL v2"
                "<br><br><b>Expand2VNC v0.1</b> es una aplicacion para expandir su pantalla usando una interfaz de video vistual y vncserver en Linux. Licencia GPL v2"
                "<br><br>Programer: Francisco Perdigon Romero. (<b>bosito7</b>)"
                "<br>Email: <a href=\"mailto:bosito7gmail.com?subject=About Expand2VNC\">bosito7@gmail.com</a>"
                "<br><br>GUTL. Grupo de usuarios de tecnologias libres."
                "<br> <a href=\"http://gutl.jovenclub.cu/\">http://gutl.jovenclub.cu/</a> ")

    def helpfunc(self):

        QtGui.QMessageBox.about(QtGui.QMainWindow(), "About Expand2VNC",
                "<b>(English) Expand2VNC v0.1</b> is an aplication to expand your screen using a virtual video interface and vncserver in Linux."
                "<br>Dependencies: x11vnc, if your system is based on Debian or Ubuntu put in a terminal <b> sudo apt-get install x11vnc </b>"
                "<br><br>Select the appropriate resolution for display on your device, there appears, select Custom and then specify it."
                "<br> After clicking Start, down the status bar will appear that you are ready and will leave the IP number to us that we have"
                "Connect from VNC client, to stop click on Stop."
                "<br><br>VNC Clients recommended for use with this tool are (with other mouse pointer does not appear):"
                "<br>For Linux, use xtightvnc to install if your system is based on Debian or Ubuntu put in a terminal <b>sudo apt-get install xtightvncviewer </b>"
                "<br>Then in a terminal put <b>vncviewer numero_ip </b>"
                "<br>For Windows and MacOS tightvnc to install instal official site and download <a href=\"http://www.tightvnc.com/\"> http://www.tightvnc.com/ </a>"
                "<br>In Android download VNC Client from the Play Store"

                "<br><br><b>(Espanish) Expand2VNC v0.1</b> es una aplicacion para expandir su pantalla usando una interfaz de video vistual y vncserver en Linux."
                "<br>Dependencias: x11vnc, si su sistema es basado en Debian o Ubuntu poner en un terminal <b>sudo apt-get install x11vnc</b>"
                "<br><br>Seleccione la resolucion adecuada para mostrar en su dispositivo, si no aparece entonces seleccione Custom y especifiquela."
                "<br>Despues de hacer clic en Start, abajo en la barra de estado aparecera que ya esta listo y saldra el numero IP al que nos tenemos que"
                " conectar desde el cliente vnc, para parar dar clic en Stop."
                "<br><br>Los clientes vnc recomendados para el uso en conjunto con esta herramienta son (con otros el puntero del mouse no aparece):"
                "<br>Para Linux use tightvnc para instalarlo si su sistema es basado en Debian o Ubuntu poner en un terminal <b>sudo apt-get install xtightvncviewer</b>"
                "<br>Luego en un terminal poner <b>vncviewer numero_ip</b>"
                "<br>Para Windows y MacOS use tightvnc para instalarlo descargar del sitio oficial <a href=\"http://www.tightvnc.com/\">http://www.tightvnc.com/</a> "
                "<br>Para Android descargar VNC Client del Play Store " )



class utils:
    @staticmethod
    def generateVirtualScreen(resolution):
        """This funtion create an virtual screen"""
        import commands

        # Obtain courrent output screen
        command = 'xrandr'
        commandOut= commands.getstatusoutput(command)
        currentScreen  = commandOut[1].split(' connected')[0].split('\n')[-1]

        virtualScreen = 'VIRTUAL1'

        # gtf 1024 600 60
        command = 'gtf ' + resolution
        print(command)
        commandOut = commands.getstatusoutput(command)

        Modeline = commandOut[1].split('Modeline ')[1].split('\n')[0]
        ModelineName = Modeline.split(' ')[0]

        # xrandr --newmode "1024x600_60.00"  48.96  1024 1064 1168 1312  600 601 604 622  -HSync +Vsync
        command = 'xrandr --newmode '+ Modeline
        print(command)
        commands.getoutput(command)

        # xrandr --addmode VirtualScreen "1024x600_60.00"
        command = 'xrandr --addmode ' + virtualScreen + ' ' + ModelineName
        print(command)
        commands.getoutput(command)

        # xrandr --output VirtualScreen --mode "1024x600_60.00" --left-of VGA1
        command = 'xrandr --output ' + virtualScreen + ' --mode ' + ModelineName + ' --left-of ' + currentScreen
        #command = 'xrandr --output ' + virtualScreen + ' --mode ' + ModelineName + ' --right-of ' + currentScreen
        print(command)
        commands.getoutput(command)

    @staticmethod
    def closeVirtualScreen():
        """This funtion close an virtual screen"""
        import commands

        # xrandr --output VirtualScreen --off
        command = 'xrandr --output VIRTUAL1 --off'
        print(command)
        commands.getoutput(command)

    @staticmethod
    def vncStart(resolution):
        """This funtion start vncserver"""
        import commands , subprocess
        # x11vnc -clip 1024x600+0+0 -viewonly
        res = resolution.split(' ')
        command = ['/usr/bin/x11vnc', '-clip' ,res[0] + 'x' + res[1] + '+0+0', '-viewonly', '-forever']
        print(command)
        sp = subprocess
        popen = subprocess.Popen(command,stdout=sp.PIPE, stderr=sp.STDOUT)
        return popen

    @staticmethod
    def obtainIP():
        """This funtion return the IP number"""
        import commands

        # Obtain courrent output screen
        command = '/sbin/ifconfig'
        commandOut= commands.getstatusoutput(command)
        print(commandOut)
        nIP = commandOut[1].split('inet:')[1].split(' ')[0]
        if(nIP == '127.0.0.1'):
            nIP = commandOut[1].split('inet:')[2].split(' ')[0]
        print(nIP)
        return nIP

if __name__ == "__main__":
       import sys
       app = QtGui.QApplication(sys.argv)
       MainWindow = QtGui.QMainWindow()
       ui = EVUI()
       ui.setupUi(MainWindow)
       MainWindow.show()
       sys.exit(app.exec_())
