# 
#\\ 全局变量的创建
# 对应的键分别为：
#       ip
#       username
#       password



def _init():
    global __login_info_dict
    __login_info_dict={}
    
    
def set_value(key: str,value: str):
    """对全局变量进行赋值

    Args:
        key (str): 键
        value (str): 值
    """
    __login_info_dict[key]=value
    
    
def get_value(key: str):
    """从全局变量中进行取值

    Args:
        key (str): 键
    """
    try:
        return __login_info_dict[key]
    except KeyError:
        return None
    
    
def _init_window_var():
    global __main_widget
    __main_widget = None
    
def set_main_widget(parm):
    __main_widget = parm
    
def get_main_widget():
    return __main_widget