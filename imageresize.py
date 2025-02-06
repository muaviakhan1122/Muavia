import cv2

# Read an image
image = cv2.imread("muavia.jpeg")

# Resize the image to a specific width and height
# resized_image = cv2.resize(image, (224, 224))
resized_image = cv2.resize(image, None, fx=0.5, fy=0.5)
# Show the resized image
cv2.imshow("Resized Image", resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#python imageresize.py
