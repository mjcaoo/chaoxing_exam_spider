from typing import List
import pandas as pd


class SingleQuestion:
    id: int
    content: str
    choices: List[str]
    answer: str
    myAnswer: str

    def __init__(self, id: int, content: str, choices: List[str], answer: str,
                 myAnswer: str):
        self.id = id
        self.content = content
        self.choices = choices
        self.answer = answer
        self.myAnswer = myAnswer

    def __str__(self):
        return f"id: {self.id}, content: {self.content}, choices: {self.choices}, answer: {self.answer}, myAnswer: {self.myAnswer}"

    def fatten(self):
        fatten_data = {'id': self.id, 'content': self.content}
        txt = 'ABCDE'
        for i in range(len(self.choices)):
            fatten_data[f'choices_{txt[i]}'] = self.choices[i]
        fatten_data['answer'] = self.answer
        fatten_data['myAnswer'] = self.myAnswer
        return fatten_data


class MultipleQuestion:
    id: int
    content: str
    choices: List[str]
    answer: str
    myAnswer: str

    def __init__(self, id: int, content: str, choices: List[str], answer: str,
                 myAnswer: str):
        self.id = id
        self.content = content
        self.choices = choices
        self.answer = answer
        self.myAnswer = myAnswer

    def __str__(self):
        return f"id: {self.id}, content: {self.content}, choices: {self.choices}, answer: {self.answer}, myAnswer: {self.myAnswer}"

    def fatten(self):
        fatten_data = {'id': self.id, 'content': self.content}
        txt = 'ABCDE'
        for i in range(len(self.choices)):
            fatten_data[f'choices_{txt[i]}'] = self.choices[i]
        fatten_data['answer'] = self.answer
        fatten_data['myAnswer'] = self.myAnswer
        return fatten_data


class JudgeQuestion:
    id: int
    content: str
    answer: str
    myAnswer: str

    def __init__(self, id: int, content: str, answer: str, myAnswer: str):
        self.id = id
        self.content = content
        self.answer = answer
        self.myAnswer = myAnswer

    def __str__(self):
        return f"id: {self.id}, content: {self.content}, answer: {self.answer}, myAnswer: {self.myAnswer}"

    def fatten(self):
        fatten_data = {'id': self.id, 'content': self.content}
        fatten_data['answer'] = self.answer
        fatten_data['myAnswer'] = self.myAnswer
        return fatten_data


class FillBlankQuestion:
    id: int
    content: str
    answer: str
    myAnswer: str

    def __init__(self, id: int, content: str, answer: str, myAnswer: str):
        self.id = id
        self.content = content
        self.answer = answer
        self.myAnswer = myAnswer

    def __str__(self):
        return f"id: {self.id}, content: {self.content}, answer: {self.answer}, myAnswer: {self.myAnswer}"

    def fatten(self):
        fatten_data = {'id': self.id, 'content': self.content}
        fatten_data['answer'] = self.answer
        fatten_data['myAnswer'] = self.myAnswer
        return fatten_data


class ExamPaper:
    id: int
    singleQuestionList: List[SingleQuestion]
    multiQuestionList: List[MultipleQuestion]
    judgeQuestionList: List[JudgeQuestion]
    fillBlankQuestionList: List[FillBlankQuestion]

    def __init__(self, id: int):
        self.id = id
        self.singleQuestionList = []
        self.multiQuestionList = []
        self.judgeQuestionList = []
        self.fillBlankQuestionList = []


if __name__ == '__main__':
    pass
