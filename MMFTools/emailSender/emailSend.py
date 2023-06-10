import smtplib, hou, os, shutil

from email.mime.text import MIMEText

scenepath = hou.hipFile.path().split("/")[:-1]
scenedir = "/".join(scenepath)
scenename = hou.hipFile.basename().replace(".hip", "")
cachenode = hou.node("..").name()

directory = ".tmp/%s" %  (cachenode)
path = os.path.join(scenedir, directory)
emailpath = path + "/email.txt"
num = hou.expandString("$WEDGENUM")

port = 465
sender = 'houdinirenderhub@gmail.com'
with open(emailpath) as f:
    info = f.readlines()
    receiver = info[0]
    cacheType = info[1]
    try:
        numwedges = int(info[4])-1
    except:
        pass

cache = hou.pwd().path().split("/")[-2]
filepath = hou.node("..").parm("file").rawValue()

lines = [
    "This email is sent in order to notify that the following node cache",
    " just finished:\n",
    cache ,
    " - ",
    filepath
]

report = "".join([line for line in lines])
msg = MIMEText(report)

msg['Subject'] = cache + " DONE"
msg['From'] = 'houdinirenderhub@gmail.com'
msg['To'] = receiver

user = 'houdinirenderhub'
password = 'anwkcjdxmescraez'

if "Wedge" in cacheType:
    if str(numwedges) == num:
        with smtplib.SMTP_SSL("smtp.gmail.com") as server:
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
        shutil.rmtree(path)
else:
    with smtplib.SMTP_SSL("smtp.gmail.com") as server:
        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())
    shutil.rmtree(path)

