import requests
import sys
import json
import os


class ClientFile:

    def __init__(self, url: str):
        self.URL = url

    def files_post(self, file_name: str):
        with open(file_name, "rb") as file:
            file_dict = {'file': file}
            response = requests.post(
                self.URL+'/files', files=file_dict)
        return response.text

    def files_get(self):
        response = requests.get(self.URL+'/files')
        return response.text

    def download_file(self, file_name: str):
        response = requests.get(self.URL + '/files/' + file_name)
        mime_type = response.headers['Content-Type'].split()[0][:-1]
        print(mime_type, file=sys.stderr)
        if (response.status_code == 404):
            return response.text
        else:
            with open(f'{file_name}', 'wb') as f:
                f.write(response.content)

            return json.dumps({'upload_file': file_name,
                               'mime-type': mime_type,
                               'search in the directory': os.getcwd()+f'/{file_name}'}, indent=2)

    def delete_file(self, file_name: str):
        response = requests.delete(self.URL + '/files/' + file_name)
        return response.text
