import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
from pydantic import BaseModel


app = FastAPI()


class ImageRequest(BaseModel):
    EncodedImage: str


def base64_to_image(encoded_string):
    image_data = base64.b64decode(encoded_string)
    image = Image.open(BytesIO(image_data))
    return image

def preprocess(image, target_size=(128, 128)):
    image_resized = image.resize(target_size).convert('RGB')
    image_array = np.array(image_resized)
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    return image_array

@app.get("/")
def greet_json():
    return {"Hello": "World!"}

@app.post("/predict")
async def predict(request: ImageRequest):
    encoded_image = request.EncodedImage
    image = base64_to_image(encoded_image)
    image = preprocess(image)
    image = np.expand_dims(image,axis=0)
    model = tf.keras.models.load_model("model.keras")
    prediction = np.argmax(model.predict(image))
    class_name = ['Clean', 'Damaged', 'Dirty']
    return class_name[prediction]


