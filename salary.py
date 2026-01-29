def calculate_salary(base_salary, days_present):

    total_days = 30

    if days_present < 0 or days_present > total_days:
        raise ValueError("Invalid number of days present")

    per_day_salary = base_salary / total_days
    gross_salary = per_day_salary * days_present

    tax = gross_salary * 0.05
    bonus = 1000 if days_present >= 25 else 0

    net_salary = gross_salary - tax + bonus

    return {
        "base_salary": round(base_salary, 2),
        "days_present": days_present,
        "per_day_salary": round(per_day_salary, 2),
        "gross_salary": round(gross_salary, 2),
        "tax_deduction": round(tax, 2),
        "bonus": bonus,
        "net_salary": round(net_salary, 2)
    }
