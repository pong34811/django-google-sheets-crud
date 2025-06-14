import gspread
from google.oauth2.service_account import Credentials

# เพิ่ม scope สำหรับ Sheets และ Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# โหลด credentials
creds = Credentials.from_service_account_file(
    "credentials/credentials.json", scopes=SCOPES
)

client = gspread.authorize(creds)

# ใช้ ID แทนชื่อ
SPREADSHEET_ID = "1t0ykHrH8CS2Cn9GLL1LUUj9N7JWsW7NogQjdscDOqos"
sheet = client.open_by_key(SPREADSHEET_ID).get_worksheet(1)

# ----- CRUD Functions -----

# CREATE
def add_row(data: list):
    sheet.append_row(data)

# READ
def get_all_data():
    return sheet.get_all_records()

# UPDATE
def update_row(row_number: int, data: list):
    """
    อัปเดตรายการที่บรรทัด row_number (เริ่มจาก 1) ด้วย data (list)
    แต่ในความเป็นจริงจะอัปเดตแถว row_number + 1 (ข้าม header)
    """
    actual_row = row_number + 1  # เพิ่ม 1 เพื่อข้าม header แถวแรก
    cell_range = f"A{actual_row}:{chr(64+len(data))}{actual_row}"
    sheet.update(cell_range, [data])

# DELETE
def delete_row(row_number: int):
    """
    ลบบรรทัดที่ row_number (เริ่มจาก 2 แทน 1)
    """
    sheet.delete_rows(row_number + 1)

