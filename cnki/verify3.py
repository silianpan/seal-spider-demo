import tesserocr
import pytesseract
from PIL import Image

image = Image.open('code4.png')

image = image.convert('L')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
image.show()

# result = tesserocr.image_to_text(image)
result = pytesseract.image_to_string(Image.open('code5.png'), lang='chi_sim')
print(result)
