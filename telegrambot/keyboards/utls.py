def get_years_old(age: int) -> str:
    if 10 <= age <= 20:
        return "лет"
    last_digit = str(age)[-1]
    if int(last_digit) == 1:
        years_old = "год"
    elif 2 <= int(last_digit) <= 4:
        years_old = "года"
    else:
        years_old = "лет"
    return years_old
