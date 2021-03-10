from maya import cmds
import os
import json
import sys
import pprint
from shutil import copyfile

USERAPPDIR = cmds.internalVar(userAppDir=True)
LIBDIR = os.path.join(USERAPPDIR, 'animinaLibrary')
SCRIPTDIR = cmds.internalVar(userScriptDir=True)
ANIMADIR = os.path.join(SCRIPTDIR,'animina')

#current project directory
PWD = cmds.workspace(query=True, directory=True)
pssp = os.sep

"""
Library for Animina to function
"""

def createDirectory(directory=LIBDIR):
    """
    creates the library directory if it doesnt exist
    """
    if not os.path.exists(directory):
        os.mkdir(directory)
        print "Creating Library Directory in  ",directory

class SelectionLibrary(dict):
    
    def storeSelection(self, selectionName):
        info = {}
        #store the current selection in the dictionary
        selection = cmds.ls(selection=True)
        
        info['selection'] = selection
        info['name'] = selectionName

        #collect original visibility state
        visHome = []
        for object in selection:
            current = cmds.getAttr(object+'.visibility')
            visHome.append(current)

        info['visibility'] = visHome
        info['vistoggle'] = False

        self[selectionName] = info

    def writeSave(self, fname='default'):
        filename = fname.split('.')
        filename = filename[0]

        #make a directory to save the icons and json
        #NOTE forcing / on path for readbility with the maya but seems fine on windows...
        defDIR = os.path.join(PWD, 'animina/')
        iconDIR = os.path.join(defDIR, filename)

        if not os.path.exists(defDIR):
            os.mkdir(defDIR)

        if not os.path.exists(iconDIR):
            os.mkdir(iconDIR)

        #clear current contents of save directory
        oldfiles = os.listdir(iconDIR)
        
        for f in oldfiles:
            os.remove(os.path.join(iconDIR,f))

        infoFile = os.path.join(iconDIR, '%s.json' % filename)
        
        #cmds.file(rename = infoFile)
        
        currentKeys = self.keys()
        for f in currentKeys:
            screenFile = os.path.join(LIBDIR, '%s.jpg' % f)
            newFile = os.path.join(iconDIR, '%s.jpg' % f)

            #print "Writing ", newFile
            copyfile(screenFile, newFile)

            #update path in dictionary
            self[f]['path'] = newFile

        with open(infoFile, 'w') as f:
            json.dump(self, f, indent=4)

        outputline = "Saved "+"<<"+filename+">>"+" to "+iconDIR
        print outputline
        sys.stdout.write(outputline)

    def find(self, directory=LIBDIR):

        if not os.path.exists(directory):
            return
        
        #find files with jpg extension
        files = os.listdir(directory)
        screenFiles = [f for f in files if f.endswith('.jpg')]
        
        if files:
            for screen in screenFiles:
                #split filenames and path
                name, ext = os.path.splitext(screen)
                path = os.path.join(directory, screen)

                #if the screenshot matches a key then add the path
                if name in self.keys():
                    #print "adding screenshot path"
                    self[name]['path'] = path

    def loadSave(self, fname='default'):
        filename = fname.split('.')
        filename = filename[0]

        defDIR = os.path.join(PWD, 'animina/')
        iconDIR = os.path.join(defDIR, filename)

        infoFile = os.path.join(iconDIR, filename+'.json')

        files = os.listdir(iconDIR)
        jFiles = [f for f in files if f.endswith('.json')]
        if filename+'.json' in jFiles:
            
            with open(infoFile, 'r') as f:
                info = json.load(f)
        else:
            return

        outputline = "Restored "+"<<"+filename+">>"+" from "+iconDIR
        print outputline
        sys.stdout.write(outputline)

        keys = info.keys()        
        #replace working dictionary with saved version        
        for key in keys:
            self[key] = info[key]
               
        #put the images back in the working library
        for key in keys:
            screenFile = self[key]['path']
            newFile = os.path.join(LIBDIR, '%s.jpg' % key)
            copyfile(screenFile, newFile)

    def saveScreenshot(self, name, directory=LIBDIR):
        path = os.path.join(directory, '%s.jpg' % name)
        
        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat',8)
        
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200, showOrnaments=False, startTime=1, endTime=1, viewer=False)
        return path

    def clearLibrary(self, directory=LIBDIR):

        if not os.path.exists(directory):
            return
        
        files = os.listdir(directory)
        screenFiles = [f for f in files if f.endswith('.jpg')]

        for fname in screenFiles:
            filepath = os.path.join(directory,fname)
            os.remove(filepath)
            #print 'Deleted ', filepath
            #delete contents of library directory
