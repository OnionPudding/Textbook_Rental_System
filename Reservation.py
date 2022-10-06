from tkinter import *
import pymysql
import tkinter.messagebox as msgbox

class Reservation:
    def __init__(self, id, name):
        self.root = Tk()
        self.root.title("PNU 산업공학과 교재 대여 시스템")
        self.root.geometry("700x600")

        self.stid = id
        self.name = name

        label1 = Label(self.root, text= self.stid + "님 환영합니다.")
        label1.pack()

        bttn1 = Button(self.root, )

        listbox = Listbox(root, selectmode="extended", width=150, height=0)


        connection1 = pymysql.connect(host='180.69.111.99', user='dbterm5095', password='wlstjd5095**', db='ptype')
        try:
            with connection1.cursor() as cursor:
                sql = "SELECT bk_no, bk_na, bk_au, pb_year, bk_stock from book"
                cursor.execute(sql)
                rs = cursor.fetchall()
                i = 0

                for row in rs:
                    listbox.insert(i, row)
                    i += 1

        finally:
            connection1.close

        listbox.pack()




        self.root.mainloop()


if __name__ == '__main__':
    a = Reservation()