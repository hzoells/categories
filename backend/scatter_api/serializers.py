from rest_framework import serializers
from scatter_api.models import Question, Answer, Player, Game
from scatter_api.requests import CreatePlayerRequest, SubmitAnswers, AnswerSubmission
from scatter_api.responses import GameQuestionsResponse
class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Question
        fields = ['question_text','id']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer_text','player','question']
class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    class Meta:
        model = Player
        fields = ['game','name','score','id']
class GameSerializer(serializers.ModelSerializer):
    def validate_name(self,value):
        try:
            Game.objects.get(name=value)
            raise serializers.ValidationError('Game name already in use')
        except Game.DoesNotExist:
            return value
    class Meta:
        model = Game
        fields = ['round_one_questions','round_two_questions','round_three_questions','round_number','name','host','num_players']
class PlayerCreateRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    game_name = serializers.CharField(max_length=200)
    def create(self,validated_data):
        return CreatePlayerRequest(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.game_name = validated_data.get('',instance.game_name)
        return instance
    def validate(self, data):
        try:
            game = Game.objects.get(name=data['game_name'])
        except Game.DoesNotExist:
            raise serializers.ValidationError("Game does not exist")
        try:
            Player.objects.get(game = game,name = data['name'])
            raise serializers.ValidationError('Player name not unique')
        except Player.DoesNotExist:
            return data
        return data

class GameQuestionsResponseSerializer(serializers.Serializer):
    game_name = serializers.CharField(max_length=200)
    questions_list = QuestionSerializer(many=True)
    def create(self, validated_data):
        return GameQuestionResponse(**validated_data)
    def update(self, instance, validated_data):
        instance.game_name = validated_data.get('game_name',instance.game_name)
        instance.questions_list = validated_data.get('questions_list',instance.questions_list)
        return instance