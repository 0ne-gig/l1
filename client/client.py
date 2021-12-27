import requests
import json


class Client:

    def __init__(self, login: str, pas: str, url: str):
        self.user_atr = {
            'login': login,
            'pas': pas
        }
        self.URL = url

    def login(self):
        response = requests.post(
            self.URL+'user', data=self.user_atr)
        self.cookies = {'access_token_cookie': dict(
            response.cookies)['access_token_cookie']}

        return self.cookies

    def post_todo(self, descr: str):
        response = requests.post(self.URL+'todo',
                                 data={'описание': descr}, cookies=self.cookies)
        return response.text

    def get_todo(self):
        response = requests.get(self.URL+'todo', cookies=self.cookies)
        todo_list = (json.dumps(response.json(), sort_keys=True,
                     ensure_ascii=False, indent=4))
        return todo_list

    def put_todo(self, id: int, descr: str):
        response = requests.put(
            self.URL+f'todo/{id}', data={'описание': descr}, cookies=self.cookies)
        return response.text

    def delete_todo(self, id: int):
        response = requests.delete(
            self.URL+f'todo/{id}', cookies=self.cookies)
        return response.text
