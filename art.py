def show_menu():
    print("\n🔭 전시회 망원경 🔭 ")
    print("1. 오늘 볼 수 있는 전시 추천🖼️")
    print("2. 지역별 전시회 찾기 ⛱️")
    print("3. 관심 키워드 전시 검색🪄")
    print("0. 끝내기")

def main():
    while True:
        show_menu()
        choice = input("번호를 선택하세요 > ")

        if choice == "1":
            print("▶ 오늘 전시 중인 작품을 추천합니다. (아직 기능 준비 중)")
        elif choice == "2":
            region = input("어느 지역의 전시를 찾을까요? > ")
            print(f"▶ [{region}] 지역 전시 정보 출력 예정입니다. (아직 기능 준비 중)")
        elif choice == "3":
            keyword = input("검색할 키워드를 입력하세요 (예: 디자인, 건축 등) > ")
            print(f"▶ 키워드 [{keyword}] 관련 전시 정보 출력 예정입니다. (아직 기능 준비 중)")
        elif choice == "0":
            print("프로그램을 종료합니다. 감사합니다!")
            break
        else:
            print("❗ 잘못된 입력입니다. 0~3 중에서 골라주세요.")

# 프로그램 실행
if __name__ == "__main__":
    main()
