from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=False,
    lang='en',
    use_gpu=False,
    show_log=False
)

def extract_text(image_path):

    result = ocr.ocr(image_path, cls=True)

    text = ""

    for line in result[0]:
        text += line[1][0] + "\n"

    return text
