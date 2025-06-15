import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from datetime import datetime

def create_session(retries=3, backoff_factor=1):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_events_from_interpark():
    url     = "https://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&Sort=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    session = create_session()
    try:
        resp = session.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ 네트워크 오류 발생: {e}")
        return []
    
    resp.encoding = "euc-kr"  # 한글 깨짐 방지
    soup = BeautifulSoup(resp.text, "html.parser")

    # 썸네일 셀(td.RKthumb) 기준으로 각 <tr> 행을 모두 선택
    thumb_cells = soup.select("td.RKthumb")
    print(f"▶ thumb 셀 개수(행 개수): {len(thumb_cells)}")

    events = []
    for td in thumb_cells:
        tr = td.parent  # <td>의 부모가 <tr>

        # 제목 & 링크
        title_a = tr.select_one("td.RKtxt span.fw_bold a")
        if not title_a:
            continue
        title = title_a.get_text(strip=True)
        link  = "https://ticket.interpark.com" + title_a["href"]

        # 장소 (첫 번째 td.Rkdate 안의 <a>)
        venue_el = tr.select_one("td.Rkdate a")
        venue = venue_el.get_text(strip=True) if venue_el else "장소 정보 없음"

        # 기간 (두 번째 td.Rkdate)
        date_cells = tr.select("td.Rkdate")
        if len(date_cells) > 1:
            period = date_cells[1].get_text(" ", strip=True)
        else:
            period = "기간 정보 없음"

        events.append({
            "title": title,
            "link":  link,
            "venue": venue,
            "date":  period
        })

    return events

def recommend_today_event():
    evs   = fetch_events_from_interpark()
    today = datetime.today().strftime("%Y.%m.%d")
    print(f"\n📅 오늘({today}) 볼 수 있는 이벤트:")
    found = False
    for e in evs:
        if today in e["date"]:
            print(f"✅ {e['title']}")
            print(f"   📍 {e['venue']}")
            print(f"   🗓️ {e['date']}")
            print(f"   🔗 {e['link']}\n")
            found = True
    if not found:
        print("😢 오늘 볼 수 있는 이벤트가 없습니다.")

def search_by_region_event():
    region = input("찾을 지역(장소) 키워드 > ").strip()
    evs    = fetch_events_from_interpark()
    results = [e for e in evs if region in e["venue"]]
    print(f"\n📍 '{region}' 지역 이벤트 {len(results)}건:")
    if results:
        for e in results:
            print(f"✅ {e['title']}  | 장소: {e['venue']}  | 기간: {e['date']}  | 링크: {e['link']}")
    else:
        print("😢 해당 지역 이벤트가 없습니다.")

def search_by_keyword_event():
    kw  = input("검색할 키워드 > ").strip()
    evs = fetch_events_from_interpark()
    results = [e for e in evs if kw in e["title"]]
    print(f"\n🔍 제목에 '{kw}' 포함 이벤트 {len(results)}건:")
    if results:
        for e in results:
            print(f"✅ {e['title']}  | 장소: {e['venue']}  | 기간: {e['date']}  | 링크: {e['link']}")
    else:
        print("😢 해당 키워드 이벤트가 없습니다.")

def show_menu():
    print("\n🎪 인터파크 이벤트 추천기 🎪")
    print("1. 오늘 볼 수 있는 이벤트 추천")
    print("2. 지역별 이벤트 찾기")
    print("3. 키워드로 이벤트 검색")
    print("4. 종료하기")

def main():
    while True:
        show_menu()
        choice = input("번호 선택 > ").strip()
        if choice == "1":
            recommend_today_event()
        elif choice == "2":
            search_by_region_event()
        elif choice == "3":
            search_by_keyword_event()
        elif choice == "4":
            print("프로그램을 종료합니다. 감사합니다! 🎉")
            break
        else:
            print("⚠️ 1~4번 중 하나를 입력해주세요.")

if __name__ == "__main__":
    main()
