import os, shutil, sys, hou

scenepath = hou.hipFile.path().split("/")[:-1]
scenedir = "/".join(scenepath)
scenename = hou.hipFile.basename().replace(".hip", "")
cachenode = hou.node("..").name()

directory = ".tmp/%s" %  (cachenode)
path = os.path.join(scenedir, directory)
emailpath = path + "/email.txt"
num = hou.expandString("$WEDGENUM")

if not os.path.exists(emailpath):
    cacheLst = ("Normal Cache", "Wedge Cache", "Cancel")
    cacheType = hou.ui.displayCustomConfirmation("What type of cache are you running?", cacheLst)
    wedgenode = 'None'
    wedge_val = None
    wedgeType = 'None'

    if cacheType == 2:
        msg = "Render Canceled"
        hou.ui.displayMessage(msg, severity=hou.severityType.Message)
        raise hou.NodeError("Canceled")
    
    if cacheLst[cacheType] == "Wedge Cache":
        wedgenode = hou.ui.selectNode(title="Select the Wedge Node:")
        if wedgenode == None:
            raise hou.NodeError("Canceled")
        
        else:
            try:
                wedgeType = str(hou.nodeType(wedgenode)).split(" ")[-2]
            except:
                msg = "The node you selected is not a wedge!"
                hou.ui.displayMessage(msg, severity=hou.severityType.Error)
                raise hou.NodeError("Canceled")

            if wedgeType == "Driver":
                wedge_val = hou.node(wedgenode).parm("numrandom").eval()
            elif wedgeType == "Top":
                wedge_val = hou.node(wedgenode).parm("wedgecount").eval()
            else:
                msg = "The node you selected is not a wedge!"
                hou.ui.displayMessage(msg, severity=hou.severityType.Error)
                raise hou.NodeError("Canceled")

    email = hou.ui.readMultiInput("Email Sender", ("Send Email To: ",))[1][0]
    
    if email == "":
        msg = "You need to set an email in order to send the information"
        hou.ui.displayMessage(msg, severity=hou.severityType.Error)
        raise hou.NodeError("Canceled")
    
    if not "@gmail.com" in email:
        msg = "The email %s is not a gmail adress!" % email
        hou.ui.displayMessage(msg, severity=hou.severityType.Error)
        raise hou.NodeError("Canceled")
    
    os.makedirs(path, exist_ok=True)
    hidfldr = scenedir + '/.tmp'
    os.system("attrib +s +h %s" % hidfldr)

    with open(emailpath, 'w+') as f:
        txt = [email, cacheLst[cacheType], wedgenode, wedgeType, str(wedge_val)]
        report = "\n".join(txt)
        f.write(report)

else:
    with open(emailpath, 'r') as f:
        try:
            wedge_check = f.readlines()[1]
        except:
            hou.ui.displayMessage("You might need to flush previous versions")
            raise hou.NodeError("Canceled")
    if "Wedge" in wedge_check:
        if num == "0":
            hou.ui.displayMessage("You might need to flush previous versions")
            with open(emailpath, 'w+') as g:
                g.write("Needs to be updated") 
            raise hou.NodeError("Canceled")
    else:
        hou.ui.displayMessage("You might need to flush previous versions")
        with open(emailpath, 'w+') as g:
                g.write("Needs to be updated")
        raise hou.NodeError("Canceled")
    
    

