from maya import cmds
import os
import pprint

from Qt import QtWidgets, QtCore, QtGui

from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui

from animina import animinaLibrary
# reload(animinaLibrary)

from animina import helpDialog
# reload(helpDialog)


# function to get maya main window pointer
def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr
    # returns the pointer to main window

def getDock(name='AniminaDock'):
    deleteDock(name)
    ctrl = cmds.workspaceControl(name, label='Animina UI')
    qtCtrl = omui.MQtUtil_findControl(ctrl)
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
    return ptr
    # returns the pointer to the dock


def deleteDock(name='AniminaDock'):
    if cmds.workspaceControl(name, query=True, exists=True):
        cmds.deleteUI(name)

# paths
USERAPPDIR = cmds.internalVar(userAppDir=True)
LIBDIR = os.path.join(USERAPPDIR, 'animinaLibrary')
SCRIPTDIR = cmds.internalVar(userScriptDir=True)
ANIMADIR = os.path.join(SCRIPTDIR,'animina')

# current project directory
PWD = cmds.workspace(query=True, directory=True)

print 'USERAPPDIR', USERAPPDIR
print 'LIBDIR', LIBDIR
print 'SCRIPTDIR,', SCRIPTDIR
print 'ANIMADIR ', ANIMADIR

SCREENSHOTDEF = os.path.join(ANIMADIR, 'Animina_small')

