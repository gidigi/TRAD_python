import http.client,json


class TRAD:
    def __headers(self):
        return ({
             'Content-type' : 'application/json;charset=utf-8',
             'Hash' : self.__hash,
             'Auth' : self.__auth,
             'Client' : self.__client,
             'User' : self.__user,
             'Type' : self.__type,
             'Company' : self.__company
        })
    def __get(self, url: str)->tuple:
        self.__conn.request('GET', url, '', self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def __post(self, url: str, post:dict)->tuple:
        self.__conn.request('POST', url, json.dumps(post), self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def __put(self, url: str, post:dict)->tuple:
        self.__conn.request('PUT', url, json.dumps(post), self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def __connect(self, url: str, post:dict)->tuple:
        self.__conn.request('CONNECT', url, json.dumps(post), self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def __delete(self, url: str, post:dict)->tuple:
        self.__conn.request('DELETE', url, json.dumps(post), self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
    def hello(self)->bool:
        result = json.loads(self.__get('/hello'))
        try:
            self.__client = result['client']
            self.__last_failed = False
            return True
        except (NameError, AttributeError):
            self.__last_failed = True
        return False
    def login(self, login:str, password:str)->bool:
        result = json.loads(
            self.__post(
                '/login', 
                {'login': login,'password':password}
            )
        )
        try:
            self.__hash = result['data']['auth']
            self.__user = result['data']['id']
            self.__last_failed = False
            return True
        except (NameError, AttributeError):
            self.__last_failed = True
        return False
    def register(
      self,
      name:str,
      email:str,
      phone:str,
      password:str
    )->int:
        result = json.loads(
            self.__post(
                '/user', 
                {
                    'name'     : name,
                    'email'    : email,
                    'phone'    : phone,
                    'password' : password
                }
            )
        )
    def tasks(self)->dict:
        result = json.loads(self.__get('/tasks'))
        return result['data']
    def taskAdd(self, name:str)->dict:
        result = json.loads(self.__post('/task', {'name':name}))
        return result
    def activities(self)->dict:
        result = json.loads(self.__get('/activities'))
        return result['data']
    def activityAdd(self, name:str)->dict:
        result = json.loads(self.__post('/activity', {'name':name}))
        return result
    def projects(self)->dict:
        result = json.loads(self.__get('/projects'))
        return result['data']
    def projectAdd(self, name:str)->dict:
        result = json.loads(self.__post('/project', {'name':name}))
        return result
    def report_start(
      self,
      project:str,
      task:str,
      activity:str,
      name:str
   )->bool:
        result = json.loads(self.__post(
          '/report',
          {
              'project':project,
              'task':task,
              'activity':activity,
              'name':name
          }
        ))
        try:
            if result['id'] > -1:
                return result["id"]
        except (NameError, AttributeError):
            self.__last_failed = True
        return -1
    def report_connect(
      self,
      report:str
   )->bool:
        result = json.loads(self.__connect(
          '/report',
          {
              'report':report
          }
        ))
        try:
            if result['id'] > -1:
                return result["id"]
        except (NameError, AttributeError):
            self.__last_failed = True
        return -1
    def report_stop(
      self,
      report:str
   )->bool:
        result = json.loads(self.__delete(
          '/report',
          {
              'report':report
          }
        ))
        try:
            if result['id'] > -1:
                return result["id"]
        except (NameError, AttributeError):
            self.__last_failed = True
        return -1
    def standup_full(
      self,
      projects:list,
      tasks:list,
      plan:str,
      blocking:str,
      yesterday:str,
      result:str,
      blocked:str,
      comment:str,
      feeling:str,
      timestamp:int,
      day:int
   )->bool:
        if self.__logined == False:
            return 
        self.__last_failed = False
        result = json.loads(self.__post(
          '/standup',
          {
            'projects':projects,
            'tasks':tasks,
            'plan':plan,
            'blocking':blocking,
            'yesterday':yesterday,
            'result':result,
            'blocked':blocked,
            'comment':comment,
            'feeling':feeling,
            'timestamp':timestamp,
            'day':day
          }
        ))
        try:
            if result['id'] > -1:
                return True
        except (NameError, AttributeError):
            self.__last_failed = True
        return False
    def standup(
      self,
      plan:str,
      blocking:str,
      yesterday:str,
      result:str,
      blocked:str,
      comment:str,
      feeling:str,
      timestamp:int,
      day:int
   )->bool:
        if self.__logined == False:
            return 
        self.__last_failed = False
        result = json.loads(self.__post(
          '/standup',
          {
              'plan':plan,
              'blocking':blocking,
              'yesterday':yesterday,
              'result':result,
              'blocked':blocked,
              'comment':comment,
              'feeling':feeling,
              'timestamp':timestamp,
              'day':day
          }
        ))
        try:
            if result['id'] > -1:
                return True
        except (NameError, AttributeError):
            self.__last_failed = True
        return False
    def __init__(self):
        self.__logined = False
        self.__last_failed = False
        self.__last_response = '';
        self.__hash = "null"
        self.__auth = "null"
        self.__client = "null"
        self.__user = "null"
        self.__company = "null"
        self.__type = "TPY0OP"
        self.__conn = http.client.HTTPSConnection('api.trad.gidigi.com', 443)
