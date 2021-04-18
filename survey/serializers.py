from rest_framework import serializers
from .models import Quiz, Option


class VoteSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()


class OptionSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    alias = serializers.UUIDField(read_only=True)
    option_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Option.objects.create(**validated_data)


class OptionSerializerWithVotes(OptionSerializer):
    vote_count = serializers.IntegerField(read_only=True)

class QuizListPageSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    alias = serializers.UUIDField(read_only=True)
    quiz_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class QuizDetailPageSerializer(QuizListPageSerializer):
    options = OptionSerializer(many=True, read_only=True)

class QuizResultPageSerializer(QuizListPageSerializer):
    options = OptionSerializerWithVotes(many=True, read_only=True)
