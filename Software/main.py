from fastapi import FastAPI
import datetime
import json
import xml.etree.ElementTree as ET
import zipfile 
import os
import uuid
import numpy as np
import tensorflow as tf

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
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Add the rest of the topic fields as sub-elements
    ET.SubElement(topic, "ReferenceLink").text = topic_data["ReferenceLink"]
    ET.SubElement(topic, "Title").text = topic_data["Title"]
    ET.SubElement(topic, "Priority").text = topic_data["Priority"]
    ET.SubElement(topic, "Index").text = str(topic_data["Index"])
    ET.SubElement(topic, "Labels")  # Empty element
    ET.SubElement(topic, "CreationDate").text = current_datetime
    ET.SubElement(topic, "CreationAuthor").text = topic_data["CreationAuthor"]
    ET.SubElement(topic, "ModifiedDate").text = current_datetime
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
    classes_names = ['Clean', 'Damaged', 'Dirty']
    model = tf.keras.models.load_model("model.keras")
    prediction = model.predict(tf.expand_dims(image, axis=0))
    prediction = classes_names[np.argmax(prediction)]
    return classes_names

def checkCo2(co2):
    return co2>800

def checkTemp(temp):
    return not 15>=temp>=25

def checkall(image,co2,temp):
    return [checkSolar_panel(image),checkCo2(co2),checkTemp(temp)]


def selectTopic(topics,title):
    for topic in topics:
        if topic["Title"] == title:
            create_xml_from_json(topic, f"./{topic['topic']['Guid']}/markup.bcf")

@app.post("/report/")
def getreport(info):
    with open('topics.json', 'r') as f:
        json_data = json.load(f)
    try:
        camera = info["camera"]
        temp = info["temp"]
        co2 = info["co2"]
        checks = checkall(camera["val"],co2["val"],temp["val"])
        
        for i,check in enumerate(checks) :
            if check:
                if i==0 and check!="Clean":
                    if check=="Dirty":
                        title = "solar panel water-cleaning"
                        selectTopic(json_data,title)
                    else:
                        title = "solar panel damage"
                        selectTopic(json_data,title)
                elif i==1:
                    title_1 = "HVAC systems" 
                    title_2 = "Co2 monitoring"
                    selectTopic(json_data,title_1)
                    selectTopic(json_data,title_2)
                else:
                    title_1 = "Temperature level monitoring"
                    title_2 = "Air conditioning system"
                    selectTopic(json_data,title_1)
                    selectTopic(json_data,title_2)
                    


        return {"message":"reccieved","statuCode":200}
    except :
        return {"message":"error","statuCode":500}