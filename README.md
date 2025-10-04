# 📊 Streamlit Google Sheets 網頁互動工具

這是一個使用 **Python + Streamlit** 製作的網頁互動應用程式，\
讓使用者能透過 **Google OAuth 登入帳號**，自動列出自己擁有的 **Google
Sheets 試算表**，\
並可直接在網頁上讀取與顯示試算表內容。

------------------------------------------------------------------------

## 🚀 功能特色

-   🔑 使用者可登入 Google 帳號並自動取得 Email\
-   📄 自動列出使用者 **擁有者為本人** 的 Google Sheets\
-   🧾 可選擇任意試算表並即時讀取內容\
-   🔁 登入狀態會自動保存，避免每次互動都要重新授權\
-   🛡️ 程式會自動檢查 OAuth 授權範圍（SCOPES）

------------------------------------------------------------------------

## 🧰 安裝需求

### 1. 安裝 Python

請確認系統中已安裝 **Python 3.8 或以上版本**。

在 macOS / Linux 檢查：

``` bash
python3 --version
```

------------------------------------------------------------------------

### 2. 安裝必要套件

在終端機執行以下指令安裝相依套件：

``` bash
pip install streamlit google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

------------------------------------------------------------------------

### 3. 建立 Google OAuth 2.0 憑證

1.  前往 [Google Cloud Console](https://console.cloud.google.com/)
2.  建立新專案\
3.  啟用以下 API：
    -   **Google Drive API**
    -   **Google Sheets API**
4.  建立「OAuth 2.0 用戶端 ID」
    -   應用程式類型選擇：**Desktop App** or **桌面應用程式**
5.  下載JSON將其改名為 `credentials.json` 並放在專案根目錄中
<img width="567" height="675" alt="image" src="https://github.com/user-attachments/assets/d19dd9cf-e655-4574-bfb7-a270631d0230" />
6.  使用 `credentials_auto_creat.py` 建立 `.streamlit/secrets.toml` 

------------------------------------------------------------------------

## 🧑‍💻 使用方式

1.  確認 `.streamlit/secrets.toml` 已放在專案資料夾中\

2.  啟動 Streamlit 伺服器：

    ``` bash
    streamlit run app.py
    ```

3.  瀏覽器會自動開啟 `http://localhost:8501`

4.  點擊「登入 Google 帳號」按鈕

5.  授權後會自動顯示你擁有的 Google Sheets 清單

6.  選擇試算表即可讀取與顯示內容

------------------------------------------------------------------------

## ⚠️ 注意事項

-   若程式顯示 `invalid_scope`：
    -   表示舊的 `token.json` 缺少新的授權範圍\
    -   程式會自動重新要求授權
-   程式僅會列出你為 **擁有者** 的 Google Sheets\
-   若該試算表沒有內容，介面會顯示提示訊息 ⚠️\
-   若遇到登入後頁面未更新，可手動刷新頁面

------------------------------------------------------------------------

## 📁 檔案結構

  檔案名稱                    說明
  --------------------------- ---------------------------------------
  `app.py`                    Streamlit 主程式
  `credentials.json`          Google OAuth 2.0 憑證（從 GCP 下載）
  `token.json`                OAuth 存取權杖，程式自動產生
  `.streamlit/secrets.toml`   用於部署至 Streamlit Cloud 時存放憑證

------------------------------------------------------------------------

## 🔒 OAuth 授權範圍 (SCOPES)

  ---------------------------------------------------------------------------------------------
  範圍                                                      用途
  --------------------------------------------------------- -----------------------------------
  `https://www.googleapis.com/auth/drive.readonly`          讀取 Google Drive 檔案清單

  `https://www.googleapis.com/auth/spreadsheets.readonly`   讀取 Google Sheets 內容

  `openid`                                                  進行 OAuth 登入驗證

  `https://www.googleapis.com/auth/userinfo.email`          取得使用者 Email
  ---------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 📬 聯絡方式

若有問題或建議，歡迎提出 [GitHub Issue](https://github.com/)
或直接聯絡作者 🙌
