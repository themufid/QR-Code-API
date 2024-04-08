from flask import Flask, send_file, request, render_template_string
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Generator QR Code</h1>
    <p>Untuk menggunakan API ini, masukkan URL ke dalam kotak di bawah ini dan klik "Buat QR Code". Anda kemudian akan diarahkan ke halaman yang menampilkan QR Code yang dihasilkan dengan opsi untuk mendownloadnya sebagai gambar PNG.</p>
    <form action="/generate-qr" method="get">
        <input type="text" name="url" placeholder="Masukkan URL" />
        <input type="submit" value="Buat QR Code" />
    </form>
    '''

@app.route('/generate-qr', methods=['GET'])
def generate_qr():
    url = request.args.get('url')
    if not url:
        return {"error": "Parameter URL tidak ada."}, 400
    
    img = qrcode.make(url)
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    img_data = img_io.getvalue()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Code Result</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
            }}
            .download-button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                outline: none;
                color: #fff;
                background-color: #4CAF50;
                border: none;
                border-radius: 15px;
                box-shadow: 0 9px #999;
                margin-top: 20px;
            }}

            .download-button:hover {{background-color: #3e8e41}}

            .download-button:active {{
                background-color: #3e8e41;
                box-shadow: 0 5px #666;
                transform: translateY(4px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>QR Code Anda</h1>
            <p>QR Code berhasil dibuat. Anda dapat mendownload gambar QR Code dengan mengklik tombol di bawah ini.</p>
            <img src="data:image/png;base64,{encoded_img_data}" alt="QR Code" /><br>
            <a href="/download-qr?url={url}" class="download-button">Download QR Code</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/download-qr')
def download_qr():
    url = request.args.get('url')
    if not url:
        return {"error": "Parameter URL tidak ada."}, 400
    
    img = qrcode.make(url)
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qr_code.png')

if __name__ == '__main__':
    app.run(debug=True)
