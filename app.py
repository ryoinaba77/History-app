import streamlit as st
import pandas as pd
import random

# ===== データ読み込み =====
df = pd.read_csv("data.csv")

# ===== セッション初期化 =====
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "answer" not in st.session_state:
    st.session_state.answer = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "history" not in st.session_state:
    st.session_state.history = []  # (正誤, カテゴリ)

st.title("歴史問題ジェネレーター（本格版）")

mode = st.selectbox("問題タイプ", ["年号", "並び替え", "原因"])

# ===== 問題作成 =====
if st.button("問題を作る"):
    if mode == "年号":
        row = df.sample(1).iloc[0]
        st.session_state.current_q = f"{row['event']}の年号は？"
        st.session_state.answer = str(row["year"])
        st.session_state.category = row["era"]

    elif mode == "並び替え":
        sample = df.sample(4)
        q = "次を古い順に並べなさい\n"
        for i, r in enumerate(sample.itertuples()):
            q += f"{chr(65+i)}. {r.event}\n"
        st.session_state.current_q = q
        sorted_df = sample.sort_values("year")
        st.session_state.answer = " → ".join(sorted_df["event"])
        st.session_state.category = "時代横断"

    elif mode == "原因":
        row = df.sample(1).iloc[0]
        st.session_state.current_q = f"{row['event']}の原因は？"
        st.session_state.answer = row["cause"]
        st.session_state.category = row["category"]

# ===== 問題表示 =====
if st.session_state.current_q:
    st.subheader("問題")
    st.write(st.session_state.current_q)

    user_input = st.text_input("あなたの答え")

    if st.button("解答する"):
        st.session_state.total += 1

        # 判定（ゆるめ一致）
        correct = st.session_state.answer in user_input

        if correct:
            st.success("正解！")
            st.session_state.score += 1
        else:
            st.error("不正解")

        st.write(f"答え：{st.session_state.answer}")

        # 履歴保存
        st.session_state.history.append(
            (correct, st.session_state.category)
        )

# ===== スコア表示 =====
st.subheader("成績")
st.write(f"{st.session_state.score} / {st.session_state.total}")

# ===== 弱点分析 =====
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history, columns=["correct", "category"])
    weak = df_hist[df_hist["correct"] == False]["category"].value_counts()

    if not weak.empty:
        st.subheader("弱点分野")
        for k, v in weak.items():
            st.write(f"{k}：{v}問ミス")
    else:
        st.write("弱点なし！")
