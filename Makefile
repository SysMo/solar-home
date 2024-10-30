mir20/port-forward:
	ssh nasko@mir20.sysmo -p 7122 -L 8086:localhost:30086 -L 3000:localhost:30300  -L 1883:localhost:31883


