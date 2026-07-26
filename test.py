import os
import cv2
from image_processing import process_image

class TestFile:
    def __init__(self, path):
        self.path = path

    def save(self, destination):
        image = cv2.imread(self.path)
        cv2.imwrite(destination, image)


imagePath = r"C:\Users\asus\OneDrive\Desktop\StrokeFlow\static\uploads\IMG20260726151355.jpg"

testFile = TestFile(imagePath)

tempPath = "temp_signature.png"

output = process_image(testFile, tempPath)

if output is None:
    print("Processing failed.")
else:
    print("PNG Created :", output)
    print("SVG Created :", "signature_" + os.path.splitext(os.path.basename(tempPath))[0] + ".svg")