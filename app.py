from flask import Flask, render_template, request, url_for
import qrcode
import os
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/generate-qr', methods=['GET'])
def generate_qr():
    url = request.args.get('url')
    if not url:
        return {"error": "URL parameter is missing."}, 400

    img = qrcode.make(url)
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template('qr_display.html', qr_image=img_data)

if __name__ == '__main__':
    app.run(debug=True)
