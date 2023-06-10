import hou, os, shutil

scenepath = hou.hipFile.path().split("/")[:-1]
scenedir = "/".join(scenepath)
try:
    node = hou.selectedNodes()[0]
    nodeType = str(node.type()).split(" ")[-1][:-1]
except:
    hou.ui.displayMessage("You need to select a cache node!", severity=hou.severityType.Error)
    quit()
    
lst = ['geometry', 'rop_geometry', 'filecache::2.0']

if not nodeType in lst:
    hou.ui.displayMessage("You need to select a cache node type!", severity=hou.severityType.Error)
    quit()

tmppath = scenedir + "/.tmp/" + str(node)
flush = hou.ui.displayConfirmation("Do you want to flush previous takes?")

if flush:
    try:
        shutil.rmtree(tmppath)
        hou.ui.displayMessage("Previous takes flushed successfully!")
    except:
        hou.ui.displayMessage("Email take flushed already, you do not need to flush it")
    