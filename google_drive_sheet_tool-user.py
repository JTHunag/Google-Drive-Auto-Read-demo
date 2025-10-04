import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email'
]

# ----------------- Streamlit Session -----------------
for key, default in {
    'creds': None,
    'user_email': None,
    'sheets': []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ----------------- OAuth Functions -----------------
def get_credentials():
    credentials_json = st.secrets.get("GOOGLE_OAUTH_CREDENTIALS_JSON")
    if not credentials_json:
        st.error("請在 .streamlit/secrets.toml 裡設定 GOOGLE_OAUTH_CREDENTIALS_JSON")
        return None
    flow = InstalledAppFlow.from_client_config(json.loads(credentials_json), SCOPES, redirect_uri="http://localhost:8501")
    creds = flow.run_local_server(port=0)
    return creds

def get_user_email(creds):
    oauth2_service = build('oauth2', 'v2', credentials=creds)
    user_info = oauth2_service.userinfo().get().execute()
    return user_info.get('email')

def list_google_sheets(drive_service, user_email):
    query = f"mimeType='application/vnd.google-apps.spreadsheet' and '{user_email}' in owners"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def read_first_sheet_content(sheets_service, sheet_id):
    metadata = sheets_service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    sheet_name = metadata['sheets'][0]['properties']['title']
    result = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    values = result.get('values', [])
    return sheet_name, values

# ----------------- Streamlit UI -----------------
st.title("📊 Google Sheets 網頁工具 (Session + Secrets)")

import streamlit as st

# 初始化 session_state
for key in ['creds', 'user_email', 'sheets', 'page']:
    if key not in st.session_state:
        st.session_state[key] = None

# 登入流程
if st.session_state['creds'] is None:
    st.write("請登入 Google 帳號")
    if st.button("登入 Google 帳號"):
        creds = get_credentials()  # 你的 OAuth 函數
        if creds:
            user_email = get_user_email(creds)  # 取得登入者 Email
            # 儲存登入資訊
            st.session_state.creds = creds
            st.session_state.user_email = user_email
            st.session_state['page'] = "main"
            st.success(f"登入成功！Email: {user_email}")
            # 登入後立即刷新頁面，顯示主頁
            st.session_state['show_main'] = True

# 主頁面（登入後）
if st.session_state.get('creds') is not None or st.session_state.get('show_main'):
    st.session_state['show_main'] = False  # 清除旗標，避免重複刷新
    st.write(f"已登入: {st.session_state['user_email']}")


    # 登出按鈕
    if st.button("登出"):
        for key in ['creds', 'user_email', 'sheets']:
            st.session_state[key] = None
        st.session_state['page'] = "login"
        st.success("已登出，請重新登入。")
        st.rerun()

# ----------------- 讀取 Google Sheets -----------------
if st.session_state.creds:
    creds = st.session_state.creds
    user_email = st.session_state.user_email
    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)

    # 列出 Sheets
    if not st.session_state.sheets:
        st.session_state.sheets = list_google_sheets(drive_service, user_email)

    sheets = st.session_state.sheets

    if not sheets:
        st.warning("你沒有擁有任何 Google Sheets！")
    else:
        sheet_names = [s['name'] for s in sheets]
        selected_sheet_name = st.selectbox("選擇試算表", sheet_names)
        selected_sheet = next(s for s in sheets if s['name'] == selected_sheet_name)

        if selected_sheet:
            sheet_link = f"https://docs.google.com/spreadsheets/d/{selected_sheet['id']}"
            st.markdown(f"🔗 [前往試算表]({sheet_link})", unsafe_allow_html=True)

            sheet_name, values = read_first_sheet_content(sheets_service, selected_sheet['id'])
            st.subheader(f"📄 {sheet_name} 內容")
            if values:
                st.table(values)
            else:
                st.info("此分頁沒有資料。")