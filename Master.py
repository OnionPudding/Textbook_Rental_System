import pymysql
from tkinter import *
from Connection import *
import tkinter.messagebox as msgbox

class Master:
    def __init__(self):
        self.root = Tk()
        self.root.title("학생 관리")
        self.root.geometry("500x600")

        label1 = Label(self.root, text="학생 관리 서비스입니다.")
        label1.pack()

        label2 = Label(self.root, text="학생의 권한을 수정하거나, 학생을 삭제할 수 있습니다.")
        label2.pack()


        frame1 = LabelFrame(self.root, text = "권한 수정")
        frame1.pack(side = "top", fill = 'x')



        frame2 = LabelFrame(self.root, text = "학생 탈퇴")
        frame2.pack(side = "top", fill = 'x')

        button2 = Button(frame2, text = "탈퇴", command = self.expel)
        button2.pack()


        frame = Frame(self.root)
        frame.pack(side = "bottom", anchor = "w")
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox = Listbox(frame, selectmode="single", width=120, height=50, yscrollcommand=scrollbar.set)

        self.sql = "select * from student"
        c = Conn()
        rs = c.execute1(self.sql)

        i = 0
        self.id = []
        self.auth = []
        for row in rs:
            self.listbox.insert(i, row['st_ID'] + " " + row['st_name'] + " " + str(row['st_auth']))
            self.id.append(row['st_ID'])
            self.auth.append(row['st_auth'])
            i += 1

        self.listbox.pack(side = "bottom")

        scrollbar.config(command=self.listbox.yview)

        bttn1 = Button(frame1, text="권한 1 부여", command=self.fix1)
        bttn2 = Button(frame1, text="권한 2 부여", command=self.fix2)
        bttn3 = Button(frame1, text="권한 3 부여", command=self.fix3)

        bttn1.pack()
        bttn2.pack()
        bttn3.pack()

        self.root.mainloop()


    def fix1(self):
        select = self.listbox.curselection()
        num = select[0]
        st_id = self.id[num]
        c = Conn()
        sql1 = "update student set st_auth = 1 where st_ID =" + str(st_id)
        c.execute3(sql1)
        self.refresh()

    def fix2(self):
        select = self.listbox.curselection()
        num = select[0]
        st_id = self.id[num]
        c = Conn()
        sql2 = "update student set st_auth = 2 where st_ID =" + str(st_id)
        c.execute3(sql2)
        self.refresh()

    def fix3(self):
        select = self.listbox.curselection()
        num = select[0]
        st_id = self.id[num]
        c = Conn()
        sql3 = "update student set st_auth = 3 where st_ID =" + str(st_id)
        c.execute3(sql3)
        self.refresh()


    def expel(self):
        select = self.listbox.curselection()
        num = select[0]
        st_id = self.id[num]
        c=Conn()
        sql1 = "select bk_no from rentalsystem where st_ID ='"  + str(st_id) + "'"
        rs = c.execute1(sql1)

        for row in rs:
            sql1 = "update book set bk_stock = bk_stock + 1 where bk_no = " + str(row['bk_no'])
            c.execute3(sql1)


        sql2 = "delete from rentalsystem where st_ID = '" + str(st_id) + "'"
        c.execute3(sql2)


        sql3 = "delete from reservation where st_ID = '" + str(st_id) + "'"
        c.execute3(sql3)

        sql4 = "delete from student where st_ID ='" + str(st_id) + "'"
        c.execute3(sql4)

        msgbox.showinfo("알림", "정상적으로 해당 학생의 데이터를 삭제하였습니다.")
        self.refresh()











    def refresh(self):
        c = Conn()
        rs = c.execute1(self.sql)

        self.listbox.delete(0, 'end')

        i = 0
        a = []
        b = []
        for row in rs:
            self.listbox.insert(i, row['st_ID'] + " " + row['st_name'] + " " + str(row['st_auth']))
            a.append(row['st_ID'])
            b.append(row['st_auth'])
            i += 1

        self.id = a
        self.auth = b

        self.listbox.config()




if __name__ == '__main__':
    Master()