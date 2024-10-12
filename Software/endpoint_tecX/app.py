from fastapi import FastAPI, HTTPException
from main import TecX
import json
from typing import Dict, Any
from pydantic import BaseModel


app = FastAPI()


class ReportInfo(BaseModel):
    camera: Dict[str, Any]
    temp: Dict[str, Any]
    co2: Dict[str, Any]


@app.post("/report/")
def getreport(info:ReportInfo):
    with open('topics.json', 'r') as f:
        json_data = json.load(f)
    try:
        camera = info.camera
        temp = info.temp
        co2 = info.co2
        tecx = TecX(camera["value"],temp["value"],co2["value"])
        checks = tecx.checkall()
        bcfzip_elements = ["bcf.version"]
        for i,check in enumerate(checks) :
            if check:
                if i==0 and check!="Clean":
                    if check=="Dirty":
                        title = "solar panel water-cleaning"
                        bcfzip_elements.append(tecx.selectTopic(json_data,title))
                    else:
                        title1 = "solar panel damage"
                        bcfzip_elements.append(tecx.selectTopic(json_data,title1))
                elif i==1 and check:
                    print(i,check)
                    title_1 = "HVAC systems" 
                    title_2 = "Co2 monitoring"
                    bcfzip_elements.append(tecx.selectTopic(json_data,title_1))
                    bcfzip_elements.append(tecx.selectTopic(json_data,title_2))
                elif i==2 and check:
                    print(i,check)
                    title_1 = "Temperature level monitoring"
                    title_2 = "Air conditioning system"
                    bcfzip_elements.append(tecx.selectTopic(json_data,title_1))
                    bcfzip_elements.append(tecx.selectTopic(json_data,title_2))
        print(bcfzip_elements)
        tecx.zip_bcf_files(bcfzip_elements,"./","file.bcfzip")
        tecx.delFolers(bcfzip_elements)
                    


        return {"message":"reccieved","statuCode":200}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
    

