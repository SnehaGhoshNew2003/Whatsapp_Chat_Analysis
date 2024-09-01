def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f(?:AM|PM|am|pm) -\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    try:
        df['message_date'] = df['message_date'].str.replace('\u202f', ' ')
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    except Exception as e:
        print(f"Error processing message dates: {e}")
    
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Split user and messages
    users = []
    messages = []
    for message in df['user_message'].astype(str):  # Ensure it's all strings
        entry = re.split(r'^(.*?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['messages'] = messages
    
    # Ensure all messages are strings
    df['messages'] = df['messages'].astype(str)
    
    # Drop the user_message column
    df.drop(columns=['user_message'], inplace=True)
    
    # Extract date and time components
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # Create period column
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
