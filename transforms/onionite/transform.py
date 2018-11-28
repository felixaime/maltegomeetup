from lxml import etree
import TransformLib
import argparse
import requests
import sys
import re


"""
    Transform: ONIONITE
    Description: Get infos about TOR Nodes by using onionite.now.sh
    Author: Felix Aime (@felixaime)
    
    Output entities:
       - maltego.custom.entities.infrastructure.TorExitNode
       - maltego.custom.entities.infrastructure.TorNickName
       - maltego.IPv4Address
"""

class Transform():

    def __init__(self):
        self.transform     = TransformLib.MaltegoTransform()
        self.parent_fields = self._additional_fields_to_dict()
        self.value         = None


    def _additional_fields_to_dict(self):
        """
            Method : _additional_fields_to_dict
            Description : Translate additional fields to dict.
            Arguments : No.
        """
        rtn = {"parent.entity.value" : ""}
        for i, field in enumerate(sys.argv[3].split("#")):
            field = field.split("=")
            if i == 0:
                rtn["entity.value"] = field[1]
            else:
                rtn[field[0]] = field[1]
        return rtn

    def ipv4_to_exitnode(self):
        """
            TOR exit nodes from IPv4 Address
        """
        res  = requests.get("https://onionite.now.sh/?s=%s" % (self.value))
        tree = etree.fromstring(res.content, etree.HTMLParser())

        for td in tree.xpath("/html/body/main/table/tbody/tr"):
            exit_node = td[1][0].attrib["href"][-40:]
            if self.parent_fields["parent.entity.value"] != exit_node:
                e = TransformLib.MaltegoEntity()
                e.setType("maltego.custom.entities.infrastructure.TorExitNode")
                e.addAdditionalFields(fieldName="nickname",
                                      displayName="Nickname", 
                                      value=str(td[1][0].text),
                                      matchingRule="strict")
                e.addAdditionalFields(fieldName="parent.entity.value",
                                      displayName="Parent Entity", 
                                      value=self.value)
                
                e.setValue(exit_node)
                self.transform.addEntityToMessage(e)

        self.transform.returnOutput()

    def exitnode_to_nickname(self):
        """
            Extract the nickname for the additional fields 
            of a Tor Exit node entity.
        """
        if "nickname" in self.parent_fields:
            if self.parent_fields["parent.entity.value"] != self.parent_fields["nickname"]:
                e = TransformLib.MaltegoEntity()
                e.setType("maltego.custom.entities.infrastructure.TorNickName")
                e.addAdditionalFields(fieldName="parent.entity.value",
                                      displayName="Parent Entity", 
                                      value=self.value)

                e.setValue(self.parent_fields["nickname"])
                self.transform.addEntityToMessage(e)
        self.transform.returnOutput()    

    def nickname_to_exit_nodes(self):
        """
            Retreive TOR exit nodes from a specific 
            nickname.
        """
        res  = requests.get("https://onionite.now.sh/?s=%s" % (self.value))
        tree = etree.fromstring(res.content, etree.HTMLParser())
        
        for td in tree.xpath("/html/body/main/table/tbody/tr"):
            exit_node = td[1][0].attrib["href"][-40:]
            if self.parent_fields["parent.entity.value"] != exit_node:
                e = TransformLib.MaltegoEntity()
                e.setType("maltego.custom.entities.infrastructure.TorExitNode")
                e.addAdditionalFields(fieldName="nickname",
                                      displayName="Nickname", 
                                      value=str(td[1][0].text),
                                      matchingRule="strict")
                e.addAdditionalFields(fieldName="parent.entity.value",
                                      displayName="Parent Entity", 
                                      value=self.value)
                e.addAdditionalFields("link#maltego.link.direction",
                                      "link#maltego.link.direction",
                                      "loose",
                                      "output-to-input")
                e.setValue(exit_node)
                self.transform.addEntityToMessage(e)

        self.transform.returnOutput()

    def exit_node_to_ipv4(self):
        """
            Extract the nickname for the additional fields 
            of a Tor Exit node entity.
        """
        res  = requests.get("https://onionite.now.sh/node/%s" % (self.value))
        tree = etree.fromstring(res.content, etree.HTMLParser())
        dd   = tree.xpath("/html/body/main/div[2]/section[1]/dl/dd[3]")
        
        ip_address = dd[0].text.split(":")[0]
        if self.parent_fields["parent.entity.value"] != ip_address:
            e = TransformLib.MaltegoEntity()
            e.setType("maltego.IPv4Address")
            e.addAdditionalFields("link#maltego.link.direction",
                                  "link#maltego.link.direction",
                                  "loose",
                                  "output-to-input") 
            e.addAdditionalFields(fieldName="parent.entity.value",
                                  displayName="Parent Entity", 
                                  value=self.value)
            e.setValue(ip_address)
            self.transform.addEntityToMessage(e)

        self.transform.returnOutput()  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", type=str, help="The method to ask")
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