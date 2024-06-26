from flask import Flask, send_file, request, make_response
import qrcode
from io import BytesIO

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
    
    response = make_response(send_file(img_io, mimetype='image/png'))
    response.headers['Content-Disposition'] = 'attachment; filename=qr_code.png'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
