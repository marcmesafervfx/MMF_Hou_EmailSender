import hou

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

node.parm("tprerender").set(1)
node.parm("tpostrender").set(1)

node.parm("prerender").set("$HOUDINI_USER_PREF_DIR/MMFTools/emailSender/emailSave.py")
node.parm("postrender").set("$HOUDINI_USER_PREF_DIR/houdini19.0/MMFTools/emailSender/emailSend.py")

node.parm("lprerender").set("python")
node.parm("lpostrender").set("python")