import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials/credentials.json", scopes=SCOPES
)

client = gspread.authorize(creds)

SPREADSHEET_ID = "1t0ykHrH8CS2Cn9GLL1LUUj9N7JWsW7NogQjdscDOqos"

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# ฟังก์ชันดึงข้อมูลทั้งหมด
def get_all_data():
    return sheet.get_all_records()

# ฟังก์ชันเช็ค username ว่ามีหรือไม่
def is_username_exists(username):
    data = get_all_data()
    for row in data:
        if row.get("username") == username:
            return True
    return False

# ฟังก์ชันสมัครสมาชิก (เพิ่มแถวใหม่)
def register_user(id, username, password, is_active, created_by, created):
    row = [id, username, password, is_active, created_by, created]
    sheet.append_row(row)

# ฟังก์ชันหาผู้ใช้ด้วย username และ password
def find_user_by_credentials(username, password):
    data = get_all_data()
    for row in data:
        row_username = str(row.get("username", "")).strip()
        row_password = str(row.get("password", "")).strip()
        if row_username == username.strip() and row_password == password.strip():
            return row
    return None

def update_last_join(username, last_join):
    # ดึงข้อมูลทั้งหมด
    all_records = sheet.get_all_records()

    # หาแถวที่ username ตรงกัน
    for idx, row in enumerate(all_records, start=2):  # เริ่มนับแถวที่ 2 เพราะแถว 1 header
        if row.get("username") == username:
            # สมมติว่าคอลัมน์ last_join เป็นคอลัมน์ที่ 7 (G)
            # ปรับเลขคอลัมน์ให้ตรงกับ Sheet จริงของคุณ
            col_index = 7
            sheet.update_cell(idx, col_index, last_join)
            break