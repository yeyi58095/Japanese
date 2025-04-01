
import random
from colorama import Fore, Style
import unicodedata

def normalize_string(s):
    return unicodedata.normalize('NFKC', s.strip().lower())

def load_flashcards(filename="flashcards.txt"):
    flashcards = {}
    learn_only_units = set()
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
            incorrect_answers.append((word, meaning))
        print()

    print("\n測驗結束！")
    if incorrect_answers:
        print("你答錯的題目：")
        for word, meaning in incorrect_answers:
            print(f"{meaning}: {word}")
    print(f"\n答對率: {correct_answers / total_questions * 100:.2f}%")
    input("按 Enter 返回主選單...")

def main():
    flashcards = load_flashcards()
    if not flashcards:
        print("無法載入卡片資料，請檢查文件內容。")
        return

    while True:
        units = list_units(flashcards)
        choice = input("\n請輸入單元編號、'all' 進行無範圍測驗，或 'exit' 退出: ").strip()

        if choice == "exit":
            print("已退出。")
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(units):
            unit = units[int(choice) - 1]
            mode = input(f"\n你已選擇 {unit}。選擇模式: 1) 學習模式  2) 測驗模式\n請輸入選項 (1/2): ").strip()
            if mode == "1":
                study_mode(flashcards, unit)
            elif mode == "2":
                quiz_mode(flashcards, unit)
            else:
                print("無效選項，返回主頁。")
        else:
            print("無效的選擇，請重新選擇。")

if __name__ == "__main__":
    main()
