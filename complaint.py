class Complaint:
    class Answer:
        def __init__(self, date: str, message: str, score: str, replier: str):
            self.date = date
            self.message = message
            self.score = score
            self.replier = replier
    

    def __init__(self, title: str, description: str, date: str, view_count: str, complainer: str):
        self.title = title
        self.description = description
        self.date = date
        self.view_count = view_count
        self.complainer = complainer
        self.answer = None
        
    def set_answer(self, date: str, message: str, score: str, replier: str):
        self.answer = Complaint.Answer(date, message, score, replier)