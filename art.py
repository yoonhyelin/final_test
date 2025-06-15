import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_exhibitions_from_naver(query):
    url = f"https://search.naver.com/search.naver?query={query}+전시"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    print("✅ HTML 받아오기 성공")
    print(soup.prettify()[:1000])  # HTML 앞부분 출력해서 구조 확인

    exhibitions = []
    # 아래는 아직 구현 중일 수 있음
    return exhibitions
    
def recommend_today(exhibitions):
    today = datetime.today().strftime("%m.%d")
    print(f"\n📅 오늘({today}) 추천 전시:")
    found = False
    for ex in exhibitions:
        if today in ex['date']:
            print(f"✅ {ex['title']}")
            print(f"📍 장소: {ex['venue']}")
            print(f"🗓️ 기간: {ex['date']}")
            print(f"🔗 링크: {ex['link']}\n")
            found = True
    if not found:
        print("😢 오늘 관람할 수 있는 전시가 없어요.")

def search_by_region():
    region = input("찾을 지역을 입력하세요 (예: 서울, 부산 등) > ")
    exhibitions = fetch_exhibitions_from_naver(region)
    print(f"\n📍 '{region}' 지역 전시 {len(exhibitions)}건:")
    if not exhibitions:
        print("😢 전시 정보를 찾을 수 없습니다.")
    for ex in exhibitions:
        print(f"✅ {ex['title']}")
        print(f"📍 장소: {ex['venue']}")
        print(f"🗓️ 기간: {ex['date']}")
        print(f"🔗 링크: {ex['link']}\n")

def search_by_keyword():
    keyword = input("검색할 키워드를 입력하세요 (예: 사진, 디자인 등) > ")
    exhibitions = fetch_exhibitions_from_naver(keyword)
    print(f"\n🔍 '{keyword}' 키워드 전시 {len(exhibitions)}건:")
    if not exhibitions:
        print("😢 해당 키워드 전시를 찾을 수 없습니다.")
    for ex in exhibitions:
        print(f"✅ {ex['title']}")
        print(f"📍 장소: {ex['venue']}")
        print(f"🗓️ 기간: {ex['date']}")
        print(f"🔗 링크: {ex['link']}\n")

def show_menu():
    print("\n🎨 전시회 추천기 🎨")
    print("1. 오늘 볼 수 있는 전시 추천")
    print("2. 지역별 전시회 찾기")
    print("3. 키워드로 전시 검색")
    print("0. 종료")

def main():
    while True:
        show_menu()
        choice = input("번호 선택 > ")
        if choice == "1":
            exhibitions = fetch_exhibitions_from_naver("서울")
            recommend_today(exhibitions)
        elif choice == "2":
            search_by_region()
        elif choice == "3":
            search_by_keyword()
        elif choice == "0":
            print("프로그램을 종료합니다. 감사합니다! 🎉")
            break
        else:
            print("⚠️ 올바른 번호를 입력해주세요.")

if __name__ == "__main__":
    main()
