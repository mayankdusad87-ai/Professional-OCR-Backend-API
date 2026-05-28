from paddleocr import PaddleOCR

ocr = None

def get_ocr():
    global ocr

    if ocr is None:
        ocr = PaddleOCR(
            use_angle_cls=False,
            lang='en',
            use_gpu=False,
            show_log=False
        )

    return ocr


def extract_text(image_path):

    ocr_instance = get_ocr()

    result = ocr_instance.ocr(image_path)

    extracted_text = ""

    for line in result[0]:
        extracted_text += line[1][0] + " "

    return extracted_text
