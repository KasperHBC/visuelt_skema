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

def plot_calendar_style(all_dates, work_dates):
    # Opbyg DataFrame
    df_calendar = pd.DataFrame({
        'Date': all_dates,
        'Weekday': all_dates.dayofweek,
        'WeekNumber': all_dates.isocalendar().week
    })
    
    # Opret en kolonne til at repræsentere blokkene i visualiseringen
    df_calendar['Block'] = 1  # Alle blokke har samme størrelse
    
    # Tilføj kolonne, der angiver om dagen er en arbejdsdag
    df_calendar['Workday'] = df_calendar['Date'].isin(work_dates)
    
    # Vi skal bruge 'Weekday' til at bestemme placeringen af hver bar i gitteret
    df_calendar['WeekdayOffset'] = df_calendar['Weekday'] + 1  # Plus 1 så vi starter fra 1 i stedet for 0
    
    # Plotly bar chart
    fig = px.bar(
        df_calendar,
        x='WeekdayOffset',  # x-positionen for hver bar
        y='Block',  # Alle bars har en højde på 1
        facet_row='WeekNumber',  # Opret en række for hver uge
        color='Workday',  # Farv bars baseret på om det er en arbejdsdag
        text='Date', # Vis datoen som tekst inde i hver bar
        color_discrete_map={True: 'blue', False: 'lightgrey'}, # Definer farver for arbejdsdag og fridag
        orientation='h' # Horisontale bars
    )
    # Opdater layoutet for at gøre bars ensartede og juster x-aksen for at starte fra 1
    fig.update_layout(
        barmode='relative',  # Relative mode betyder, at bars ikke stables over hinanden
        xaxis={'type': 'category', 'categoryorder': 'category ascending', 'tickmode': 'array', 'tickvals': list(range(1, 8)), 'ticktext': list('MTWTFSS')},
        yaxis={'visible': False, 'showticklabels': False},  # Skjul y-aksen
        showlegend=False,  # Skjul legenden
        plot_bgcolor='white'  # Sæt baggrundsfarven til hvid
    )
    
    # Fjern gridlinjer
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    # Sæt tekstfarven til hvid for fridage, så den er usynlig
    fig.update_traces(textfont_color='white', selector={'name': 'False'})
    
    # Sæt en ensartet bredde for alle bars og indstil barernes farve
    fig.update_traces(width=0.4, marker_line_color='black', marker_line_width=0.5)

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
        fig = plot_calendar_style(all_dates, work_dates)
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()




