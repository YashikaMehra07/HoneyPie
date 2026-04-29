import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
import pandas as pd 
import dbfunc
import calplot
# import seaborn as sns 
# import numpy as np
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
import plotly.io as pio

# from matplotlib.colors import ListedColormap

# df= pd.DataFrame(np.random.random((5,5)), columns=['a', 'b', 'c', 'd', 'e'])
# sns.heatmap(df)
# plt.show()

def monthly_emotions(username):
    mood_data = dbfunc.get_user_mood_data(username)
    if not mood_data:
        return f'<p>No mood data available for {username}.</p>'

    df= pd.DataFrame(mood_data, columns=['Timestamp', 'Mood1', 'Mood2'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])
    df['Date']= df['Timestamp'].dt.date
    
    # daily_moods = df.melt(id_vars=['Date'], value_vars=['Mood1', 'Mood2'])
    # daily_moods = daily_moods.groupby(['Date', 'value']).size().reset_index(name='count')
    # daily_moods = daily_moods.loc[daily_moods.groupby('Date')['count'].idxmax()]  # Select most frequent mood per day
    combined_df = (
        df.melt(id_vars=['Date'], value_vars=['Mood1', 'Mood2'])
        .groupby(['Date', 'value'])
        .size()
        .unstack(fill_value=0)
    )
    daily_moods = combined_df.idxmax(axis=1).reset_index()
    daily_moods.columns = ['Date', 'value']

    mood_to_number = {
        'angry': 6.5, 
        'disgust': 3.70, 
        'fear': 1, 
        'happy': 5.25, 
        'neutral': 7, 
        'sad': 2.5, 
        'surprise': 4.5
    }
    daily_moods['Mood_Num'] = daily_moods['value'].map(mood_to_number)

    # Add dummy mood values to enforce colormap range
    padding_dates = pd.date_range(start="2025-03-25", periods=7, freq='D')
    padding_values = pd.Series([1, 2.5, 3.7, 4.5, 5.25, 6.5, 7], index=padding_dates)

    # Combine with real data
    mood_series = pd.Series(daily_moods['Mood_Num'].values, index=pd.to_datetime(daily_moods['Date']))
    mood_series = pd.concat([mood_series, padding_values])

    fig, ax=calplot.calplot(mood_series,
                            # fillcolor= 'orange',
                            yearascending = False,
                            edgecolor = 'black', 
                    cmap='nipy_spectral', 
                    # cmap=custom_cmap, 
                    figsize=(10, 4),  
                    colorbar=False)
    # cbar= fig.axes[-1]
    # cbar.set_yticks([1,2.5,3.70,4.5,5.25,6.5,7])
    # cbar.set_yticklabels(['Fear', 'Sad', 'Disgust', 'Surprise', 'Happy', 'Angry', 'Neutral'])
    # plt.title('Your Emotion Chart')
    # Add manual colorbarfor ax in fig.axes:
    for ax in fig.get_axes():
        ax.tick_params(labelsize=8)

    norm = Normalize(vmin=1, vmax=7)
    cmap = plt.get_cmap('nipy_spectral')
    cbar_ax = fig.add_axes([0.93, 0.2, 0.015, 0.6])  # (left, bottom, width, height)
    cb = ColorbarBase(cbar_ax, cmap=cmap, norm=norm, ticks=[1, 2.5, 3.7, 4.5, 5.25, 6.5, 7])
    cb.ax.set_yticklabels(['Fear', 'Sad', 'Disgust', 'Surprise', 'Happy', 'Angry', 'Neutral'])
    fig.tight_layout()
    cb.ax.tick_params(labelsize=8) 

    # 🔍 Print today's dominant mood
    today = datetime.today().date()
    today_row = daily_moods[daily_moods['Date'] == today]

    if not today_row.empty:
        dominant_today = today_row['value'].values[0]
        print(f"🟡 Dominant mood for today ({today}): {dominant_today}")
    else:
        print(f"⚪ No dominant mood found for today ({today})")

    print(mood_series.describe())
    print(mood_series.head())
    print(mood_series.dtypes)
    print(mood_series.isna().sum())



    # Save plot to buffer
    buf = io.BytesIO()
    plt.subplots_adjust(left=0.05, right=0.90, top=0.92, bottom=0.1)  # leave space for colorbar
    plt.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    buf.close()

    return f'''
<div style="text-align:center;">
    <img src="data:image/png;base64,{img_base64}" class="img-fluid"/>
</div>
'''

def daily_emotions(username, selected_date=None):
    colors = {
        'angry': 'darkred',
        'disgust': 'darkgreen',
        'fear': 'black',
        'happy': 'yellow',
        'neutral': 'gray',
        'sad': 'darkblue',
        'surprise': 'limegreen'
    }
    emotions = list(colors.keys())
    mood_data = dbfunc.get_user_mood_data(username)

    df= pd.DataFrame(mood_data, columns=['Timestamp', 'Mood1', 'Mood2'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])
    df['Date']= df['Timestamp'].dt.date

    today = datetime.today().date() if selected_date is None else selected_date
    start_of_week = today - timedelta(days=today.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    df_week= df[df['Date'].isin(week_dates)]
    #count each emotion per day per source 
    
    daily_data={}
    for source in ['Mood1', 'Mood2']:
        source_df= df_week.groupby(['Date', source]).size().unstack(fill_value=0)
        daily_data[source]= source_df

    combined_df= sum(daily_data.values())
    #sorting cols n dates
    combined_df= combined_df.reindex(week_dates, fill_value=0)
    percent_df = combined_df.div(combined_df.sum(axis=1), axis=0).fillna(0) * 100

    # Plotting the bar chart
    fig= go.Figure()
    for emotion in emotions:
        if emotion in percent_df.columns:
            fig.add_trace(go.Bar(
                x=percent_df.index,
                y=percent_df[emotion],
                name=emotion,
                marker_color=colors[emotion],
                hovertemplate=f"{emotion}: %{{y:.2f}}%<extra></extra>"
            ))

    fig.update_layout(
        barmode='stack',
        title="Weekly Emotion Percentage Chart",
        xaxis_title="Date",
        yaxis_title="Emotion Percentage",
        xaxis=dict(tickangle=-45),
        legend_title="Emotions",
        hovermode="x unified"
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    
