import streamlit as st
import random
import os

def load_flashcards(file="flashcards.txt"):
    flashcards = {}
    current_unit = None
    # 確保使用相對於本檔案的路徑
    filepath = os.path.join(os.path.dirname(__file__), file)
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_unit = line[1:-1]
                flashcards[current_unit] = {}
            elif ": " in line and current_unit:
                key, value = line.split(": ", 1)
                flashcards[current_unit][key] = value
    return flashcards

def run_quiz(cards):
    st.header("Flashcards 無範圍測驗系統")
    if "idx" not in st.session_state:
        st.session_state.idx = 0
        st.session_state.order = list(cards.items())
        random.shuffle(st.session_state.order)
        st.session_state.score = 0
        st.session_state.total = len(st.session_state.order)
        st.session_state.history = []
        st.session_state.user_input = ""
        st.session_state.last_result = ""

    if st.session_state.idx < st.session_state.total:
        question, answer = st.session_state.order[st.session_state.idx]
        st.write(f"解釋：**{answer}**")
        st.session_state.user_input = st.text_input(
            "請輸入對應假名", value=st.session_state.user_input, key="input"
        )

        if st.button("提交"):
            user_input = st.session_state.user_input.strip()
            if user_input == question:
                st.session_state.last_result = f"✅ 正確！"
                st.session_state.score += 1
            else:
                st.session_state.last_result = f"❌ 錯誤！正確答案是：{question}"
                st.session_state.history.append((question, answer))

            st.session_state.user_input = ""  # 清空輸入
            st.session_state.idx += 1
            st.rerun()

        if st.session_state.last_result:
            st.markdown(st.session_state.last_result)
    else:
        st.write("測驗結束！")
        st.write(f"正確率：{st.session_state.score} / {st.session_state.total}")
        if st.session_state.history:
            st.write("你答錯的題目：")
            for q, a in st.session_state.history:
                st.write(f"- {q}: {a}")
        if st.button("重新開始"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def main():
    st.set_page_config(page_title="Flashcards 無範圍測驗", layout="centered")
    flashcards = load_flashcards()
    all_cards = {}
    for unit in flashcards:
        all_cards.update(flashcards[unit])
    run_quiz(all_cards)

if __name__ == "__main__":
    main()
