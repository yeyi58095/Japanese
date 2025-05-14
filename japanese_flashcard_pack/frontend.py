import streamlit as st
import random
from logic import load_flashcards, normalize_string, save_incorrect

def main():
    st.set_page_config(page_title="Flashcards 測驗", layout="centered")
    st.title("📘 日文單字 Flashcards 測驗")

    # 載入題庫
    try:
        flashcards = load_flashcards()
    except FileNotFoundError as e:
        st.error(str(e))
        return

    # 單元選擇
    unit_names = list(flashcards.keys())
    unit = st.selectbox("選擇單元", unit_names)

    # 題庫與總題數
    all_cards = list(flashcards[unit].items())
    total_available = len(all_cards)
    random.shuffle(all_cards)  # 題目打亂

    # 顯示總題數提示
    st.markdown(f"💡 本單元共有 **{total_available}** 題")

    # 題數選擇（加上「全部」選項）
    options = list(range(1, total_available + 1))
    options.append("全部")
    choice = st.selectbox("請選擇要測驗的題數", options, index=min(9, len(options)-2))
    num_questions = total_available if choice == "全部" else int(choice)

    # 初始化測驗狀態
    if st.button("開始測驗") or "selected" not in st.session_state or st.session_state.get("current_unit") != unit:
        st.session_state.selected = all_cards[:num_questions]
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.total = len(st.session_state.selected)
        st.session_state.wrongs = []
        st.session_state.current_unit = unit
        st.session_state.last_result = ""

    # 進行中題目
    if "selected" in st.session_state and st.session_state.idx < st.session_state.total:
        q, a = st.session_state.selected[st.session_state.idx]
        st.write(f"解釋：**{a}**")
        user_input = st.text_input("請輸入對應假名", key=f"q_{st.session_state.idx}")

        if st.button("提交"):
            if normalize_string(user_input) == normalize_string(q):
                st.session_state.last_result = f"✅ 正確！"
                st.session_state.score += 1
            else:
                st.session_state.last_result = f"❌ 錯誤！正確答案是：{q}"
                st.session_state.wrongs.append((a, user_input, q))
            st.session_state.idx += 1
            st.rerun()

        if st.session_state.last_result:
            st.markdown(st.session_state.last_result)

        if st.button("退出"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # 測驗結束
    elif "selected" in st.session_state and st.session_state.idx >= st.session_state.total:
        st.subheader("✅ 測驗結束")
        st.write(f"正確率：{st.session_state.score} / {st.session_state.total}")

        if st.session_state.wrongs:
            st.write("你答錯的題目：")
            for meaning, user, correct in st.session_state.wrongs:
                st.write(f"- {meaning}: 你的回答：{user}, 正解：{correct}")
            save_incorrect(st.session_state.wrongs)

        if st.button("重新開始"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
