import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from uuid import uuid4


class User:
    def __init__(self, config) -> None:
        import yaml

        self.config = yaml.safe_load(open(config, "r"))
        self.cookies = self.config["cookies"]
        self.urls = self.config["urls"]
        self.print_info()

    def print_info(self):
        print("Using your cookies: \n", self.cookies)
        print("Collect urls: ")
        for url in self.urls:
            print(url)


class Spider:
    def __init__(self, user: User):
        self.urls = user.urls
        self.headers = self.generate_headers(user.cookies)
        self.q_list = []
        self.all_q = []

    def generate_headers(self, cookies):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0",
        }
        headers["Cookie"] = cookies

        return headers

    def get_response(self, url):
        time.sleep(0.2)
        return requests.get(url, headers=self.headers)

    def get_questions_list(self, url):
        self.q_list = []
        soup = BeautifulSoup(self.get_response(url).text, "lxml")
        q_sections = soup.find_all("ul")

        for section in q_sections:
            for _ in section.find_all("li"):
                self.q_list.append(_["data"])

    def get_question_info(self, base_url, q_id):
        url = (
            base_url[: base_url.index("questionLinkId") + 15]
            + q_id
            + base_url[base_url.index("questionLinkId") + 24 :]
        )
        response = self.get_response(url)
        soup = BeautifulSoup(response.text, "lxml")
        category = soup.find("div", class_="tit").span.text.strip()
        if "论述题" in category:
            return None
        title = soup.find("div", class_="tit").p.text.strip()
        options = []
        for _ in soup.find("div", class_="optionBox").find_all("div"):
            options.append(_.text.strip())
        answer = soup.find("div", class_="correctAnswer").text.strip()

        return [q_id, category, title, *options, answer]

    def get_all_questions(self, url):
        for idx, q in enumerate(self.q_list):
            question = self.get_question_info(url, q)
            if question is None:
                continue
            self.all_q.append(question)
            print("%d Saving: %s" % (idx + 1, q))
        print("Amount: ", len(self.q_list))

    def save_to_excel(
        self,
    ):
        q_data = pd.DataFrame(self.all_q)
        res = q_data.drop_duplicates(2)
        xls_name = uuid4()
        res.to_excel("%s.xlsx" % xls_name, index=False, header=False)
        print("save to:", xls_name)

    def begin(self):
        for url in self.urls:
            print("Collecting: ", url)
            self.get_questions_list(url)
            self.get_all_questions(url)
        self.save_to_excel()


user = User("zjt.yaml")
spider = Spider(user)
spider.begin()
