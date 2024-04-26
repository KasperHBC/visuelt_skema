import streamlit as st
import pandas as pd

# Funktion til at indlæse data (du kan tilpasse stien eller tilføje argumenter efter behov)
def load_data():
    return pd.read_excel("./Data 2024 v.23.xlsm", sheet_name='14-27')

# Funktion til at finde datoer for en lærer
def find_teacher_dates(df, initials, relevant_teacher_columns):
    date_list = []
    for col in relevant_teacher_columns:
        teacher_rows = df[col] == initials
        dates = df.loc[teacher_rows, "Dato"]
        date_list.extend(dates.dropna().tolist())
    return date_list

# Hoveddel af Streamlit app
def main():
    df = load_data()
    relevant_teacher_columns = [col for col in df.columns if 'Lærer' in col and df.columns.get_loc(col) < df.columns.get_loc("KODER")]

    st.title('Lærer Kalender Dashboard')
    teacher_initials = st.selectbox('Vælg lærer initialer:', ['Ochr', 'AzUm', 'PeJo', 'PaDa', 'HeTh', 'BjPo', 'JeKN', 'ChLy', 'PeBN', 'HeGr', 'BriR', 'MaGS', 'KasC', 'ChPe'])

    if st.button('Vis Datoer'):
        dates = find_teacher_dates(df, teacher_initials, relevant_teacher_columns)
        if dates:
            st.write('Datoer for', teacher_initials, ':')
            st.write(dates)
        else:
            st.write('Ingen datoer fundet for valgte lærer.')

if __name__ == "__main__":
    main()

