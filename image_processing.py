import cv2
import os
import numpy as np


def convert_to_svg(mask, svgPath):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    with open(svgPath, "w") as svg:
        h, w = mask.shape

        svg.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        )

        for contour in contours:
            if len(contour) < 2:
                continue

            epsilon = 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            path = "M "

            for point in approx:
                x, y = point[0]
                path += f"{x} {y} L "

            path = path[:-2]

            svg.write(
                f'<path d="{path}" fill="none" stroke="black" stroke-width="2"/>\n'
            )

        svg.write("</svg>")


def process_image(file, filepath):

    file.save(filepath)

    image = cv2.imread(filepath)

    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bilateralimage = cv2.bilateralFilter(grayImage, 9, 75, 75)

    _, thresh = cv2.threshold(
        bilateralimage,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contours, hierarchy = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = [c for c in contours if cv2.contourArea(c) > 30]

    if not contours:
        return None

    largestContour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largestContour)

    centerX = x + w // 2
    centerY = y + h // 2

    filteredContours = []

    for c in contours:

        x1, y1, w1, h1 = cv2.boundingRect(c)

        contourCenterX = x1 + w1 // 2
        contourCenterY = y1 + h1 // 2

        distance = np.sqrt(
            (contourCenterX - centerX) ** 2 +
            (contourCenterY - centerY) ** 2
        )

        if distance < 300:
            filteredContours.append(c)

    if not filteredContours:
        return None

    xMin = min(cv2.boundingRect(c)[0] for c in filteredContours)
    yMin = min(cv2.boundingRect(c)[1] for c in filteredContours)

    xMax = max(
        cv2.boundingRect(c)[0] + cv2.boundingRect(c)[2]
        for c in filteredContours
    )

    yMax = max(
        cv2.boundingRect(c)[1] + cv2.boundingRect(c)[3]
        for c in filteredContours
    )

    padding = 10

    xMin = max(0, xMin - padding)
    yMin = max(0, yMin - padding)

    xMax = min(image.shape[1], xMax + padding)
    yMax = min(image.shape[0], yMax + padding)

    croppedImage = image[yMin:yMax, xMin:xMax]

    croppedGray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(croppedGray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    sharpenKernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    rgbImage = cv2.filter2D(croppedImage, -1, sharpenKernel)
    transparentImage = np.zeros((rgbImage.shape[0], rgbImage.shape[1], 4),dtype=np.uint8)
    transparentImage[:, :, :3] = rgbImage
    transparentImage[:, :, 3] = mask
    transparentImage[mask == 0] = [0, 0, 0, 0]

    filename = os.path.basename(filepath)

    outputFilename = "signature_" + filename

    outputPath = os.path.join(
        "static/uploads",
        outputFilename
    )

    cv2.imwrite(
        outputPath,
        transparentImage
    )

    svgFilename = (
        "signature_" +
        os.path.splitext(filename)[0] +
        ".svg"
    )

    svgPath = os.path.join(
        "static/uploads",
        svgFilename
    )

    convert_to_svg(mask, svgPath)

    height, width = transparentImage.shape[:2]

    pngSize = round(
        os.path.getsize(outputPath) / 1024,
        2
    )

    svgSize = round(
        os.path.getsize(svgPath) / 1024,
        2
    )

    return {
        "pngFile": outputFilename,
        "svgFile": svgFilename,
        "width": width,
        "height": height,
        "pngSize": pngSize,
        "svgSize": svgSize
    }