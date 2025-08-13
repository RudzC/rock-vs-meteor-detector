# Rock vs. Meteor Detector - Flask App

### Detect meteorites vs. rocks in uploaded images using a YOLOv11 model trained on the [Meteor vs. Rock Dataset](https://universe.roboflow.com/aiprojects-jxzlb/merged_meteorvsrock) 

---

### Model

**Architecture:** YOLOv11 (Ultralytics)  
**Task:** Binary detection – Meteorite vs. Rock  
**Dataset:** [Roboflow Universe – Meteor vs Rock](https://universe.roboflow.com/aiprojects-jxzlb/merged_meteorvsrock)  
*Disclaimer: This model was trained on a limited dataset and may produce incorrect predictions.*

---

### Docker

Build image:
```shell
docker build -t meteorite_vs_rock_object_detection:latest --build-arg INSTALL_MODE=gpu .
```

**Note:** The `INSTALL_MODE` argument accepts:
- `"gpu"` - for CUDA-enabled environments
- `"cpu"` **default** - **recommended** for running the app in CPU-only environments

Run container:
```shell
docker run --rm -p 4000:80 --name meteor-rock meteorite_vs_rock_object_detection
```

View the app at: http://localhost:4000/

---

### CI/CD (GitHub Actions → Oracle Cloud VM)

This repository includes a deployment workflow using [appleboy/ssh-action](https://github.com/appleboy/ssh-action) to build and run the Docker image on an Oracle Compute Instance.

**Live Demo:** [Rock vs. Meteor Detector – Flask App](http://158.180.235.149/)

**Required repository secrets:**
- `HOST` – the public IP or hostname of your running instance
- `SSH_KEY` – the private key for the `ubuntu` user (no passphrase)

Pushing to the `master` branch triggers the workflow.  
The workflow connects via SSH, pulls the latest code, builds the Docker image, and starts the container bound to port 80 on the VM.

---

Health check endpoint (GET /health) for CI/CD smoke tests.

---

Usage guide with screenshots of input and output.

---

Performance metrics from training (mAP, precision/recall, confusion matrix).

Artifacts: include or link your training outputs:
import from -> model/YOLO_BBoxMeteorRockDetector_Final_20_jul/detect/meteor_rock_detector/*

Sample images (1–2 meteors, 1–2 rocks) and expected outputs.

---

Licences:

