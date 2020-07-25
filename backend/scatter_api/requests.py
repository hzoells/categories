class CreatePlayerRequest(object):
    def __init__(self,name,game_name):
        self.name = name
        self.game_name = game_name

class SubmitAnswers(object):
    def __init__(self,answers):
        self.answers=answers
class AnswerSubmission(object):
    def __init__(self,answer_text,question_id):
        self.answer_text = answer_text
        self.question_id = question_id
