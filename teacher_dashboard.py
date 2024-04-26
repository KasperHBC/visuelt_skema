import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Funktion til at indlæse data (du kan tilpasse stien eller tilføje argumenter efter behov)
def load_data(sheet_name):
    return pd.read_excel("./Data 2024 v.23.xlsm", sheet_name=sheet_name)
    
def get_sheet_names():
    xl = pd.ExcelFile("./Data 2024 v.23.xlsm")
    return xl.sheet_names

# Funktion til at finde datoer for en lærer
def find_teacher_dates(df, initials, relevant_teacher_columns):
    date_list = []
    for col in relevant_teacher_columns:
        teacher_rows = df[col] == initials
        dates = df.loc[teacher_rows, "Dato"]
        date_list.extend(dates.dropna().tolist())
    return date_list


def get_date_range_from_weekdays(start_week, end_week, year=2024):
    first_day_of_year = datetime.datetime(year, 1, 1)
    start_date = first_day_of_year + datetime.timedelta(days=(start_week - 1) * 7 - first_day_of_year.weekday())
    end_date = first_day_of_year + datetime.timedelta(days=(end_week * 7) - first_day_of_year.weekday())
    all_dates = pd.date_range(start=start_date, end=end_date)
    # Filtrer for at udelukke lørdage (5) og søndage (6)
    weekdays = all_dates[~all_dates.weekday.isin([5, 6])]
    return weekdays

def plot_dates(all_dates, work_dates):
    df_dates = pd.DataFrame({
        'Date': all_dates,
        'Type': all_dates.isin(work_dates).map({True: 'Arbejdsdag', False: 'Fridag'}),
        'WeekNumber': all_dates.week
    })
    
    df_dates = df_dates.groupby('WeekNumber').agg({
        'Date': ['min', 'max'],
        'Type': 'first'
    }).reset_index()
    
    # Renaming columns
    df_dates.columns = ['WeekNumber', 'Start', 'Finish', 'Type']

    # Add one day to 'Finish' so that the last day is included in the timeline
    df_dates['Finish'] = df_dates['Finish'] + pd.Timedelta(days=1)
    
    fig = px.timeline(
        df_dates, 
        x_start="Start", 
        x_end="Finish", 
        y="Type", 
        text='WeekNumber',
        color='Type',
        labels={'Type': 'Dagstype', 'WeekNumber': 'Ugenummer'}, 
        color_discrete_map={'Arbejdsdag': 'blue', 'Fridag': 'grey'}
    )
    
    fig.update_traces(textposition='inside', marker=dict(line=dict(width=1, color='black')))
    fig.update_layout(xaxis=dict(tickformat='%d %B %Y', tickmode='linear'))
    fig.update_yaxes(categoryorder='total ascending')

    # Skjul ugenumre for fridage
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, text=t.text if t.name == 'Arbejdsdag' else ['']))
    
    return fig


# Opdater 'main' funktionen til at inkludere visualisering
def main():
    st.title('Lærer Kalender Dashboard')

    sheet_names = get_sheet_names()
    sheet_name = st.selectbox('Vælg et sheet:', sheet_names)
    
    df = load_data(sheet_name)
    relevant_teacher_columns = [col for col in df.columns if 'Lærer' in col and df.columns.get_loc(col) < df.columns.get_loc("KODER")]

    teacher_initials = st.selectbox('Vælg lærer initialer:', ['Ochr', 'AzUm', 'PeJo', 'PaDa', 'HeTh', 'BjPo', 'JeKN', 'ChLy', 'PeBN', 'HeGr', 'BriR', 'MaGS', 'KasC', 'ChPe'])

    if st.button('Vis Datoer'):
        work_dates = find_teacher_dates(df, teacher_initials, relevant_teacher_columns)
        work_dates = [pd.Timestamp(date) for date in work_dates]
        weeks = sheet_name.split('-')
        all_dates = get_date_range_from_weekdays(int(weeks[0]), int(weeks[1]), year=2024)  # Tjek at året passer
        fig = plot_dates(all_dates, work_dates)
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()




