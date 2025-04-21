import unicodedata
import random

def normalize_string(s):
    return unicodedata.normalize('NFKC', s.strip().lower())

def load_flashcards(filename="flashcards.txt"):
    flashcards = {}
    current_unit = None
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_unit = line[1:-1]
                flashcards[current_unit] = {}
            elif ": " in line and current_unit:
                word, meaning = line.split(": ", 1)
                flashcards[current_unit][word] = meaning
    return flashcards

def get_priority_list(wrong_file="wrong_answers.txt"):
    priority_words = set()
    try:
        with open(wrong_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("解釋: "):
                    parts = line.strip().split(", ")
                    correct_answer = parts[2].split(": ")[1]
                    priority_words.add(correct_answer)
    except FileNotFoundError:
        pass
    return priority_words

def save_incorrect(incorrect_answers, path="wrong_answers.txt"):
    if not incorrect_answers:
        return
    with open(path, "a", encoding="utf-8", errors="ignore") as f:
        f.write("\n=== 測驗紀錄 ===\n")
        for meaning, user_answer, correct_answer in incorrect_answers:
            clean_user_answer = ''.join(c for c in user_answer if unicodedata.category(c)[0] != "C")
            f.write(f"解釋: {meaning}, 你的回答: {clean_user_answer}, 正確答案: {correct_answer}\n")

def select_quiz_questions(flashcards_dict, num=10, prioritize=True):
    all_items = list(flashcards_dict.items())
    priority_words = get_priority_list() if prioritize else set()
    priority = [(w, m) for w, m in all_items if w in priority_words]
    others = [(w, m) for w, m in all_items if w not in priority_words]
    random.shuffle(others)
    questions = priority + others
    return questions[:num]
