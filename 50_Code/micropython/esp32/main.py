from smbed.services import Runtime

runtime = Runtime.from_config_file('config.json')
runtime.start()
