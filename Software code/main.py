from fastapi import FastAPI
import time
import json
import xml.etree.ElementTree as ET
import zipfile 
import os
import uuid

# gui -> dosier with that name <- file called mrkup xml contain topic and details / next -> compression bcf.version 
# 


def create_xml_from_json(json_data, xml_file_path):
    # Create the root element <Markup>
    
    root = ET.Element("Markup")
    
    # Create the <Topic> element and set its attributes
    topic_data = json_data['topic']
    if topic_data["Guid"] == None:
        topic_data["Guid"] = uuid.uuid4()
    os.mkdir(topic_data["Guid"])
    topic = ET.SubElement(root, "Topic", {
        "Guid": topic_data["Guid"],
        "TopicType": topic_data["TopicType"],
        "TopicStatus": topic_data["TopicStatus"]
    })
    
    # Add the rest of the topic fields as sub-elements
    ET.SubElement(topic, "ReferenceLink").text = topic_data["ReferenceLink"]
    ET.SubElement(topic, "Title").text = topic_data["Title"]
    ET.SubElement(topic, "Priority").text = topic_data["Priority"]
    ET.SubElement(topic, "Index").text = str(topic_data["Index"])
    ET.SubElement(topic, "Labels")  # Empty element
    ET.SubElement(topic, "CreationDate").text = topic_data["CreationDate"]
    ET.SubElement(topic, "CreationAuthor").text = topic_data["CreationAuthor"]
    ET.SubElement(topic, "ModifiedDate").text = topic_data["ModifiedDate"]
    ET.SubElement(topic, "ModifiedAuthor").text = topic_data["ModifiedAuthor"]
    ET.SubElement(topic, "DueDate").text = topic_data["DueDate"]
    ET.SubElement(topic, "Description").text = topic_data["Description"]
    ET.SubElement(topic, "Stage")  # Empty element
    ET.SubElement(topic, "Type").text = topic_data["Type"]
    ET.SubElement(topic, "Status").text = topic_data["Status"]
    ET.SubElement(topic, "StatusNote")  # Empty element
    ET.SubElement(topic, "Budget").text = str(topic_data["Budget"])
    ET.SubElement(topic, "Progress").text = str(topic_data["Progress"])
    
    # Create the <DocumentReference> element
    doc_ref_data = json_data['documentReference']
    doc_ref = ET.SubElement(root, "DocumentReference", {
        "Guid": doc_ref_data["Guid"]
    })
    
    # Add the rest of the document reference fields as sub-elements
    ET.SubElement(doc_ref, "Filename").text = doc_ref_data["Filename"]
    ET.SubElement(doc_ref, "Description").text = doc_ref_data["Description"]
    ET.SubElement(doc_ref, "ReferencedDocument").text = doc_ref_data["ReferencedDocument"]
    
    # Write the XML to a file
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)
    

# Load JSON data from a file



app = FastAPI()

def checkSolar_panel(image):
    return model.predict(image) == 1

def checkCo2(co2):
    return co2>800

def checkTemp(temp):
    return not 15>=temp>=25

def selectTopic():
    with open('temp.json', 'r') as f:
        json_data = json.load(f)

    create_xml_from_json(json_data, f"./{json_data['topic']['Guid']}/markup.bcf")

@app.post("/report/")
def getreport(info):
    try:
        camera = info["camera"]
        temp = info["temp"]
        co2 = info["co2"]
        waterLevel = info["waterLevel"]
        

        return {"message":"reccieved","statuCode":200}
    except :
        return {"message":"error","statuCode":500}