import tkinter as tk

root = tk.Canvas(width=800,height=600)
root.pack()

x = 0
y = 300
a = 50

#pomalsie moznost
#def stvorec():
#    global x,y
#    root.delete("all")
#    root.create_rectangle(x,y,x+a,y+a,fill="#ff0000")
#    x+=50
#    root.update()
#    root.after(200, stvorec)
#
#stvorec()

daco = root.create_rectangle(x,y,x+a,y+a,fill="#ff0000")
def daco():
    root.move(daco, 10, 10)
    

daco()

root.mainloop()
