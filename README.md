# 📸 QR Attendance System

A simple Python-based **QR Code Attendance System**.
It uses **OpenCV** to scan QR codes via webcam and automatically logs attendance into an Excel file.

---

## 🚀 Features

* ✅ Scan QR Codes via Webcam (OpenCV’s `QRCodeDetector`)
* ✅ Stores attendance in `attendance_qr.xlsx` (auto-created if missing)
* ✅ Avoids duplicate entries for the same student on the same day
* ✅ Highlights already marked students in a different color
* ✅ Plays a beep sound on successful scan (Windows only)

---

## 📂 Project Structure

```
📁 QR-Attendance-System
 ┣ 📄 qr_scanner.py          # main scanner
 ┣ 📄 qr_generator.py    # Script to generate QR codes for students
 ┣ 📄 attendance_qr.xlsx # Auto-created attendance file
 ┣ 📄 README.md          # Project documentation
```

---

## ⚙️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/QR-Attendance-System.git
   cd QR-Attendance-System
   ```

2. Install dependencies:

   ```bash
   pip install opencv-python pandas openpyxl pillow
   ```

3. (Optional) Windows users for beep sound:

   ```bash
   pip install pywin32
   ```

---

## ▶️ Usage

### 1. Generate QR Codes

Run the QR generator script to create QR codes for students:

```bash
python qr_generator.py
```

This creates a `qrcodes/` folder with individual student QR images.
QR payload format:

```
ID=101|NAME=YA
```

### 2. Start the Scanner

```bash
python qr_scanner.py
```

* Click **Run the code** → Opens webcam.
* Show a QR code → Attendance is logged into `attendance_qr.xlsx`.
* Click **q or Ctrl +C** or press **Q** → Stops the scanner.

---

## 📊 Attendance File Format

Attendance is saved in **Excel** (`attendance_qr.xlsx`) with columns:

| timestamp           | date       | time     | student\_id | name       | source    |
| ------------------- | ---------- | -------- | ----------- | ---------- | --------- |
| YYYY-MM-DD 10:15:20 | YYYY-MM-DD | 10:15:20 | 101         | YA         | QR Webcam |

---

## 🛠️ Tech Stack

* **Python 3.8+**
* **OpenCV** (QR code detection)
* **Pandas + OpenPyXL** (Excel storage)
* **Pillow** (QR image handling)

---

## 💡 Future Improvements

* Student database with photos
* Admin dashboard to view/export attendance reports
* Email/SMS notifications for parents

---

## 📜 License

This project is licensed under the **MIT License**.
Feel free to use and improve 🚀
