import tkinter as tk 
from time import strftime 

root = tk.Tk()
root.title("Digital Clock")

def time():
    string_time = strftime('%I:%H:%M:%S %p')
    label.config(text=string_time) 
    label.after(1000, time) 

label = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
label.pack(anchor='center')
time()
root.mainloop()