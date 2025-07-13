from rest_framework import serializers
from banking.models import Loan, LoanPayment
from banking.serializers.bank_serializer import BankSerializer
from banking.serializers.loan_payment_serializer import LoanPaymentSerializer 

class LoanDetailSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    progress = serializers.SerializerMethodField()
    payments = LoanPaymentSerializer(many=True, read_only=True)


    class Meta:
        model = Loan
        fields = "__all__"  # Or list specific fields you want to expose

    def get_progress(self, loan):
        total = loan.amount or 0
        paid_qs = loan.payments.filter(status="paid")


        amount_paid = sum(p.amount_paid for p in paid_qs)
        remaining = total - amount_paid
        percent = (amount_paid / total) * 100 if total else 0

        return {
            "percentage": round(percent, 2),
            "amount_paid": amount_paid,
            "remaining": remaining,
            "status": "complete" if percent >= 100 else "in_progress"
        }
