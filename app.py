from flask import Flask, render_template
from model.model import YOLOModel
import os
os.environ['ULTRALYTICS_VERBOSE'] = '0'

app = Flask(__name__)
obj_detect_model = YOLOModel()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_route():
    return obj_detect_model.predict()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)