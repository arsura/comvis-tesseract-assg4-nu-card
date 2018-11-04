#include <opencv2/opencv.hpp>

int main(int, char**)
{
    cv::VideoCapture cap(0);
    if(!cap.isOpened()) return -1;
    cv::Mat gray;
    cv::namedWindow("windows",1);
    for(;;)
    {
        cv::Mat frame;
        cap >> frame;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);

        cv::imshow("windows", gray);
        if(cv::waitKey(30) >= 0) break;
    }
    return 0;
}