import json
import cv2
import numpy as np
import base64


def encode_image_to_base64(image):

    """Encodes an image to a Base64 string without saving to disk."""
    _, buffer = cv2.imencode(".png", image)
    # Convert the image buffer to bytes
    image_bytes = buffer.tobytes()
    # Encode the bytes to a Base64 string
    return base64.b64encode(image_bytes).decode("utf-8")

def decode_base64_img(encoded_img):
    # Decode Base64 string to bytes
    image_bytes = base64.b64decode(encoded_img)
    # Convert bytes to NumPy array    
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode NumPy array to OpenCV image
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)


def lambda_handler(event, context):
    # Get the image data from the event
    img_base64 =  event['body']
    # Decode the Base64 string to an OpenCV image
    img = decode_base64_img(img_base64)
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Encode the grayscale image to Base64
    gray_base64 = encode_image_to_base64(gray_img)
    

    return {
        'statusCode': 200,
        'body': gray_base64,
        "isBase64Encoded": True,
        'headers': {
            'Content-Type': 'image/png',
        }
    }
