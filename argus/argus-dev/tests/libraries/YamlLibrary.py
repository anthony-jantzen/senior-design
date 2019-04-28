import yaml

class YamlLibrary:
	def __init__(self, yaml_path):
		self.yaml_path = yaml_path

	def change_config_capture_file(self, argus_access_point, new_config_file):
		argus_config = self._open_yaml_file()
		argus_config['access_points'][argus_access_point]['capture_file'] = new_config_file
		self._write_to_yaml_file(argus_config)

	def _open_yaml_file(self):
		with open(self.yaml_path) as f:
			argus_config = yaml.load(f)
		return argus_config

	def _write_to_yaml_file(self, new_config):
		with open(self.yaml_path, 'w') as f:
			yaml.dump(new_config, f)
