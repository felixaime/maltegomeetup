import TransformLib
import argparse
import subprocess
import sys
import os
import re

"""
    Transform: EXIFTOOL
    Description: Retreives file metadata by using exiftool
    Author: Felix Aime (@felixaime)
    
    Output entities:
       - maltego.Alias
       - maltego.Date
       - maltego.Software
       - maltego.GPS
"""

class Transform():

    def __init__(self):
        self.transform     = TransformLib.MaltegoTransform()
        self.value         = None
        self.parent_fields = self._additional_fields_to_dict()

    def _additional_fields_to_dict(self):
        """
            Description : Translate additional fields to dict.
        """
        rtn = {"parent.entity.value" : "", "entity.value" : ""}
        try:
            for i, field in enumerate(sys.argv[3].split("#")):
                field = field.split("=")
                if i == 0:
                    rtn["entity.value"] = field[1]
                else:
                    rtn[field[0]] = field[1]
        except:
            pass
        return rtn

    def extract_metadata(self):
        """
            Get the metadata of a file
        """

        if "/" in self.value:
            current_file = self.value
        elif "full_path" in self.parent_fields:
            current_file = self.parent_fields["full_path"]
        else:
            print("<!-- Please specify a full path -->")
            exit()

        p   = subprocess.run( [ "exiftool", current_file ],
                                shell=False,
                                stdout=subprocess.PIPE,
                                timeout=10)
        res = (p.stdout).decode("utf-8")

        returned_values = []

        for line in res.splitlines():
            try:
                metadata_key   = line.split(" : ")[0].strip()
                metadata_value = line.split(" : ")[1].strip()

                if "Creator" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Alias")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Created by")
                        e.setValue(metadata_value)
                        self.transform.addEntityToMessage(e)
                if "Author" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Alias")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Author")
                        e.setValue(metadata_value)
                        self.transform.addEntityToMessage(e)
                elif "Last Modified By" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Alias")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",           
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Last Modified By")
                        e.setValue(metadata_value)
                        self.transform.addEntityToMessage(e)
                elif "Software" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Software")                   
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Created with")
                        e.setValue(metadata_value)
                        self.transform.addEntityToMessage(e)
                elif "GPS Position" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.GPS")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setValue(metadata_value)
                        self.transform.addEntityToMessage(e)
                elif "Modify Date" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Date")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Modified on")
                        e.setValue(metadata_value.split(" ")[0])
                        self.transform.addEntityToMessage(e)
                elif "Create Date" in metadata_key:
                    if metadata_value not in returned_values:
                        returned_values.append(metadata_value)
                        e = TransformLib.MaltegoEntity()
                        e.setType("maltego.Date")
                        e.addAdditionalFields(fieldName="parent.entity.value",
                                              displayName="Parent Entity",
                                              value=self.parent_fields["entity.value"])
                        e.setLinkLabel("Created on")
                        e.setValue(metadata_value.split(" ")[0])
                        self.transform.addEntityToMessage(e)
            except:
                continue
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