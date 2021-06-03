import xlrd
import xlwt
from loguru import logger


class Excel_read_write():
    
    def __init__(self):
        self.sheet_name=["B变量注释","I变量注释","D变量注释","P变量注释","V变量注释"]
        self.write_style()
        
        
    def write_style(self):
        # 对齐方式
        self.aligment=xlwt.Alignment()
        self.aligment.horz=0x02
        # self.aligment.vert=0x01
        # 边框
        self.borders=xlwt.Borders()
        self.borders.left=1
        self.borders.right=1
        self.borders.top=1
        self.borders.bottom=1
        # 字体
        self.font=xlwt.Font()
        self.font.name="name 宋体"
        # self.font.height=20*16          #20为衡量单位，16为字号
        self.font.bold=False            #加粗
        self.font.underline=False       #下划线
        self.font.italic=False          #斜体
        self.font.colour_index=0        #颜色
        # 背景色
        self.pattern=xlwt.Pattern()
        self.pattern.pattern=xlwt.Pattern.SOLID_PATTERN
        self.pattern.pattern_fore_colour=1
        # 样式设置
        self.my_style=xlwt.XFStyle()
        # self.my_style.font=self.font
        self.my_style.alignment=self.aligment
        # self.my_style.borders=self.borders
        # self.my_style.pattern=self.pattern
        
    
    def creat_read_wbook(self,file_name):
        self.read_wbook=xlrd.open_workbook(file_name)
        # 获取sheet对象
        self.read_sheet_names=self.read_wbook.sheet_names()     #获取所有sheet名字
        self.read_sheet_numbers=self.read_wbook.nsheets         #获取sheet的数量
        self.read_sheet_objects=self.read_wbook.sheets()        #获取所有sheet对象
        # self.read_wbook.sheet_by_name("sheet_name")   #通过sheet名查找
        # self.read_wbook.sheet_by_index(index)         #通过索引查找
        pass
    
    def read_all_coment(self,sheet: object):
        """对于表中的数据按列进行读取

        Args:
            sheet (object): 要读取的表

        Returns:
            [type]: 返回一个按 每列所有行数据 组成的 n列*n行的列表
        """
        column_list=[[None]*255,[None]*255,[None]*255,[None]*255,[None]*255]
        for i in range(sheet.ncols-1):
            column_list[i]=sheet.col_values(i+1,1,sheet.nrows)
        return column_list
    
    
    def creat_write_wbook(self,sheet_name: list):
        """创建写入的excel表对象

        Args:
            sheet_name (list): [description]
        """
        self.write_wbook=xlwt.Workbook()
        self.write_sheet_list=[]
        for i in range(len(sheet_name)):
            self.write_sheet_list.append(self.write_wbook.add_sheet(sheet_name[i],cell_overwrite_ok=True))
        
        
    def write_row_sheet(self,sheet: object,row: int,column: int,datas: list):
        """在表中按行写入数据

        Args:
            sheet (object): excel表中哪一页
            row (int): 第几行
            column (int): 第几列
            datas (list): 写入的数据
        """
        for i in range(len(datas)):
            sheet.write(row,i+column,datas[i],self.my_style)
            
    
    def write_column_sheet(self,sheet: object,row: int,column: int,datas: list):
        """向表中按列写入数据

        Args:
            sheet (object): 表
            row (int): 第几行
            column (int): 第几列
            datas (list): 数据
        """
        for i in range(len(datas)):
            sheet.write(i+row,column,datas[i],self.my_style)
        
    def save_wbook(self,file_name: str):
        """将创建的excel写入对象保存

        Args:
            file_name (str): 要保存的文件路径和名称
        """
        self.write_wbook.save(file_name)

if __name__ =="__main__":
    
    #写excel
    """
    list_a,list_b,list_c,list_d,list_e=[1]*300,[2]*300,[3]*300,[4]*300,[5]*300
    lists=[list_a,list_b,list_c,list_d,list_e]
    # print(list_a)
    
    excel=Excel_read_write()
    excel.creat_write_wbook(excel.sheet_name)
    row_data=["变量序号","中文注释","英文注释","日文注释","韩文注释","其他注释"]
    comment_num=["B","I","D","P","V"]
    for i in range(5):
        excel.write_row_sheet(excel.write_sheet_list[i],0,0,row_data)
        excel.write_column_sheet(excel.write_sheet_list[i],1,0,[comment_num[i]+"%03d"%j for j in range(256)])
        
    excel.save_wbook("new.xls")
    """
    #读excel
    excel=Excel_read_write()
    excel.creat_read_wbook("你好.xls")
    print(excel.read_sheet_names)
    print(excel.read_sheet_numbers)
    print(excel.read_sheet_objects)
    print(excel.read_all_coment(excel.read_sheet_objects[0]))
    print(excel.read_sheet_objects[0].name)     #获取sheet的name
    print(excel.read_sheet_objects[0].nrows)    #获取sheet的行数
    print(excel.read_sheet_objects[0].ncols)    #获取sheet的列数
    
    
    
        
    

    