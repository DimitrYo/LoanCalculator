import math
import argparse

parser = argparse.ArgumentParser(description="Loan calculator")

parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()

what_calculate_msg = """What do you want to calculate?
type "n" - for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:\n"""

enter_pricipal_msg = "Enter the loan principal:\n"
payment_msg = "Enter the monthly payment:\n"
interest_msg = "Enter the loan interest:\n"
annuity_msg = "Enter the annuity payment:\n"
periods_msg = "Enter the number of periods:\n"

res_principal_msg = "Your loan principal = {}!"
res_payment_msg = "Your monthly payment = {}!"
overpayment_msg = "Overpayment = {}"
repay_time_msg = "It will take {} years and {} months to repay this loan!"
repay_time_years_msg = "It will take {} years to repay this loan!"
incorrect_par_msg = "Incorrect parameters"
monthly_payment_msg = "Month {}: payment is {}"


def int_rate():
    if args.interest is None:
        print_error()

    interest_percent = float(args.interest)
    return interest_percent / (12 * 100)


def get_periods():
    if args.periods is None:
        print_error()
    return int(args.periods)


def get_pricipal():
    if args.principal is None:
        print_error()
    return int(args.principal)


def rate_ann(rate, n):
    temp = math.pow(1 + rate, n)
    return (rate * temp) / (temp - 1)


def annuity(rate, n, principal):
    return principal * rate_ann(rate, n)


def print_error():
    print(incorrect_par_msg)
    exit()

def invalid_payment():
    if args.payment is not None:
        print_error()
        exit()

def empty_principal():
    if args.principal is None:
        if args.payment is None:
            print_error()

        payment = int(args.payment)
        interest_rate = int_rate()

        periods = get_periods()
        principal = math.ceil(payment / rate_ann(interest_rate, periods))
        print(res_principal_msg.format(principal))
        print(overpayment_msg.format("%.f" % (payment * periods - principal)))
        exit()


def empty_periods():
    if args.periods is None:
        if args.payment is None:
            print_error()

        payment = int(args.payment)
        interest_rate = int_rate()
        principal = get_pricipal()

        months = math.ceil(math.log(payment / (payment - interest_rate * principal), 1 + interest_rate))
        years = months // 12
        final_month = months - years * 12
        if (final_month == 0):
            print(repay_time_years_msg.format(years))
        else:
            print(repay_time_msg.format(years, final_month))
        print(overpayment_msg.format("%.f" % (payment * months - principal)))
        exit()


if __name__ == '__main__':

    calculate_type = args.type

    if calculate_type == "annuity":
        empty_principal()
        empty_periods()

        principal = get_pricipal()
        periods = get_periods()
        interest_rate = int_rate()

        payment = math.ceil(annuity(interest_rate, periods, principal))
        print(res_payment_msg.format("%.f" % payment))
        print(overpayment_msg.format("%.f" % (payment * periods - principal)))
    elif calculate_type == "diff":
        invalid_payment()

        principal = get_pricipal()
        periods = get_periods()
        interest_rate = int_rate()

        total = 0
        for i in range(1, periods + 1):
            montly_payment = math.ceil(principal / periods + interest_rate * (principal - principal / periods * (i - 1)))
            total += montly_payment
            print(monthly_payment_msg.format(i, montly_payment))
        print()
        print(overpayment_msg.format("%.f" % (total - principal)))

    else:
        print_error()