# qr_scanner.py
# Scans QR codes via webcam using OpenCV's built-in QRCodeDetector (no external zbar needed)
# Logs attendance to attendance_qr.xlsx (one row per scan per day)
import os
import sys
import datetime as dt
import pandas as pd
import cv2

ATTENDANCE_FILE = "attendance_qr.xlsx"

def parse_payload(data: str):
    """
    Expected format: ID=101|NAME=Arun Kumar
    Returns (student_id, name) or (None, None) if invalid.
    """
    try:
        parts = dict(p.split("=", 1) for p in data.split("|"))
        sid = parts.get("ID", "").strip()
        name = parts.get("NAME", "").strip()
        if sid and name:
            return sid, name
    except Exception:
        pass
    return None, None

def read_attendance():
    if os.path.exists(ATTENDANCE_FILE):
        try:
            return pd.read_excel(ATTENDANCE_FILE)
        except Exception:
            # corrupted or open in Excel: save a backup name and start new
            backup = f"attendance_backup_{int(dt.datetime.now().timestamp())}.xlsx"
            os.rename(ATTENDANCE_FILE, backup)
            return pd.DataFrame(columns=["timestamp","date","time","student_id","name","source"])
    else:
        return pd.DataFrame(columns=["timestamp","date","time","student_id","name","source"])

def already_marked_today(df, sid, date_str):
    if df.empty:
        return False
    subset = df[(df["student_id"] == sid) & (df["date"] == date_str)]
    return not subset.empty

def append_and_save(df, row):
    df2 = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    # Write whole file each time; simple and reliable for demo-size data
    df2.to_excel(ATTENDANCE_FILE, index=False)
    return df2

def draw_polygon(frame, points):
    pts = points.astype(int).reshape(-1, 2)
    for i in range(len(pts)):
        p1 = tuple(pts[i])
        p2 = tuple(pts[(i + 1) % len(pts)])
        cv2.line(frame, p1, p2, (0, 255, 0), 2)
    return frame

def main():
    print("Opening webcam... Press 'q' to quit.")
    cap = cv2.VideoCapture(0)  # try 1 or 2 if you have multiple cameras
    if not cap.isOpened():
        print("ERROR: Could not open camera. If another app is using it, close that app and retry.")
        sys.exit(1)

    detector = cv2.QRCodeDetector()
    attendance_df = read_attendance()
    today_str = dt.date.today().isoformat()
    session_scanned = set()  # avoid double spam within same run

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Camera frame not received. Exiting...")
            break

        # Try multi QR first (OpenCV 4.5+), else fallback to single
        decoded_items = []
        try:
            retval, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)
            if retval and decoded_info is not None and points is not None:
                for i, data in enumerate(decoded_info):
                    if data:
                        decoded_items.append((data, points[i]))
        except Exception:
            data, pts, _ = detector.detectAndDecode(frame)
            if data:
                decoded_items.append((data, pts))

        # Process any decoded QRs
        for data, pts in decoded_items:
            if pts is not None:
                frame = draw_polygon(frame, pts)

            sid, name = parse_payload(data)
            label = "Invalid QR"
            color = (0, 0, 255)

            if sid and name:
                key = f"{sid}@{today_str}"
                if key in session_scanned or already_marked_today(attendance_df, sid, today_str):
                    label = f"{sid} - {name} (Already Marked Today)"
                    color = (0, 165, 255)
                else:
                    now = dt.datetime.now()
                    row = {
                        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                        "date": now.date().isoformat(),
                        "time": now.strftime("%H:%M:%S"),
                        "student_id": sid,
                        "name": name,
                        "source": "QR Webcam",
                    }
                    attendance_df = append_and_save(attendance_df, row)
                    session_scanned.add(key)
                    label = f"Marked: {sid} - {name}"
                    color = (0, 255, 0)
                    # optional beep on Windows
                    try:
                        import winsound
                        winsound.Beep(1200, 120)
                    except Exception:
                        pass

            # Put label near the first corner if available
            org = (10, 30)
            if pts is not None:
                p0 = pts.reshape(-1, 2)[0]
                org = (int(p0[0]), int(p0[1]) - 10)

            cv2.putText(frame, label, org, cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

        cv2.imshow("QR Attendance - Press 'q' to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved attendance to {ATTENDANCE_FILE}")

if __name__ == "__main__":
    main()
