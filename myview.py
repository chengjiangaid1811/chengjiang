from tkinter import *
from tkinter.messagebox import *
import sys
import time
from socket import *
from tkinter import ttk
from random import randint


class Do_random(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_page()

    def create_page(self):
        def dorandom():
            no = randint(start.get(), end.get())
            Label(self, text='恭喜 %s 号同学！！' % no, pady='50', font=('Calibri', 30)).grid(row=4, column=1, columnspan=3)

        start = IntVar()
        end = IntVar()
        start.set(1)
        end.set(17)
        Label(self, pady='10').grid(row=0, column=1)
        Label(self, text='随机起始值', pady='10').grid(row=1, column=1)
        Label(self, text='随机终止值', pady='10').grid(row=2, column=1)
        Entry(self, textvariable=start).grid(row=1, column=2)
        Entry(self, textvariable=end).grid(row=2, column=2)
        Button(self, text='随机选个号', command=dorandom, pady='30', font=('Calibri', 12)).grid(row=3, column=1)


class InputFrame(Frame):
    def __init__(self, master, s,name):
        Frame.__init__(self, master)
        self.s = s
        self.create_page(s,name)


    def create_page(self,s,name1):
        name = StringVar()
        name.set('录入者:%s'%name1)
        type = StringVar()
        type.set('--输入新的类型--')
        data1 = 'A'
        s.send(data1.encode())
        data2 = s.recv(1024).decode()
        list1 = data2.split('##')

        def save(s):
            nonlocal list1
            type1 = c.get()
            if type1 == '--输入新的类型--':
                showerror('error', '请选择题目类型...')
                return
            ask = t1.get(1.0, END)
            answer = t2.get(1.0, END)
            data = 'S##%s##%s##%s##%s' % (type1, name1, ask, answer)
            s.send(data.encode())
            data = s.recv(128).decode()
            if data == 'OK':
                showinfo('感谢您','题目上传成功！')
                t1.delete(1.0, END)
                t2.delete(1.0, END)
                # type.set('--输入新的类型--')
                if type1 not in list1:
                    data1 = 'A'
                    s.send(data1.encode())
                    data2 = s.recv(1024).decode()
                    list1 = data2.split('##')
                    c['values'] = list1
            else:
                showerror('有bug！','%s'%data)

        def create_type():
            showinfo('额','把左边类型栏内容删除写上新东西即可...\n ps:新类型重启软件后下拉菜单可见')

        t1 = Text(self, height=5, width=80)
        t1.grid(row=2, columnspan=4)
        t1.insert(INSERT, '填入问题')

        t2 = Text(self, height=15, width=80)
        t2.grid(row=3, columnspan=4)
        t2.insert(INSERT, '填入答案')

        c = ttk.Combobox(self, textvariable=type)
        c['values'] = list1
        c.grid(row=0, sticky=W)
        Label(self, textvariable=name).grid(row=0, column=1)
        Button(self, text='存入题库', command=lambda s=None: save(self.s)).grid(row=0, column=2)
        Button(self, text='新建题型', command=create_type).grid(row=0, column=3)


class QueryFrame(Frame):
    def __init__(self, master, s,name):
        Frame.__init__(self, master)
        self.usrname = name
        self.s = s
        self.create_page()

    def create_page(self):
        flag = 2
        data1 = 'A'
        self.s.send(data1.encode())
        data2 = self.s.recv(1024).decode()
        list1 = data2.split('##')
        type = StringVar()
        name = StringVar()


        def ask(s):
            nonlocal flag
            print(name2.get())
            if flag == 1 or flag == 2:
                list4 = []
                l2 = []
                for j in list2:
                    l2.append(j.get())
                list3 = iter(l2)
                print(list3)
                for i in list1:
                    p = next(list3)
                    if p == 1:
                        list4.append(i)

                data = '%s##'%name2.get()+'##'.join(list4)
                s.send(data.encode())
                data = s.recv(4096).decode()
                self.l = data.split('##')
                t1.delete(1.0, END)
                t2.delete(1.0, END)
                name.set(self.l[3])
                type.set(self.l[2])
                t1.insert(INSERT, '%s' %self.l[0])
                t1.tag_add('answer', '1.0', END)
                t1.tag_config('answer', font=('Calibri', 12))
                flag = 0
            else:
                t2.delete(1.0, END)
                t2.insert(INSERT, '%s' % self.l[1])
                t2.tag_add('answer', '1.0', END)
                t2.tag_config('answer', font=('Calibri', 12))
                flag = 1

        def deltest(s,l):
            if flag == 2 or flag == 0:
                showerror("error","请将答案展示后再上传编辑")
                return
            elif l[3] == self.usrname or self.usrname == "admin":
                data = "D##" + l[0]
            else:
                choo = askokcancel("error","非上传者或管理员无法删除或修改题库\n是否标记该题目有误?")
                if choo == True:
                    data = "M##" + l[0]
                else:
                    return
            s.send(data.encode())
            showinfo("","已发送请求")

        def update(s,l):
            if flag == 2 or flag == 0:
                showerror("error","请将答案展示后再删除")
                return
            elif l[3] == self.usrname or self.usrname == "admin":
                data = "D##" + l[0]
                s.send(data.encode())
            else:
                choo = askokcancel("error","非上传者或管理员无法修改题库\n是否标记该题目有误?")
                if choo == True:
                    data = "M##" + l[0]
                    s.send(data.encode())
                    return
                else:
                    return
            type1 = type.get()
            ask1 = t1.get(1.0, END)
            answer1 = t2.get(1.0, END)
            data = 'S##%s##%s##%s##%s' % (type1, self.usrname, ask1, answer1)
            s.send(data.encode())
            data = s.recv(128).decode()
            if data == 'OK':
                showinfo('感谢您', '题目修改成功！')
                self.create_page()
            else:
                showinfo('error', '%s'%data)
                self.create_page()

        fr1 = Frame(self)
        fr1.grid(row=4,rowspan=6,sticky=NW)
        list2 = []
        n=2
        for i in list1:
            list2.append(IntVar())
            b = Checkbutton(fr1,text=i,variable=list2[-1])
            b.grid(row=n,column=0,sticky=W)
            n += 1
        Label(self,text="上传者：").grid(sticky=E,row=3, column=1)
        Label(self,text="题目类型：").grid(sticky=E,row=3, column=3)
        Label(self).grid( row=2, column=3)
        name2=IntVar()
        Checkbutton(self, text='只抽我的题库', variable=name2).grid(row=3, column=5)
        Entry(self,textvariable=name).grid(row=3, column=2,sticky=W)
        Entry(self, textvariable=type).grid(row=3, column=4,sticky=W)
        t1 = Text(self, height=6,width=80)
        t1.grid(row=4, column=1, columnspan=5)
        t2 = Text(self, height=20,width=80)
        t2.grid(row=5, column=1, columnspan=5)
        Button(self,text="删除题目",command=lambda s=None: deltest(self.s,self.l)).grid(row=1,column=2)
        Button(self,text="修改题目",command=lambda s=None: update(self.s,self.l)).grid(row=1,column=3)
        Button(self,text='随机抽题', command=lambda s=None: ask(self.s)).grid(row=1, column=1)


class CountFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        Label(self, text='count page').grid()


class AboutFrame(Frame):
    def __init__(self, master, s):
        Frame.__init__(self, master)
        self.s = s
        self.create_page()

    def create_page(self):
        Label(self, text='about page').grid()
