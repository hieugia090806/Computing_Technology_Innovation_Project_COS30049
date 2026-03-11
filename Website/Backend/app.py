#-- app.py --#
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Quan trọng: Cho phép React gọi API
import os
import sys

# 1. Thiết lập đường dẫn
current_dir = os.path.dirname(os.path.abspath(__file__))
training_path = os.path.join(current_dir, "Training")
results_path = os.path.join(current_dir, "Results")

# Đảm bảo folder Results tồn tại để không bị lỗi khi lưu ảnh
if not os.path.exists(results_path):
    os.makedirs(results_path)

if training_path not in sys.path:
    sys.path.append(training_path)

# Import bộ não xử lý user input
from Brain import run_analysis

app = Flask(__name__)
CORS(app) # Fix lỗi "Blocked by CORS policy" khi chạy React

# Route để Frontend lấy ảnh Confusion Matrix
@app.route('/Results/<filename>')
def display_results(filename):
    return send_from_directory(results_path, filename)

# API xử lý Email Spam (Text Input)
@app.route('/api/predict-email', methods=['POST'])
def handle_email():
    data = request.json
    content = data.get('content', '')
    # Gọi Brain với mode 'email'
    results = run_analysis(content, 'email')
    return jsonify(results)

# API xử lý URL (Link Input)
@app.route('/api/predict-url', methods=['POST'])
def handle_url():
    data = request.json
    url = data.get('url', '')
    # Gọi Brain với mode 'url'
    results = run_analysis(url, 'url')
    return jsonify(results)

# API xử lý Malware (File Upload)
@app.route('/api/predict-file', methods=['POST'])
def handle_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    # Với file, ta tạm thời lấy tên file để Brain chọn Expert Malware
    results = run_analysis(file.filename, 'file')
    return jsonify(results)

if __name__ == '__main__':
    # Chạy ở port 5000 để khớp với cấu hình Frontend của Hiếu
    app.run(debug=True, port=5000)