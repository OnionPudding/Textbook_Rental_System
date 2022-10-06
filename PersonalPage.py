from tkinter import *
from Connection import *
from RentalList import *
from ReservationList import *
from Master import *
import tkinter.messagebox as msgbox

class Personal:
    def __init__(self, id, name):
        self.root = Tk()
        self.root.title("PNU 산업공학과 교재 대여 시스템")
        self.root.geometry("700x600")

        self.stid = id
        self.name = name
        c = Conn()

        sql1 = "select st_auth from student where st_ID = " + str(self.stid)
        rs1 = c.execute2(sql1)
        self.auth = rs1['st_auth']




        label1 = Label(self.root, text=self.name + "님 환영합니다.")
        label1.pack()

        sql2 = "select count(*) as cn from rentalsystem where st_ID =" + str(self.stid)
        rs2 = c.execute2(sql2)
        self.a_no = 5 - rs2['cn']
        self.label2 = Label(self.root, text= "대여하실 수 있는 책은 총 " + str(self.a_no) + "권입니다.")
        self.label2.pack()

        frame1 = Frame(self.root)
        frame1.pack()



        button0 = Button(frame1, text="대출 내역 확인", command = self.rentallist)
        button1 = Button(frame1, text="예약 내역 확인", command = self.reservlist)
        button2 = Button(frame1, text="대출하기", command = self.rental)
        button3 = Button(frame1, text="기증하기", command = self.donate)
        button4 = Button(frame1, text="학생관리", command = self.master)
        button5 = Button(frame1, text= "로그아웃", command = self.logout)



        button0.pack(side = "left")
        button1.pack(side = "left")
        button2.pack(side = "left")

        if self.auth == 3 or 1:
            button3.pack(side = "left")

        if self.auth == 1:
            button4.pack(side = "left")

        button5.pack(side = "left")

        frame2 = Frame(self.root)
        frame2.pack()

        scrollbar = Scrollbar(frame2)
        scrollbar.pack(side = "right", fill = "y")

        self.listbox = Listbox(frame2, selectmode="single", width=120, height=50, yscrollcommand = scrollbar.set)


        sql1 = "SELECT bk_no, bk_na, bk_au, bk_stock from book"
        rs = c.execute1(sql1)
        i = 0
        for row in rs:
            self.listbox.insert(i, str(row['bk_no']) + " " + row['bk_na'] + " " + row['bk_au'] + " " + str(
                row['bk_stock']))
            i += 1
        self.listbox.pack()

        scrollbar.config(command = self.listbox.yview)

        self.root.mainloop()

    def rental(self):
        c = Conn()
        if self.a_no > 0 :
            select = self.listbox.curselection()
            bk_no = select[0] + 1001
            st_history = []

            sql = "select bk_no from rentalsystem where st_ID = '" + str(self.stid) +"'"
            rs = c.execute1(sql)
            for row in rs:
                st_history.append(int(row['bk_no']))

            for row in st_history:
                if bk_no == row:
                    msgbox.showerror("경고", "이미 해당 서적은 대출하셨습니다.")
                    return




            sql0 = "select bk_stock from book where bk_no =" + str(bk_no)
            rs = c.execute2(sql0)
            bk_stock = rs['bk_stock']

            if bk_stock >= 1:
                sql1 = "select max(rt_no) as max from rentalsystem"
                rs = c.execute2(sql1)
                rt_no = rs['max'] + 1

                sql2 = "insert into rentalsystem values(" + str(
                    rt_no) + ", 1, sysdate(), date_add(sysdate(), interval 7 day), 0, '" + str(
                    self.stid) + "', " + str(bk_no) + ", '" + str(self.stid) + "', " + str(bk_no) + ")"
                c.execute3(sql2)
                sql3 = "update book set bk_stock = bk_stock - 1 where bk_no = " + str(bk_no)
                c.execute3(sql3)
                msgbox.showinfo("알림", "정상적으로 대출되었습니다.")
                self.refresh()

            else:
                reserv = msgbox.askquestion("알림", "대출 가능한 서적이 존재하지 않습니다. 해당 도서를 예약하시겠습니까?")
                if reserv == 'yes':
                    self.reservation()


        else:
            msgbox.showerror("경고", "최대 대출 권수를 초과하셨습니다.")


    def refresh(self):
        c = Conn()
        sql2 = "select count(*) as cn from rentalsystem where st_ID =" + str(self.stid)
        rs2 = c.execute2(sql2)
        self.a_no = 5 - rs2['cn']
        self.label2.config(text= "대여하실 수 있는 책은 총 " + str(self.a_no) + "권입니다.")

        self.listbox.delete(0, 'end')
        sql1 = "SELECT bk_no, bk_na, bk_au, bk_stock from book"
        rs = c.execute1(sql1)
        i = 0
        for row in rs:
            self.listbox.insert(i, str(row['bk_no']) + " " + row['bk_na'] + " " + row['bk_au'] + " " + str(
                row['bk_stock']))
            i += 1
        self.listbox.config()


    def donate(self):
        c = Conn()
        select = self.listbox.curselection()
        bk_no = select[0] + 1001
        sql1 = "update book set bk_stock = bk_stock + 1 where bk_no = " + str(bk_no)
        c.execute3(sql1)
        msgbox.showinfo("알림", "기증해주셔서 감사합니다!")
        self.refresh()

    def rentallist(self):
        RentalList(self.stid, self.name)

    def reservlist(self):
        ReservList(self.stid, self.name)


    def reservation(self):
        c = Conn()
        select = self.listbox.curselection()
        bk_no = select[0] + 1001
        sql = "select count(re_no) as c from reservation where Student_st_ID = " + str(self.stid)
        rs = c.execute2(sql)
        num = rs['c']

        if num > 5:
            msgbox.showerror("경고", "최대 예약 권수를 초과하셨습니다.")
        else:
            sql0 = "select rt_no, min(ru_date), et_nt from rentalsystem where bk_no =" + str(bk_no)
            rs = c.execute2(sql0)
            rt_no = rs['rt_no']
            et_nt = rs['et_nt']
            ru_date = rs['min(ru_date)']

            if et_nt == 0:
                sql1 = "update rentalsystem set et_nt = 1 where rt_no =" + str(rt_no)
                c.execute3(sql1)

            sql2 = "select max(re_no) as m from reservation"
            rs = c.execute2(sql2)
            re_no = int(rs['m']) + 1
            sql3 = "insert into reservation values(" + str(re_no) + ", sysdate(), '" + str(ru_date) + "', '" + str(self.stid) + "', " + str(bk_no) + ", " + str(bk_no) + ", '" + str(self.stid) + "')"
            c.execute3(sql3)
            msgbox.showinfo("알림", "예약이 완료되었습니다.")

    def master(self):
        Master()


    def logout(self):
        self.root.destroy()
        from Start import Start
        Start()













if __name__ == '__main__':
    a = Personal(1111, "")
