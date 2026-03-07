#-- app.py --#
from flask import Flask, render_template, request, send_from_directory
import os
import sys

# Thiết lập đường dẫn đến folder Training và Results
current_dir = os.path.dirname(os.path.abspath(__file__))
training_path = os.path.join(current_dir, "Training")
results_path = os.path.join(current_dir, "Results")

if training_path not in sys.path:
    sys.path.append(training_path)

from Brain import run_analysis #

app = Flask(__name__)

# Route để Flask có thể hiển thị ảnh từ folder Results ra Web
@app.route('/Results/<filename>')
def display_results(filename):
    return send_from_directory(results_path, filename)

@app.route('/', methods=['GET', 'POST']) # Cho phép cả GET và POST để fix lỗi 405
def index():
    data_folder = os.path.join(current_dir, "Data")
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
    csv_files.sort()

    results = None
    if request.method == 'POST':
        selected_file = request.form.get('file_name')
        if selected_file:
            file_path = os.path.join(data_folder, selected_file)
            # Gọi Brain xử lý và trả về dict kết quả
            results = run_analysis(file_path)

    return render_template('index.html', files=csv_files, results=results)

if __name__ == '__main__':
    app.run(debug=True)