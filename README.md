# Rock vs. Meteor Detector - Flask App

### Detect meteorites vs. rocks in uploaded images using a YOLOv11 model trained on the [Meteor vs. Rock Dataset](https://universe.roboflow.com/aiprojects-jxzlb/merged_meteorvsrock) 

---

### Model

**Architecture:** YOLOv11 [YOLO11n](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt) from (Ultralytics)  
**Task:** Binary detection – Meteorite vs. Rock  
**Dataset:** [Roboflow Universe – Meteor vs Rock](https://universe.roboflow.com/aiprojects-jxzlb/merged_meteorvsrock) Annotated using Bounding Boxes  
*Disclaimer: This model was trained on a limited dataset and may produce incorrect predictions.*

---

### Docker

Clone project:
```shell
git clone https://github.com/RudzC/rock-vs-meteor-detector.git && cd rock-vs-meteor-detector
```

Build image:
```shell
docker build -t meteorite_vs_rock_object_detection:latest --build-arg INSTALL_MODE=cpu .
```
            
Run container:
```shell
docker run -d --cpus 1.0 -p 4000:80 --name meteorite_vs_rock_object_detection --restart unless-stopped meteorite_vs_rock_object_detection
```

Clone, Build and Run on **GPU** (Optional):
```shell
git clone https://github.com/RudzC/rock-vs-meteor-detector.git && cd rock-vs-meteor-detector
docker build -t meteorite_vs_rock_object_detection:gpu --build-arg INSTALL_MODE=gpu .
docker run --rm --gpus all -p 4000:80 --name meteor-rock meteorite_vs_rock_object_detection:gpu
```

View the app at: http://localhost:4000/

**Notes:** The `INSTALL_MODE` argument accepts:
- `"cpu"` **default** - **recommended** for running the app in CPU-only environments
- `"gpu"` - for CUDA-enabled environments 

*Use the provided shell command examples for Cloning/Building/Running a functional working version of the App.*

**Optionally:** Run Without Docker

```shell
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Go to: http://localhost:4000

### App Usage

1. Navigate and load application in browser using the above provided local URL.
2. On the home page click on the choose file input form and select an image containing the Meteorite or Rock that you wish the model to classify
3. After selecting the desired image click the upload button to trigger the models' detect method.
4. In just a few seconds the image will be displayed showcasing the models' prediction label and accuracy score. 

*The reset button can be used to reset the Input and Output displayed on the screen.*

---

### CI/CD (GitHub Actions → Oracle Cloud VM)

This repository includes a deployment workflow using [appleboy/ssh-action](https://github.com/appleboy/ssh-action) to build and run the Docker image on an Oracle Compute Instance.

**Required repository secrets:**
- `HOST` – the public IP or hostname of your running instance
- `SSH_KEY` – the private key for the `ubuntu` user (no passphrase)

Pushing to the `master` branch triggers the workflow.  
The workflow connects via SSH, pulls the latest code, builds the Docker image, and starts the container bound to port 80 on the VM.

**Live Demo:** [Rock vs. Meteor Detector – Flask App](http://158.180.235.149/)

**Notes**: The deploy-master.yml currently configured for CPU. Make sure to use the proper docker commands when switching to GPU.

---

### Model Metrics and Evaluations

**Performance metrics from training (mAP, precision/recall, confusion matrix).**
<img loading="lazy" width="auto" height="auto" src="/model/YOLO_BBoxMeteorRockDetector_Final_20_jul/detect/meteor_rock_detector/results.png" alt="results png" />
*Image 1: training and validation metrics*

**Confusion matrix from training.**
<img loading="lazy" width="auto" height="auto" src="/model/YOLO_BBoxMeteorRockDetector_Final_20_jul/detect/meteor_rock_detector/confusion_matrix.png" alt="results png" />
*Image 2: confusion matrix results*

> Note: More detailed training metrics and example detections are available in **model/YOLO_BBoxMeteorRockDetector_Final_20_jul/detect/meteor_rock_detector/**

---

### Licences

