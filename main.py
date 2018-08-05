from flask import Flask
from flask_restful import Resource, Api
from lib_jokes import jokes

app = Flask(__name__)
api = Api(app)

def startup_job():
  if jokes.flush_jokes():
    print("jokes.flush_jokes(): OK")
  else:
    print("jokes.flush_jokes(): FAIL")

  print("Starting... jokes.update_jokes()")
  if jokes.update_jokes():
    print("jokes.update_jokes(): OK")
  else:
    print("jokes.update_jokes(): FAIL")

class route_getJokes(Resource):
  def get(self):
    data = jokes.get_jokes()
    if data is not None:
      return {'status':'OK','data':data}
    return {'status':'FAIL', 'message':'No joke found'}, 400

class route_flushJokes(Resource):
  def get(self):
    if jokes.flush_jokes():
      return {'status':'OK','message':'Databse is flushed'}
    return {'status':'FAIL'}, 400

class route_getNewJokes(Resource):
  def get(self):
    data = jokes.download_jokes()
    if data is not None:
      return {'status':'OK','data':data}
    return {'status':'FAIL','message':'Error when downloading jokes'}, 400

api.add_resource(route_getJokes, '/getJokes')
api.add_resource(route_flushJokes, '/flushJokes')
api.add_resource(route_getNewJokes, '/getNewJokes')

if __name__ == '__main__':
  startup_job()
  app.run(host='0.0.0.0', port=5000, debug=True)
