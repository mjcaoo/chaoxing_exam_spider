from lxml import etree
from ExamPaper import ExamPaper, SingleQuestion, MultipleQuestion, JudgeQuestion, FillBlankQuestion


class HtmlParser:

    def __init__(self, html):
        self.html = html
        self.tree = etree.HTML(self.html,
                               parser=etree.HTMLParser(encoding='utf-8'))

    def getSingleSelectIds(self):
        single_choice_div = self.tree.xpath(
            '//div[@class="ansCardBox"][h3[contains(text(), "单选题")]]')
        single_choice_li_data = [
            li.get('data') for li in single_choice_div[0].xpath('.//li')
        ]
        # single_choice_li_text = [li.text.strip() for li in single_choice_div[0].xpath('.//li')]
        return single_choice_li_data

    def getMultiSelectIds(self):
        multi_choice_div = self.tree.xpath(
            '//div[@class="ansCardBox"][h3[contains(text(), "多选题")]]')
        multi_choice_li_data = [
            li.get('data') for li in multi_choice_div[0].xpath('.//li')
        ]
        # multi_choice_li_text = [li.text.strip() for li in multi_choice_div[0].xpath('.//li')]
        return multi_choice_li_data

    def getJudgeIds(self):
        judge_div = self.tree.xpath(
            '//div[@class="ansCardBox"][h3[contains(text(), "判断题")]]')
        judge_li_data = [li.get('data') for li in judge_div[0].xpath('.//li')]
        # judge_li_text = [li.text.strip() for li in judge_div[0].xpath('.//li')]
        return judge_li_data

    def getFillIds(self):
        fill_div = self.tree.xpath(
            '//div[@class="ansCardBox"][h3[contains(text(), "论述题")]]')
        fill_li_data = [li.get('data') for li in fill_div[0].xpath('.//li')]
        # fill_li_text = [li.text.strip() for li in fill_div[0].xpath('.//li')]
        return fill_li_data

    def parseSingleSelect(self, qid: int) -> SingleQuestion:
        content = self.tree.xpath(
            '//div[@class="answerCon border16"]//div[@class="tit"]//p//text()')
        content = content[0].strip()
        choices = self.tree.xpath(
            '//div[@class="optionBox"]/div[@class="optionCon"]')
        choices_content = [element.text.strip() for element in choices]
        myanswer = self.tree.xpath(
            '//div[@class="myanswer"]//div[@class="answerInfo fontBold"]/p//text()'
        )
        myanswer_text = "".join(
            [text.strip() for text in myanswer if text.strip()])
        correct_answer = self.tree.xpath(
            '//div[@class="greenColor correctAnswer"]//text()')
        correct_answer_text = "".join(
            [text.strip() for text in correct_answer if text.strip()])
        return SingleQuestion(qid, content, choices_content,
                              correct_answer_text, myanswer_text)

    def parseMultiSelect(self, qid: int) -> MultipleQuestion:
        content = self.tree.xpath(
            '//div[@class="answerCon border16"]//div[@class="tit"]//p//text()')
        content = content[0].strip()
        choices = self.tree.xpath(
            '//div[@class="optionBox"]/div[@class="optionCon"]')
        choices_content = [element.text.strip() for element in choices]
        myanswer = self.tree.xpath(
            '//div[@class="myanswer"]//div[@class="answerInfo fontBold"]/p//text()'
        )
        myanswer_text = "".join(
            [text.strip() for text in myanswer if text.strip()])
        correct_answer = self.tree.xpath(
            '//div[@class="greenColor correctAnswer"]//text()')
        correct_answer_text = "".join(
            [text.strip() for text in correct_answer if text.strip()])
        return MultipleQuestion(qid, content, choices_content,
                                correct_answer_text, myanswer_text)

    def parseJudge(self, qid: int) -> JudgeQuestion:
        content = self.tree.xpath(
            '//div[@class="answerCon border16"]//div[@class="tit"]//p//text()')
        content = content[0].strip()
        # choices = self.tree.xpath(
        #     '//div[@class="optionBox"]/div[@class="optionCon"]')
        # choices_content = [element.text.strip() for element in choices]
        myanswer = self.tree.xpath(
            '//div[@class="myanswer"]//div[@class="answerInfo fontBold"]/p//text()'
        )
        myanswer_text = "".join(
            [text.strip() for text in myanswer if text.strip()])
        correct_answer = self.tree.xpath(
            '//div[@class="greenColor correctAnswer"]//text()')
        correct_answer_text = "".join(
            [text.strip() for text in correct_answer if text.strip()])
        return JudgeQuestion(qid, content, correct_answer_text, myanswer_text)

    def parseFill(self, qid: int) -> FillBlankQuestion:
        content = self.tree.xpath(
            '//div[@class="answerCon border16"]//div[@class="tit"]//p//text()')
        content = content[0].strip()
        my_answer = self.tree.xpath(
            '//div[@class="myanswer"]//div[@class="answerInfo"]//p//text()')
        my_answer_text = "".join(
            [text.strip() for text in my_answer if text.strip()])
        correct_answer = self.tree.xpath(
            '//div[@class="greenColor correctAnswer"]//p//text()')
        correct_answer_text = "".join(
            [text.strip() for text in correct_answer if text.strip()])
        return FillBlankQuestion(qid, content, correct_answer_text,
                                 my_answer_text)

    def getEntryPointsUrl(self):
        li_elements = self.tree.xpath(
            f"//li[contains(@title, '习近平新时代中国特色社会主义思想概论')]/@data")
        for i in range(len(li_elements)):
            li_elements[i] = "https://mooc1-api.chaoxing.com" + li_elements[i]
        return li_elements
    
    def getExamPaperParams(self):
        courseId = self.tree.xpath('//input[@name="courseId"]/@value')[0]
        classId = self.tree.xpath('//input[@name="classId"]/@value')[0]
        examId = self.tree.xpath('//input[@name="examRelationId"]/@value')[0]
        examAnswerId = self.tree.xpath('//input[@name="answerId"]/@value')[0]
        return {"courseId": courseId, "classId": classId, "examId": examId, "examAnswerId": examAnswerId}


if __name__ == '__main__':
    # with open(r'D:\Repositories\spider\chaoxing_mooc_spider\test\infos.html',
    #           'r',
    #           encoding='utf-8') as f:
    #     html = f.read()
    # parser = HtmlParser(html)
    # print(parser.getSingleSelectIds())
    # print(parser.getMultiSelectIds())
    # print(parser.getJudgeIds())
    # print(parser.getFillIds())
    with open(
            r'D:\Repositories\spider\chaoxing_mooc_spider\test\contents\Exam Details.html',
            'r',
            encoding='utf-8') as f:
        html = f.read()
    parser = HtmlParser(html)
    print(parser.parseFill(123456))
    # with open(
    #         r'D:\Repositories\spider\chaoxing_mooc_spider\test\contents\single.html',
    #         'r',
    #         encoding='utf-8') as f:
    #     html = f.read()
    # parser = HtmlParser(html)
    # print(parser.parseSingleSelect(123456))
    # with open(
    #         r'D:\Repositories\spider\chaoxing_mooc_spider\test\contents\multi.html',
    #         'r',
    #         encoding='utf-8') as f:
    #     html = f.read()
    # parser = HtmlParser(html)
    # print(parser.parseSingleSelect(123456))
    # with open(
    #         r'D:\Repositories\spider\chaoxing_mooc_spider\test\contents\judge.html',
    #         'r',
    #         encoding='utf-8') as f:
    #     html = f.read()
    # parser = HtmlParser(html)
    # print(parser.parseJudge(123456))
