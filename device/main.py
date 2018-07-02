import pantilt

import mqtt.client

def move_x(obj, asdf, msg):
	value = msg.payload
	pantilt.x(value)

cli = Clint()

cli.add_callback("ptz/x", move_x)
