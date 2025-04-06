import cv2
import hashlib
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
import random
import requests
from datetime import datetime

cities_data = {
    1: ["Paris", "", "FR", 1], 2: ["Madrid", "", "ES", 1], 3: ["Tokyo", "", "JP", 1], 4: ["Rome", "", "IT", 1], 5: ["Milan", "", "IT", 1],
    6: ["New York", "NY", "US", 1], 7: ["Amsterdam", "", "NL", 1], 8: ["Sydney", "", "AU", 1], 9: ["Singapore", "", "SG", 1], 10: ["Barcelona", "", "ES", 1],
    11: ["Taipei", "", "TW", 1],
    12: ["Seoul", "", "KR", 1],
    13: ["London", "", "GB", 1],
    14: ["Dubai", "", "AE", 1],
    15: ["Berlin", "", "DE", 1],
    16: ["Osaka", "", "JP", 1],
    17: ["Bangkok", "", "TH", 1],
    18: ["Los Angeles", "CA", "US", 1],
    19: ["Istanbul", "", "TR", 1],
    20: ["Melbourne", "", "AU", 1],
    21: ["Hong Kong", "", "HK", 1],
    22: ["Munich", "", "DE", 1],
    23: ["Las Vegas", "NV", "US", 1],
    24: ["Florence", "", "IT", 1],
    25: ["Prague", "", "CZ", 1],
    26: ["Dublin", "", "IE", 1],
    27: ["Kyoto", "", "JP", 1],
    28: ["Vienna", "", "AT", 1],
    29: ["Lisbon", "", "PT", 1],
    30: ["Venice", "", "IT", 1],
    31: ["Kuala Lumpur", "", "MY", 1],
    32: ["Athens", "", "GR", 1],
    33: ["Orlando", "FL", "US", 1],
    34: ["Toronto", "", "CA", 1],
    35: ["Miami", "FL", "US", 1],
    36: ["San Francisco", "CA", "US", 1],
    37: ["Shanghai", "", "CN", 1],
    38: ["Frankfurt", "", "DE", 1],
    39: ["Copenhagen", "", "DK", 1],
    40: ["Zurich", "", "CH", 1],
    41: ["Washington", "DC", "US", 1],
    42: ["Pattaya", "", "TH", 1],
    43: ["Vancouver", "", "CA", 1],
    44: ["Stockholm", "", "SE", 1],
    45: ["Mexico City", "", "MX", 1],
    46: ["Oslo", "", "NO", 1],
    47: ["São Paulo", "", "BR", 1],
    48: ["Phuket", "", "TH", 1],
    49: ["Helsinki", "", "FI", 1],
    50: ["Brussels", "", "BE", 1],
    51: ["Budapest", "", "HU", 1],
    52: ["Guangzhou", "", "CN", 1],
    53: ["Nice", "", "FR", 1],
    54: ["Palma", "", "ES", 1],
    55: ["Honolulu", "HI", "US", 1],
    56: ["Beijing", "", "CN", 1],
    57: ["Warsaw", "", "PL", 1],
    58: ["Seville", "", "ES", 1],
    59: ["Valencia", "", "ES", 1],
    60: ["Shenzhen", "", "CN", 1],
    61: ["Doha", "", "QA", 1],
    62: ["Abu Dhabi", "", "AE", 1],
    63: ["Antalya", "", "TR", 1],
    64: ["Fukuoka", "", "JP", 1],
    65: ["Sapporo", "", "JP", 1],
    66: ["Busan", "", "KR", 1],
    67: ["Macau", "", "MO", 1],
    68: ["Edinburgh", "", "GB", 1],
    69: ["Montreal", "", "CA", 1],
    70: ["Cancún", "", "MX", 1],
    71: ["Bologna", "", "IT", 1],
    72: ["Rhodes", "", "GR", 1],
    73: ["Verona", "", "IT", 1],
    74: ["Delhi", "", "IN", 1],
    75: ["Porto", "", "PT", 1],
    76: ["Ho Chi Minh City", "", "VN", 1],
    77: ["Buenos Aires", "", "AR", 1],
    78: ["Marne-la-Vallée", "", "FR", 1],
    79: ["Rio de Janeiro", "", "BR", 1],
    80: ["Kraków", "", "PL", 1],
    81: ["Heraklion", "", "GR", 1],
    82: ["Johor Bahru", "", "MY", 1],
    83: ["Hanoi", "", "VN", 1],
    84: ["Tel Aviv", "", "IL", 1],
    85: ["Sharjah", "", "AE", 1],
    86: ["Thessaloniki", "", "GR", 1],
    87: ["Lima", "", "PE", 1],
    88: ["Medina", "", "SA", 1],
    89: ["Tbilisi", "", "GE", 1],
    90: ["Riyadh", "", "SA", 1],
    91: ["Tallinn", "", "EE", 1],
    92: ["Marrakech", "", "MA", 1],
    93: ["Mecca", "", "SA", 1],
    94: ["Denpasar", "", "ID", 1],
    95: ["Punta Cana", "", "DO", 1],
    96: ["Santiago", "", "CL", 1],
    97: ["Vilnius", "", "LT", 1],
    98: ["Jerusalem", "", "IL", 1],
    99: ["Zhuhai", "", "CN", 1],
    100: ["Cairo", "", "EG", 1]
}

