from xml.dom.minidom import parse, parseString
import xml.dom.minidom
from pprint import pprint
from loguru import logger

class Comment_xml_parse():
    """
        1.读取文件
        2.增删改查
        3.解析xml
        4.增加注释
        5.修改
        6.删除
    """
    def __init__(self):

        # 创建原始的注释列表集合
        self._comment_B, self._comment_I, self._comment_D, self._comment_P, self._comment_V = [None]*256, [None]*256, [None]*256, [None]*256, [None]*256

        self.comment_lists = [self._comment_B, self._comment_I, self._comment_D, self._comment_P, self._comment_V]
        
    
    def read_xml(self,path):
        """读取xml文件

        Args:
            path (str): 读取的xml文件
        """
        # 获取dom对象
        self.path = path
        self.dom = xml.dom.minidom.parse(self.path)
        # 获取xml根元素
        self.root = self.dom.documentElement
        self.__element__=["VarB","VarI","VarD","VarP","VarV"]
        # 获取子元素列表
        self.ele_vars_b = self.root.getElementsByTagName("VarB")
        self.ele_vars_i = self.root.getElementsByTagName("VarI")
        self.ele_vars_d = self.root.getElementsByTagName("VarD")
        self.ele_vars_p = self.root.getElementsByTagName("VarP")
        self.ele_vars_v = self.root.getElementsByTagName("VarV")
        
        # 创建原始子元素集合列表
        self.xml_lists = [self.ele_vars_b, self.ele_vars_i, self.ele_vars_d, self.ele_vars_p, self.ele_vars_v]
        self.dom_2_comment()
    
    
    def dom_2_comment(self):
        """解析注释的xml文件，并将注释反映在一个五维list中
        """
        i = 0
        for xml_list in self.xml_lists:
            for num in range(len(xml_list)):
                # 获取并赋值子元素的属性值
                attr_num = xml_list[num].getAttribute("num")
                self.comment_lists[i][int(attr_num)] = xml_list[num].getAttribute("comment")
            i = i+1   
            
    
    def comment_2_dom(self):
        """将注释列表写入dom中
        """
        self.element_remove_all()
        for i in range(5):
            for num in range(len(self.comment_lists[i])):
                if not self.comment_lists[i][num] is None :
                        self.element_add(i,num,self.comment_lists[i][num])
        self.root.appendChild(self.dom.createTextNode("\n"))
        
        
    # 如何增加子元素，以及增加子元素后写入文件的先后顺序有没有影响
    def element_add(self,element_type:int,num:int,comment:str):
        """增加子元素

        Args:
            element (str): 增加的子元素名
            num (str): num属性值
            comment (str): comment属性值
        """
        child_element = self.dom.createElement(self.__element__[element_type])
        child_element.setAttribute("num","%03d"%num)
        child_element.setAttribute("comment",comment)
        self.root.appendChild(self.dom.createTextNode("\n\t"))    #解决生成的xml文件对齐问题
        self.root.appendChild(child_element)

    
    def element_remove_all(self):
        """移除子节点的所有元素
        """
        del self.root.childNodes[:]
        pass
    
    
    def element_change(self,element_type: int,num: int,new_comment: str):
        """改变一个元素的注释

        Args:
            element (str): 要改变的元素
            num (str): 序号
            new_comment (str): 新注释
        """
        self.xml_lists[element_type][num].setAttribute("comment",new_comment)
        pass
    

    def _xml_updata(self):
        self.dom.toxml()
        pass
    
    
    @logger.catch
    def xml_write(self,path):
        self._xml_updata()
        with open(path, "w", encoding = "utf-8") as f:
            self.dom.writexml(f, indent = "", addindent = "", newl = "", encoding = "utf-8")
    
    

    
    
    
if __name__ == "__main__":    
  
    xml_obj = Comment_xml_parse("var_note.xml")    

  
    print(" --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  -- ")
    print(xml_obj.xml_lists)
    print(xml_obj.root.childNodes)
    xml_obj.ele_vars_b[4].setAttribute("num","99999")
    print(" --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  -- ")

    
    xml_obj.comment_lists[0][2]="hahaha"
    xml_obj.comment_lists[0][5]="hahaha"
    xml_obj.comment_lists[4][30]="hahaha"

    xml_obj.comment_2_dom()
    xml_obj._xml_updata()
    print(xml_obj.comment_lists)
    print(xml_obj.xml_lists)

    xml_obj.xml_write("new.xml")
    
    # 下面的方法也可以直接修改元素的属性
    # print(xml_obj.ele_vars_b[0].attributes._attrs["comment"].nodeValue)
    # xml_obj.ele_vars_b[0].attributes._attrs["comment"].nodeValue="nodevalue"
    # xml_obj.ele_vars_b[0].attributes._attrs["num"].nodeValue="nodevalue"
