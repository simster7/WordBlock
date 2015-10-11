from tkinter import *
import SubjectContext as sc
class App:
    
    def __init__(self, master):

        optimal, secondary = [], []

        frame = Frame(master)
        frame.grid()

        self.label = Label(frame, text="Enter subject:")
        self.label.grid(row=0, column=0)

        self.sub = Entry(frame, width=20)
        self.sub.grid(row=0, column=1)

        self.label2 = Label(frame, text="Enter word to replace:")
        self.label2.grid(row=1, column=0)

        self.rep = Entry(frame, width=20)
        self.rep.grid(row=1, column=1)
        
        self.opt = Label(frame, text="Optimal words:")
        self.opt.grid(row=2, column=0)

        self.opt_w = Text(frame, height=20, width=30)
        self.opt_w.grid(row=3, column=0)

        self.sec = Label(frame, text="Secondary words:")
        self.sec.grid(row=2, column=1)

        self.sec_w = Text(frame, height=20, width=30)
        self.sec_w.grid(row=3, column=1)

        def search(context, word):
            subject = sc.SubjectContext(context)
            optimal, secondary = subject.get(word)
            self.opt_w.delete('1.0', END)
            self.opt_w.insert(END, '\n'+'\n'.join(optimal))
            self.sec_w.delete('1.0', END)
            self.sec_w.insert(END, '\n'+'\n'.join(secondary))

        self.find = Button(frame, text="Fuck", command=lambda: search(self.sub.get(), self.rep.get()))
        self.find.grid(row=1, column=2)


root = Tk()
app = App(root)
root.mainloop()
