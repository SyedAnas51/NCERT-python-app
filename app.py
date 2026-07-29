"""
@Author: Pranta Sarker
Institute: North East University Bangladesh
Language: Python
Version: 3.x
"""

from tkinter import *
from tkinter import messagebox
from calculator import is_number, casting, add, subtract, multiply, divide


def actionauthor():
    messagebox.showinfo("Author", "Pranta Sarker\nBatch: 6th\nDepartment: CSE\nNorth East University Bangladesh")


def _run_operation(label_text, fg, bg, op_func):
    Showtemplabel.delete(0, END)
    Showlabel.delete(0, END)

    Showtemplabel.config(fg=fg, bg=bg)
    Showtemplabel.insert(0, label_text)
    Showtemplabel.place(relx=0.5, rely=0.5, anchor='center')

    ans = "0"
    Showlabel.insert(0, ans)
    Showlabel.place(relx=0.5, rely=0.6, anchor='center')

    num1 = Numberentry1.get()
    num2 = Numberentry2.get()

    if is_number(num1) and is_number(num2):
        num1 = casting(num1)
        num2 = casting(num2)
        try:
            ans = str(op_func(num1, num2))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero")
            return

        Showtemplabel.delete(0, END)
        Showlabel.delete(0, END)
        Showtemplabel.config(fg=fg, bg=bg)
        Showtemplabel.insert(0, label_text)
        Showtemplabel.place(relx=0.5, rely=0.5, anchor='center')
        Showlabel.insert(0, ans)
        Showlabel.place(relx=0.5, rely=0.6, anchor='center')
    else:
        messagebox.showerror("Error", "Enter a Valid number\ne.g. 123, 0.123, .123, -0.123, 123.456")


def actionPlus():
    _run_operation('Summation', 'red', '#9ed8ee', add)


def actionMinus():
    _run_operation('Subtraction', 'green', '#ece7e2', subtract)


def actionMul():
    _run_operation('Multiplication', 'blue', '#cacba9', multiply)


def actionDiv():
    _run_operation('Division', 'yellow', '#8dad96', divide)


if __name__ == "__main__":
    root = Tk()
    root.title('My First Python Calculator')
    root.geometry('380x300+200+250')
    Titlelabel = Label(root, fg='green', font='none 10 bold underline', text='Python Calculator', compound=CENTER)
    Titlelabel.place(relx=0.5, rely=0.1, anchor='center')
    Showlabel = Entry(root)
    Showtemplabel = Entry(root)
    Numberentry1 = Entry(root)
    Numberentry2 = Entry(root)
    Numberentry1.place(relx=0.5, rely=0.3, anchor='center')
    Numberentry2.place(relx=0.5, rely=0.4, anchor='center')

    plusbutton = Button(root, text="+", width=5, command=actionPlus)
    plusbutton.place(relx=0.1, rely=0.7)

    minusbutton = Button(root, text="-", width=5, command=actionMinus)
    minusbutton.place(relx=0.3, rely=0.7)

    mulbutton = Button(root, text="*", width=5, command=actionMul)
    mulbutton.place(relx=0.5, rely=0.7)

    divbutton = Button(root, text="/", width=5, command=actionDiv)
    divbutton.place(relx=0.7, rely=0.7)

    authorbutton = Button(root, text='Author', width=6, command=actionauthor)
    authorbutton.place(relx=0.5, rely=0.95, anchor='center')

    root.resizable(False, False)
    root.mainloop()
