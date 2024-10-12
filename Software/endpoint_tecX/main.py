import datetime
import xml.etree.ElementTree as ET
import zipfile 
import os
import uuid
import requests
import json
import zipfile
import shutil

class TecX:
    def __init__(self,image,temp,co2):
        self.image = image
        self.temp = temp
        self.co2 = co2
    
    def zip_bcf_files(self,elements, folder_path, output_bcf):
        with zipfile.ZipFile(output_bcf, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Loop through the elements list
            for file_path in elements:
                # Check if the path is a directory
                if os.path.isdir(file_path):
                    # Recursively add files from directories
                    for root, dirs, all_files in os.walk(file_path):
                        for file in all_files:
                            full_file_path = os.path.join(root, file)
                            zipf.write(full_file_path, os.path.relpath(full_file_path, folder_path))
                else:
                    # It's a file, so add it directly
                    full_file_path = os.path.join(folder_path, file_path)
                    if os.path.exists(full_file_path):
                        zipf.write(full_file_path, os.path.relpath(full_file_path, folder_path))
                    else:
                        print(f"Warning: {file_path} does not exist and was not added.")

    def create_xml_from_json(self,json_data, xml_file_path):
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
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

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
        if "documentReference" in json_data.keys():
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


    
    def checkSolar_panel(self):
        API_TOKEN = os.environ.get("API_TOKEN")

        # Your Hugging Face model URL
        API_URL = "https://aymenfk-tecx-model.hf.space/predict"

        # Headers including authorization
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        payload = json.dumps({
            "EncodedImage": self.image
        })

        # Send the POST request to TensorFlow Serving
        response = requests.post(API_URL, headers=headers,data=payload)
        return response
    

    def checkCo2(self):
        return self.co2>800

    def checkTemp(self):
        return not 15<=self.temp<=25

    def checkall(self):
        return [self.checkSolar_panel(),self.checkCo2(),self.checkTemp()]

    def delFolers(self,elements):
        elements.pop(0)
        for element in elements:
            shutil.rmtree(element)

    def selectTopic(self,topics,title):
        for topic in topics:
            if topic["Title"] == title:
                self.create_xml_from_json(topic, f"./{topic['topic']['Guid']}/markup.bcf")
                return topic["topic"]["Guid"]




