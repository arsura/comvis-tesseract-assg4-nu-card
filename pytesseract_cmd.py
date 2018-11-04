import pytesseract
import cv2 as cv

def pytesseract_cmd(src_path):
    nu_card_data = pytesseract.image_to_string(cv.imread(src_path), lang='tha+eng')
    return nu_card_data