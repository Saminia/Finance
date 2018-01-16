from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Frame, Label, Entry, Treeview
import numpy as np
from numpy import pv


class NPV(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.CreateUI()


    def CreateUI(self):
        self.parent.title("NPV Calculator")
        self.pack(fill=BOTH, expand=True)

        global value
        value = 0
        global ir
        ir = StringVar()
        global com
        com = StringVar()
        global var1
        var1 = StringVar()
        global var2
        var2 = StringVar()
        global res
        res = StringVar()
        global sva
        global jaz



        frame1 = Frame(self)
        frame1.pack(fill=X)

        lb1 = Label(frame1, text="Interest rate % :", width=15)
        lb1.pack(side=LEFT, padx=5, pady=5)

        ir = StringVar()
        en1 = Entry(frame1,textvariable=ir)
        en1.pack(fill=X, padx=5, expand=True)
        ir.trace("w", lambda name, index, mode, ir=ir: callback_d(self, ir))


        frame2 = Frame(self)
        frame2.pack(fill=X)

        lb2 = Label(frame2, text="Compounding :", width=15)
        lb2.pack(side=LEFT, padx=5, pady=5)

        com = StringVar()
        en2 = Entry(frame2,textvariable=com)
        en2.pack(fill=X, padx=5, expand=True)
        com.trace("w", lambda name, index, mode, com=com: callback_c(self, com))

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lb3 = Label(frame3, text="Cash Flows at:", width=15 )
        lb3.pack(side=LEFT, padx=5, pady=5)

        opt1 = ["end", "begin"]
        var1.set(opt1[0])
        m1 = OptionMenu(frame3, var1, *opt1)
        m1.pack(side=LEFT, padx=5, pady=5)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lb4 = Label(frame4, text="No. of time periods:", width=15 )
        lb4.pack(side=LEFT, padx=5, pady=5)

        opt2 = [1,2,3,4,5,6,7,8,9,10,15,18,20,25,30,35,40]
        var2.set(opt2[0])
        m2 = OptionMenu(frame4, var2, *opt2)
        m2.pack(side=LEFT, padx=5, pady=5)

        frame5 = Frame(self)
        frame5.pack(fill=X)

        lb5 = Label(frame5, text="Line", width=5)
        lb5.pack(side=LEFT, padx=5, pady=5)

        lb6 = Label(frame5, text="Time Periods", width=15)
        lb6.pack(side=LEFT, padx=5, pady=5)

        lb7 = Label(frame5, text="Cash Flows", width=15)
        lb7.pack(side=LEFT, padx=5, pady=5)
        self.sva = []
        self.svi = []

        frame7 = Frame(self)
        frame7.pack(fill=X)
        self.co = 0



        def flowat(*args):
            print(var1.get())


        def period_changed(*args):
            map(self.Treeview.delete, self.Treeview.get_children())
            self.dict_a = {}
            self.dict_b = {}

            for child in frame7.winfo_children(): child.destroy()


            for i in range(int(var2.get())):
                ii = len(self.sva)
                self.sva.append(StringVar())
                self.svi.append(StringVar())
                var = StringVar()
                self.sva[ii]=var
                vi= StringVar()
                self.svi [ii] = vi
                Label(frame7, text=(i), width=5).grid(row=i+5, column=0)
                Entry(frame7, textvariable=var, width=10).grid(row=i+5, column=1)
                Label(frame7, text=('@'), width=3).grid(row=i+5, column=2)
                Entry(frame7, textvariable=vi).grid(row=i+5, column=3)
                print(vi)
                self.sva[ii].trace("w", lambda name, index, mode, var=var,  ii=ii: callback_a(self, var, ii))
                self.svi[ii].trace("w", lambda name, index, mode,  par=vi, ii=ii: callback_b(self,par, ii))

        var1.trace("w", flowat)
        var2.trace("w", period_changed)


        def calo(*args):
            calc()
            co=0
            sumi = 0
            for k in self.dict_a:
                if k in self.dict_b:
                    for no in range(int(self.dict_a[k])):
                        co += 1
                        #pev=pv(rate=ir.get(), nper=com.get(), pmt=12, fv=self.dict_b[k], when=var1.get())
                        if var1.get() == "end":
                            pev= round(int(self.dict_b[k])/ (1+(int(ir.get())/100)/ int(com.get()))**(int(com.get())*co),2)
                        else:
                            pev= round(int(self.dict_b[k])/ (1+(int(ir.get())/100)/ int(com.get()))**(int(com.get())*(co-1)),2)
                        sumi += pev
                        self.Treeview.insert('', 'end', text=co, values=(self.dict_b[k],pev))
            self.Treeview.insert('', 'end', text='', values=('Total',round(sumi),2))




        frame30 = Frame(self)
        frame30.pack(fill=X)

        bt1 = Button(frame30, text="Calculate:", width=8, command=calo)
        bt1.pack(side=LEFT, padx=5, pady=5)

        result = Treeview(frame30)

        result.grid(row=5, column=2, columnspan=1)
        result['columns'] = ('cashflow', 'presentvalue')
        result.heading("#0", text='Period', anchor='w')
        result.column("#0", anchor="w", width=5)
        result.heading('cashflow', text='Cash Flow')
        result.column('cashflow', anchor='center', width=50)
        result.heading('presentvalue', text='Present Value')
        result.column('presentvalue', anchor='center', width=50)
        result.grid(sticky=(N, S, W, E))
        self.Treeview = result
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        result.pack(fill=X, padx=5, expand=True)


        def calc(*args):
            for child in result.get_children():
                result.delete(child)


        self.dict_a = {}
        def callback_a(self, sv ,i):
            self.dict_a[i]=sv.get()


        self.dict_b = {}
        def callback_b(self, pa ,i):
            self.dict_b[i]=pa.get()


        def callback_c(self, com):
            print(com.get())


        def callback_d(self, ir):
            print(ir.get())

    def errorMsg(self,msg):
        if msg == 'error':
            tkinter.messagebox.showerror('Error!', 'Something went wrong! Maybe invalid entries')
        #elif msg == 'divisionerror':
            #tkinter.messagebox.showerror('Division Error', 'The value of input number 2 is 0. No dividing by 0')

    def cal(self):
        try:
            self.parent.tree()
            value = self.parent.LoadTable()
            res.set(self.makeAsItIs(value))
        except:
            self.errorMsg('error')

    def makeAsItIs(self, value):
        if (value == int(value)):
            value = int(value)
        return value

def main():
    master = Tk()
    master.geometry("400x440")
    NPV(master)
    master.mainloop()

if __name__ == '__main__':
    main()

