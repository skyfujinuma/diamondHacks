import cv2

stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

# Background subtractor
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

    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2  # Center of frame

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Detect contours (fish)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Quadrant counts
    q1 = q2 = q3 = q4 = 0
    fish_id = 0

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            fish_id += 1
            x, y, w_box, h_box = cv2.boundingRect(contour)
            x_center = x + w_box // 2
            y_center = y + h_box // 2

            # Determine quadrant
            if x_center < cx and y_center < cy:
                q1 += 1  # Top-left
            elif x_center >= cx and y_center < cy:
                q2 += 1  # Top-right
            elif x_center < cx and y_center >= cy:
                q3 += 1  # Bottom-left
            elif x_center >= cx and y_center >= cy:
                q4 += 1  # Bottom-right

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
            cv2.putText(frame, f"Fish {fish_id}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Draw quadrant lines (green and thick)
    cv2.line(frame, (cx, 0), (cx, h), (0, 255, 0), 3)  # Vertical
    cv2.line(frame, (0, cy), (w, cy), (0, 255, 0), 3)  # Horizontal

    # Display counts for each quadrant
    cv2.putText(frame, f"Q1: {q1}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Q2: {q2}", (cx + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Q3: {q3}", (10, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Q4: {q4}", (cx + 10, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Total count
    total_fish = q1 + q2 + q3 + q4
    cv2.putText(frame, f"Total Fish: {total_fish}", (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show result
    cv2.imshow("Fish Detection with Quadrants", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting stream...")
        break

cap.release()
cv2.destroyAllWindows()