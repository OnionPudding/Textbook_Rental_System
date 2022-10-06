from tkinter import *
from Join import Join
from Login import Login

class Start:

    def __init__(self):
        self.root = Tk()
        self.root.title("PNU 산업공학과 교재 대여 시스템")
        self.root.geometry("450x280")

        self.stid = None
        self.stname = None

        self.label1 = Label(self.root, text="PNU 산업공학과 교재 대여 시스템을 이용해주셔서 감사합니다.")
        self.label2 = Label(self.root, text="서비스 이용을 위해 로그인해주세요. 계정이 없으실시 회원가입을 해주세요.")
        self.label1.pack()
        self.label2.pack()

        frame = Frame(self.root)
        frame.pack()

        btn1 = Button(frame, text="회원가입", command=self.gojoin)
        btn1.pack(side = "left")

        btn2 = Button(frame, text="로그인", command=self.gologin)
        btn2.pack(side = "right")


        self.root.mainloop()


    def gojoin(self):
        Join()

    def gologin(self):
        self.root.destroy()
        Login()




if __name__ == '__main__':
    a = Start()





























