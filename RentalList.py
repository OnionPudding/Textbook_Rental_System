import pymysql
from Connection import *
import tkinter.messagebox as msgbox
from tkinter import *

class RentalList:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.root = Tk()
        self.root.title("PNU 산업공학과 교재 대여 시스템")
        self.root.geometry("700x300")

        c = Conn()

        label1 = Label(self.root, text=self.name + "님의 대출 목록입니다.")
        label1.pack()

        self.sql1 = "select count(*) as cn from rentalsystem where st_ID =" + str(self.id)
        rs2 = c.execute2(self.sql1)
        self.a_no = rs2['cn']
        self.label2 = Label(self.root, text= "총 " + str(self.a_no) + "권을 대여하셨습니다.")
        self.label2.pack()

        frame = Frame(self.root)
        frame.pack()

        button1 = Button(frame, text="반납하기", command=self.returnbook)
        button1.pack(side = "left")

        button2 = Button(frame, text="연장하기", command=self.extendbook)
        button2.pack(side = "right")

        self.listbox = Listbox(self.root, selectmode="single", width=150, height=0)
        self.sql2 = "SELECT b, bk_na, bk_au, rt_no, rt_date, ru_date from (SELECT b.bk_no as b, bk_na, bk_au, rt_no, rt_date, ru_date, st_ID from book as b join rentalsystem where b.bk_no = rentalsystem.bk_no)a where st_ID = " + str(self.id)
        rs = c.execute1(self.sql2)
        i = 0
        self.bk_no = []
        self.rt_no = []
        for row in rs:
            self.listbox.insert(i, str(row['b']) + " " + row['bk_na'] + " " + row['bk_au'] + " " + str(
                row['rt_date']) + " "+ str(row['ru_date']))
            self.bk_no.append(row['b'])
            self.rt_no.append(row['rt_no'])
            i += 1

        self.listbox.pack()

        self.root.mainloop()


    def returnbook(self):
        select = self.listbox.curselection()
        num = select[0]
        bk_no = self.bk_no[num]

        c = Conn()
        sql1 = "delete from rentalsystem where bk_no = " + str(bk_no) + " and st_ID = '" + str(self.id) + "'"
        c.execute3(sql1)
        sql2 = "update book set bk_stock = bk_stock + 1 where bk_no = " + str(bk_no)
        c.execute3(sql2)
        msgbox.showinfo("알림", "정상적으로 반납이 완료 되었습니다.")
        self.refresh()

    def extendbook(self):
        select = self.listbox.curselection()
        num = select[0]
        rt_no = self.rt_no[num]

        c = Conn()

        sql1 = "select et_nt from rentalsystem where rt_no =" + str(rt_no)
        rs = c.execute2(sql1)
        et_nt = int(rs['et_nt'])
        if et_nt == 0:
            sql2 = "update rentalsystem set et_nt = 1, ru_date = date_add(ru_date, interval 7 day) where rt_no = " + str(rt_no)
            c.execute3(sql2)

            msgbox.showinfo("알림", "정상적으로 연장되었습니다.")
            self.refresh()
        else:
            msgbox.showerror("에러", "연장횟수를 초과하셨습니다.")



        c = Conn()
        sql1 = "select rt_amount from rentalsystem where "

    def refresh(self):
        c = Conn()
        rs2 = c.execute2(self.sql1)
        self.a_no = rs2['cn']
        self.label2.config(text= "총 " + str(self.a_no) + "권을 대여하셨습니다.")


        self.listbox.delete(0, 'end')
        rs = c.execute1(self.sql2)
        i = 0
        b = []
        for row in rs:
            self.listbox.insert(i, str(row['b']) + " " + row['bk_na'] + " " + row['bk_au'] + " " + str(
                row['rt_date']) + " " + str(row['ru_date']))
            b.append(row['b'])
            i += 1

        self.bk_no = b
        self.listbox.config()





if __name__ == '__main__':
    a = RentalList(1111, "master")
