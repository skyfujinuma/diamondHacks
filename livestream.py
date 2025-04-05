import cv2

stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

frame_count = 0
print("Enter 'quit' or 'exit' to quit the stream.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or error.")
        break

    frame_count += 1
    print(f"Frame: {frame_count}", end="\r")  # prints on the same line

    if frame_count % 30 == 0:
        processed_frame = frame
        cv2.imshow("Live Stream", processed_frame)


    # Show the stream

    # Check for 'q' key to quit from OpenCV window (optional)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting stream...")
        break

cap.release()
cv2.destroyAllWindows()