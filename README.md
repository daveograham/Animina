Welcome to Animina v0.94!

This is a selection tool for any maya user. It will help you create, store, and recall selections from the outliner to speed up your workflow.

Health warnings: Many, this is a work in progress. Currently tested on Maya 2019 & 2020, Mac and Windows.
		 Creates a folder called animinaLibrary in your maya directory. This is needed to save screenshots.

Requires the QtPy wrapper by Mottosso https://github.com/mottosso/Qt.py (please check its own license requirements)
Copy the Qt.py file to your maya scripts folder.

Authors: David Graham (inspired by the super helpful Udemy course by Dhruv Govil)

Please contact me with problems/suggestions:
daveograham@protonmail.com

This project is licensed under the terms of the MIT license


New in v0.94 - A help dialog! The UI has been rearranged a little to include a help button which explains the useage of the save/load/create buttons

New in v0.93 - Restoring a save now checks if objects have been deleted in the outliner and removes them from the groups
	       Fixed output of save paths and adds output to the command reponse window when saving
	       Paths have Maya style / separators, however they don't appear to be an issue in windows.

New in v0.92 - Saving now uses a default directory if no name is specified to save
	       saves default.json to ../scenes/animina/default   in your current project scenes folder 
	       All other saves go in named folders under ../scenes/animina/

New in v0.91 - Saving! You can now save the selection groups in the UI to the scenes folder in your current project
	       Future updates will include a proper file dialog
	     - Multiple clicks! Shift and command/control clicking the UI will select everything between clicks (shift)
	       or individual items (control). The selection is stored in the active Maya selection. Happy skin binding!

New in v0.9 - Visibility selection
	    - Joint Local Rotation Axis is hidden in the screenshot
	    - Turns off auto child selection highlighting in the screenshot

New in v0.8 - Screenshots now use isolate mode
	    - Screenshot files are now cleared at the end of the session
	    - Screenshot files are delete when clearing a selection group

New in v0.7 - Now with screenshots!


INSTALLATION:
Copy the entire Animina folder to your Maya scripts folder e.g.  ../2020/scripts
Copy Qt.py to the scripts folder

Run these two lines in the script editor or add to a custom shelf button:

from animina import animinaUI
animinaUI.SelectionUI()
