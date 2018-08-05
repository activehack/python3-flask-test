import json
import requests
import os
from random import shuffle

class jokes:
  data = []
  endpoint_url = 'http://api.icndb.com/jokes/random/'
  local_data_uri = '/dev/shm/python3_test_jokes.json'

  @classmethod
  def get_jokes(cls, jcount=10):
    try:
      ret = cls.get_all_jokes()    
      shuffle(ret)
      return ret[:jcount]
    except:
      return None

  @classmethod
  def update_jokes(cls):
    print("Downloading jokes...")
    new_jokes = cls.download_jokes()
    if new_jokes is None:
      new_jokes = []
    print("%s joke(s) downloaded" % (len(new_jokes)))
    if cls.add_joke(new_jokes):
      return True
    return False

  @classmethod
  def download_joke(cls):
    r = requests.get(cls.endpoint_url)
    if r.status_code == 200:
      data = r.json()
      return data['value']
    return None

  @classmethod
  def download_jokes(cls):
    local_jokes = cls.get_all_jokes()
    if local_jokes is None:
      local_jokes = []
    ret = []
    err_max = 3
    err_count = 0
    while len(ret) < 10 and err_count < 3:
      j = cls.download_joke()
      if j is None:
        err_count += 1
        continue
        
      ''' skip if joke already in local_jokes '''
      if j['id'] in [x['id'] for x in local_jokes]:
        continue

      ''' skip if joke already in ret '''
      if j['id'] in [x['id'] for x in ret]:
        continue

      ret.append(j)
    if err_count >= 3:
      return None
    return ret

  @classmethod
  def get_all_jokes(cls):    
    try:
      with open(cls.local_data_uri) as f:
        data = json.load(f)
      return data
    except Exception as e:      
      return None

  @classmethod
  def add_joke(cls, jokes):
    try:
      with open(cls.local_data_uri,'w') as f:
        f.write(json.dumps(jokes))
      return True
    except:
      return False

  @classmethod
  def flush_jokes(cls):
    try:
      os.remove(cls.local_data_uri)
    except:
      pass
    return True
