import TransformLib
import sys
import os

transform = TransformLib.MaltegoTransform()
current_directory = sys.argv[1]

for item in os.listdir(current_directory):
    if os.path.isdir(os.path.join(current_directory,item)):
        e = TransformLib.MaltegoEntity()
        e.setType("maltego.custom.entities.explorer.directory")
        e.setValue(os.path.join(current_directory,item))
        transform.addEntityToMessage(e)
    else:
        e = TransformLib.MaltegoEntity()
        e.setType("maltego.custom.entities.explorer.file")
        e.setValue(os.path.join(current_directory,item))
        transform.addEntityToMessage(e)

transform.returnOutput()

