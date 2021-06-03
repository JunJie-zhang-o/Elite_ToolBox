import json,os
from pprint import pprint


class login_info():
    
    def __init__(self,file_path="./config/login_info.json") -> None:
        self.file_path=file_path
        self.ip=[]
        self.username=[]
        self.password=[]
        self.info=[{'ip': self.ip}, {'username': self.username}, {'password': self.password}]
        pass
    
        
    def read_from_json(self):
        """读json文件
        """         
        if self.__check_file(self.file_path):
            with open(self.file_path,"r") as f:
                data = json.load(f)
                self.ip=data[0]["ip"]
                self.username=data[1]["username"]
                self.password=data[2]["password"]
            self.__update()
            return data 

    
    def write_json(self):
        """写json文件
        """
        self.__is_create_folder()
        self.__update()
        with open(self.file_path,"w") as f:
            json.dump(self.info,f,indent=4)
            
            
    def __check_file(self,path):
        """检查文件是否存在
        """
        if os.path.exists(path):
            return True
        else:
            return False
    
    
    def __is_create_folder(self):
        """创建目录
        """
        if not self.__check_file(self.__get_main_folder()):
            os.mkdir("./config")
        
        
    def __get_main_folder(self):
        """获取配置的文件夹名
        """
        return "./config"
    
    
    def __update(self):
         self.info=[{'ip': self.ip}, {'username': self.username}, {'password': self.password}]
        
    
if __name__ == "__main__":
    print(os.getcwd())
    login = login_info("./config/login_info.json")

    login.ip.append("192.168.1.200")
    login.ip.append("127.0.0.1")

    login.username.append("root")
    login.username.append("elite")

    login.password.append("elite2014")
    login.password.append("elite2020")
    login.write_json()
    data = login.read_from_json()
    pprint(data)
    print(login.info)
