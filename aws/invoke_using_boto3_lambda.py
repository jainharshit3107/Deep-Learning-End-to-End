import boto3
import math
import dateutil
import json
import os

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
client = boto3.client(service_name='sagemaker-runtime')
def lambda_handler(event, context):
    payload = event.read()
    payload = bytearray(payload)
    response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType="application/x-image", Body=payload)
    result = response["Body"].read()
    # result will be in json format and convert it to ndarray
    result = json.loads(result)
    # the result will output the probabilities for all classes
    # find the class with maximum probability and print the class index
    index = np.argmax(result)
    object_categories = ["Bacterial Spot", "Early Blight", "Late blight",
               "Leaf Mold", "Septoria leaf spot", "Spider mites", "Target Spot",
               "YellowLeaf Curl Virus", "Mosaic Virus", "Healthy"]
