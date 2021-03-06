import serial
import time
from tkinter import *
import random
import sys
import glob
from PIL import Image, ImageTk

i = 0
root = Tk()

# Colors
darkish = '#%02x%02x%02x' % (29, 30, 38)
whitish = '#%02x%02x%02x' % (214, 216, 218)
code_green = '#%02x%02x%02x' % (80, 200, 70)
code_green_light = '#%02x%02x%02x' % (170, 200, 150)
code_dark = '#%02x%02x%02x' % (23, 24, 30)


class sim:
    simRunning = False
    simStart = False
    exp_time = 0
    msg = ""
    msgOld = ""
    timesTen = False
    serial = None
    error_text  = Label(text="Can't connect to null", fg="red", bg=darkish)
    error_text.grid(row=21, column=4)
    updateTime = True


flightSim = sim

timesTen = False
root.minsize(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
root.configure(bg=darkish)

w = Label(root, text="BlueOrigin Flight Simulator", font='Helvetica 20 bold', bg=darkish, fg=whitish).grid(row=0, column=0, columnspan=6, padx=10)
w2 = Label(root, text="", bg=darkish).grid(row=1, column=0)
text_packet = Label(text="", bg=darkish, fg=whitish).grid(row=18, column=4)
packet_title = Label(text="Text Packet:", bg=darkish, fg=whitish).grid(row=11, column=4)
connected = False
exp_time = 0

simRunning = False
simStart = False

arduinoOutput = Label(text="Arduino Output   \n", font='Helvetica 18 bold', bg=darkish, fg=whitish).grid(row=19, column=4)


#path = "logo.png"
#img = ImageTk.PhotoImage(Image.open(path).resize((320, 100), Image.ANTIALIAS))
#panel = Label(root, image=img, borderwidth=0)
#panel.photo = img
#panel.grid(row=20,column=1)

def connect(port_name):
    sim.error_text.config(text="Connecting to "+port_name+" ...", fg="blue", bg=darkish)
    try:
        sim.serial = serial.Serial(port_name, 115200, timeout=5)  # BlueOrigin specifies 115,200 baud rate
        sim.error_text.config(text="Connected to " + port_name, fg="green", bg=darkish)

    except:
        sim.error_text.config(text="Can't connect to "+port_name, fg="red", bg=darkish)


def linearUpdate(thing, time1, time2, dist):

    timeNum = ((dist)/(time2-time1)) * 0.1
    if (flightSim.exp_time > time1 and flightSim.exp_time < time2):
        thing.set(thing.get() + timeNum)

def expUpdate(thing, time1, time2, max):

    timeNum = ((max - thing.get())/(time2-time1))
    if (flightSim.exp_time > time1 and flightSim.exp_time < time2):
        thing.set(thing.get() + timeNum)


def running():



    print(sim.serial.readline())
    msgSim = Label(root, text=flightSim.msg, font='Helvetica 18 bold', bg=code_dark,
                   fg=code_green)
    msgSim.grid(row=5, rowspan=7, column=4, sticky="n")

    msgSimOld = Label(root, text=flightSim.msg, font='Helvetica 16 italic', bg=code_dark,
                   fg=code_green_light)
    msgSimOld.grid(row=4, rowspan=7, column=4, sticky="n")

    text_packet = Label(text="", font='Helvetica 17 bold', bg=darkish, fg=code_green)
    text_packet.grid(row=12, column=4)
    expTime = Label(text="Experimental Time : " + "%.1f seconds" % flightSim.exp_time, font='Helvetica 18 bold',
                    bg=darkish, fg=whitish)

    expTime.grid(row=2, column=4)

    buffer = 0.1

    while True:
        if flightSim.timesTen and flightSim.updateTime:
            flightSim.exp_time += 1
            buffer = 1
        elif flightSim.updateTime:
            flightSim.exp_time += 0.1

        if flightSim.simStart:
            flightSim.updateTime = True
            flightSim.msg = "[0:00] Main Engine Ignition Command"
            flightSim.exp_time = 0
            time.sleep(0.5)
            flightSim.simStart = False
            altitude.set(3750)
            liftoff_warning.set(1)
            status.set('@')

        if flightSim.simRunning:

            linearUpdate(altitude, 7, 135, 142706-3650)
            linearUpdate(altitude, 135, 153, 195343-142706)
            linearUpdate(altitude, 153, 160, 215346-195343)
            linearUpdate(altitude, 160, 179, 260739-215346)
            linearUpdate(altitude, 179, 245, 328475-260739)
            linearUpdate(altitude, 179, 245, 269939-328475)
            linearUpdate(altitude, 179, 451, 23822-269939)
            linearUpdate(altitude, 451, 632, 4080-23822)

            linearUpdate(y_vel, 7, 135, 2981)
            linearUpdate(y_vel, 135, 153, 2890-2981)
            linearUpdate(y_vel, 153, 179, 2059-2890)
            linearUpdate(y_vel, 179, 245, 0-2059)
            linearUpdate(y_vel, 245, 358, 0-3323)
            linearUpdate(y_vel, 358, 632, 3300)
            linearUpdate(y_vel, 632, 650, 23)

            if flightSim.exp_time > 7 and flightSim.exp_time < (7 + buffer) :

                flightSim.msg = "[0:07] Liftoff"
                flightSim.msgOld = "[0:00] Main Engine Ignition Command"
                liftoff_warning.set(0)
                status.set('A')


            if flightSim.exp_time > 135 and flightSim.exp_time < (135  + buffer) :

                flightSim.msg = "[2:15] Max G on Ascent"
                flightSim.msgOld = "[0:07] Liftoff"
                status.set('A')

            if flightSim.exp_time > 153 and flightSim.exp_time < (153 +  buffer):

                flightSim.msg = "[2:33] Main Engine Cut Off"
                flightSim.msgOld = "[2:15] Max G on Ascent"
                status.set('B')

            if flightSim.exp_time > 160 and flightSim.exp_time < (160 + buffer ):

                flightSim.msg = "[2:40] Separate CC"
                flightSim.msgOld = "[2:33] Main Engine Cut Off"

                status.set('C')

            if flightSim.exp_time > 179 and flightSim.exp_time < (179 + buffer ):

                # Microgravity begins here

                flightSim.msg = "[2:59] Sensed Acceleration < 0.001g"
                flightSim.msgOld = "[2:40] Separate CC"

                status.set('D')
                rcs_warning.set(1)


            if flightSim.exp_time > 245 and flightSim.exp_time < (245 + buffer):

                flightSim.msg = "[4:05] Apogee"
                flightSim.msgOld = "[2:59] Sensed Acceleration < 0.001g"

                status.set('E')
                y_vel.set(0)

            if flightSim.exp_time > 307 and flightSim.exp_time < (307 + buffer):
                flightSim.msg = "[5:07] Sensed Acceleration > 0.001g"
                flightSim.msgOld =  "[4:05] Apogee"
                status.set('F')



            if flightSim.exp_time > 324 and flightSim.exp_time < (324 + buffer):
                flightSim.msg = "[5:24] Sensed Acceleration > 0.01g"
                flightSim.msgOld =  "[5:07] Sensed Acceleration > 0.001g"
                status.set('F')
                rcs_warning.set(0)


            if flightSim.exp_time > 342 and flightSim.exp_time < (342 + buffer):
                flightSim.msg = "[5:42] Sensed Acceleration > 0.1g"
                flightSim.msgOld =  "[5:24] Sensed Acceleration > 0.01g"
                status.set('F')


            if flightSim.exp_time > 358 and flightSim.exp_time < (358 + buffer):
                flightSim.msg = "[5:58] Sensed Acceleration > 1.0g"
                flightSim.msgOld =  "[5:42] Sensed Acceleration > 0.1g"
                status.set('F')


            if flightSim.exp_time > 375 and flightSim.exp_time < (375 + buffer):
                flightSim.msg = "[6:15] Max G on Reentry"
                flightSim.msgOld =  "[5:58] Sensed Acceleration > 1.0g"
                status.set('F')


            if flightSim.exp_time > 451 and flightSim.exp_time < (451 + buffer):
                flightSim.msg = "[7:31] Mortar Deploy Drogues"
                flightSim.msgOld = "[6:15] Max G on Reentry"
                chute_warning.set(1)
                status.set('G')

            if flightSim.exp_time > 527 and flightSim.exp_time < (527 + buffer):
                flightSim.msg = "[8:47] Peak Parachute Load"
                flightSim.msgOld = "[7:31] Mortar Deploy Drogues"
                chute_warning.set(0)
                status.set('G')

            if flightSim.exp_time > 632 and flightSim.exp_time < (632 + buffer):
                flightSim.msg = "[10:32] Iniate Terminal Decelerator"
                flightSim.msgOld = "[8:47] Peak Parachute Load"
                landing_warning.set(1)
                status.set('G')

            # No times specified in documentation for the below - could be variable

            if flightSim.exp_time > 655 and flightSim.exp_time < (655 + buffer):
                flightSim.msg = "[10:55] Landing"
                flightSim.msgOld = "[10:32] Iniate Terminal Decelerator"
                landing_warning.set(0)
                status.set('H')

            if flightSim.exp_time > 675 and flightSim.exp_time < (675 + buffer):
                flightSim.msg = "[11:15] Safing"
                flightSim.msgOld = "[10:55] Landing"
                status.set('I')

            if flightSim.exp_time > 700 and flightSim.exp_time < (700 + buffer):
                flightSim.msg = "[11:40] Finished"
                flightSim.msgOld = "[11:15] Safing"
                status.set('J')

            if flightSim.exp_time > 702 and flightSim.exp_time < (702 + buffer):
                flightSim.simRunning = False
                flightSim.updateTime = False



        if (flightSim.updateTime) :
            flightSim.exp_time += random.randrange(-1, 1, 1)/100  # if second decimal isn't always 0

        time.sleep(.1)  # data sent at 10Hz


        text = ('['+status.get() + "," + "%.2f," % flightSim.exp_time
                + "%.6f" % altitude.get() + ','
                + "%.6f" % x_vel.get() + ',' + "%.6f" % y_vel.get() + ',' + "%.6f" % z_vel.get() + ','
                + str(acceleration.get()) + ',\n0.000000,0.000000'

                # Attitude is orientation with respect to an inertial frame of reference
                + str(x_att.get()) + ',' + str(y_att.get()) + ',' + str(z_att.get()) + ','
                + str(x_ang_vel.get()) + ','
                + str(y_ang_vel.get()) + ','
                + str(z_ang_vel.get()) + ','
                + str(liftoff_warning.get()) + ','
                + str(rcs_warning.get()) + ','
                + str(escape_warning.get()) + ','
                + str(chute_warning.get()) + ','
                + str(landing_warning.get())
                + ',' + str(fault_warning.get())+']')

        text_packet.config(text=text)
        expTime.config(text="Experimental Time : " + "%.1f seconds" % flightSim.exp_time)
        msgSim.config(text=flightSim.msg)
        msgSimOld.config(text=flightSim.msgOld)

        if (flightSim.simRunning) :
            sim.serial.write(str.encode(text))

        root.update_idletasks()
        root.update()



#  Order of Data Fields:
status = StringVar()        # 1
# experimental time         # 2
altitude = IntVar()         # 3
x_vel = DoubleVar()         # 4
y_vel = DoubleVar()         # 5
z_vel = DoubleVar()         # 6
acceleration = DoubleVar()  # 7
# reserved                  # 8
# reserved                  # 9
x_att = DoubleVar()         # 10
y_att = DoubleVar()         # 11
z_att = DoubleVar()         # 12
x_ang_vel = DoubleVar()     # 13
y_ang_vel = DoubleVar()     # 14
z_ang_vel = DoubleVar()     # 15
liftoff_warning = IntVar()  # 16
rcs_warning = IntVar()      # 17
escape_warning = IntVar()   # 18
chute_warning = IntVar()    # 19
landing_warning = IntVar()  # 20
fault_warning = IntVar()    # 21

Label(root, text="Flight Status", font='Helvetica 16 bold', bg=darkish, fg=whitish).grid(row=2, column=0, padx=30)
Label(root, text="Warnings", font='Helvetica 16 bold', bg=darkish, fg=whitish).grid(row=2, column=1)
Label(root, text="Values", font='Helvetica 16 bold', bg=darkish, fg=whitish).grid(row=2, column=2)

c2 = Checkbutton(root, text='RCS Warning', variable=rcs_warning, bg=darkish, fg=whitish).grid(row=3, column=1, sticky='w', padx=60)

c3 = Checkbutton(root, text='Escape Warning', variable=escape_warning, bg=darkish, fg=whitish).grid(row=4, column=1, sticky='w', padx=60)

c4 = Checkbutton(root, text='Chute Warning', variable=chute_warning, bg=darkish, fg=whitish).grid(row=5, column=1, sticky='w', padx=60)

c5 = Checkbutton(root, text='Landing Warning', variable=landing_warning, bg=darkish, fg=whitish).grid(row=6, column=1, sticky='w', padx=60)

c6 = Checkbutton(root, text='Fault Warning', variable=fault_warning, bg=darkish, fg=whitish).grid(row=7, column=1, sticky='w', padx=60)

c7 = Checkbutton(root, text='Liftoff Warning', variable=liftoff_warning, bg=darkish, fg=whitish).grid(row=8, column=1, sticky='w', padx=60)

# Flight Status

R1 = Radiobutton(root, text="None Reached", variable=status, value='@', bg=darkish, fg=whitish).grid(row=3, column=0, sticky='w', padx=60)
status.set('@')

R2 = Radiobutton(root, text="Liftoff", variable=status, value='A', bg=darkish, fg=whitish).grid(row=4, column=0, sticky='w', padx=60)

R3 = Radiobutton(root, text="Meco", variable=status, value='B', bg=darkish, fg=whitish).grid(row=5, column=0, sticky='w', padx=60)

R4 = Radiobutton(root, text="Coast_Start", variable=status, value='C', bg=darkish, fg=whitish).grid(row=6, column=0, sticky='w', padx=60)

R5 = Radiobutton(root, text="Separation", variable=status, value='D', bg=darkish, fg=whitish).grid(row=7, column=0, sticky='w', padx=60)

R6 = Radiobutton(root, text="Apogee", variable=status, value='E', bg=darkish, fg=whitish).grid(row=8, column=0, sticky='w', padx=60)

R7 = Radiobutton(root, text="Coast_End", variable=status, value='F', bg=darkish, fg=whitish).grid(row=9, column=0, sticky='w', padx=60)

R8 = Radiobutton(root, text="Under_Chutes", variable=status, value='G', bg=darkish, fg=whitish).grid(row=10, column=0, sticky='w', padx=60)

R9 = Radiobutton(root, text="Landing", variable=status, value='H', bg=darkish, fg=whitish).grid(row=11, column=0, sticky='w', padx=60)

R10 = Radiobutton(root, text="Safing", variable=status, value='I', bg=darkish, fg=whitish).grid(row=12, column=0, sticky='w', padx=60)

R11 = Radiobutton(root, text="Finished", variable=status, value='J', bg=darkish, fg=whitish).grid(row=13, column=0, sticky='w', padx=60)

# Values

l1 = Label(root, text="Velocity X-Axis               ", bg=darkish, fg=whitish).grid(row=3, column=2, sticky='w')
e1 = Entry(root, text="Velocity X-Axis               ", bg=darkish, fg=whitish, textvariable=x_vel, width=4, highlightbackground=code_dark).grid(row=3, column=2, sticky='e', padx=20)
l2 = Label(root, text="Velocity Y-Axis               ", bg=darkish, fg=whitish).grid(row=4, column=2, sticky='w')
e2 = Entry(root, text="Velocity Y-Axis               ", bg=darkish, fg=whitish, textvariable=y_vel, width=4, highlightbackground=code_dark).grid(row=4, column=2, sticky='e', padx=20)
l1 = Label(root, text="Velocity Z-Axis               ", bg=darkish, fg=whitish).grid(row=5, column=2, sticky='w')
e3 = Entry(root, text="Velocity Z-Axis               ", bg=darkish, fg=whitish, textvariable=z_vel, width=4, highlightbackground=code_dark).grid(row=5, column=2, sticky='e', padx=20)
l1 = Label(root, text="Acceleration                  ", bg=darkish, fg=whitish).grid(row=6, column=2, sticky='w')
e4 = Entry(root, text="Acceleration                  ", bg=darkish, fg=whitish, textvariable=acceleration, width=4, highlightbackground=code_dark).grid(row=6, column=2, sticky='e', padx=20)
l1 = Label(root, text="Altitude                      ", bg=darkish, fg=whitish).grid(row=7, column=2, sticky='w')
e5 = Entry(root, text="Altitude                      ", bg=darkish, fg=whitish, textvariable=altitude, width=4, highlightbackground=code_dark).grid(row=7, column=2, sticky='e', padx=20)
l1 = Label(root, text="Angular Velocity X-Axis       ", bg=darkish, fg=whitish).grid(row=8, column=2, sticky='w')
e1 = Entry(root, text="Angular Velocity X-Axis       ", bg=darkish, fg=whitish, textvariable=x_ang_vel, width=4, highlightbackground=code_dark).grid(row=8, column=2, sticky='e', padx=20)
l1 = Label(root, text="Angular Velocity Y-Axis       ", bg=darkish, fg=whitish).grid(row=9, column=2, sticky='w')
e2 = Entry(root, text="Angular Velocity Y-Axis       ", bg=darkish, fg=whitish, textvariable=y_ang_vel, width=4, highlightbackground=code_dark).grid(row=9, column=2, sticky='e', padx=20)
l1 = Label(root, text="Angular Velocity Z-Axis       ", bg=darkish, fg=whitish).grid(row=10, column=2, sticky='w')
e3 = Entry(root, text="Angular Velocity Z-Axis       ", bg=darkish, fg=whitish, textvariable=z_ang_vel, width=4, highlightbackground=code_dark).grid(row=10, column=2, sticky='e', padx=20)
l1 = Label(root, text="Attitude X-Axis               ", bg=darkish, fg=whitish).grid(row=11, column=2, sticky='w')
e1 = Entry(root, text="Attitude X-Axis               ", bg=darkish, fg=whitish, textvariable=x_att, width=4, highlightbackground=code_dark).grid(row=11, column=2, sticky='e', padx=20)
l1 = Label(root, text="Attitude Y-Axis               ", bg=darkish, fg=whitish).grid(row=12, column=2, sticky='w')
e2 = Entry(root, text="Attitude Y-Axis               ", bg=darkish, fg=whitish, textvariable=y_att, width=4, highlightbackground=code_dark).grid(row=12, column=2, sticky='e', padx=20)
l1 = Label(root, text="Attitude Z-Axis               ", bg=darkish, fg=whitish).grid(row=13, column=2, sticky='w')
e3 = Entry(root, text="Attitude Z-Axis               ", bg=darkish, fg=whitish, textvariable=z_att, width=4, highlightbackground=code_dark).grid(row=13, column=2, sticky='e', padx=20)

output = Frame(root, width=600, height=150, bg=code_dark).grid(row=20, column=4, sticky='e', padx=20)

info = Frame(root, width=600, height=150, bg=code_dark).grid(row=2, rowspan=7, column=4, sticky='e', padx=20)
msg = Label(root, text="", font='Helvetica 18 bold', bg=darkish, fg=whitish).grid(row=2, rowspan=7, column=4, sticky='e', padx=20)
# display everything

root.title("BlueOrigin FlightSim")

top = root.winfo_toplevel()
menuBar = Menu(top)
top['menu'] = menuBar
subMenu = Menu(menuBar)
portMenu = Menu(menuBar)

def normalSpeed():
    flightSim.timesTen = False


def timesTen():
    flightSim.timesTen = True


def runSimulation():

    flightSim.simRunning = True
    flightSim.simStart = True


menuBar.add_cascade(label='Representative Flight Simulation', menu=subMenu)
subMenu.add_command(label='Run Simulation', command=runSimulation)
subMenu.add_command(label='x10 Speed', command=timesTen)
subMenu.add_command(label='Regular Speed', command=normalSpeed)

menuBar.add_cascade(label='Ports', menu=portMenu)

if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)] #checks windows ports
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    ports = glob.glob('/dev/tty[A-Za-z]*') #checks for anything starting with /dev/tty
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Your platform is not supported')

for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        if (sys.platform.startswith('win)')) :
            portMenu.add_command(label=port, command = connect(port))
        else :
            portMenu.add_command(label=port)
    except (OSError, serial.SerialException):
        pass

connect("/dev/cu.usbmodem1421")

#create window for viewing

timesTen = False


running()



