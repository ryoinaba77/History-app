import streamlit as st
import random

events = [
    {"event": "大化の改新", "year": 645},
    {"event": "壬申の乱", "year": 672},
    {"event": "平安京遷都", "year": 794},
    {"event": "鎌倉幕府成立", "year": 1192},
    {"event": "承久の乱", "year": 1221},
    {"event": "応仁の乱", "year": 1467},
    {"event": "関ヶ原の戦い", "year": 1600},
    {"event": "江戸幕府成立", "year": 1603},
    {"event": "日露戦争", "year": 1904},
]

st.title("歴史問題ジェネレーター")

if st.button("問題を作る"):
    selected = random.sample(events, 4)
    st.write("次を古い順に並べなさい")
    for i, e in enumerate(selected):
        st.write(f"{chr(65+i)}. {e['event']}")

    answer = sorted(selected, key=lambda x: x["year"])
    
    if st.button("答えを見る"):
        st.write("答え：")
        for e in answer:
            st.write(e["event"])
