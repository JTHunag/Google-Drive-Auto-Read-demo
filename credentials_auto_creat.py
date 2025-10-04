import json
import os

with open("credentials.json", "r") as f:
    data = json.load(f)

os.makedirs(".streamlit", exist_ok=True)

with open(".streamlit/secrets.toml", "w") as f:
    f.write('GOOGLE_OAUTH_CREDENTIALS_JSON = """\\\n')
    json.dump(data, f, indent=2)
    f.write('\n"""')

print("✅ 已建立 .streamlit/secrets.toml")