from typing import Any, List, Union
import requests
from HtmlParser import HtmlParser
from ExamPaper import ExamPaper, SingleQuestion, MultipleQuestion, JudgeQuestion, FillBlankQuestion
from time import sleep
from tqdm import tqdm
import pandas as pd


class Spider:
    url: str
    headers: Union[dict, None]
    cookies: Union[dict, None]
    params: Union[dict, None]
    method: str
    timeout: int

    def __init__(self,
                 headers: Union[dict, None] = None,
                 cookies: Union[dict, None] = None) -> None:
        self.headers = headers
        self.cookies = cookies

    def sendRequest(self,
                    url: str,
                    method: str = 'GET',
                    params: Union[dict, None] = None,
                    timeout: int = 10) -> str:
        response = requests.request(method,
                                    url,
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    params=params,
                                    timeout=timeout)
        return response.text

    def __call__(self,
                 url: str,
                 method: str = 'GET',
                 params: Union[dict, None] = None,
                 timeout: int = 10):
        return self.sendRequest(url, method, params, timeout)


class ExamPaperSpider(Spider):

    def __init__(
        self,
        headers: dict,
        cookies: dict,
        timeSleep: float = 0.5,
    ) -> None:
        super().__init__(headers, cookies)
        self.examPaperUrl = "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/examcode"
        self.lookDetailUrl = "https://mooc1-api.chaoxing.com/exam/phone/look-detail"
        self.lookInfoUrl = "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail"
        self.timeSleep = timeSleep

    def setParams(self, parmas: dict) -> None:
        self.infoParams = parmas.copy()
        self.detailParams = parmas.copy()
        self.detailParams["isDetail"] = 1

    def getExamPaperParams(self):
        response = self.sendRequest(self.examPaperUrl, 'GET')
        parser = HtmlParser(response)
        entryPoints = parser.getEntryPointsUrl()
        params = []
        for entryPoint in entryPoints:
            response = self.sendRequest(entryPoint, 'GET')
            parser = HtmlParser(response)
            examPaperParam = parser.getExamPaperParams()
            params.append(examPaperParam)
        return params

    def getExamPaperInfos(self) -> None:
        self.infoParams["isDetail"] = 0
        response = self.sendRequest(self.lookInfoUrl,
                                    'GET',
                                    params=self.infoParams)
        parser = HtmlParser(response)
        self.singleQuestionIds = parser.getSingleSelectIds()
        self.multipleQuestionIds = parser.getMultiSelectIds()
        self.judgeQuestionIds = parser.getJudgeIds()
        self.fillQuestionIds = parser.getFillIds()

    def getSingleQuestions(self, pbar: tqdm) -> List[SingleQuestion]:
        singleQuestions: List[SingleQuestion] = []
        _params = self.detailParams.copy()
        for qid in self.singleQuestionIds:
            pbar.set_description(f"正在获取单选题: {qid}")
            _params["questionLinkId"] = qid
            response = self.sendRequest(self.lookDetailUrl,
                                        'GET',
                                        params=_params)
            parser = HtmlParser(response)
            singleQuestions.append(parser.parseSingleSelect(qid))
            sleep(self.timeSleep)  # 延迟一段时间，防止请求过快
            pbar.update(1)
        return singleQuestions

    def getMultipleQuestions(self, pbar: tqdm) -> List[MultipleQuestion]:
        multiQuestions: List[MultipleQuestion] = []
        _params = self.detailParams.copy()
        for qid in self.multipleQuestionIds:
            pbar.set_description(f"正在获取多选题: {qid}")
            _params["questionLinkId"] = qid
            response = self.sendRequest(self.lookDetailUrl,
                                        'GET',
                                        params=_params)
            parser = HtmlParser(response)
            multiQuestions.append(parser.parseMultiSelect(qid))
            sleep(self.timeSleep)  # 延迟一段时间，防止请求过快
            pbar.update(1)
        return multiQuestions

    def getJudgeQuestions(self, pbar: tqdm) -> List[JudgeQuestion]:
        judgeQuestions: List[JudgeQuestion] = []
        _params = self.detailParams.copy()
        for qid in self.judgeQuestionIds:
            pbar.set_description(f"正在获取判断题: {qid}")
            _params["questionLinkId"] = qid
            response = self.sendRequest(self.lookDetailUrl,
                                        'GET',
                                        params=_params)
            parser = HtmlParser(response)
            judgeQuestions.append(parser.parseJudge(qid))
            sleep(self.timeSleep)  # 延迟一段时间，防止请求过快
            pbar.update(1)
        return judgeQuestions

    def getFillQuestions(self, pbar: tqdm) -> List[FillBlankQuestion]:
        fillQuestions: List[FillBlankQuestion] = []
        _params = self.detailParams.copy()
        for qid in self.fillQuestionIds:
            pbar.set_description(f"正在获取填空题: {qid}")
            _params["questionLinkId"] = qid
            response = self.sendRequest(self.lookDetailUrl,
                                        'GET',
                                        params=_params)
            parser = HtmlParser(response)
            fillQuestions.append(parser.parseFill(qid))
            sleep(self.timeSleep)  # 延迟一段时间，防止请求过快
            pbar.update(1)
        return fillQuestions

    def getExamPaper(self, examId: int) -> ExamPaper:
        self.getExamPaperInfos()
        pbar = tqdm(total=len(self.singleQuestionIds) +
                    len(self.multipleQuestionIds) +
                    len(self.judgeQuestionIds) + len(self.fillQuestionIds),
                    desc=f"正在获取试卷: {examId}")
        examPaper = ExamPaper(examId)
        examPaper.singleQuestionList = self.getSingleQuestions(pbar)
        examPaper.multiQuestionList = self.getMultipleQuestions(pbar)
        examPaper.judgeQuestionList = self.getJudgeQuestions(pbar)
        examPaper.fillBlankQuestionList = self.getFillQuestions(pbar)
        return examPaper


class TestExamPaperSpider:

    def __init__(self, headers: dict, cookies: dict, parmas: dict) -> None:
        self.spider = ExamPaperSpider(headers, cookies)

    def testGetExamPaperInfos(self):
        self.spider.getExamPaperInfos()
        print(self.spider.singleQuestionIds)
        print(self.spider.multipleQuestionIds)
        print(self.spider.judgeQuestionIds)
        print(self.spider.fillQuestionIds)

    def testGetSingleQuestions(self):
        pbar = tqdm(total=len(self.spider.singleQuestionIds))
        singleSelectorList = self.spider.getSingleQuestions(pbar)
        data = [selector.fatten() for selector in singleSelectorList]
        print(data)
        df = pd.DataFrame(data)
        df.to_csv('single.csv', index=False, encoding='gbk')

    def testGetFillQuestions(self):
        pbar = tqdm(total=len(self.spider.fillQuestionIds))
        fillBlankSelectorList = self.spider.getFillQuestions(pbar)
        for selector in fillBlankSelectorList:
            print(selector)


if __name__ == '__main__':
    from Config import Config

    config = Config(
        r'D:\Repositories\spider\chaoxing_mooc_spider\test\config.yaml')
    testExamPaperSpider = TestExamPaperSpider(config.headers, config.cookies,
                                              config.params[0])
    testExamPaperSpider.testGetExamPaperInfos()
    testExamPaperSpider.testGetSingleQuestions()
    # testExamPaperSpider.testGetFillQuestions()
