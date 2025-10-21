#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Open Logitech camera on /dev/video0 with V4L2 backend
    cv::VideoCapture cap("/dev/video0", cv::CAP_V4L2);
    if(!cap.isOpened()) {
        std::cerr << "ERROR: Could not open camera!" << std::endl;
        return -1;
    }

    // Reduce resolution for BBB
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 320);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 240);
    cap.set(cv::CAP_PROP_FPS, 15);

    cv::Mat frame;
    // Capture a few frames to "warm up"
    for(int i = 0; i < 10; i++) {
        cap >> frame;
        if(!frame.empty()) break;
        cv::waitKey(100);
    }

    if(frame.empty()) {
        std::cerr << "ERROR: No frames captured!" << std::endl;
		    }

    // Save the frame to the SD card
    cv::imwrite("/mnt/<SD_card_mount>/test_capture.jpg", frame);
    std::cout << "Saved frame to /mnt/<SD_card_mount>/test_capture.jpg" << std::endl;

    return 0;
}