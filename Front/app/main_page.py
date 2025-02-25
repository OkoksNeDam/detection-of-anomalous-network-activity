import streamlit as st


def show_main_page() -> None:
    st.set_page_config(
        page_title="anomaly detection",
    )

    st.write("# Обнаружение аномальной сетевой активности на хосте с использованием машинного обучения")


show_main_page()