# this is the main UI class
class SelectionUI(QtWidgets.QWidget):

    def __init__(self, dock=True):
        if dock:
            parent = getDock()
        else:
            # remove original dock and create dialog UI under the maya main window
            deleteDock()

            # delete if it already exists
            try:
                cmds.deleteUI('animinaName')
            except:
                print "No previous UI Exists"
            
            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('animinaName')
            parent.setWindowTitle('Animina UI')
            layout = QtWidgets.QVBoxLayout(parent)

        super(SelectionUI, self).__init__(parent=parent)

        self.library = animinaLibrary.SelectionLibrary()
        self.buildUI()
        
        # add this widget to parent, query the parent using parent() and find layout()
        self.parent().layout().addWidget(self)
        # show QDialog if the dock doesnt exist
        if not dock:
            parent.show()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        # help layout widget ==========
        labWidget = QtWidgets.QWidget()
        labLayout = QtWidgets.QHBoxLayout(labWidget)
        layout.addWidget(labWidget)

        helpBtn = QtWidgets.QPushButton('Help')
        helpBtn.clicked.connect(self.help)
        labLayout.addWidget(helpBtn)

        label = QtWidgets.QLabel(self)
        label.setText('Enter a selection group name or a save directory:')
        layout.addWidget(label)

        # create field and button ==================================
        # child horizontal layout
        createWidget = QtWidgets.QWidget()
        layout.addWidget(createWidget)

        createLayout = QtWidgets.QHBoxLayout(createWidget)
        self.createNameField = QtWidgets.QLineEdit()
        createLayout.addWidget(self.createNameField)
        
        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createGroup)
        createLayout.addWidget(createBtn)

        # ==== start List widget ======
        size = 72
        buffer = 12
        # list widget - creates a grid list widget to display the selection thumbnails
        self.listWidget  = QtWidgets.QListWidget()
        
        # test multi selection
        self.listWidget.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

        # use icon mode in the list widget
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size,size))

        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        # list behaviour (needs a toggle) EXPERIMENT
        # loads selection on click of an icon V0.9+ this is now standard
        self.listWidget.clicked.connect(self.load)

        # buttons - first row ====================================
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)
        
        # visibility button
        visBtn = QtWidgets.QPushButton('Visibility')
        visBtn.clicked.connect(self.hideGroups)
        btnLayout.addWidget(visBtn)

        # reresh button
        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)
        
        # delete space button
        deleteBtn = QtWidgets.QPushButton('Delete')
        deleteBtn.clicked.connect(self.deleteGroup)
        btnLayout.addWidget(deleteBtn)
        
        # second row buttons =======================================
        btnWidget2 = QtWidgets.QWidget()
        btnLayout2 = QtWidgets.QHBoxLayout(btnWidget2)
        layout.addWidget(btnWidget2)

        # save to file
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.saveFile)
        btnLayout2.addWidget(saveBtn)

        # load from file
        loadBtn = QtWidgets.QPushButton('Load')
        loadBtn.clicked.connect(self.loadFile)
        btnLayout2.addWidget(loadBtn)

        # connect close button signal to the close method in the QDialog
        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.closeAnimina)
        btnLayout2.addWidget(closeBtn)

    def closeAnimina(self):
        self.library.clearLibrary()
        deleteDock()

    def help(self):
        dlg = helpDialog.HelpWindow()
        if dlg.exec_():
            print("Opened help!")
        else:
            print("Closed help!")

    def saveScreenshot(self, name='Screen', directory=LIBDIR):
        # creates dir if it doesnt exist
        if not os.path.exists(directory):
            os.mkdir(directory)
            print 'Created LIBDIR at ', LIBDIR
        
        # check if anything is in the selection memory
        if not self.library.currentSelection:
            print 'nothing in selection'
            return

        currentKey = self.library.currentSelection

        path = os.path.join(directory, '%s.jpg' % currentKey)

        # isolate the object
        panels = cmds.playblast(activeEditor=True)

        # check for joints and turn off Local joint axis display
        currentObjects = self.library[currentKey]['selection']
        
        flag = []
        for obj in currentObjects:
            if cmds.objectType(obj) == 'joint' and cmds.getAttr(obj+'.displayLocalAxis') == True:
                # check the children of this joint
                relatives = cmds.listRelatives(obj, allDescendents=True, type='joint')
                flag.append(obj)
                if relatives:
                    flag.extend(relatives)
        
        if flag:
            # print flag
            for obj in flag:
                cmds.setAttr(obj+'.displayLocalAxis', False)

        activePanel = panels.split('|')[-1]

        cmds.editor(activePanel, edit=True, lockMainConnection=True, mainListConnection='activeList' )
        cmds.isolateSelect(activePanel,state=1)

        #save current view
        homeView = cmds.cameraView(camera='persp')
        highlightMode = cmds.selectPref(selectionChildHighlightMode=0,query=True)

        cmds.selectPref(selectionChildHighlightMode=1)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        currentTime = cmds.currentTime(query=True)

        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=600, height=600, showOrnaments=False, startTime=currentTime, endTime=currentTime, viewer=False)

        # turn off isolation
        cmds.isolateSelect(activePanel,state=False)            
        # turn back on any local rotation axis
        if flag:
            for obj in flag:
                cmds.setAttr(obj+'.displayLocalAxis', True)

        # reset view
        cmds.cameraView(homeView, camera='persp', e=True, setCamera=True)
        cmds.selectPref(selectionChildHighlightMode=highlightMode)

        self.populate()

    def createGroup(self):
        
        # check if you have a selection
        if not cmds.ls(selection=True):
            cmds.warning("You need a selection!")
            return

        # take the user input in the name field
        selectionName = self.createNameField.text()

        # check if you have a name
        if not selectionName.strip():
            cmds.warning("You must give a name!")
            return

        # check if name exists already ignoring case
        keyslow = [i.lower() for i in self.library.keys()]

        # if selectionName in self.library.keys():
        if selectionName.lower() in keyslow:
            cmds.warning("Name already exists!")
            return

        # pass this name to the selection manager...
        self.library.storeSelection(selectionName)
        # and the temporary current selection variable
        self.library.currentSelection = selectionName

        # add widget with new selection group name
        item = QtWidgets.QListWidgetItem(selectionName)
        self.listWidget.addItem(item)
        self.createNameField.clear()
        self.saveScreenshot()

    def populate(self):
        # clear list widget and repopulate
        self.listWidget.clear()

        # find screenfiles in library
        self.library.find()

        for key in self.library.keys():
  
            item = QtWidgets.QListWidgetItem(key)
            self.listWidget.addItem(item)
            slist = self.library[key]['selection']
            if 'path' in self.library[key]:
                icon = QtGui.QIcon(self.library[key]['path'])
                item.setIcon(icon)
                item.setToolTip(pprint.pformat(slist))

            else:
                icon = QtGui.QIcon(SCREENSHOTDEF)
                item.setIcon(icon)
                item.setToolTip(pprint.pformat(slist))

    def hideGroups(self):

        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        selectedItems = [tag for tag in self.listWidget.selectedItems()]

        for item in selectedItems:
            # get the selection from the key
            key = item.text()
            selectionList = self.library[key]['selection']
            visHome = self.library[key]['visibility']
            # print visHome

            # list to store original vis state
            if self.library[key]['vistoggle'] == False:
                for i, object in enumerate(selectionList):
                    cmds.setAttr(object+'.visibility',False)
                self.library[key]['vistoggle'] = True
            else:
                for i, object in enumerate(selectionList):
                    cmds.setAttr(object+'.visibility',visHome[i])
                    self.library[key]['vistoggle'] = False

    def deleteGroup(self):
               
        if self.library.keys():
            # get current selected group from widget
                       
            currentItem = self.listWidget.currentItem()
            if not currentItem:
                return

            selectedItems = [tag for tag in self.listWidget.selectedItems()]

            for item in selectedItems:
                toClear = item.text()
                # print self.library[toClear].keys()
                # remove widget from UI
                # returns noKey if the key doesnt exist
            
                # check and remove attached screenshot
                if 'path' in self.library[toClear].keys():
                    spath = os.path.join(LIBDIR, '%s.jpg' % toClear)
                    os.remove(spath)

                # remove entry from dictionary
                deleted = self.library.pop(toClear,'noKey')

            self.populate()

    def saveFile(self):
        filename = self.createNameField.text()
        # only use lowercase filenames
        filename = filename.lower()

        if not self.library.keys():
            cmds.warning("No groups created yet!")
            return

        if not filename.strip():
            # cmds.warning("Use the create field to enter a filename")
            self.library.writeSave(fname='default')
        else:
            self.library.writeSave(fname=filename)

        self.createNameField.clear()

    def loadFile(self):
        filename = self.createNameField.text()
        # only use lowercase filenames
        filename = filename.lower()

        if not filename.strip():
            defaultDIR = os.path.join(PWD, 'animina/default')

            if not os.path.exists(defaultDIR):
                cmds.warning("No default save folder exists yet")
            else:
                self.library.clear()
                self.listWidget.clear()
                self.library.loadSave(fname='default')

        else:
            saveDIR = os.path.join(PWD, 'animina/')
            saveDIR = os.path.join(saveDIR, filename)
            if not os.path.exists(saveDIR):
                fwarning = "Save folder <"+filename+"> does not exist yet"
                cmds.warning(fwarning)
            else:
                self.library.clear()
                self.listWidget.clear()
                self.library.loadSave(fname=filename)
        
        # print self.library.keys()
        self.createNameField.clear()
        self.populate()

    def checkSelected(self):
        """
        Checks the selected selection grouping
        """
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return

        selectedItems = [tag for tag in self.listWidget.selectedItems()]
        
        names = []
        for item in selectedItems:
            iconText = item.text()
            names.append(iconText)
         
        # get current selection from listwidget and add to maya selection
        storedSelection = []
        for key in names:
            getsel = self.library[key]['selection']
            storedSelection.extend(getsel)

        self.currentSelection = storedSelection

    def load(self):
        # loads widget selection into maya active selection
        self.checkSelected()

        loadobjects = self.currentSelection

        # check the objects exist in the scene
        outliner = cmds.ls(dagObjects=True)

        for obj in loadobjects:
            if obj not in outliner:
                loadobjects.remove(obj)
                stringWarning = 'Object '+obj+' not found in scene'
                cmds.warning(stringWarning)

        cmds.select(clear=True)
        cmds.select(loadobjects)
        cmds.setFocus("MayaWindow")
