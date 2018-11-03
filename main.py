import datetime
import os
import cv2 as cv
import numpy as np
from dir import *
from read_write import read_line_to_list, write_line
from validate import *

cv.namedWindow("windows", cv.WINDOW_NORMAL)

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
        thrsh_for_text_ret, threshold_frame_for_text = cv.threshold(gray, 20, 255, cv.THRESH_BINARY)

        contours, hierarchy = cv.findContours(threshold_frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        max_x = max_y = max_w = max_h = 1

        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)
            # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
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

        # cv.rectangle(frame, (crop_size["x"], crop_size["y"]), (crop_size["wide"], crop_size["height"]), (0, 255, 0), 5)
        
        # Draw rect on photo
        # cv.rectangle(frame, (crop_size["x"] + 850, crop_size["y"] + 320), (crop_size["x"] + 1150, crop_size["y"] + 670), (0, 255, 0), 5)

        crop_img = threshold_frame_for_text[crop_size["y"]:crop_size["height"], crop_size["x"]:crop_size["wide"]]
        crop_img = cv.resize(crop_img, None, fx=0.7, fy=0.7)

        time_now = "{:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now())
        file_name = "{}_crop_thrs_img.jpg".format(time_now)
        cv.imwrite("{}{}".format(CROP_THRS_DIR, file_name), crop_img)
        cv.imwrite("{}{}".format(RAW_FRAME_WITH_RECT, file_name), frame)

        # tesseract process
        tesseract_cmd(CROP_THRS_DIR, file_name, TESSERACT_OUTPUT_DIR, "tha+eng")

        # read data
        nu_card_data = read_line_to_list(TESSERACT_OUTPUT_DIR + "{}_crop_thrs_img.jpg.txt".format(time_now))
        index_id = find_id(nu_card_data)
        university_name = nu_card_data[index_id - 4]
        nu_id = nu_card_data[index_id]
        name = nu_card_data[index_id - 2]
        new_nu_card_data = [nu_id, name]

        # validate
        is_nu_card = university_name_validate("Naresuan University", university_name)

        if (not is_nu_card): 
            print("Not Nu Card")
            continue

        if (index_id == -1):
            print("Not Found ID")
            continue

        # write data
        data_name = "{}_{}.txt".format(time_now, nu_id)
        write_line(NU_CARD_DATA, data_name, new_nu_card_data)

        crop_nu_card_photo = frame[crop_size["y"] + 320:crop_size["y"] + 670, crop_size["x"] + 850:crop_size["x"] + 1150]
        photo_name = "{}_{}.jpg".format(time_now, nu_id)
        cv.imwrite("{}{}".format(NU_CARD_DATA, photo_name), crop_nu_card_photo)

        cv.imshow("windows", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
