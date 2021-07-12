# -*- coding:utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from merry import Merry
from loguru import logger
import socket
import struct
import collections
import time
import math

import inc.global_value as glo



class Port_8056(QThread):
    dic_8056 = pyqtSignal(dict)
    sign_except = pyqtSignal(str)
    
    merry = Merry()
    merry.logger.disabled = True
    
    @merry._try
    def __init__(self) -> None:
        super().__init__()
        # 先定义全局变量供异常使用
        global parm
        parm = self
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 设置超时时间
        self.socket_client.settimeout(8)
        # 连接参数服务器，参数必须为元组格式
        self.HOST = glo.get_value("ip")
        self.index = 0
        self.lost = 0
        # self.data_len = 366
        self.data_len = 462
        self.data_len = 535
        

    def __var__(self):
        # 创建一个保留键值的字典对象
        dic = collections.OrderedDict()
        # 初始化字典
        dic['MessageSize'] = 'I'
        # 时间戳
        dic['TimeStamp'] = 'Q'
        # 循环模式
        dic['autorun_cycleMode'] = 'B'
        # 关节坐标系
        dic["machinePos01"], dic['machinePos02'],dic['machinePos03'],dic['machinePos04'],dic['machinePos05'],dic['machinePos06'],dic['machinePos07'],dic['machinePos08'] = 'd'*8
        # 直角坐标系
        dic["machinePose01"], dic['machinePose02'],dic['machinePose03'],dic['machinePose04'],dic['machinePose05'],dic['machinePose06']= 'd'*6
        # 用户坐标系
        dic['machineUserPose01'],dic['machineUserPose02'],dic['machineUserPose03'],dic['machineUserPose04'],dic['machineUserPose05'],dic['machineUserPose06']="d"*6
        # 关节额定力矩百分比
        dic['torque01'],dic['torque02'],dic['torque03'],dic['torque04'],dic['torque05'],dic['torque06'],dic['torque07'],dic['torque08'] = 'd'*8
        # 机器人状态
        dic['robotState'] = 'i'
        # 伺服使能状态
        dic['servoReady'] = 'i'
        # 同步状态
        dic['can_motor_run'] = 'i'
        # 各轴电机转速
        dic['motor_speed01'],dic['motor_speed02'],dic['motor_speed03'],dic['motor_speed04'],dic['motor_speed05'],dic['motor_speed06'], dic['motor_speed07'],dic['motor_speed08'] = 'i'*8
        # 机器人模式
        dic['robotMode'] = 'i'
        # 模拟量输入输出数据
        dic['analog_ioInput01'],dic['analog_ioInput02'],dic['analog_ioInput03'],dic['analog_ioOutput01'],dic['analog_ioOutput02'],dic['analog_ioOutput03'],dic['analog_ioOutput04'],dic['analog_ioOutput05'] = 'd'*8
        # 数字量输入数据
        dic['digital_ioInput'] = 'Q'
        # 数字量输出数据
        dic['digital_ioOutput'] = 'Q'
        # 碰撞报警状态
        dic['collision'] = 'B'
        dic['machineFlangePose01'],dic['machineFlangePose02'],dic['machineFlangePose03'],dic['machineFlangePose04'],dic['machineFlangePose05'],dic['machineFlangePose06'] = 'd'*6
        dic['machineUserFlangePose01'],dic['machineUserFlangePose02'],dic['machineUserFlangePose03'],dic['machineUserFlangePose04'],dic['machineUserFlangePose05'],dic['machineUserFlangePose06'] = 'd'*6
        return dic

    @merry._try
    def run(self):
        self.socket_client.connect((self.HOST,8056))
        
        while True:
            dic = self.__var__()
            # logger.info("1")
            # logger.info(dic)
            # print("index =", self.index)
            # 接收数据
            data = self.socket_client.recv(self.data_len)
            # print("接收到的源数据为："+str(data))

            # 判断接收数据的长度
            if len(data) != self.data_len:    
                self.lost += 1
                # logger.info("数据长度错误"+str(self.lost))
                continue
            # logger.info(data)
            names =[]
            ii=range(len(dic))
            for key ,i in zip(dic ,ii):
                # fmtsize为长度
                # print(key,i)
                # 获取对应键值对打包时的长度
                fmtsize = struct.calcsize(dic[key])
                # print("fmtstr为"+str(fmtsize))
                # 从索引为0截取指定长度的数据，并将之后的数据覆盖data
                data1,data = data[0:fmtsize],data[fmtsize:]
                # print("data1:"+str(data1))
                # print("data"+str(data))
                # fmt为解包时的格式串
                fmt = "!" + dic[key]
                names.append(struct.unpack(fmt,data1))
                # 对应键的值扩充为列表，索引为0的为数据格式（以便后面解析数据时进行复用），索引为1的为数据
                dic[key] = dic[key], struct.unpack(fmt,data1)
                # print(dic[key])
                
            output = ""
            # print("------------------------")
            # print(dic)

            
            for key in dic.keys ():
                output += str(key) + ":" + str(dic[key][1][0]) + ";\n"
                output = "lost : " + str(self.lost) + " index : " + str(self.index) + ";" + output + "\n"
            if self.index % 15 == 0:
                # 发射信号
                # self.print_info(dic)
                print(dic["MessageSize"][1][0])
                self.dic_8056.emit(dic)


            self.index = self.index +1
            output = ""
            dic = {}
            data = ""
            # self.msleep(1)


    def stop(self):
        self.socket_client.close()    
        self.terminate()
        print("线程运行结束")
        print(self.isFinished())

    def print_info(self,dic):
        # 打 印 时 间 戳
        print("时间戳")
        timestamp01_value = dic['TimeStamp'][1][0] // 1000
        timeValue = time.gmtime(int( timestamp01_value ))
        print(time.strftime ("%Y-%m-%d %H:%M:%S", timeValue ))
        #打 印 所 有 信 息
        print("所有信息")
        # print(output)
        #打 印 直 角 坐 标
        print("直角坐标")
        print(dic['machinePose01'][1][0],dic['machinePose02'][1][0],dic['machinePose03'][1][0],dic['machinePose04'][1][0],dic['machinePose05'][1][0]*180 , dic['machinePose06'][1][0])
        #打 印 用 户 坐 标
        print("用户坐标")
        print(dic['machineUserPose01'][1][0] , dic['machineUserPose02'][1][0] , dic['machineUserPose03'][1][0] , dic['machineUserPose04'][1][0]*180/ math.pi ,dic['machineUserPose05'][1][0]*180/ math.pi ,dic['machineUserPose06'][1][0]*180/ math.pi)
        #打 印 关 节 额 定 力 矩 百 分 比
        print("关节额定力矩百分比")
        print(dic['torque01'][1][0],dic['torque02'][1][0],dic['torque03'][1][0],dic['torque04'][1][0],dic['torque05'][1][0],dic['torque06'][1][0] ,dic['torque07'][1][0],dic['torque08'][1][0])
        #打 印 机 器 人 状 态
        print("机器人状态")
        print(dic['robotState'][1][0])
        #打 印 伺 服 使 能 状 态
        print("伺服使能状态")
        print(dic['servoReady'][1][0])
        #打 印 同 步 状 态
        print("同步状态")
        print(dic['can_motor_run'][1][0])
        #打 印 各 轴 电 机 转 速
        print("各轴电机转速")
        print(dic['motor_speed01'][1][0] , dic['motor_speed02'][1][0] , dic['motor_speed03'][1][0] , dic['motor_speed04'][1][0] , dic['motor_speed05'][1][0] ,dic['motor_speed06'][1][0] , dic['motor_speed07'][1][0] , dic['motor_speed08'][1][0])
        #打 印 机 器 人 模 式
        print("机器人模式")
        print(dic['robotMode'][1][0])
        #打 印 模 拟 量 输 入 口 数 据
        print("模拟量输入数据")
        print(dic['analog_ioInput01'][1][0] , dic['analog_ioInput02'][1][0] , dic['analog_ioInput03'][1][0])
        #打 印 模 拟 量 输 出 口 数 据
        print("模拟量输出数据")
        print(dic['analog_ioOutput01'][1][0] , dic['analog_ioOutput02'][1][0] , dic['analog_ioOutput03'][1][0] , dic['analog_ioOutput04'][1][0] , dic['analog_ioOutput05'][1][0])
        #打 印 数 字 量 输 入 口 数 据 的 二 进 制 形 式
        print("数字量输入的二进制数据")
        print(bin(dic['digital_ioInput'][1][0])[2:].zfill(64))
        #打 印 数 字 量 输 出 口 数 据 的 二 进 制 形 式
        print("数字量输出的二进制数据")
        print(bin(dic['digital_ioOutput'][1][0])[2:].zfill(64))
        # 打 印 碰 撞 报 警 状 态
        print("碰撞报警状态")
        print(dic["collision"][1][0])
        # 打 印 直 角 坐 标 系 下 的 法 兰 盘 中 心 位 姿
        # print(dic['machineFlangePose01'][1][0] , dic['machineFlangePose02'][1][0] , dic['machineFlangePose03'][1][0] ,dic['machineFlangePose04'][1][0] , dic['machineFlangePose05'][1][0] , dic['machineFlangePose06'][1][0])
        # 打 印 用 户 坐 标 系 下 的 法 兰 盘 中 心 位 姿
        # print(dic['machineUserFlangePose01'][1][0] , dic['machineUserFlangePose02'][1][0] ,dic['machineUserFlangePose03'][1][0] , dic['machineUserFlangePose04'][1][0] ,dic['machineUserFlangePose05'][1][0] , dic['machineUserFlangePose06'][1][0])
        pass

    @merry._except(ConnectionRefusedError)
    def except_(e):
        global parm
        logger.error("8056 ConnectionRefusedError")
        logger.error(e)
        parm.sign_except.emit("ConnectionRefusedError")
        # parm.terminate()
        pass
    


if __name__ == "__main__":
    pass