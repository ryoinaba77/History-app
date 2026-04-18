import streamlit as st
import pandas as pd
import random

df = pd.read_csv("data.csv")

# ===== 弱点優先 =====
def weighted_sample(df, history):
    if len(history) < 5:
        return df.sample(1)

    wrong = [h[1] for h in history if not h[0]]
    if not wrong:
        return df.sample(1)

    weak = random.choice(wrong)
    filtered = df[df["era"] == weak]

    return filtered.sample(1) if len(filtered) else df.sample(1)

# ===== 初期化 =====
if "q" not in st.session_state:
    st.session_state.q = ""
if "a" not in st.session_state:
    st.session_state.a = ""
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "cat" not in st.session_state:
    st.session_state.cat = ""

st.title("早実対策・社会（特化版）")

mode = st.selectbox("問題タイプ", [
    "年代整序（最重要）",
    "因果関係",
    "記述（50字）",
    "用語確認"
])

# ===== 出題 =====
if st.button("問題を出す"):

    if mode == "年代整序（最重要）":
        sample = df.sample(5)
        q = "次を古い順に並べなさい\n"
        for i, r in enumerate(sample.itertuples()):
            q += f"{chr(65+i)}. {r.event}\n"

        st.session_state.q = q
        ans = sample.sort_values("year")
        st.session_state.a = " → ".join(ans["event"])
        st.session_state.cat = "横断"

    elif mode == "因果関係":
        row = weighted_sample(df, st.session_state.history).iloc[0]
        st.session_state.q = f"{row['event']}が起きた理由と結果を答えよ"
        st.session_state.a = row["cause"] + " → " + row["result"]
        st.session_state.cat = row["era"]

    elif mode == "記述（50字）":
        row = weighted_sample(df, st.session_state.history).iloc[0]
        st.session_state.q = f"{row['event']}について説明せよ（50字）"
        st.session_state.a = row["cause"] + " → " + row["result"]
        st.session_state.cat = row["era"]

    elif mode == "用語確認":
        row = weighted_sample(df, st.session_state.history).iloc[0]
        st.session_state.q = f"次の説明に当てはまる用語は？\n{row['cause']}→{row['result']}"
        st.session_state.a = row["event"]
        st.session_state.cat = row["era"]

# ===== 表示 =====
if st.session_state.q:
    st.subheader("問題")
    st.write(st.session_state.q)

    user = st.text_input("解答")

    if st.button("採点"):
        st.session_state.total += 1

        correct = False
        if st.session_state.a in user:
            correct = True
        elif len(user) > 15:
            correct = True  # 記述は部分点

        if correct:
            st.success("正解")
            st.session_state.score += 1
        else:
            st.error("不正解")

        st.write("答え：", st.session_state.a)

        st.session_state.history.append((correct, st.session_state.cat))

# ===== 成績 =====
st.subheader("成績")
st.write(f"{st.session_state.score} / {st.session_state.total}")

# ===== 弱点 =====
if st.session_state.history:
    df_h = pd.DataFrame(st.session_state.history, columns=["c", "cat"])
    weak = df_h[df_h["c"] == False]["cat"].value_counts()

    if not weak.empty:
        st.subheader("弱点")
        for k, v in weak.items():
            st.write(f"{k}：{v}問ミス")
