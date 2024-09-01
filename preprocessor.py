import pandas as pd
import re

def preprocess(data):
    # Regular expression to split the messages and extract dates
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f(?:AM|PM|am|pm) -\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Replace special unicode characters and convert to datetime
    df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
    
    # Force datetime conversion and handle errors
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce')
    
    # Check for any NaT values (failed conversions)
    if df['message_date'].isna().sum() > 0:
        print(f"Warning: {df['message_date'].isna().sum()} dates could not be parsed and are set to NaT.")

    # Rename column after conversion
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Ensure all non-parsed dates are removed or handled
    df = df.dropna(subset=['date'])

    # Split user and messages
    users = []
    messages = []
    for message in df['user_message'].astype(str):
        entry = re.split(r'^(.*?):\s', message)
        if entry[1:]:  # User and message exist
            users.append(entry[1])
            messages.append(entry[2])
        else:  # System message or error
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract date and time components using .dt accessor
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create a period column
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
