import gspread
from google.oauth2.service_account import Credentials

# เพิ่ม scope สำหรับ Sheets และ Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# โหลด credentials
creds = Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

client = gspread.authorize(creds)

# ใช้ ID แทนชื่อ
SPREADSHEET_ID = "1t0ykHrH8CS2Cn9GLL1LUUj9N7JWsW7NogQjdscDOqos"

# เปิด sheet
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

def get_all_data():
    return sheet.get_all_records()

def add_row(data):
    sheet.append_row(data)
