import yaml
from urllib.parse import urlparse, parse_qs

class Config:
    headers: dict
    cookies: list
    # params: list

    def __init__(self, config_file: str) -> None:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.headers = config['headers']
        self.cookies = [self.parseCookies(cookie) for cookie in config['cookies']]
        # self.params = self.parseUrls(config['urls'])

    def parseCookies(self, cookies_str: str) -> dict:
        cookies = {}
        for cookie in cookies_str.split(';'):
            key, value = cookie.strip().split('=')
            cookies[key] = value
        return cookies

    # def parseUrls(self, urls_str: str) -> list:
    #     params = []
    #     for url in urls_str:
    #         parsed_url = urlparse(url)
    #         query_params = parsed_url.query
    #         params_dict = parse_qs(query_params)
    #         params.append(params_dict)
    #     return params
    
    def __str__(self) -> str:
        return f'headers: {self.headers}, cookies: {self.cookies}'