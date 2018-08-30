import xml.etree.ElementTree as et
import urllib2  # the lib that handles the url stuff
import os

xml_id = os.environ['PHOENIX_XML_ID']
xml_code = os.environ['PHOENIX_XML_CODE']

data = urllib2.urlopen('https://www.phoenixbse.com/index.php?a=xml&sa=pos_list&uid=' + xml_id + '&code=' + xml_code)
tree = et.parse(data)
root = tree.getroot()
class position:
    def __init__(self,data):
        self.data={}
        if data.tag=='position':
            if len(data.items())>0:
                for attrib,val in data.items():
                    self.data[attrib]=val
        for pos_data in data:
            if pos_data.tag=='ship_info':
                self.data['ship_info']={}
                if len(pos_data.items())>0:
                    for attrib,val in pos_data.items():
                        self.data['ship_info'][attrib.lower()]=val
            elif pos_data.tag=='cargo_space':
                self.data['cargo_space']={}
                for cargo in pos_data:  
                    if len(cargo.items())>0:
                        cargo_type='_'
                        for attrib,val in cargo.items():
                            if attrib=='type':
                                cargo_type=val.replace(' ','_').lower()
                        self.data['cargo_space'][cargo_type]={}
                        for attrib,val in cargo.items():
                            if attrib!='type':
                                self.data['cargo_space'][cargo_type][attrib.lower()]=val
            elif pos_data.tag=='turns':
                self.data['turns']=[]
                for turn in pos_data:  
                    if len(turn.items())>0:
                        for attrib,val in turn.items():
                            if attrib=='day':
                                self.data['turns'].append(int(val))
            else:
                self.data[pos_data.tag]=pos_data.text
pos_list=[]
for child in root:
    for data in child:
        pos=position(data)
        pos_list.append(pos)
         # testing
