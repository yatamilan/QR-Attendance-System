# qr_generator.py
# Creates a PNG QR for each student in students.csv and saves to ./qr_codes

import os
import pandas as pd
import qrcode

INPUT_CSV = "students.csv"
OUT_DIR = "qr_codes"

def safe_filename(s: str) -> str:
    keep = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in s.strip())
    return keep

def make_payload(student_id: str, name: str) -> str:
    # Simple, easy-to-parse payload
    # Example: ID=101|NAME=Arun Kumar
    return f"ID={student_id}|NAME={name}"

def main():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR, exist_ok=True)

    df = pd.read_csv(INPUT_CSV, dtype=str)  # keep IDs as strings
    for _, row in df.iterrows():
        sid = row["student_id"].strip()
        name = row["name"].strip()

        payload = make_payload(sid, name)

        img = qrcode.make(payload)
        filename = f"{safe_filename(sid)}_{safe_filename(name)}.png"
        out_path = os.path.join(OUT_DIR, filename)
        img.save(out_path)
        print(f"Created: {out_path} -> {payload}")

    print("\nAll QR codes generated in ./qr_codes")
    print("Tip: Open a QR on your phone screen to test scanning.")

if __name__ == "__main__":
    main()
