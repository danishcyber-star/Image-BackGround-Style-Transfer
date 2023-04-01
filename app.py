from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

app = Flask(__name__)

hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[0], shape[1])
    offset_y = max(shape[0] - shape[1], 0) // 2
    offset_x = max(shape[1] - shape[0], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

def load_image(uploaded_file, image_size=(256, 256)):
    img = Image.open(uploaded_file)
    img = tf.convert_to_tensor(img)
    img = crop_center(img)
    img = tf.image.resize(img, image_size)
    if img.shape[-1] == 4:
        img = img[:, :, :3]
    img = tf.reshape(img, [-1, image_size[0], image_size[1], 3])/255

    return img

def apply_style(content_image, style_image):
    style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    return stylized_image.numpy()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stylize', methods=['POST'])
def stylize():
    content_image = load_image(request.files['content'])
    style_image = load_image(request.files['style'])
    stylized_image = apply_style(content_image, style_image)
    return jsonify({'result': stylized_image.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
