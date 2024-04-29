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
        'Workday': all_dates.isin(work_dates),
        'Weekday': all_dates.dayofweek,
        'WeekNumber': all_dates.isocalendar().week
    })
    
    # Opret en kolonne til at repræsentere blokkene i visualiseringen
    df_calendar['Block'] = df_calendar['Workday'].apply(lambda x: 1 if x else 0)
    
    # Vi skal bruge 'Weekday' til at bestemme placeringen af hver bar i gitteret
     # Opret et fast 'WeekdayOffset' for hver ugedag (1-5 for mandag til fredag)
    df_calendar['WeekdayOffset'] = df_calendar['Date'].dt.dayofweek.replace(range(5), range(1, 6))
    
    # Plotly bar chart
    fig = px.bar(
        df_calendar,
        x='WeekdayOffset',
        y='WeekNumber',
        color='Workday',
        text='Block',  # Tildeler 'Block' værdien til teksten
        color_discrete_map={True: 'blue', False: 'lightgrey'},
        orientation='h'
    )
    
    # Fastlæg en fast bredde for hver bar for at sikre de er ensartede
    fig.update_traces(width=0.8)  # Fastlægger en ensartet bredde for firkanterne
    
    # Sæt x-aksen for at vise alle fem dage, med faste punkter for hver ugedag
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 6)),  # faste værdier for ugedagene
        ticktext=['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag']
    )
    
    # Fastlæg y-aksens ticks til at vise "Uge: [nummer]"
    fig.update_yaxes(
        tickmode='array',
        tickvals=df_calendar['WeekNumber'].unique(),
        ticktext=['Uge: ' + str(wn) for wn in df_calendar['WeekNumber'].unique()]
    )
    
    # Tilpas layout for at sikre at firkanterne ikke bliver strukket og har ens størrelse
    fig.update_layout(
        barmode='overlay',  # Bruger 'overlay' for at sikre, at firkanterne ikke bliver stablet
        xaxis={
            'tickmode': 'array',
            'tickvals': list(range(1, num_workdays + 1)),  # Fastlæg tickværdier for arbejdsdagene
            'ticktext': ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag']
        },
        yaxis_tickformat = 'Uge: ',  # Tilføj præfikset "Uge: " til y-aksens ticks

        )
    # Opdater layoutet for at fjerne gaps mellem bares, og indstil y-aksen til at vise ugenumre
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    
    # Opdater tekstpositionen og skjul den for ikke-arbejdsdage
    fig.for_each_trace(lambda t: t.update(text="") if t.name == 'False' else None)
    
    # Opdater figurens størrelse, hvis det er nødvendigt
    fig.update_layout(width=800, height=600)
    
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




