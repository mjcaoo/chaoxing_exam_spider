import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from uuid import uuid4

base_urls = ["https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88346255&examId=4043938&examAnswerId=108132952&isDetail=true&questionLinkId=883625095&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88346303&examId=4043581&examAnswerId=107709237&isDetail=true&questionLinkId=883634750&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88346346&examId=4071281&examAnswerId=108001256&isDetail=true&questionLinkId=883640298&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88346385&examId=4043945&examAnswerId=108762283&isDetail=true&questionLinkId=883647658&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88346437&examId=4028267&examAnswerId=107536016&isDetail=true&questionLinkId=883661557&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88356656&examId=4071796&examAnswerId=108402959&isDetail=true&questionLinkId=883666269&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88356711&examId=4080775&examAnswerId=108293415&isDetail=true&questionLinkId=883672436&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88356727&examId=4028714&examAnswerId=107644896&isDetail=true&questionLinkId=883684547&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88356759&examId=4020175&examAnswerId=107962588&isDetail=true&questionLinkId=883795744&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88356795&examId=4044487&examAnswerId=108885263&isDetail=true&questionLinkId=883693889&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88384774&examId=4049496&examAnswerId=108038974&isDetail=true&questionLinkId=883701017&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88384831&examId=4082023&examAnswerId=108296591&isDetail=true&questionLinkId=883716927&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88384885&examId=4045769&examAnswerId=108885991&isDetail=true&questionLinkId=883737907&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88384939&examId=4021364&examAnswerId=107963702&isDetail=true&questionLinkId=883732539&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88384983&examId=4045625&examAnswerId=108300738&isDetail=true&questionLinkId=883752716&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88385074&examId=4049502&examAnswerId=108040005&isDetail=true&questionLinkId=883754931&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88385128&examId=3991061&examAnswerId=107952397&isDetail=true&questionLinkId=883767093&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88385170&examId=4031067&examAnswerId=108515791&isDetail=true&questionLinkId=883776683&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88385198&examId=3991064&examAnswerId=107952766&isDetail=true&questionLinkId=883781708&times=0&newVersion=1#INNER",
            "https://mooc1-api.chaoxing.com/exam-ans/exam/phone/look-detail?courseId=234859562&classId=88385227&examId=4029838&examAnswerId=107648239&isDetail=true&questionLinkId=883788831&times=0&newVersion=1#INNER",]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0",
    'Cookie': 'k8sexam=1702039958.618.7074.965538;jrose=C5F76FD91F41FF12CD955B987A06BB72.mooc-exam-3592995947-6x3z8;fid=18743;fanyamoocs=11401F839C536D9E;lv=1;_uid=236978760;uf=b2d2c93beefa90dc62d0140d27586032be363a80c34379c8fe958e0334cc3c2206fe4b8fded3793271f24f21e45ebfb3748a002894d7f44e88b83130e7eb4704a07401fce4235b32ce915f659a7402a863282831c4613bcccd60b9b15fdb7d7c18f9e357a656b0fa;_d=1702039892836;UID=236978760;vc=182600D54CC052FE42F51E8288D90E60;vc2=E0E8FB507CC7E93FD17E6ABA227129A4;vc3=WXTjoMU5rNOKruyxvKm%2BZ4XxbbPIqaeKyEVUGwwlQ%2B9%2FUyxCxO%2BBN%2FKkj0CWvTwbvRweuA5l6x9nnTR1k%2FvHIW3AbvvlqSLBfJBulePn4hQa%2BhdZNeQ%2FMubhSs2hmbyPOfhZljPcuxen8O16sq%2FAEbnKa86M06I%2Bsy3RUXak%2BlI%3D0a5ff9315da532b090f9138f2d21f0ed;cx_p_token=e0f9c53c7be90220071b31593d8fdb41;p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyMzY5Nzg3NjAiLCJsb2dpblRpbWUiOjE3MDIwMzk4OTI4MzgsImV4cCI6MTcwMjY0NDY5Mn0.EDTruKb27DnB-SzW-PkBy97ZKR-VJJrZU7gQ4qGteLk;xxtenc=1378a860e1067324f83580679ff7fd9b;DSSTASH_LOG=C_38-UN_755-US_236978760-T_1702039892838;source="";thirdRegist=0;route=7644025d506561102d55bac4c90cbeeb'
}


class Spider:
    def __init__(self, url, header):
        self.base_url = url
        self.headers = header
        self.q_list = []
        self.all_q = []
        self.questions_list()
        self.get_all_questions()
        self.save_to_excel()

    def get_response(self, url=None):
        if url == None:
            url = self.base_url
        return requests.get(url, headers=self.headers)

    def questions_list(self):
        soup = BeautifulSoup(self.get_response().text, "lxml")
        q_sections = soup.find_all("ul")
        for section in q_sections:
            for _ in section.find_all("li"):
                self.q_list.append(_["data"])

    def get_question_info(self, q_id):
        url = self.base_url[:self.base_url.index(
            "questionLinkId")+15]+q_id+self.base_url[self.base_url.index("questionLinkId")+24:]
        response = self.get_response(url)
        soup = BeautifulSoup(response.text, "lxml")
        category = soup.find("div", class_="tit").span.text.strip()
        title = soup.find("div", class_="tit").p.text.strip()
        options = []
        for _ in soup.find("div", class_="optionBox").find_all("div"):
            options.append(_.text.strip())
        answer = soup.find("div", class_="correctAnswer").text.strip()
        return [q_id, category, title, *options, answer]

    def get_all_questions(self):
        for idx, q in enumerate(self.q_list):
            self.all_q.append(self.get_question_info(q))
            time.sleep(0.5)
            print("%d Saving: %s" % (idx + 1, q))
        print("Amount: ", len(self.q_list))

    def save_to_excel(self, ):
        q_data = pd.DataFrame(self.all_q)
        xls_name = uuid4()
        q_data.to_excel("ori/%s.xlsx"%xls_name)
        print("save to:ori/%s.xlsx"%xls_name)


for base_url in base_urls:
    demo = Spider(base_url, headers)
