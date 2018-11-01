import os
import cv2 as cv
import numpy as np
from dir import *
from readfile import read_line_to_list


def tesseract_cmd(src_path, image, des_path, lang):
    os.system("tesseract {}{} {}{} -l {} -c preserve_interword_spaces=1".format(src_path, image, des_path, image, lang)) 

def dont_equal_frame_screen(src_w, src_h, current_w, current_h):
    return src_h != current_h and src_w != current_w

def main():
    cap = cv.VideoCapture(SRC_DIR)
    while(cap.isOpened()):
        frame_ret, frame = cap.read()
        frame_height, frame_width = frame.shape[:2]

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        thrsh_ret, threshold_frame = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
        thrsh_for_text_ret, threshold_frame_for_text = cv.threshold(gray, 25, 255, cv.THRESH_BINARY)

        contours, hierarchy = cv.findContours(threshold_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        max_h = 1
        max_w = 1
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            if ((w > max_w) and (h > max_h) and dont_equal_frame_screen(frame_width, frame_height, w, h)):
                max_h = h
                max_w = w
                max_x = x
                max_y = y

        crop_size = {
            "x": max_x,
            "y": max_y,
            "height": (max_y + max_h),
            "wide": (max_x + max_w)
        }

        cv.rectangle(threshold_frame_for_text, (crop_size["x"], crop_size["y"]), (crop_size["wide"], crop_size["height"]), (0, 255, 0), 10)

        crop_img = threshold_frame_for_text[crop_size["y"]:crop_size["height"], crop_size["x"]:crop_size["wide"]]
        crop_img = cv.resize(crop_img, None, fx=0.7, fy=0.7)
        cv.imwrite("{}{}".format(CROP_THRS_DIR, "crop_threshold.jpg"), crop_img)

        # tesseract process
        tesseract_cmd(CROP_THRS_DIR, "crop_threshold.jpg", TESSERACT_OUTPUT_DIR, "tha+eng")

        # read data
        nu_card_data = read_line_to_list(TESSERACT_OUTPUT_DIR + "crop_threshold.jpg.txt")
        university_name = nu_card_data[0]
        name = nu_card_data[2]
        nu_id = nu_card_data[4]

        print(university_name, name, nu_id)
        # validate

        break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()
