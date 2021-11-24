from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

MODEL = tf.keras.models.load_model(r"C:\Users\HP\Desktop\Tomato_model\1")
CLASS_NAMES = ["Bacterial Spot", "Early Blight", "Late blight",
               "Leaf Mold", "Septoria leaf spot", "Spider mites", "Target Spot",
               "YellowLeaf Curl Virus", "Mosaic Virus", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hahahah Manu here!"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)

    index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[index]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': int(confidence)
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
