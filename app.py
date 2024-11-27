from flask import Flask, request, jsonify, send_file, render_template
import face_recognition
from PIL import Image, ImageDraw
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return jsonify({'message': 'No faces detected in the image'}), 200

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # Load an emoji image
    emoji = Image.open("emoji.png")

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_width = right - left
        face_height = bottom - top

        # Resize emoji to fit the face
        emoji_resized = emoji.resize((face_width, face_height))

        # Paste the emoji over the face
        pil_image.paste(emoji_resized, (left, top), emoji_resized)

    # Save the modified image to a BytesIO stream
    img_io = io.BytesIO()
    pil_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    # Ensure the templates folder exists
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Create an example HTML template
    with open('templates/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Emoji Face Mask</title>
</head>
<body>
    <h1>Upload an Image</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*">
        <button type="submit">Upload</button>
    </form>
</body>
</html>""")

    app.run(debug=True)