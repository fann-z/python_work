import os
import threading
import socket
import qrcode
from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_local_ip():
    """
    获取本机的局域网 IP 地址。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def generate_qr_code(url):
    """
    根据提供的 URL 生成二维码，并保存到静态文件夹中。
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/qr_code.png")


@app.route('/')
def index():
    """
    主页面，显示上传文件表单、已上传文件列表及二维码。
    """
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("index.html", files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    处理文件上传请求，将文件保存到指定目录。
    """
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return "File uploaded successfully!", 200


@app.route('/download/<filename>')
def download_file(filename):
    """
    提供文件下载服务。
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def run_server():
    """
    启动 Flask 服务，生成二维码并打印访问链接。
    """
    local_ip = get_local_ip()
    url = f"http://{local_ip}:5000"
    print("Starting the File Transfer System...")
    print(f"Access the system by visiting {url} in your browser.")
    generate_qr_code(url)
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    threading.Thread(target=run_server).start()
