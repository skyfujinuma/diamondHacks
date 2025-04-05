import cv2

stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

# Initialize background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

frame_count = 0
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or error.")
        break

    frame_count += 1
    print(f"Frame: {frame_count}", end="\r")

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Find contours (i.e., the fish in the stream)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (noise), and count the number of detected fish
    fish_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to consider as a fish (adjust as needed)
            fish_count += 1

            # Get the bounding box for each fish
            x, y, w, h = cv2.boundingRect(contour)

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box for detected fish
            cv2.putText(frame, f"Fish {fish_count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the number of detected fish
    cv2.putText(frame, f"Fish Count: {fish_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the processed frame
    cv2.imshow("Fish Detection", frame)

    # Check for 'q' key to quit from OpenCV window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting stream...")
        break

cap.release()
cv2.destroyAllWindows()