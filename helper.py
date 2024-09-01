from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for messages in df['messages']:
        words.extend(messages.split())
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]
    links = []
    for messages in df['messages']:
        links.extend(extract.find_urls(messages))
    return num_messages,len(words), num_media_messages,len(links)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df
def create_wordcloud(selected_user, df):
    # Load stop words
    with open('bengali_stop_words.txt') as f:
        stop_words = f.read().splitlines()

    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]

    # Filter out unwanted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(messages):
        if isinstance(messages, str):  # Ensure the messages is a string
            words = [word for word in messages.lower().split() if word not in stop_words]
            return " ".join(words)
        return ""

    wc = WordCloud(width=500, height=500, min_font_size=20, background_color='white')
    
    # Convert all messages to strings and remove stop words
    temp['messages'] = temp['messages'].astype(str).apply(remove_stop_words)
    
    # Concatenate all messages into a single string
    text = temp['messages'].str.cat(sep=" ")

    # Check if there's any text to generate the word cloud
    if not text.strip():  # If text is empty or whitespace only
        print("No words to display in the word cloud.")
        return WordCloud(width=500, height=500, background_color='white').generate('')  # Generate empty word cloud

    # Generate and return the word cloud
    df_wc = wc.generate(text)
    return df_wc


def most_common_words(selected_user, df):
    f = open('bengali_stop_words.txt')
    stop_words = f.read().splitlines()
    f.close()  # Close the file after reading

    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for messages in temp['messages'].astype(str):  # Ensure messages are strings
        words.extend([word for word in messages.lower().split() if word not in stop_words])

    if not words:
        print("No words to count.")
        return pd.DataFrame(columns=['word', 'count'])  # Return empty DataFrame

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for messages in df['messages'].astype(str):  # Ensure messages are strings
        emojis.extend([c for c in messages if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user.lower() != 'overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
def activity_heatmap(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap
