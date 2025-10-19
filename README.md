# Bird-Detector

About:
An embeedded camera vision & AI project, using a self-trained TensorFlow Lite model to detect Birds. Project is intended to run on a BeagleBone Black with use of OpenCV. Uses a specially formated mini SD card, flashed with a customised, minimal Debian Bookworm image, faciliting neural networking based AI in a low-resource enviorment (0.5GB RAM, 1GHz CPU).

Project Objectives:
- Accurately detect birds for images taken with the embedded system
- Integrate a Neural Network, image processing, image capture on a low-resource embedded system (BeagleBone Black)
- Self-train a Neural Network for image processing (with TensorFlow) from scratch with high accuracy for detecting birds
- Learn how to configure a bookworm image for the use of large software on a low-resource embedded system


Materials/Resources required:
- BeagleBone Black
- mini SD card with high transfer speeds; >= 256GB (option to adjust .img file for lower capacity miniSD)
- Webcam with standard USB-A connector to BBB
- PC with WSL capability, or Linux based PC; preferably access to a Workspace for NeuralNetwork training to offload work

High Level Step-by-Step:

1. Adjust a pre-built Debian Bookworm image to expand image capacity. Adding an extended partition and a data partion at 150GB. This is a requirement for the heavy install of opencv and tensorflow-lite for the limited storage on the BBB. BBB will boot and run off SD card.
2. Download, Cmake, make, install opencv and tensorflow lite on SD card. Utilise /tmp folder on SD card to ensure adqueate capacity.
3. On BBB run test compilation for a .cpp file using opencv, to capture and process an image from connected webcam. 
4. On your PC: produce image database, prepare pipline, train a NN in different layers -> produce reliable .tflite model for bird recognition check for for use on BBB.
5. Utilise the .tflite model in consujunction with OpenCV and TensorFlow Lite to compile a programme, which takes an image, saves it and then calculates the probability of a bird being present in the taken image.
6. Test your project on variety of pictures, e.g. take pictures off a monitor displaying birds, other animals, or backgrounds. -> This is shown in the demonstration_video.mp4 file, have a look.

Outcome:
- Approx. 4 second processing time from command to bird detection probablity outcome
- 97% accuracy for images in city and nature enviorments (as per training set); shortfalls on non-nature objects, i.e.: planes, indoor images
- Proficicency in debugging for building software and debugging scripts
- Proficency in use of TensorFlow and OpenCV
- Proficency in navigating Linux

Licensing & Attribution

This project uses only open-source tools and libraries, including TensorFlow Lite and OpenCV, under their respective licenses.  
All training data, code, and models included here are original or publicly available for non-commercial use.
Some sections of this project were developed with the assistance of OpenAI. All results and implementation decisions were reviewed, tested, and finalized by the author.
If you believe any additional license attribution is required, please reach out.

