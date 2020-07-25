from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from scatter_api.models import Question, Answer, Player, Game
from scatter_api import serializers
from scatter_api.serializers import QuestionSerializer, AnswerSerializer, PlayerSerializer, GameSerializer, PlayerCreateRequestSerializer, GameQuestionsResponseSerializer
from scatter_api.requests import CreatePlayerRequest
from scatter_api.responses import GameQuestionsResponse
import random
# Create your views here.
def index(request):
    return HttpResponse("Hello world This is the scatterAPI")
#
#   Questions at /questions
#
class QuestionList(APIView):
    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#   Question Detail at /questions/<id>
#
class QuestionDetail(APIView):
    def get_object(self,pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
    def get(self, request,pk,format=None):
        question = self.get_object(pk)
        serializer=QuestionSerializer(question)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        question=self.get_object(pk)
        serializer=QuestionSerializer(question,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        question = self.get_object(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#
#   Games at /games
#
class GameList(APIView):
    def newName(self, name):
        try:
            Game.objects.get(name=name)
            return False
        except Game.DoesNotExist:
            return True
    def get(self, request, format=None):
        games = Game.objects.all()
        serializer=GameSerializer(games,many=True)
        return Response(serializer.data)
    #requires a name field
    def post(self,request,format=None):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            questions_per_round=12
            game = serializer.save(round_number=1)
            question_numbers=random.sample(list(Question.objects.values_list('id',flat=True)),3*questions_per_round)
            print(question_numbers)
            for i in range(0,questions_per_round):
                game.round_one_questions.add(Question.objects.get(pk=question_numbers[i]))
                game.round_two_questions.add(Question.objects.get(pk=question_numbers[i+questions_per_round]))
                game.round_three_questions.add(Question.objects.get(pk=question_numbers[i+2*questions_per_round]))
            serializer = GameSerializer(game)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#   Game detail at games/<game_name>
#
class GameDetail(APIView):
    def get_object(self,game_name):
        try:
            return Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise Http404
    def get(self, request,game_name,format=None):
        game = self.get_object(game_name)
        serializer=GameSerializer(game)
        return Response(serializer.data)
    def put(self, request, game_name, format=None):
        game=self.get_object(game_name)
        serializer=GameSerializer(game,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, game_name, format=None):
        game = self.get_object(game_name)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
#   Serve a list of questions for the current round at games/<game_name>/questions
#
class GameQuestionsList(APIView):
    def get_game(self, game_name):
        try:
            return Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise Http404
    def get(self, request, game_name):
        game = self.get_game(game_name)
        if game.round_number == 1:
            questions_list = game.round_one_questions.all()
            response_object = GameQuestionsResponse(questions_list=questions_list,game_name=game_name)
            serializer = GameQuestionsResponseSerializer(response_object)
        if game.round_number == 2:
            questions_list = game.round_two_questions.all()
            response_object = GameQuestionsResponse(questions_list=questions_list,game_name=game_name)
            serializer = GameQuestionsResponseSerializer(response_object)
        if game.round_number == 3:
            questions_list = game.round_three_questions.all()
            response_object = GameQuestionsResponse(questions_list=questions_list,game_name=game_name)
            serializer = GameQuestionsResponseSerializer(response_object)
        return Response(serializer.data)

#
#   All player answers from the current round at games/<game_name>/questions
#
class GameAnswersList(APIView):
    def get_game(self, game_name):
        try:
            return Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise Http404
    def get_questions(self,game):
        if game.round_number == 1:
            serializer=QuestionSerializer(game.round_one_questions.all(),many=True)
        if game.round_number == 2:
            serializer=QuestionSerializer(game.round_two_questions.all(),many=True)
        if game.round_number == 3:
            serializer=QuestionSerializer(game.round_three_questions.all(),many=True)
        return serializer.data
    def get(self, request, game_name):
        game=self.get_game(game_name)
        data = {"questions":self.get_questions(game),"players":[]}
        for player in Player.objects.filter(game=game):
            answers = AnswerSerializer(Answer.objects.filter(player=player),many=True)
            player_data = {
                "player":PlayerSerializer(player).data,
                "answers":answers.data
            }
            data["players"].append(player_data)
        return Response(data)

#
#   Score players and get the current game score at games/<game_name>/score
#
class Score(APIView):
    def get_game(self, game_name):
        try:
            return Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise Http404
    def post(self,request,game_name):
        game=self.get_game(game_name)
        if ("player_id" in request.data.keys() and "scores" in request.data.keys()):
            if request.data["player_id"] == game.host:
                players = Player.objects.filter(game=game)
                for player in players:
                    if str(player.id) in request.data["scores"].keys():
                        player.score += request.data["scores"][str(player.id)]
                        player.save()
                        answers = Answer.objects.filter(player=player)
                        for answer in answers:
                            answer.delete()
                game.round_number+=1
                game.save()
                serializer=PlayerSerializer(players,many=True)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response("player not host",status=status.HTTP_400_BAD_REQUEST)
        return Response("bad request format",status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,game_name):
        game=self.get_game(game_name)
        players = Player.objects.filter(game=game)
        serializer=PlayerSerializer(players,many=True)
        return Response(serializer.data)

#
#   Player at /players
#
class PlayerList(APIView):
    def get_game(self, game_name):
        try:
            return Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise Http404
    def get(self,request,format=None):
        players = Player.objects.all()
        serializer=PlayerSerializer(players,many=True)
        return Response(serializer.data)
    def post(self,request,format=None):
        serializer = PlayerCreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            game = Game.objects.get(name=data.game_name)
            prior = Player.objects.filter(game=game)
            if not prior:
                isHost=True
            else:
                isHost=False
            player = Player(name=data.name,game = game,score=0)
            player.save()
            game.num_players+=1
            game.save()
            print(player.id)
            if isHost:
                game.host = player.id
                game.save()
            serializer = PlayerSerializer(player)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



#
#   Submit player answers and get a list of submitted answers at answers/
#
class PlayerAnswers(APIView):
    def get_player(self, pk):
        try:
            return Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            raise Http404
    def validate_answer(self, answer):
        if ('answer_text' in answer.keys() and 'question_id' in answer.keys()):
            return True
        return False
    #answer submission for player pk
    def post(self,request,pk):
        player = self.get_player(pk)
        if 'answers' in request.data.keys():
            for ans in request.data['answers']:
                if self.validate_answer(ans):
                    answer = Answer(answer_text=ans['answer_text'],question=Question.objects.get(pk=ans['question_id']),player=Player.objects.get(pk=pk))
                    answer.save()
            return Response("Questions submitted",status=status.HTTP_201_CREATED)
        return Response("no answer member", status = status.HTTP_400_BAD_REQUEST)
    #get all answers submitted by player pk
    def get(self,request,pk):
        player=self.get_player(pk)
        answers = Answer.objects.filter(player=player)
        serializer = AnswerSerializer(answers,many=True)
        return Response(serializer.data)
  


#create a host field with a GUID created by the creator's computer?
