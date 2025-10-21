# 🐦 Bird Detector

> **An embedded AI vision project** built to detect birds using a self-trained TensorFlow Lite model running on a **BeagleBone Black** board with **OpenCV**.

---

## 📖 About the Project

**Bird Detector** is an embedded computer vision and AI system designed to identify birds in real-time using a **custom-trained TensorFlow Lite model**.  
It runs on a **BeagleBone Black** — a low-resource embedded platform (0.5 GB RAM, 1 GHz CPU) — powered by a **custom minimal Debian Bookworm image** optimized for AI workloads.

🧠 The goal is to demonstrate efficient neural network inference and image processing on constrained hardware.

---

## 🎯 Project Objectives

- 🐦 Accurately detect birds in captured images  
- ⚙️ Integrate image capture, OpenCV-based processing, and neural inference on BeagleBone Black  
- 🧩 Train a custom neural network (TensorFlow) from scratch for bird detection  
- 🧰 Learn how to configure and optimize a Debian Bookworm image for running large software on limited hardware  

---

## 🧱 Materials & Resources

| Component | Purpose |
|------------|----------|
| **BeagleBone Black (BBB)** | Target embedded system |
| **Mini SD Card (≥ 256 GB, high-speed)** | Storage for Debian image, OpenCV, TensorFlow Lite |
| **USB Webcam** | Image capture |
| **PC with WSL or Linux** | For dataset preparation, neural network training, and model export |

> 💡 *You can adjust the `.img` file for smaller SD cards if needed.*

---

## 🧩 High-Level Steps

1. 🧰 **Prepare the Image**  
   Expand a pre-built Debian Bookworm image to add extended and data partitions (~150 GB).  
   This supports TensorFlow Lite and OpenCV installation. The BBB will boot and operate entirely from the SD card.

2. ⚙️ **Install Dependencies**  
   Build and install OpenCV and TensorFlow Lite on the SD card using CMake and Make.  
   Use `/tmp` to buffer compilation to prevent storage overflow.

3. 📸 **Test OpenCV**  
   On the BBB, compile and run a simple C++ program to capture and process an image from the connected webcam.

4. 💻 **Train the Neural Network**  
   On your PC:
   - Build a training dataset  
   - Create a data pipeline  
   - Train and test a convolutional neural network  
   - Export the final `.tflite` model for deployment  

5. 🧠 **Integrate AI on BeagleBone**  
   Combine OpenCV and TensorFlow Lite in a C++ program to:
   - Capture and save an image  
   - Perform inference using the `.tflite` model  
   - Output the probability of a bird being detected  

6. 🎥 **Evaluate Results**  
   Test using a range of images — from real-life captures to pictures of birds on a screen.  
   See results demonstrated in `demonstration_video.mp4`.

   Exmaple screengrab:
   <img width="2962" height="1819" alt="sample" src="https://github.com/user-attachments/assets/6346c9b2-f9a3-4ddd-bfd0-9e869a2942ce" />
   📸 Image Sources & Copyright
   | Image | Source |
   |--------|---------|
   | 🐦 **Bird** | [https://share.google/images/2Tbj2tCM9aaDRsCms](https://share.google/images/2Tbj2tCM9aaDRsCms) |
   | 🐄 **Cow**  | [https://share.google/images/bOBIeDCsq6d1UeGOL](https://share.google/images/bOBIeDCsq6d1UeGOL) |

---

## 📊 Outcomes

- ⚡ **Processing time:** ~4 seconds from capture to classification  
- 🎯 **Accuracy:** ~97 % (in nature and city images)  
- 🧩 **Limitations:** Misclassifications on non-natural objects (planes, indoor scenes)  
- 💻 **Skills Developed:**  
  - Debugging complex builds and scripts  
  - TensorFlow and OpenCV proficiency  
  - Embedded Linux navigation and optimization  

---

## ⚖️ Licensing & Attribution

This project uses **open-source tools and libraries**, including **TensorFlow Lite** and **OpenCV**, under their respective licenses.  

All training data, code, and models are **original** or **publicly available** for non-commercial use.  

Some components were developed with assistance from **OpenAI tools**, with all design and implementation verified and finalized by the author.  

If you believe any additional license attribution is needed, please reach out.

---

## 💬 Author

**felilos**  
📧 dnbtodubsteptofac@gmail.com  


