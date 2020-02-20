import cv2
from copy import deepcopy
import numpy as np
import utils

RESCALE = 3

def find_cell_param(joints):
    # Set up the detector with default parameters.
    params = cv2.SimpleBlobDetector_Params()
    # filter by area
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 50
    detector = cv2.SimpleBlobDetector_create(params)
    # Detect blobs
    keypoints = detector.detect(~joints)
    sorted_keypoints = sorted(keypoints, key=lambda x: (x.pt[0], x.pt[1]))
    min_keypoint = sorted_keypoints[0]
    max_keypoint = sorted_keypoints[-1]
    # for it, keypoint in enumerate(keypoints):
    # img_contours = deepcopy(img)
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    # im_with_keypoints = cv2.drawKeypoints(img_contours, [min_keypoint, max_keypoint], np.array([]), (0, 0, 255),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("Keypoints", im_with_keypoints)
    # cv2.waitKey(0)
    return (max_keypoint.pt[0] - min_keypoint.pt[0]) / 7, (max_keypoint.pt[1] - min_keypoint.pt[1]) / 7, min_keypoint.pt, max_keypoint.pt


def get_joints(img):
    img = cv2.resize(img, (int(img.shape[1]/RESCALE), int(img.shape[0]/RESCALE)))
    # retval = cv2.getPerspectiveTransform(img) TO DO  https://blog.ayoungprogrammer.com/2013/03/tutorial-creating-multiple-choice.html/
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bin_img = cv2.adaptiveThreshold(cv2.bitwise_not(img_gray), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    scale = 20
    horizontal_size = bin_img.shape[0] // scale
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    img_eroded_horizontal = cv2.erode(bin_img, horizontal_structure, anchor=(-1, -1))
    img_dilated_horizontal = cv2.erode(img_eroded_horizontal, horizontal_structure, anchor=(-1, -1))

    vertical_size = bin_img.shape[1] // scale
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    img_eroded_vertical = cv2.erode(bin_img, vertical_structure, anchor=(-1, -1))
    img_dilated_vertical = cv2.erode(img_eroded_vertical, vertical_structure, anchor=(-1, -1))

    # mask = img_dilated_vertical + img_dilated_horizontal
    joints = cv2.bitwise_and(img_dilated_horizontal, img_dilated_vertical)
    return bin_img, joints


def recognize_grid(model, img):
    bin_img, joints = get_joints(img)
    cell_height, cell_width, min_pt, max_pt = find_cell_param(joints)
    grid = []
    for x in range(-1, 8):
        row = []
        for y in range(-1, 8):
            roi = bin_img[int(min_pt[1]+cell_width*x):int(min_pt[1]+cell_width*(x+1)),
                          int(min_pt[0]+cell_height*y):int(min_pt[0]+cell_height*(y+1))]
            alpha = 0.1
            roi = roi[int(roi.shape[1]*alpha):int(roi.shape[1]*(1-alpha)), int(roi.shape[0]*alpha):int(roi.shape[0]*(1-alpha))]
            row.append(utils.predict_digit(model, roi))
            # cv2.imshow("ROI: ", roi)
            # cv2.waitKey(0)
        grid.append(row)
    return grid


def main():
    model = utils.load_mnist_model()
    img = cv2.imread("./SudokuOnline/puzzle1.jpg")

    sudoku_grid = recognize_grid(model, img)
    print(np.matrix(sudoku_grid))

    img = cv2.resize(img, (int(img.shape[1]/RESCALE), int(img.shape[0]/RESCALE)))
    cv2.imshow("Img: ", img)
    # cv2.imshow("Gray: ", img_gray)
    # cv2.imshow("Bin: ", bin_img)
    # cv2.imshow("Dilated horizontal: ", img_dilated_horizontal)
    # cv2.imshow("Dilated vertical: ", img_dilated_vertical)
    # cv2.imshow("Joints: ", joints)
    # cv2.imshow("Mask: ", mask)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
