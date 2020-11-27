 # This project requires PyBluez
from tkinter import *
import bluetooth
import time
global o,current
current=[0,0]
o=1
#-------------------------------------------------------------------------------------------------------------

#------------------------------------configure---------------------------------------------------------
f_step= 0.5                                                                                      #-----
b_step= 0.5                                                                                      #-----
r_step= 1                                                                                    #------  
l_step= 1                                                                                    #------
#-------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#Look for all Bluetooth devices
#the computer knows about.
print("Searching for devices...")
print("")
#Create an array with all the MAC
#addresses of the detected devices
nearby_devices = bluetooth.discover_devices()
#Run through all the devices found and list their name
num = 0
print("Select your device by entering its coresponding number...")
for i in nearby_devices:
	num+=1
	print(num , ": " , bluetooth.lookup_name( i ))

#Allow the user to select their Arduino
#bluetooth module. They must have paired
#it before hand.
selection = int(input("> ")) - 1
print("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]
l=[bd_addr]
print(l)

port = 1
#________________________________________________________________________________________________________________
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr,1))
sock.send("F")
time.sleep(1)
sock.send("B")
time.sleep(1)
sock.send("D")
#_________________________________________________________________________________________________________________
def f():
        sock.send("F")
        time.sleep(f_step)
        sock.send("D")
def b():
        sock.send("B")
        time.sleep(b_step)
        sock.send("D")
def r():
        global o
        o=o-1
        sock.send("R")
        time.sleep(r_step)
        sock.send("D")
def l():
        global o
        o=o+1
        sock.send("L")
        time.sleep(l_step)
        sock.send("D")
#_______________________________________________________________________
def Y_AXIS(x):
        if x>0:
                for i in range(x):
                        f()
                        time.sleep(1)
        if x<0:
                for i in range(-x):
                        b()
                        time.sleep(1)
        if x==0:
                pass
def X_AXIS(x):
        if x>0:
                r()
                time.sleep(1)
                Y_AXIS(x)

        if x<0:
                l()
                time.sleep(1)
                Y_AXIS(-x)
        if x==0:
                pass
def direction():
        global o
        if o%4==2:
                while not(o%4==1):
                        r()
        if (o%4==3 or o%4==0):
                while not(o%4==1):
                        l()
        
#______________________________________________________________________________________
def done():
        global current
        l=eval(g.get())
        c=current
        vertical=int(l[1] - c[1])
        horizontal=int(l[0] - c[0])
        Y_AXIS(vertical)
        X_AXIS(horizontal)
        time.sleep(1)
        direction()
        print(vertical,horizontal)
        current=(l)
        g.set("")
        s.set(current)
def home():
        g.set("[0,0]")
        done()
#_______________________________________________________________________________________________
if __name__=="__main__":
        gui=Tk()
        gui.configure(background="sky blue")
        gui.title("PSEUDO GPS")
        gui.geometry("600x300")
        global current
        #__________________________________________________________________________________________
        heading=Label(gui,text="PGPS",font=('broadway',30),bg="sky blue").pack()
        label1=Label(gui,text="CURRENT",bg="sky blue",font=('broadway')).place(x=100,y=100)
        s=StringVar()
        entrybox1=Entry(gui,textvariable=s,width=25,bg="orange").place(x=100,y=120)
        s.set(str(current))
        label2=Label(gui,text="GOTO",bg="sky blue",font=('broadway')).place(x=300,y=100)
        g=StringVar()
        entrybox2=Entry(gui,textvariable=g,width=25,bg="orange").place(x=300,y=120)
        #_________________________________________________________________________________________
        button1=Button(gui,text='HOME',command=home).place(x=100,y=200)
        button2=Button(gui,text='DONE',command=done).place(x=300,y=200)
        gui.mainloop()
#________________________________________________________________________________________

