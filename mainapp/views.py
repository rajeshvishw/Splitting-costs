from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Expense, Balance
from .serializers import UserSerializer, ExpenseSerializer, BalanceSerializer

class UserAPIView(APIView):
    def get(self, request, user_id=None):
        if user_id:
            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseAPIView(APIView):
    def get(self, request, expense_id=None):
        if expense_id:
            try:
                expense = Expense.objects.get(expense_id=expense_id)
                serializer = ExpenseSerializer(expense)
                return Response(serializer.data)
            except Expense.DoesNotExist:
                return Response({"Expense ID not valid"}, status=status.HTTP_404_NOT_FOUND)
        expenses = Expense.objects.all().order_by('-created_at')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save()
            if expense.type == 'Equal':
                self.handle_equal_split(expense)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_equal_split(self, expense):
        print(expense.amount)
        totalpeople = len(expense.participants.all()) + 1
        percentage_per_person = 100 / totalpeople
        amount_per_person = expense.amount / totalpeople
        for participant in expense.participants.all():
            participant.amount_owed = amount_per_person
            participant.percentage_share = percentage_per_person
            participant.save()
            self.update_balance(expense.player, participant.user, amount_per_person)

    def update_balance(self, player, participant, amount):
        balance, created = Balance.objects.get_or_create(from_user=participant, to_user=player)
        balance.amount += amount
        balance.save()

class BalanceAPIView(APIView):
    def get(self, request, user_id):
        balances = Balance.objects.filter(from_user_id=user_id).exclude(amount=0)
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data)
