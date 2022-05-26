from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
# from pprint import pprint

pd.set_option('display.max_rows', None)

start_before_string = '2020-08-01T01:00:00.000000'
end_before_string = '2021-01-31T01:00:00.000000'
start_after_string = '2021-02-01T01:00:00.000000'
end_after_string = '2021-08-01T01:00:00.000000'

start_before = datetime.fromisoformat(start_before_string)
end_before = datetime.fromisoformat(end_before_string)
start_after = datetime.fromisoformat(start_after_string)
end_after = datetime.fromisoformat(end_after_string)

arrests = pd.read_csv('OpenData-Arrests-All.csv', parse_dates=['Date'])
offences = pd.read_csv('OpenData-Offenses-All.csv', parse_dates=['IncidentDate'])
victims = pd.read_csv('OpenData-Victims-All.csv', parse_dates=['IncidentDate'])
# leoka = pd.read_csv('OpenData-LEOKA-All.csv', parse_dates=['Date'])


def filter(df, start, end, date_key='IncidentDate'):
    return df.loc[(df[date_key] >= start) & (df[date_key] <= end)]


arrests_before = filter(arrests, start_before, end_before, 'Date')
arrests_after = filter(arrests, start_after, end_after, 'Date')
offences_before = filter(offences, start_before, end_before)
offences_after = filter(offences, start_after, end_after)
victims_before = filter(victims, start_before, end_before)
victims_after = filter(victims, start_after, end_after)
# leoka_before = filter(leoka, start_before, end_before)
# leoka_after = filter(leoka, start_after, end_after)

fig, ax = plt.subplots()

offences_before_count = offences_before['NIBRS Crime Description'].value_counts()
offences_after_count = offences_after['NIBRS Crime Description'].value_counts()
before_title = (
    'Before Decriminalization(' +
    f'{start_before_string.split("T")[0]} - {end_before_string.split("T")[0]})'
)
after_title = (
    'After Decriminalization(' +
    f'{start_after_string.split("T")[0]} - {end_after_string.split("T")[0]})'
)

high_amount = offences_before_count[offences_before_count > 1000].rename(before_title).to_frame()\
    .join(offences_after_count[offences_after_count > 1000].rename(after_title).to_frame())

low_amount = offences_before_count[offences_before_count <= 1000].rename(before_title).to_frame()\
    .join(offences_after_count[offences_after_count <= 1000].rename(after_title).to_frame())


def plot_chart(df, ax, fig, yticks):
    df.plot(
        ax=ax,
        kind='bar',
        ylabel='Incidents Recorded',
        yticks=yticks,
        fontsize=7,
        title='Oregon Crime Statistics 6 Months Before and After Drug Decriminalization'
    )
    ax.set_axisbelow(True)
    ax.grid(color='lightgray', linestyle='dashed')
    fig.tight_layout()
    plt.show()


plot_chart(high_amount, ax, fig, range(0, 20000, 1000))
# plot_chart(low_amount, ax, fig, range(0, 1000, 50))
# offences_ = filter(
#     offences,
#     '2021-12-01T01:00:00.000000',
#     '2022-03-01T01:00:00.000000',
# )['NIBRS Crime Description'].value_counts()

# print(offences_before_count)
# print(offences_after_count)
