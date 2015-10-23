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

    def startfunc(self):
        if (self.start == False):
            self.start_pushButton.setText('Stop')
            resolutionList = ['640 480 60','1024 600 60','1024 768 60', '1366 768 60']
            i = self.resolution_comboBox.currentIndex()
            if (i < 4):
                resolution = resolutionList[i]
            else:
                if(self.customres_lineEdit.text() != ''):
                    resolution = self.customres_lineEdit.text()

            utils.generateVirtualScreen(resolution)
            self.popen = utils.vncStart(resolution)
            self.start = True

        else:
            self.start_pushButton.setText('Star')
            self.popen.kill()
            utils.closeVirtualScreen()
            self.start = False


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
        command = ['/usr/bin/x11vnc', '-clip' ,res[0] + 'x' + res[1] + '+0+0', '-viewonly']
        print(command)
        sp = subprocess
        popen = subprocess.Popen(command,stdout=sp.PIPE, stderr=sp.STDOUT)
        return popen

    @staticmethod
    def obtainIP():
        """This funtion create an virtual screen"""
        import commands

        # Obtain courrent output screen
        command = '/bin/ifconfig'
        commandOut= commands.getstatusoutput(command)


# if __name__ == "__main__":
#       import sys
#       app = QtGui.QApplication(sys.argv)
#       MainWindow = QtGui.QMainWindow()
#       ui = EVUI()
#       ui.setupUi(MainWindow)
#       MainWindow.show()
#       sys.exit(app.exec_())
utils.obtainIP()