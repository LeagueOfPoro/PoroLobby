import psutil
import requests
from exceptions.ClientNotRunningException import ClientNotRunningException

# This class was inspired by lcu-driver: https://github.com/sousa-andre/lcu-driver
class ConnectionManager:

    def __init__(self) -> None:
        self.proc = self._findLeagueClientProcess()
        if not self.proc:
            raise ClientNotRunningException()
        self._extractConnectionSettings()
        self.baseUrl = f'https://127.0.0.1:{self.app_port}'

        self.session = requests.Session()
        self.session.auth = ('riot', self.remoting_auth_token)
        self.session.verify = False
        requests.urllib3.disable_warnings()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def get(self, url) -> requests.Response:
        return self.session.get(self.baseUrl + url)
    
    def post(self, url, jsonData) -> requests.Response:
        return self.session.post(self.baseUrl + url, json=jsonData)

    def isConnected(self):
        return self.get("/lol-summoner/v1/current-summoner").status_code == 200
    def _findLeagueClientProcess(self) -> psutil.Process:
        for proc in psutil.process_iter():
            if proc.name() == "LeagueClientUx.exe":
                return proc
    
    def _extractConnectionSettings(self) -> None:
        for item in self.proc.cmdline():
            if item.startswith('--app-pid='):
                self.app_pid = item.split('=', 1)[1]
            elif item.startswith('--app-port='):
                self.app_port = item.split('=', 1)[1]
            elif item.startswith('--remoting-auth-token='):
                self.remoting_auth_token = item.split('=', 1)[1]
