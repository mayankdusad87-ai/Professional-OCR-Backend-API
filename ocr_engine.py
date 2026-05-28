import easyocr

reader = None


def get_reader():

    global reader

    if reader is None:

        reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    return reader


def extract_text(image_path):

    reader_instance = get_reader()

    results = reader_instance.readtext(image_path)

    extracted_text = ""

    for result in results:

        text = result[1]

        extracted_text += text + " "

    return extracted_text
