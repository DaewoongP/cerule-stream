import paho.mqtt.client as paho
import ptz.ptz
 
move = ptz.ptz.move()

class cam:
    def size(self, Tw, Th):#bounding box's size return
        size = Tw * Th
        print(size)
        return size

    def delta(self, Cx, Cy, lx, ly):#camera
        dx = Cx - lx
        dy = Cy - ly

        #center vs camera point
        if (Cx != lx):
            (dx-320)/64+12
                
        if (Cy != ly):
            tilt.ChangeDutyCycle((dy-240)/48+12)


class app:
    def on_moveX(object, userdata, msg):
        a = int(str(msg.payload)[2:4])
        print(a)
        
        if (a >= 0): #App's key >
            move.right(a)
            
        if (a <= 0): #App's key <
            move.left(10)
        
    def on_moveY(object, userdata, msg):
        a = int(str(msg.payload)[2:4])
        print(a)
        
        if (a >= 0): #App's key ^
            move.up(a)
            
        if (a <= 0): #App's key v
            move.down(10)
        
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        #size = int(str(msg.payload)[2:3])

<<<<<<< Updated upstream
    def on_size(object, userdata, msg):
        a = int(str(msg.payload)[2:4])
        print(a)

    def on_delta(object, userdata, msg):
        a = int(str(msg.payload)[2:4])
        print(a)
    client = paho.Client()#...

    client.message_callback_add("mqtt/size", on_size)#callback to function
    client.message_callback_add("mqtt/delta", on_delta)
    client.message_callback_add("mqtt/message", on_message)
    client.message_callback_add("mqtt/moveX", on_moveX)
    client.message_callback_add("mqtt/moveY", on_moveY)

    client.connect("localhost", 1883)#broker set
    client.subscribe("mqtt/#")#sub 'ptz'

    client = paho.Client()  #...
    client.message_callback_add("app/moveX", on_moveX)
    client.message_callback_add("app/moveY", on_moveY)

    client.connect("localhost", 1883)  #broker set
    client.subscribe("app/#")  #sub 'ptz'

    client.loop_forever()


