#include <iostream>
#include <thread>             // for this_thread::sleep_for
#include <chrono>             // for chrono::milliseconds
#include <opencv2/opencv.hpp>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/model.h"

using namespace std;
using namespace cv;

// ===============================
// CONFIGURATION
// ===============================
const string MODEL_PATH = <model_path>;
const string IMAGE_PATH = <output_path>;
const Size IMG_SIZE(128, 128);
const float THRESHOLD = 0.5f;

// ===============================
// MAIN
// ===============================
int main() {
    cout << " ^=^t  Loading TensorFlow Lite model..." << endl;
    auto model = tflite::FlatBufferModel::BuildFromFile(MODEL_PATH.c_str());
    if (!model) {
	        cerr << " ^}^l Failed to load model: " << MODEL_PATH << endl;
        return -1;
    }

    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    if (tflite::InterpreterBuilder(*model, resolver)(&interpreter) != kTfLiteOk) {
        cerr << " ^}^l Failed to build interpreter." << endl;
        return -1;
    }

    interpreter->SetNumThreads(1); // BBB is single-core heavy tasking
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        cerr << " ^}^l Failed to allocate tensors." << endl;
        return -1;
    }
    cout << " ^|^e Model loaded successfully." << endl;

    // -------------------------------
    // Capture image
    // -------------------------------
    VideoCapture cap("/dev/video0", cv::CAP_V4L2);
    if (!cap.isOpened()) {
        cerr << " ^}^l Could not open camera!" << endl;
        return -1;
    }
	

    cap.set(CAP_PROP_FRAME_WIDTH, 320);
    cap.set(CAP_PROP_FRAME_HEIGHT, 240);
    cap.set(CAP_PROP_FPS, 15);

    Mat frame;
    for (int i = 0; i < 10; ++i) {
        cap >> frame;
        if (!frame.empty()) break;
        this_thread::sleep_for(chrono::milliseconds(100));
    }

    if (frame.empty()) {
        cerr << " ^}^l Failed to capture frame." << endl;
        return -1;
    }

    imwrite(IMAGE_PATH, frame);
    cout << " ^=^s  Saved frame to " << IMAGE_PATH << endl;

    // -------------------------------
    // Preprocess image
    // -------------------------------
    Mat resized;
	resize(frame, resized, IMG_SIZE);
    cvtColor(resized, resized, COLOR_BGR2RGB);
    resized.convertTo(resized, CV_32FC3, 1.0 / 255.0);
	
    float* input = interpreter->typed_input_tensor<float>(0);
    memcpy(input, resized.data, sizeof(float) * IMG_SIZE.width * IMG_SIZE.height * 3);

    // -------------------------------
    // Run inference
    // -------------------------------
    cout << " ^z^y  ^o Running inference..." << endl;
    if (interpreter->Invoke() != kTfLiteOk) {
        cerr << " ^}^l Inference failed." << endl;
        return -1;
    }

    float* output = interpreter->typed_output_tensor<float>(0);
    float prob = output[0];

    cout << "Result: " << prob << endl;
    if (prob >= THRESHOLD)
        cout << " ^=^u^j  ^o  Bird detected! Probability: " << prob << endl;
    else
        cout << " ^=^z  No bird detected (Probability: " << prob << ")" << endl;

    return 0;
}