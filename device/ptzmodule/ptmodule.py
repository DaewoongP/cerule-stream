import json
import paho.mqtt.client as paho
import ptzmodule.ptz.ptz
 
move = ptzmodule.ptz.ptz.move()

class bbox:
    def size(self, userdata, msg):
        box= str(msg.payload.decode("utf-8", "ignore"))
        #print(type(box)) # mqtt sub type
        box = json.loads(box)
        #print(type(box)) # json load type

        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        object_name = box[4]
        
        w = x2 - x1
        h = y2 - y1
        size = w * h
        print("box name :",object_name)
        print("size :",size)

    def delta(self, userdata, msg):#camera
        lx = 320
        ly = 240
        
        box= str(msg.payload.decode("utf-8", "ignore"))
        box = json.loads(box)

        x1 = box[0]
        y1 = box[1]
        x2 = box[2]
        y2 = box[3]
        
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        dx = cx - lx
        dy = cy - ly

        if (cx >= 640):
            cx = 320
        elif (cx <= 0):
            cx = 320
        elif (cy >= 480):
            cy = 240
        elif (cy <= 0):
            cy = 240
        else:
            print("centerX :",cx)
            print("centerY :",cy)

        
        #center vs camera point
        if (cx != lx):
            if (dx >= 0):
                move.x(dx)
            if (dx <= 0):
                move.x(dx)

        if (cy != ly):
            if (dy >= 0):
                move.y(dy)
            if (dy <= 0):
                move.y(dy)

    client = paho.Client()#...

    client.message_callback_add("bbox/size", size)#callback to function
    client.message_callback_add("bbox/delta", delta)

    client.connect("localhost", 1883)#broker set
    client.subscribe("bbox/#")#sub 'ptz'

    client.loop_forever()


class app:
    def on_moveX(object, userdata, msg):
        t = len(msg.payload)
        a = int(str(msg.payload)[2:2 + t])
        print(a)
        if (a >= 0): #App's key >
            move.right(a)
            
        if (a <= 0): #App's key <
            move.left(a)
        
    def on_moveY(object, userdata, msg):
        t = len(msg.payload)
        a = int(str(msg.payload)[2:2 + t])
        print(a)
        
        if (a >= 0): #App's key ^
            move.up(a)
            
        if (a <= 0): #App's key v
            move.down(a)

    client = paho.Client()#...
    client.message_callback_add("app/moveX", on_moveX)
    client.message_callback_add("app/moveY", on_moveY)

    client.connect("localhost", 1883)#broker set
    client.subscribe("app/#")#sub 'ptz'

    client.loop_forever()
