PYTHON_VER=3.12
VENV_PATH:= ${PWD}/venv
LIB_PATH = ${PWD}/smbed

venv/install_pkgs:
	/bin/bash -c "source $(VENV_PATH)/bin/activate && pip install -r requirements.txt"
	
venv/create:
	python3 -m venv $(VENV_PATH)

venv/add_lib_path:
	echo ${LIB_PATH} > venv/lib/python$(PYTHON_VER)/site-packages/smo.pth

setup: venv/create venv/install_pkgs venv/add_lib_path

# DEV=/dev/ttyACM0
DEV=/dev/ttyUSB0

upython/firmware:
	esptool.py --chip esp32c3 --port ${DEV} erase_flash
	esptool.py --chip esp32c3 --port ${DEV} --baud 921600 write_flash -z 0x0 scratch/ESP32_GENERIC_C3-20241025-v1.24.0.bin

upython/connect:
	mpremote connect ${DEV}

upython/ls:
	mpremote fs ls

upython/clean:
	mpremote run smbed/tools/cleanup.py

upython/mkdirs:
	mpremote fs mkdir /cert
	
# upython/install_pkgs:
# 	mpremote run tools/install_pkgs.py

upython/install_pkgs:
	mpremote connect /dev/ttyUSB0 mip install logging
	mpremote connect /dev/ttyUSB0 mip install 'github:brainelectronics/micropython-modbus'
	
upython/upload:
	mpremote fs cp -rf smbed :/
	mpremote fs cp main.py :/
	mpremote fs cp config.json :/
	# mpremote fs cp /data/Workspace/Hynergy/hyboard/cert/out/ca/ca-sysmo.crt :/cert/ca.crt
	# mpremote fs cp /data/Workspace/Hynergy/hyboard/cert/out/client/sysmo.crt :/cert/sysmo.crt
	# mpremote fs cp /data/Workspace/Hynergy/hyboard/cert/out/client/sysmo.key :/cert/sysmo.key

	mpremote reset
	mpremote repl

upython/repl:
	mpremote repl

