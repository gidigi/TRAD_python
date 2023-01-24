import http.client,json


class TRAD:
    def __headers(self):
        out = {'Content-type' : 'application/json;charset=utf-8'}
        if self.__hash != "null":
            out["Hash"] = self.__hash
        if self.__auth != "null":
            out["Auth"] = self.__auth
        if self.__client != "null":
            out["Client"] = self.__client
        if self.__user != "null":
            out["User"] = self.__user
        if self.__type != "null":
            out["Type"] = self.__type
        if self.__company != "null":
            out["Company"] = self.__company
        return out
    def __get(self, url: str)->tuple:
        self.__conn.request('GET', url, '', self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
        print(response.status)
    def __post(self, url: str, post:dict)->tuple:
        self.__conn.request('POST', url, json.dumps(post), self.__headers()) 
        response = self.__conn.getresponse()
        self.__last_response = response
        if response.status == 200:
            return response.read().decode()
        print(response.status)
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
            self.__company = result['data']['company']
            self.__auth    = result['data']['auth']
            self.__hash    = result['data']['hash']
            self.__user    = result['data']['id']
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
        result = self.__post(
            '/user', 
            {
                    'name'     : name,
                    'email'    : email,
                    'phone'    : phone,
                    'password' : password
            }
        )
        return json.loads(result)['id']
    def users(self)->dict:
        result = self.__get('/users')
        print(result)
        return json.loads(result)
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

    def companies(self)->dict:
        print(self.__get('/companies'))
        result = json.loads(self.__get('/companies'))
        print(result)
        return result['data']
    def companyAdd(self, name:str)->dict:
        result = json.loads(self.__post('/company', {'name':name}))
        return result
    def trackerAdd(self,project,task,activity,name):
        result = json.loads(self.__post(
          '/tracker',
          {
              'project':project,
              'task':task,
              'activity':activity,
              'name':name,
          }
        ))
        try:
            if result['id'] > -1:
                return result['id']
        except (NameError, AttributeError):
            return -1
        return -1
    def trackerStart(self, tracker):
        result = json.loads(self.__post(
          '/start',
          {
              'tracker':tracker
          }
        ))
    def trackerStop(self, tracker):
        result = json.loads(self.__post(
          '/stop',
          {
              'tracker':tracker
          }
        ))
    def trackerLate(self, tracker, start, stop):
        result = json.loads(self.__post(
          '/report',
          {
              'tracker':tracker,
              'start':start,
              'stop':stop
          }
        ))
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
