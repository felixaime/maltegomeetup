import TransformLib
import subprocess
import sys

transform    = TransformLib.MaltegoTransform()
current_file = sys.argv[1]

p   = subprocess.run( [ "exiftool", current_file ], shell=False, stdout=subprocess.PIPE, timeout=10)
res = (p.stdout).decode("utf-8")

for line in res.splitlines():
    try:
        metadata_key   = line.split(" : ")[0].strip()
        metadata_value = line.split(" : ")[1].strip()

        if "Author" in metadata_key:
            e = TransformLib.MaltegoEntity()
            e.setType("maltego.Alias")
            e.setValue(metadata_value)
            transform.addEntityToMessage(e)
        # elif "Creator" in metadata_key...
    except:
        continue

transform.returnOutput()