openWeatherAPIKey = "787eb916eeb102320bd5dc58ef8e88bf"

def accessWeather():
    city_id = random.randint(1, 100)
    city_info = cities_data[city_id]

    city = city_info[0]
    state = city_info[1]
    country = city_info[2]

    
    location = f"{city},{state},{country}" if state else f"{city},{country}"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={openWeatherAPIKey}"

    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    

# Check if the response is a list and not empty
    if isinstance(geo_data, list) and geo_data:
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
    else:
        print(f"Could not find location or invalid response for: {location}")
        return

    
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openWeatherAPIKey}"
    )

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if "main" in weather_data:
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
    if "wind" in weather_data:
        speed = weather_data["wind"]["speed"]


        print(f"{city}, {country} --> {temp}K")
        print(f"{city}, {country} --> {humidity}g/kg")
        print(f"{city}, {country} --> {speed}km/h")
        weather = temp * humidity - speed
        weather = round(weather)
        print(weather)

        return temp, humidity, speed, city, country, weather
    else:
        print("Weather data not found.")
        return

def get_current_time():
    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

# --- GUI Code ---
def get_quadrant_string(data):
    return ''.join(
        f"{q['count']}_{q['avg'][0]:.2f}_{q['avg'][1]:.2f}" 
        for q in data.values()
    )


def generate_hash(password, quadrant_data, weather, time):
    quad_str = get_quadrant_string(quadrant_data)
    horse = str(weather)
    combined = password + quad_str + horse + time
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
        
        time = get_current_time()
        temp, humidity, speed, city, country, weather = accessWeather()

        hash_result = generate_hash(password, self.quadrant_data, weather, time)
        result_text = "\n".join([
            f"Q1 - Count: {self.quadrant_data['Q1']['count']}, Avg Pos: {self.quadrant_data['Q1']['avg']}",
            f"Q2 - Count: {self.quadrant_data['Q2']['count']}, Avg Pos: {self.quadrant_data['Q2']['avg']}",
            f"Q3 - Count: {self.quadrant_data['Q3']['count']}, Avg Pos: {self.quadrant_data['Q3']['avg']}",
            f"Q4 - Count: {self.quadrant_data['Q4']['count']}, Avg Pos: {self.quadrant_data['Q4']['avg']}",
            f"---------",
            f"Weather in: " + city + ", " + country,
            f"Temperature: " + str(temp) + "K",
            f"Humidity: " + str(humidity) + "g/kg",
            f"Wind: " + str(speed) + "km/h",
            f"W-Value: " + str(weather),
            f"---------",
            f"Time: " + time,
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