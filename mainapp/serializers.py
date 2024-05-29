from rest_framework import serializers
from .models import User, Expense, Participant, Balance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['user', 'amount_owed', 'percentage_share']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['expense_id', 'player', 'amount', 'type', 'participants', 'created_at']
        read_only_fields = ['expense_id', 'created_at']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            Participant.objects.create(expense=expense, **participant_data)
        return expense

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
