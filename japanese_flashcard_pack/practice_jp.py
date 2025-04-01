
import random
from colorama import Fore, Style
import unicodedata

def normalize_string(s):
    return unicodedata.normalize('NFKC', s.strip().lower())

def load_flashcards(filename="flashcards.txt"):
    flashcards = {}
    current_unit = None

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    current_unit = line[1:-1]
                    flashcards[current_unit] = {}
                elif current_unit and ": " in line:
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        word, meaning = parts
                        flashcards[current_unit][word] = meaning
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到。請確認文件存在並重新運行。")
    return flashcards

def list_units(flashcards):
    units = list(flashcards.keys())
    print("可用的單元：")
    for idx, unit in enumerate(units, start=1):
        print(f"{idx}. {unit} (學習/測驗模式)")
    return units

def study_mode(flashcards, unit):
    print(f"\n學習模式：{unit}")
    for word, meaning in flashcards[unit].items():
        print(f"{word}: {meaning}\n")
    input("已完成學習，按 Enter 返回主選單...")

def save_incorrect_answers(incorrect_answers):
    if not incorrect_answers:
        return
    with open("wrong_answers.txt", "a", encoding="utf-8") as f:
        f.write("\n=== 測驗紀錄 ===\n")
        for meaning, user_answer, correct_answer in incorrect_answers:
            f.write(f"解釋: {meaning}, 你的回答: {user_answer}, 正確答案: {correct_answer}\n")

def quiz_mode(flashcards, unit):
    print(f"\n測驗模式：{unit} (輸入 'home' 返回主頁)")
    flashcards_list = list(flashcards[unit].items())
    random.shuffle(flashcards_list)
    total_questions = len(flashcards_list)
    correct_answers = 0
    incorrect_answers = []

    for word, meaning in flashcards_list:
        user_answer = input(f"解釋：{meaning}\n請輸入對應假名: ").strip()
        if normalize_string(user_answer) == "home":
            print("返回主頁...")
            return
        elif normalize_string(user_answer) == normalize_string(word):
            print(Fore.GREEN + "正確！" + Style.RESET_ALL)
            correct_answers += 1
        else:
            print(Fore.RED + f"錯誤！正確答案是：{word}" + Style.RESET_ALL)
            incorrect_answers.append((meaning, user_answer, word))
        print()

    print("\n測驗結束！")
    if incorrect_answers:
        print("你答錯的題目：")
        for meaning, user_answer, correct_answer in incorrect_answers:
            print(f"{meaning}: 你的回答：{user_answer}, 正確答案：{correct_answer}")
        save_incorrect_answers(incorrect_answers)
        print("\n已將錯誤題目記錄至 'wrong_answers.txt'")
    print(f"\n答對率: {correct_answers / total_questions * 100:.2f}%")
    input("按 Enter 返回主選單...")

def review_wrong_answers():
    try:
        with open("wrong_answers.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("目前沒有錯誤紀錄。")
        input("按 Enter 返回主選單...")
        return

    questions = []
    for line in lines:
        if line.startswith("解釋: "):
            parts = line.strip().split(", ")
            meaning = parts[0].split(": ")[1]
            correct_answer = parts[2].split(": ")[1]
            questions.append((meaning, correct_answer))

    if not questions:
        print("目前沒有錯誤紀錄。")
        input("按 Enter 返回主選單...")
        return

    print("\n複習錯誤題目模式 (輸入 'home' 返回主頁)")
    random.shuffle(questions)
    correct_answers = 0

    for meaning, correct_answer in questions:
        user_answer = input(f"解釋：{meaning}\n請輸入對應假名: ").strip()
        if normalize_string(user_answer) == "home":
            print("返回主頁...")
            return
        elif normalize_string(user_answer) == normalize_string(correct_answer):
            print(Fore.GREEN + "正確！" + Style.RESET_ALL)
            correct_answers += 1
        else:
            print(Fore.RED + f"錯誤！正確答案是：{correct_answer}" + Style.RESET_ALL)
        print()

    print("\n複習結束！")
    print(f"\n答對率: {correct_answers / len(questions) * 100:.2f}%")
    input("按 Enter 返回主選單...")

def main():
    flashcards = load_flashcards()
    if not flashcards:
        print("無法載入卡片資料，請檢查文件內容。")
        return

    while True:
        print("\n選單：")
        print("1. 單元學習/測驗")
        print("2. 複習錯誤題目")
        print("3. 退出")
        choice = input("請輸入選項 (1/2/3): ").strip()

        if choice == "3":
            print("已退出。")
            break
        elif choice == "1":
            units = list_units(flashcards)
            unit_choice = input("\n請輸入單元編號: ").strip()
            if unit_choice.isdigit() and 1 <= int(unit_choice) <= len(units):
                unit = units[int(unit_choice) - 1]
                mode = input(f"\n你已選擇 {unit}。選擇模式: 1) 學習模式  2) 測驗模式\n請輸入選項 (1/2): ").strip()
                if mode == "1":
                    study_mode(flashcards, unit)
                elif mode == "2":
                    quiz_mode(flashcards, unit)
                else:
                    print("無效選項，返回主選單。")
            else:
                print("無效的選擇，請重新選擇。")
        elif choice == "2":
            review_wrong_answers()
        else:
            print("無效選項，請重新選擇。")

if __name__ == "__main__":
    main()
