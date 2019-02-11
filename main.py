# coding=utf-8
from login import *
file_no = '5.1'
ADDR=('39.108.82.241',8888)
# ADDR=('127.0.0.1',8888)
root = Tk()
root.title('小程序')
Login_page(root,ADDR,file_no)
root.mainloop()
