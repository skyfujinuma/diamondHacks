import cv2
import hashlib
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

# --- GUI Code ---
def get_quadrant_string(data):
    return ''.join(
        f"{q['count']}_{q['avg'][0]:.2f}_{q['avg'][1]:.2f}" 
        for q in data.values()
    )

def generate_hash(password, quadrant_data):
    quad_str = get_quadrant_string(quadrant_data)
    combined = password + quad_str
    return hashlib.sha256(combined.encode()).hexdigest()

class HashGeneratorApp(QWidget):
    def __init__(self, quadrant_data):
        super().__init__()
        self.quadrant_data = quadrant_data
        self.setWindowTitle('Password Creation - Fish Tracker')
        self.setGeometry(100, 100, 500, 400)
        
        # Layout setup
        layout = QVBoxLayout()

        # Password Input
        self.password_label = QLabel('Enter a password to generate a hash:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Generate Hash Button
        self.generate_button = QPushButton('Generate Hash', self)
        self.generate_button.clicked.connect(self.on_submit)
        
        # Result area
        self.result_label = QLabel('')
        self.result_label.setWordWrap(True)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def on_submit(self):
        password = self.password_input.text()
        if not password:
            self.result_label.setText("Please enter a password.")
            return
        
        hash_result = generate_hash(password, self.quadrant_data)
        result_text = "\n".join([
            f"Q1 - Count: {self.quadrant_data['Q1']['count']}, Avg Pos: {self.quadrant_data['Q1']['avg']}",
            f"Q2 - Count: {self.quadrant_data['Q2']['count']}, Avg Pos: {self.quadrant_data['Q2']['avg']}",
            f"Q3 - Count: {self.quadrant_data['Q3']['count']}, Avg Pos: {self.quadrant_data['Q3']['avg']}",
            f"Q4 - Count: {self.quadrant_data['Q4']['count']}, Avg Pos: {self.quadrant_data['Q4']['avg']}",
            f"\nGenerated Hash:\n{hash_result}"
        ])
        self.result_label.setText(result_text)

# --- Stream and Tracking Code ---
stream_url = "https://edge03.nginx.hdontap.com/hosb1/scripps_kelp_cam-ptz.stream/chunklist_w97654465.m3u8"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Failed to open stream!")
    exit()

fgbg = cv2.createBackgroundSubtractorMOG2()
frame_count = 0
print("Press 'q' to quit.")

column_width = 150
frame_center_x = 870
left_x = frame_center_x - (column_width // 2)
right_x = frame_center_x + (column_width // 2)

second_column_width = 150
second_frame_center_x = 610
second_left_x = second_frame_center_x - column_width - (second_column_width // 2)
second_right_x = second_frame_center_x - column_width + (second_column_width // 2)

fish_positions = {}
q1_positions, q2_positions, q3_positions, q4_positions = [], [], [], []

while True:
    ret, frame = cap.read()
    if not ret:
        print("Stream ended or error.")
        break

    frame_count += 1
    print(f"Frame: {frame_count}", end="\r")

    h, w, _ = frame.shape
    left_part = frame[:, :left_x]
    right_part = frame[:, right_x:]
    second_left_part = right_part[:, :second_left_x]
    second_right_part = right_part[:, second_right_x:]

    combined_frame = cv2.hconcat([left_part, second_left_part, second_right_part])
    fgmask = fgbg.apply(combined_frame)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    combined_w = left_part.shape[1] + second_left_part.shape[1] + second_right_part.shape[1]
    combined_h = frame.shape[0]

    fish_id = 0
    q1_positions.clear(), q2_positions.clear(), q3_positions.clear(), q4_positions.clear()

    for contour in contours:
        if cv2.contourArea(contour) > 300:
            x, y, w_box, h_box = cv2.boundingRect(contour)
            fish_id += 1
            x_center = x + w_box // 2
            y_center = y + h_box // 2

            fish_positions[fish_id] = (x_center, y_center)

            if x_center < combined_w // 2 and y_center < combined_h // 2:
                q1_positions.append((x_center, y_center))
            elif x_center >= combined_w // 2 and y_center < combined_h // 2:
                q2_positions.append((x_center, y_center))
            elif x_center < combined_w // 2 and y_center >= combined_h // 2:
                q3_positions.append((x_center, y_center))
            else:
                q4_positions.append((x_center, y_center))

            cv2.rectangle(combined_frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
            cv2.putText(combined_frame, f"Life", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def calculate_average(positions):
        if positions:
            avg_x = sum(p[0] for p in positions) / len(positions)
            avg_y = sum(p[1] for p in positions) / len(positions)
            return avg_x, avg_y
        return 0, 0

    q1_avg_x, q1_avg_y = calculate_average(q1_positions)
    q2_avg_x, q2_avg_y = calculate_average(q2_positions)
    q3_avg_x, q3_avg_y = calculate_average(q3_positions)
    q4_avg_x, q4_avg_y = calculate_average(q4_positions)

    cv2.line(combined_frame, (combined_w // 2, 0), (combined_w // 2, combined_h), (0, 255, 0), 3)
    cv2.line(combined_frame, (0, combined_h // 2), (combined_w, combined_h // 2), (0, 255, 0), 3)

    cv2.putText(combined_frame, f"Avg Q1: ({q1_avg_x:.2f}, {q1_avg_y:.2f})  Life Count: {len(q1_positions)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q2: ({q2_avg_x:.2f}, {q2_avg_y:.2f})  Life Count: {len(q2_positions)}", (combined_w // 2 + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q3: ({q3_avg_x:.2f}, {q3_avg_y:.2f})  Life Count: {len(q3_positions)}", (10, combined_h // 2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(combined_frame, f"Avg Q4: ({q4_avg_x:.2f}, {q4_avg_y:.2f})  Life Count: {len(q4_positions)}", (combined_w // 2 + 10, combined_h // 2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Fish Detection with Average Positions and Count", combined_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("Quitting stream...")
        break

    if key == ord('p'):
        print("Launching password creation GUI...")

        quadrant_data = {
            'Q1': {'count': len(q1_positions), 'avg': (q1_avg_x, q1_avg_y)},
            'Q2': {'count': len(q2_positions), 'avg': (q2_avg_x, q2_avg_y)},
            'Q3': {'count': len(q3_positions), 'avg': (q3_avg_x, q3_avg_y)},
            'Q4': {'count': len(q4_positions), 'avg': (q4_avg_x, q4_avg_y)},
        }

        app = QApplication(sys.argv)
        window = HashGeneratorApp(quadrant_data)
        window.show()
        sys.exit(app.exec_())

cap.release()
cv2.destroyAllWindows()