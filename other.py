import cv2
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.maxArea = 25000
params.filterByConvexity = False
params.filterByInertia = False
params.filterByCircularity = False

detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(th3)
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(th3,
                                      keypoints,
                                      np.array([]),
                                      (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

cv2.destroyAllWindows()

df = pd.DataFrame([{'size': x.size, 'x': x.pt[0], 'y': -1*x.pt[1]} for x in keypoints])
plt.figure()
plt.scatter(df['x'], df['y'], s=df['size'], c='none', edgecolor='r')
plt.show()
