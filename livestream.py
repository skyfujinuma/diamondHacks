import cv2
import math

stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

frame_count = 0
print("Press 'q' to quit.")

# Define the width of the columns to be cut out
column_width = 150  # The width of the column to remove
frame_center_x = 870  # This is the center of a typical 1280px wide frame
left_x = frame_center_x - (column_width // 2)  # Left edge of the first column
right_x = frame_center_x + (column_width // 2)  # Right edge of the first column

# Define second column to be cut out (you can adjust the second column width or position as needed)
second_column_width = 150  # Adjust the width of the second column if necessary
second_frame_center_x = 610
second_left_x = second_frame_center_x - column_width - (second_column_width // 2)  # Left edge of the second column
second_right_x = second_frame_center_x - column_width + (second_column_width // 2)  # Right edge of the second column

# Dictionary to track the previous positions of fish
fish_positions = {}

# Define the fish count in quadrants and their positions
q1_positions = []
q2_positions = []
q3_positions = []
q4_positions = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or error.")
        break

    frame_count += 1
    print(f"Frame: {frame_count}", end="\r")

    h, w, _ = frame.shape

    # Cut out the first vertical column (middle column)
    left_part = frame[:, :left_x]  # Left side of the first column
    right_part = frame[:, right_x:]  # Right side of the first column

    # Cut out the second vertical column (additional column to remove)
    second_left_part = right_part[:, :second_left_x]  # Left part of the second column
    second_right_part = right_part[:, second_right_x:]  # Right part of the second column

    # Combine the left and right parts of both column cuts
    combined_frame = cv2.hconcat([left_part, second_left_part, second_right_part])

    # Apply background subtraction on the modified frame (excluding both columns)
    fgmask = fgbg.apply(combined_frame)

    # Detect contours (fish) in the combined frame
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the new width and height for quadrants after column removal
    combined_w = left_part.shape[1] + second_left_part.shape[1] + second_right_part.shape[1]
    combined_h = frame.shape[0]

    fish_id = 0

    # Reset quadrant positions
    q1_positions.clear()
    q2_positions.clear()
    q3_positions.clear()
    q4_positions.clear()

    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Only consider contours larger than a minimum size (e.g., 300)
        if area > 300:  # Threshold for contour area (you can adjust this for smaller fish detection)
            x, y, w_box, h_box = cv2.boundingRect(contour)

            fish_id += 1
            x_center = x + w_box // 2
            y_center = y + h_box // 2

            # Save the current position as the previous one for the next frame
            fish_positions[fish_id] = (x_center, y_center)

            # Classify fish into quadrants and store positions
            if x_center < combined_w // 2 and y_center < combined_h // 2:
                q1_positions.append((x_center, y_center))  # Top-left
            elif x_center >= combined_w // 2 and y_center < combined_h // 2:
                q2_positions.append((x_center, y_center))  # Top-right
            elif x_center < combined_w // 2 and y_center >= combined_h // 2:
                q3_positions.append((x_center, y_center))  # Bottom-left
            elif x_center >= combined_w // 2 and y_center >= combined_h // 2:
                q4_positions.append((x_center, y_center))  # Bottom-right

            # Draw bounding box and label (adjusting the coordinates to match the full frame)
            cv2.rectangle(combined_frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
            cv2.putText(combined_frame, f"Life", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Calculate the average x and y for each quadrant
    def calculate_average(positions):
        if positions:
            avg_x = sum(pos[0] for pos in positions) / len(positions)
            avg_y = sum(pos[1] for pos in positions) / len(positions)
            return avg_x, avg_y
        return 0, 0

    q1_avg_x, q1_avg_y = calculate_average(q1_positions)
    q2_avg_x, q2_avg_y = calculate_average(q2_positions)
    q3_avg_x, q3_avg_y = calculate_average(q3_positions)
    q4_avg_x, q4_avg_y = calculate_average(q4_positions)

    # Draw quadrant lines (green and thick) within the combined frame
    cv2.line(combined_frame, (combined_w // 2, 0), (combined_w // 2, combined_h), (0, 255, 0), 3)  # Vertical
    cv2.line(combined_frame, (0, combined_h // 2), (combined_w, combined_h // 2), (0, 255, 0), 3)  # Horizontal

    # Display the average x,y position and total fish count for each quadrant
    cv2.putText(combined_frame, f"Avg Q1: ({q1_avg_x:.2f}, {q1_avg_y:.2f})  Life Count: {len(q1_positions)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q2: ({q2_avg_x:.2f}, {q2_avg_y:.2f})  Life Count: {len(q2_positions)}", (combined_w // 2 + 10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q3: ({q3_avg_x:.2f}, {q3_avg_y:.2f})  Life Count: {len(q3_positions)}", (10, combined_h // 2 + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q4: ({q4_avg_x:.2f}, {q4_avg_y:.2f})  Life Count: {len(q4_positions)}", (combined_w // 2 + 10, combined_h // 2 + 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the result with detected fish
    cv2.imshow("Fish Detection with Average Positions and Count", combined_frame)

    # Check for 'q' key to quit from OpenCV window
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Quitting stream...")
        break

cap.release()
cv2.destroyAllWindows()