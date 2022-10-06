from tkinter import *
import pymysql
import tkinter.messagebox as msgbox
from PersonalPage import Personal

class Login:

    def __init__(self):
        self.root = Tk()
        self.root.title("로그인")
        self.root.geometry("280x200")

        self.stid = None
        self.stname = None


        frame1 = LabelFrame(self.root)
        frame1.pack()
        frame2 = LabelFrame(self.root)
        frame2.pack()

        label1 = Label(frame1, text="학번", width=5)
        label1.pack(side="left")
        label2 = Label(frame2, text="이름", width=5)
        label2.pack(side="left")

        self.e1 = Entry(frame1, width=15)
        self.e1.pack()

        self.e2 = Entry(frame2, width=15)
        self.e2.pack()

        self.event = 0

        lgbttn = Button(self.root, text = "로그인", command=self.login)
        lgbttn.pack()


        self.root.mainloop()

    def login(self):
        conn = pymysql.connect(host='180.69.111.99', user='dbterm5095', password='wlstjd5095**', db='ptype')
        curs = conn.cursor()

        self.stid = self.e1.get()
        self.stname = self.e2.get()
        sql = "select * from student where st_ID = %s and st_name = %s"
        curs.execute(sql, (self.stid, self.stname))
        rs = curs.fetchall()

        if len(rs) == 0:
            msgbox.showinfo("경고", "존재하지 않는 계정입니다.")
        else:
            msgbox.showinfo("로그인 성공", self.stname + "님 환영합니다.")
            self.root.destroy()
            Personal(self.stid, self.stname)







if __name__ == '__main__':
    a = Login()



