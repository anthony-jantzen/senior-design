import json

class JSONLibrary:
	@staticmethod
	def get_dict_from_json_file(json_file):
		with open(json_file, 'r') as f:
			data = f.read()
		return json.loads(data)
