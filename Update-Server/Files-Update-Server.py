from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api
import os
import datetime
import argparse

app = Flask(__name__)
api = Api(app)

PATH = "/home/hk/Connectivity-Solutions/Update-Server/Files"

class getLastModifiedTimeOfFiles(Resource):

	def __init__(self):

		self.files = os.listdir(PATH)

	def get(self):

		Data = {}

		for ind,file in enumerate(self.files):
			stat = os.path.getmtime(os.path.join(PATH,file))
			file_info = datetime.datetime.fromtimestamp(stat)
			filename, date , time = file, str(file_info).split(' ')[0], str(file_info).split(' ')[1]
			Data[ind] = {'File_Name' : filename, 'Date' : date, 'Time' : time} 

		message = {
			'status' : 200,
			'message' : "OK",
			'data' : Data
		}
		response = jsonify(message)
		response.status_code = 200
		return response


@app.route("/files/<path:path>")
def get_file(path):

	return send_from_directory(PATH, path, as_attachment=True)


def main():

	api.add_resource(getLastModifiedTimeOfFiles, '/')

if __name__ == '__main__':
	main()
	app.run(debug=True)