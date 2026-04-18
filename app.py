import streamlit as st
import pandas as pd
import random

# CSV読み込み
df = pd.read_csv("data.csv")

st.title("歴史問題ジェネレーター（強化版）")

mode = st.selectbox("問題タイプ", ["年号", "並び替え", "原因"])

if st.button("問題を作る"):

    if mode == "年号":
        row = df.sample(1).iloc[0]
        st.write(f"{row['event']}の年号は？")
        if st.button("答え"):
            st.write(f"{row['year']}年")

    elif mode == "並び替え":
        sample = df.sample(4)
        st.write("次を古い順に並べなさい")
        for i, r in enumerate(sample.itertuples()):
            st.write(f"{chr(65+i)}. {r.event}")
        if st.button("答え"):
            sorted_df = sample.sort_values("year")
            for r in sorted_df.itertuples():
                st.write(r.event)

    elif mode == "原因":
        row = df.sample(1).iloc[0]
        st.write(f"{row['event']}の原因は？")
        if st.button("答え"):
            st.write(row["cause"])
