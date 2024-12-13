from typing import List
from ExamPaperSpider import ExamPaperSpider
from ExamPaper import ExamPaper
from Config import Config
import pandas as pd


class DataSaver:

    def __init__(self, outDir: str):
        self.outDir = outDir
        self.data: List[pd.DataFrame] = []
        self.csvNames = [
            'singleQuestions.csv', 'multiQuestions.csv', 'judgeQuestions.csv',
            'fillBlankQuestions.csv'
        ]
        self.htmlNames = [
            'singleQuestions.html', 'multiQuestions.html',
            'judgeQuestions.html', 'fillBlankQuestions.html'
        ]

    def loadData(self):
        self.data = []
        for csvName in self.csvNames:
            try:
                df = pd.read_csv(f'{self.outDir}/{csvName}')
                self.data.append(df)
            except FileNotFoundError:
                self.data.append(pd.DataFrame())

    def saveData(self, data: List[ExamPaper]):
        self.loadData()
        allQuestion = [[], [], [], []]

        for examPaper in data:
            for question in examPaper.singleQuestionList:
                allQuestion[0].append(question.fatten())
            for question in examPaper.multiQuestionList:
                allQuestion[1].append(question.fatten())
            for question in examPaper.judgeQuestionList:
                allQuestion[2].append(question.fatten())
            for question in examPaper.fillBlankQuestionList:
                allQuestion[3].append(question.fatten())

        self.data[0] = pd.concat(
            [self.data[0], pd.DataFrame(allQuestion[0])], ignore_index=True)
        self.data[1] = pd.concat(
            [self.data[1], pd.DataFrame(allQuestion[1])], ignore_index=True)
        self.data[2] = pd.concat(
            [self.data[2], pd.DataFrame(allQuestion[2])], ignore_index=True)
        self.data[3] = pd.concat(
            [self.data[3], pd.DataFrame(allQuestion[3])], ignore_index=True)

        for i in range(4):
            self.data[i].drop_duplicates(subset=['content'], inplace=True)
            self.data[i].sort_values(by=['content'], inplace=True)
            self.data[i].reset_index(drop=True, inplace=True)
            self.data[i].to_csv(f'{self.outDir}/{self.csvNames[i]}',
                                encoding='utf-8',
                                index=False)
            self.saveToHtml(self.data[i], self.htmlNames[i])

    def saveToHtml(self, data: pd.DataFrame, fileName: str):
        savePath = f'{self.outDir}/{fileName}'
        data['idx'] = data.index + 1
        columns = list(data.columns)
        columns.insert(0, columns.pop(columns.index('idx')))
        data = data.loc[:, columns]

        html_head = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="/assets/styles.css">
            {'<script src="/assets/script.js"></script>' if fileName in ['singleQuestions.html', 'multiQuestions.html'] else ''}
            </head>
            <body>
            """

        html_tail = """
            </body>
            </html>
            """

        if fileName == 'singleQuestions.html':
            table = "<table><tr><th>NO</th><th>题目</th><th>选项A</th><th>选项B</th><th>选项C</th><th>选项D</th><th>答案</th></tr>"
            for row in data.itertuples():
                marked = [0, 0, 0, 0]
                marked["ABCD".index(str(row.answer))] = 1
                tableRow = f"<tr><td>{row.idx}</td><td>{row.content}</td><td class='{'green' if marked[0] else ''}'>{row.choices_A}</td><td class='{'green' if marked[1] else ''}'>{row.choices_B}</td><td class='{'green' if marked[2] else ''}'>{row.choices_C}</td><td class='{'green' if marked[3] else ''}'>{row.choices_D}</td><td>{row.answer}</td></tr>"
                table += tableRow
            table += "</table>"
            with open(savePath, 'w', encoding='utf-8') as f:
                f.write(f"{html_head}{table}{html_tail}")
        elif fileName == 'multiQuestions.html':
            table = "<table><tr><th>NO</th><th>题目</th><th>选项A</th><th>选项B</th><th>选项C</th><th>选项D</th><th>答案</th></tr>"
            for row in data.itertuples():
                marked = [0, 0, 0, 0]
                for answer in str(row.answer):
                    marked["ABCD".index(answer)] = 1
                tableRow = f"<tr><td>{row.idx}</td><td>{row.content}</td><td class='{'green' if marked[0] else ''}'>{row.choices_A}</td><td class='{'green' if marked[1] else ''}'>{row.choices_B}</td><td class='{'green' if marked[2] else ''}'>{row.choices_C}</td><td class='{'green' if marked[3] else ''}'>{row.choices_D}</td><td>{row.answer}</td></tr>"
                table += tableRow
            table += "</table>"
            with open(savePath, 'w', encoding='utf-8') as f:
                f.write(f"{html_head}{table}{html_tail}")
        elif fileName == 'judgeQuestions.html':
            table = "<table><tr><th>NO</th><th>题目</th><th>答案</th></tr>"
            for row in data.itertuples():
                tableRow = f"<tr class='{'green' if str(row.answer) == '对' else 'red'}'><td>{row.idx}</td><td>{row.content}</td><td>{row.answer}</td></tr>"
                table += tableRow
            table += "</table>"
            with open(savePath, 'w', encoding='utf-8') as f:
                f.write(f"{html_head}{table}{html_tail}")
        elif fileName == 'fillBlankQuestions.html':
            table = "<table><tr><th>NO</th><th>题目</th><th>答案</th></tr>"
            for row in data.itertuples():
                tableRow = f"<tr><td>{row.idx}</td><td>{row.content}</td><td>{row.answer}</td></tr>"
                table += tableRow
            table += "</table>"
            with open(savePath, 'w', encoding='utf-8') as f:
                f.write(f"{html_head}{table}{html_tail}")


class GetExamPaper:

    def __init__(self, config_file: str):
        self.config = Config(config_file)
        self.headers = self.config.headers
        self.cookies = self.config.cookies
        # self.params = self.config.params
        self.data = []
        self.dataSaver = DataSaver('out')
        for cookie in self.cookies:
            print(f'开始爬取{cookie.get("UID", "")}的试卷')
            self.getExamPaper(cookie)

    def getExamPaper(self, cookies):
        data: list[ExamPaper] = []
        spider = ExamPaperSpider(self.headers, cookies, 0.15)
        params = spider.getExamPaperParams()
        for param in params:
            spider.setParams(param)
            data.append(spider.getExamPaper(param['examId']))

        self.dataSaver.saveData(data)


if __name__ == '__main__':
    # config_file = r'D:\Repositories\spider\chaoxing_mooc_spider\config.yaml'
    # GetExamPaper(config_file)
    DataSaver('out').saveData([])
