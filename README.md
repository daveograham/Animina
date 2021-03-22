Welcome to Animina v0.95!

This is a selection tool for any maya user. It will help you create, store, and recall complex selections from the outliner or viewport to speed up your workflow.

<img src="https://github.com/daveograham/Animina/blob/main/animinaex.png" width="660" height="500">

----------------------

----------------------
Tips:

The widget is dockable and supports multiple selections using cmd/ctrl or shift clicks

A rigging example: select an entire joint chain from the outliner, enter a name in the Animina window and store the selection using the create button. Next select a model skin and store in the same way. You can now ctrl click both icons in the Animina window to quickly recall the selection to bind the skin.

Animation: Can you never find that pesky tounge controller buried in the mesh? Select it one time from the outliner, add to the Animina window and keep it open while animating.


------------------
Authors: David Graham (inspired by the super helpful Udemy course by Dhruv Govil)

Health warnings: Many, this is a work in progress. Currently tested on Maya 2019 & 2020, Mac and Windows.
		 Creates a folder called animinaLibrary in your maya directory. This is needed to save screenshots.

Requires the QtPy wrapper by Mottosso https://github.com/mottosso/Qt.py (please check its own license requirements)
Follow the link and download the Qt.py file. Then copy to your maya scripts folder.

This project is licensed under the terms of the MIT license

-----------------------------------------------------------

INSTALLATION:
Copy the entire Animina folder to your Maya scripts folder e.g.  ../20xx/scripts

Copy the Qt.py file (from https://github.com/mottosso/Qt.py) to the ../20xx/scripts folder

Your folder should look like this:

../scripts/Qt.py

../scripts/animina/__ init__.py

../scripts/animina/animinaUI.py

../scripts/animina/animinaLibrary.py

../scripts/animina/helpDialog.py

../scripts/animina/Animina_small.jpg


In Maya, run these two lines in the script editor or add to a custom shelf button:

--------------------------------

from animina import animinaUI

animinaUI.SelectionUI()

--------------------------------


CHANGE LOG:

New in v0.95 - Fixed a bug where saving a selection to disc would change the current Maya scenefile name. Loading also now replaces the current selections in the animina window.

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
