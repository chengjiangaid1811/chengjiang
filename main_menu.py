from myview import *





class Main_page(object):
    def __init__(self, master,s,name):
        self.s = s
        self.root = master
        self.root.geometry('800x600')
        self.root.title('main')
        # self.get_typelist()
        self.create_page(name)

    # def get_typelist(self):
    #     data1 = 'A'
    #     self.s.send(data1.encode())
    #     data2 = self.s.recv(1024).decode()
    #     self.list1 = data2.split('##')

    def create_page(self,name):
        self.input_page = InputFrame(self.root,self.s,name)
        self.query_page = QueryFrame(self.root,self.s,name)
        self.count_page = CountFrame(self.root,self.s)
        self.about_page = AboutFrame(self.root,self.s)
        self.do_random_page =Do_random(self.root)
        self.query_page.pack()

        menubar = Menu(self.root)
        menubar.add_command(label='查询', command=self.queryData)
        menubar.add_command(label='题库录入', command=self.inputData)
        menubar.add_command(label='沙场点兵', command=self.do_random)
        menubar.add_command(label='统计', command=self.countData)
        menubar.add_command(label='关于', command=self.aboutData)
        self.root['menu'] = menubar
    def do_random(self):
        self.do_random_page.pack()
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack_forget()
        self.about_page.pack_forget()


    def inputData(self):
        self.input_page.pack()
        self.do_random_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack_forget()
        self.about_page.pack_forget()

    def queryData(self):
        self.input_page.pack_forget()
        self.query_page.pack()
        self.count_page.pack_forget()
        self.about_page.pack_forget()
        self.do_random_page.pack_forget()

    def countData(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack()
        self.about_page.pack_forget()
        self.do_random_page.pack_forget()

    def aboutData(self):
        self.input_page.pack_forget()
        self.query_page.pack_forget()
        self.count_page.pack_forget()
        self.do_random_page.pack_forget()
        self.about_page.pack()
