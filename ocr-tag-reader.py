import cv2
import pytesseract
import csv
from datetime import datetime

# OCR設定
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# CSVファイルの準備
csv_file = open('read_numbers.csv', mode='a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'Number'])

# カメラ起動（PC内蔵カメラ）
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 前処理（グレースケール → ブラー → 二値化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCRで数値読み取り
    text = pytesseract.image_to_string(thresh, config=custom_config).strip()

    # 表示
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Tag Reader', frame)

    # "s"キーを押したら読み取った文字を保存
    if cv2.waitKey(1) & 0xFF == ord('s'):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow([now, text])
        print(f"保存: {text}")
    
    # "q"キーで終了
    if cv2.waitKey(1) % 0xFF == ord('q'):
        break

cap.relase()
csv_file.close()
cv2.destroyAllWindows()