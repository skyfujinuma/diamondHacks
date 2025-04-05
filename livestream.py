import cv2

stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or error.")
        break

    cv2.imshow("Live Stream", frame)

    # Wait for 1ms and check for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting stream...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()