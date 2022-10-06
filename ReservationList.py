import pymysql
from Connection import *
import tkinter.messagebox as msgbox
from tkinter import *

class ReservList:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.root = Tk()
        self.root.title("PNU 산업공학과 교재 대여 시스템")
        self.root.geometry("700x300")

        c = Conn()

        label1 = Label(self.root, text=self.name + "님의 예약 목록입니다.")
        label1.pack()

        self.listbox = Listbox(self.root, selectmode="single", width=150, height=0)
        sql = "select bk_no, bk_na, bk_au, rec_date from book join (select rec_date, bk_no as b from reservation where st_id ='" + str(self.id) + "')a where bk_no = b"
        rs = c.execute1(sql)
        i = 0
        for row in rs:
            self.listbox.insert(i, str(row['bk_no']) + " " + row['bk_na'] + " " + row['bk_au'] + " " + str(
                row['rec_date']))
            i += 1

        self.listbox.pack()


        button = Button(self.root, text = "확인", command = self.exit)
        button.pack()

        self.root.mainloop()

    def exit(self):
        self.root.destroy()

if __name__ == '__main__':
    a = ReservList("201627509", "김종음")