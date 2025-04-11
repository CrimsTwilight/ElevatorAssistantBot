VALUE = 248



def calculate_productivity(data: dict) -> str:
    value = VALUE / 60

    if 'number_of_orders' in data:
        orders: int = data.get('number_of_orders')
        hours: int = data.get('number_of_hours')
        productivity_per_hour: float = orders * value / hours
    else:
        points: int = data.get('number_of_points')
        hours: int = data.get('number_of_hours')
        productivity_per_hour: float = points / hours

    if productivity_per_hour < 15:
        rate = 5.5
    elif productivity_per_hour < 25:
        rate = 6.5
    elif productivity_per_hour < 100:
        rate = 7.5 + (productivity_per_hour - 25) * 0.1
    else:
        rate = 15 + (productivity_per_hour - 100) * 0.1

    return (f'Производительность в час: <b>{productivity_per_hour:.1f} б/час</b>.\n'
            f'Всего баллов: <b>{productivity_per_hour * hours:.1f} б</b>.\n'
            f'Ставка: <b>{rate:.2f} р/час</b>.\n'
            f'Зарплата за день: <b>{rate * hours:.2f} р</b>.\n')
