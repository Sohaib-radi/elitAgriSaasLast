from decimal import Decimal, ROUND_HALF_UP
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from banking.models.loan import Loan
from banking.models.loan_payment import LoanPayment

def generate_loan_payment_schedule(loan: Loan, user):
    
    if loan.repayment_method not in [
        Loan.RepaymentMethod.MONTHLY,
        Loan.RepaymentMethod.QUARTERLY,
        Loan.RepaymentMethod.YEARLY
    ]:
        return  # Bullet or custom are manually handled

    # Step 1: Prepare loan data
    P = loan.amount
    r = Decimal(loan.interest_rate) / Decimal("100.0")
    n = loan.loan_duration
    start_date = loan.start_date

    # Step 2: Determine frequency
    if loan.repayment_method == Loan.RepaymentMethod.MONTHLY:
        interval = 1
    elif loan.repayment_method == Loan.RepaymentMethod.QUARTERLY:
        interval = 3
    elif loan.repayment_method == Loan.RepaymentMethod.YEARLY:
        interval = 12

    periods = n // interval
    periodic_rate = r / Decimal("12.0") * interval

    # Step 3: Calculate installment amount (annuity formula)
    if periodic_rate > 0:
        installment = P * periodic_rate / (1 - (1 + periodic_rate) ** -periods)
    else:
        installment = P / periods

    installment = installment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Step 4: Generate payments
    remaining = P
    current_date = start_date

    for i in range(1, periods + 1):
        interest = (remaining * periodic_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        principal = (installment - interest).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        remaining = (remaining - principal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        LoanPayment.objects.create(
            loan=loan,
            payment_date=current_date,
            amount_paid=installment,
            principal_paid=principal,
            interest_paid=interest,
            remaining_balance=remaining,
            payment_method=LoanPayment.PaymentMethodChoices.BANK_TRANSFER,
            status=LoanPayment.StatusChoices.PENDING,
            note="Auto-generated installment",
            farm=loan.farm, 
            created_by=user,
        )

        current_date += relativedelta(months=interval)
