import numpy as np
import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt

from config import get_app_client

app_client = get_app_client()


def show_model_upload():
    st.header('Загрузка обученной модели')
    uploaded_file = st.file_uploader('Загрузка модели', type=['pickle'])
    if uploaded_file is not None:
        file = {'model_file': (uploaded_file.name, uploaded_file)}
        app_client.model_upload(model_file=file)


def show_model_list():
    st.header('Список загруженных моделей')
    st.dataframe({"Загруженные модели": app_client.get_models_list()}, hide_index=True, use_container_width=True)


def show_generate_report():
    st.header('Отчет о найденных аномалиях')
    uploaded_models = app_client.get_models_list()
    selected_model = st.selectbox('Выберите модель:', uploaded_models, key='report')
    uploaded_flow = st.file_uploader('Загрузка данных', type=['zip'])
    if st.button("Сгенерировать отчет") and selected_model and uploaded_flow:
        file = {
            'uploaded_flow': (uploaded_flow.name, uploaded_flow),
        }
        response = app_client.get_anomalies_report(file=file, model=selected_model)
        trained_ire, ire_list, flow_filenames =\
            response['trained_ire'], response['ire_list'], response['flow_filenames']

        indexes_of_anomalies = np.where(np.array(ire_list) > trained_ire)
        list_of_anomalies = list(np.array(flow_filenames)[list(indexes_of_anomalies[0])])
        st.write(f"Аномальными являются те потоки, значение которых превышает IRE = {trained_ire}.")
        st.write(f"Количество потенциальных аномальных потоков: {len(list_of_anomalies)}.")
        st.write('Значения IRE для потенциальных аномальных потоков:')
        st.dataframe({"flow_name": list_of_anomalies, "IRE": np.array(ire_list)[list(indexes_of_anomalies[0])]})

        plt.figure(figsize=(10, 5))
        plt.plot(range(len(ire_list)), ire_list, label='IRE', color='blue')
        plt.title('График значений ошибок реконструкции')
        plt.xlabel('Log record number')
        plt.ylabel('IRE value')
        plt.legend()
        plt.grid()

        # Отображение графика в Streamlit
        st.pyplot(plt)


def show_main_page() -> None:
    st.set_page_config(
        page_title="anomaly detection",
    )

    st.write("# Обнаружение аномальной сетевой активности на хосте с использованием машинного обучения")
    st.divider()
    show_model_upload()
    st.divider()
    show_model_list()
    st.divider()
    show_generate_report()

show_main_page()
