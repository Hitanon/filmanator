def get_histories_dict(histories):
    dates = set([history.date for history in histories])
    grouped_histories = dict.fromkeys(dates)
    for history in histories:
        if grouped_histories[history.date] is None:
            grouped_histories[history.date] = [history.title]
        else:
            grouped_histories[history.date].append(history.title)
    return grouped_histories