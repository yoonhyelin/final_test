import os

possible_paths = [
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"✅ Chrome이 설치된 경로: {path}")
        break
else:
    print("❌ Chrome 설치 경로를 찾을 수 없습니다.")
