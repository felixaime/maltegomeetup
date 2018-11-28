import TransformLib
import argparse
import sys
import os
import re

"""
    Transform: EXPLORER
    Description: Retreives a directory content
    Author: Felix Aime (@felixaime)
    
    Output entities:
       - maltego.custom.entities.explorer.directory
       - maltego.custom.entities.explorer.file
"""

class Transform():

    def __init__(self):
        self.transform     = TransformLib.MaltegoTransform()
        self.value         = None

    def get_directory_content(self):
        """
            Get the content of a directory
        """

        # Get the directory full path.
        if "/" in self.value:
            current_directory = self.value
        elif "full_path" in self.parent_fields:
            current_directory = self.parent_fields["full_path"]
        else:
            print("<!-- Please specify a full path -->")
            exit()

        # Parse the directory content.
        for item in os.listdir(current_directory):
            if os.path.isdir(os.path.join(current_directory,item)):
                e = TransformLib.MaltegoEntity()
                e.setType("maltego.custom.entities.explorer.directory")
                e.addAdditionalFields(fieldName="full_path",
                                      displayName="Full path",
                                      value=os.path.join(current_directory,item))
                e.setValue(item)
                self.transform.addEntityToMessage(e)
            else:
                e = TransformLib.MaltegoEntity()
                e.setType("maltego.custom.entities.explorer.file")
                e.addAdditionalFields(fieldName="full_path",
                                      displayName="Full path",
                                      value=os.path.join(current_directory,item))
                e.setValue(item)
                self.transform.addEntityToMessage(e)
        self.transform.returnOutput()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, help='The method to ask')
    args = parser.parse_known_args()

    method = args[0].method

    try:
        t = Transform()
        t.value = args[1][0].strip()

        if re.match("[a-zA-Z\_]+", method):
            eval("t.%s()" % (method))
    except:
        print("<!-- Issue with the transform -->")
        exit()