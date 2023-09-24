import numpy as np
import cv2


def read_images_and_times():
    # List of exposure times
    times = np.array([0.0333, 0.1000, 0.3333, 0.6250, 1.3000, 4.0000], dtype=np.float32)
    base_path = "../image_sources/HDR images/"

    # List of image filenames
    filenames = ["office_1.jpg", "office_2.jpg", "office_3.jpg", "office_4.jpg", "office_5.jpg", "office_6.jpg"]
    images = []
    for filename in filenames:
        im = cv2.imread(base_path + filename)
        print(base_path + filename)
        images.append(im)

    return images, times


images, times = read_images_and_times()

# Align input images
alignMTB = cv2.createAlignMTB()
alignMTB.process(images, images)

# Obtain Camera Response Function (CRF)
calibrateDebevec = cv2.createCalibrateDebevec()
responseDebevec = calibrateDebevec.process(images, times)

# Merge images into an HDR linear image
mergeDebevec = cv2.createMergeDebevec()
hdrDebevec = mergeDebevec.process(images, times, responseDebevec)

# Save HDR image.
cv2.imwrite("results/HDR_image.hdr", hdrDebevec)

# Tonemap using Drago's method to obtain 24-bit color image
tonemapDrago = cv2.createTonemapDrago(1.0, 0.7)
ldrDrago = tonemapDrago.process(hdrDebevec)
ldrDrago = 3 * ldrDrago
cv2.imwrite("results/ldr-Drago.jpg", ldrDrago * 255)
