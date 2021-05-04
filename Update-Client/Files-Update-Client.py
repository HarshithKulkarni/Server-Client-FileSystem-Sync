import os
import platform
import time
import requests
import datetime
import urllib.request
import shutil

SERVER_IP = "http://localhost"
SERVER_PORT = "5000"
PATH = "/home/hk/Connectivity-Solutions/Update-Client/Files"

def main():
	URL = SERVER_IP + ":" + SERVER_PORT
	try:
		while 1:

			current_files = os.listdir(PATH)
			response = requests.get(URL)
			response = response.json()['data']
			server_files = []
			for k in response.keys():
				server_files.append(response[k]['File_Name'])
			for i in current_files:
				if(i not in server_files):
					print(f"{i} Purged from Server, So Removing from Local Machine!!")
					os.remove(os.path.join(PATH,i))
					print(f"{i} Purged from Local Machine!!")
			for key in response.keys():
				server_file = response[key]['File_Name']
				if(server_file in current_files):
					for file in current_files:						
						if(file == server_file):
							if platform.system() == 'Windows':
								stat = os.path.getctime(os.path.join(PATH,file))
								current_file_info = datetime.datetime.fromtimestamp(stat)
							else:
								stat = os.path.getmtime(os.path.join(PATH,file))
								current_file_info = datetime.datetime.fromtimestamp(stat)

							server_file_date, server_file_time = response[key]['Date'], response[key]['Time']
							server_file_info = server_file_date + " " + server_file_time
							server_file_info = server_file_info.split('.')[0]
							server_file_info = datetime.datetime.strptime(server_file_info,'%Y-%m-%d %H:%M:%S')
							
							if(server_file_info > current_file_info):
								print(f"{server_file} changed on Server!!! Updating...")
								url = URL + "/files/" + server_file
								with urllib.request.urlopen(url) as resp, open(os.path.join(PATH,server_file), 'wb') as out_file:
									shutil.copyfileobj(resp, out_file)
								print("Updated!!")

				else:
					print(f"New File Added to Server {server_file}")
					url = URL + "/files/" + server_file
					with urllib.request.urlopen(url) as resp, open(os.path.join(PATH,server_file), 'wb') as out_file:
						shutil.copyfileobj(resp, out_file)
					print("New File Updated!!")

			time.sleep(1)

	except KeyboardInterrupt:
		exit()

if __name__ == '__main__':
	main()