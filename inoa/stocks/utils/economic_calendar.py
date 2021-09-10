import investpy


def economic_calendar():
    dates = investpy.economic_calendar()
    dates_info = []
    length = len(dates)

    for count in range(0,length):
        info = {}

        info = {
            "id" : dates.loc[count].at['id'],
            "date": dates.loc[count].at['date'],
            "time": dates.loc[count].at['time'],
            "zone": dates.loc[count].at['zone'],
            "currency": dates.loc[count].at['currency'],
            "importance": dates.loc[count].at['importance'],
            "event": dates.loc[count].at['event'],
            "actual": dates.loc[count].at['actual'],
            "forecast": dates.loc[count].at['forecast'],
            "previous": dates.loc[count].at['previous']
        }
        
        dates_info.append(info)
    
    return dates_info

