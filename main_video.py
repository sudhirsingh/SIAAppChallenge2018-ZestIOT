import cv2
import imutils
import numpy as np
from imutils import contours
from skimage import measure

# define the list of boundaries
# hsv
boundaries = [
    ([111, 74, 111], [122, 232, 241]),  # blue
    ([86, 111, 67], [99, 255, 177]),  # green
    ([26, 43, 102], [39, 255, 215]),  # yellow
    ([167, 103, 126], [180, 213, 209])  # red
]
colors = ['Blue', 'Green', 'Yellow', 'Red']


def inside_boundary(b, g, r, boundary):
    if b in xrange(boundary[0][0], boundary[1][0] + 1) and g in xrange(boundary[0][1], boundary[1][1] + 1) \
            and r in xrange(boundary[0][2], boundary[1][2] + 1):
        return True
    return False


def convert_frames_to_video(frames, pathOut, fps):
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frames)):
        # writing to a image array
        out.write(frames[i])
    out.release()


frames = []
cap = cv2.VideoCapture('top-rotated.mp4')
success, frame = cap.read()
while success:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # loop over the boundaries
    flag = False
    for i, (lower, upper) in enumerate(boundaries):
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(hsv, hsv, mask=mask)
        output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        # threshold the image to reveal light regions in the
        # blurred image
        thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]
        # perform a series of erosions and dilations to remove
        # any small blobs of noise from the thresholded image
        thresh = cv2.erode(thresh, None, iterations=4)
        thresh = cv2.dilate(thresh, None, iterations=4)

        # perform a connected component analysis on the thresholded
        # image, then initialize a mask to store only the "large"
        # components
        labels = measure.label(thresh, neighbors=8, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")

        # loop over the unique components
        for label in np.unique(labels):
            # if this is the background label, ignore it
            if label == 0:
                continue

            # otherwise, construct the label mask and count the
            # number of pixels
            labelMask = np.zeros(thresh.shape, dtype="uint8")
            labelMask[labels == label] = 255
            numPixels = cv2.countNonZero(labelMask)

            # if the number of pixels in the component is sufficiently
            # large, then add it to our mask of "large blobs"
            if numPixels > 300:
                mask = cv2.add(mask, labelMask)

        # find the contours in the mask, then sort them from left to
        # right
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        try:
            cnts = contours.sort_contours(cnts)[0]
            flag = True
        except:
            pass
        # loop over the contours
        for (j, c) in enumerate(cnts):
            # draw the bright spot on the image
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(frame, (int(cX), int(cY)), int(radius),
                       (0, 0, 255), 3)
            cv2.putText(frame, "{} {}".format(colors[i], j + 1), (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    if flag:
        cv2.putText(frame, "Detected", (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (113, 204, 46), 1)
    else:
        cv2.putText(frame, "Not Detected", (290, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (60, 76, 231), 1)
    cv2.putText(frame, "Top View", (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (219, 152, 52), 1)
    frames.append(frame)
    # cv2.imshow("video", frame)
    # key = cv2.waitKey(1) & 0xFF
    #
    # # if the `q` key was pressed, break from the loop
    # if key == ord("q"):
    #     break
    success, frame = cap.read()
# do a bit of cleanup
cap.release()

# cv2.destroyAllWindows()

convert_frames_to_video(frames, 'top_edited.mp4', 30)
