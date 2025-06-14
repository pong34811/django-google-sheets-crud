import gspread
from google.oauth2.service_account import Credentials
import uuid
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
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# ----- CRUD Functions -----
# READ
def get_all_data():
    return sheet.get_all_records()

def is_username_exists(username):
    data = get_all_data()
    for row in data:
        if row.get("username") == username:
            return True
    return False

def register_user(username, password):
    user_id = str(uuid.uuid4())
    sheet.append_row([user_id, username, password])

def find_user_by_credentials(username, password):
    data = get_all_data()
    for row in data:
        row_username = str(row.get("username", "")).strip()
        row_password = str(row.get("password", "")).strip()
        if row_username == username.strip() and row_password == password.strip():
            return row
    return None