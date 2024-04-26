import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

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


def get_date_range_from_weeks(start_week, end_week, year=2024):
    first_day_of_year = datetime.datetime(year, 1, 1)  # Start fra 1. januar det angivne år
    start_date = first_day_of_year + datetime.timedelta(days=(start_week - 1) * 7 - first_day_of_year.weekday())
    end_date = first_day_of_year + datetime.timedelta(days=(end_week * 7) - first_day_of_year.weekday())
    return pd.date_range(start=start_date, end=end_date)
def plot_dates(all_dates, work_dates):
    # Opret en DataFrame med alle dage og marker arbejdsdage
    df_dates = pd.DataFrame({'Date': all_dates})
    df_dates['Type'] = df_dates['Date'].apply(lambda x: 'Arbejdsdag' if x in work_dates else 'Fridag')
    
    # Brug plotly til at visualisere
    fig = px.timeline(df_dates, x_start="Date", x_end="Date", y="Type", color='Type',
                      labels={'Type': 'Dagstype'}, color_discrete_map={'Arbejdsdag': 'blue', 'Fridag': 'grey'})
    fig.update_yaxes(categoryorder='total ascending')
    return fig
 

# Opdater 'main' funktionen til at inkludere visualisering
def main():
    weeks = sheet_name.split('-')
    all_dates = get_date_range_from_weeks(int(weeks[0]), int(weeks[1]))

    df = load_data(sheet_name)
    relevant_teacher_columns = [col for col in df.columns if 'Lærer' in col and df.columns.get_loc(col) < df.columns.get_loc("KODER")]

    st.title('Lærer Kalender Dashboard')
    teacher_initials = st.selectbox('Vælg lærer initialer:', ['Ochr', 'AzUm', 'PeJo', 'PaDa', 'HeTh', 'BjPo', 'JeKN', 'ChLy', 'PeBN', 'HeGr', 'BriR', 'MaGS', 'KasC', 'ChPe'])

    if st.button('Vis Datoer'):
        work_dates = find_teacher_dates(df, teacher_initials, relevant_teacher_columns)
        work_dates = [pd.Timestamp(date) for date in work_dates]
        fig = plot_dates(all_dates, work_dates)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()



