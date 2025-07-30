from flask import Flask, render_template, request, url_for
import cv2
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files.get('image')
    if not file:
        return "No image uploaded", 400

    original_path = os.path.join(UPLOAD_FOLDER, 'original.png')
    sketch_path = os.path.join(OUTPUT_FOLDER, 'sketch.png')
    
    file.save(original_path)

    # Image to sketch conversion
    img = cv2.imread(original_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    inv_blur = 255 - blur
    sketch = cv2.divide(gray, inv_blur, scale=256.0)
    cv2.imwrite(sketch_path, sketch)

    return render_template(
        'index.html',
        original=url_for('static', filename='uploads/original.png'),
        sketch=url_for('static', filename='output/sketch.png')
    )

if __name__ == '__main__':
    app.run(debug=True)
