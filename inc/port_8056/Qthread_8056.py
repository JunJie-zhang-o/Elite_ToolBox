# -*- coding:utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
import socket
import struct
import collections
import time
import math
HOST = "192.168.1.200"
PORT = 8056

# socket.AF_INET:IPV4
# socket.SOCK_STREAM:流式socket for TCP
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 设置超时时间
s.settimeout(8)
# 连接参数服务器，参数必须为元组格式
s.connect((HOST,PORT))
index = 0
lost = 0


class Port_8056(QThread):
    dic_8056 = pyqtSignal(dict)
    
    
    def __init__(self) -> None:
        super().__init__()
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 设置超时时间
        self.s.settimeout(8)
        # 连接参数服务器，参数必须为元组格式
        self.s.connect((HOST,8056))
        self.index = 0
        self.lost = 0

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
        dic['analog_ioInput01'],dic['analog_ioInput02'],dic['analog_ioInput03'],dic['analog_ioOutput01'],dic['analog_ioOutput02'],dic['analog_ioOutput03'] = 'd',dic['analog_ioOutput04'] = 'd',dic['analog_ioOutput05'] = 'd'*5
        # 数字量输入数据
        dic['digital_ioInput'] = 'Q'
        # 数字量输出数据
        dic['digital_ioOutput'] = 'Q'
        # 碰撞报警状态
        dic['collision'] = 'B'
        return dic


    def run(self):
        
        while True:
        
            print("index =", self.index)
            # 接收数据
            data = s.recv (366)
            print("接收到的源数据为："+str(data))

            # 判断接收数据的长度
            if len(data) != 366:    
                self.lost += 1
                print("数据长度错误"+str(self.lost))
                continue
            
            names =[]
            ii=range(len(dic))
            for key ,i in zip(dic ,ii):
                # fmtsize为长度
                print(key,i)
                # 获取对应键值对打包时的长度
                fmtsize = struct.calcsize (dic[key ])
                print("fmtstr为"+str(fmtsize))
                # 从索引为0截取指定长度的数据，并将之后的数据覆盖data
                data1 , data = data [0: fmtsize], data[fmtsize :]
                print("data1:"+str(data1))
                # print("data"+str(data))
                # fmt为解包时的格式串
                fmt = "!" + dic[key]
                names.append(struct.unpack(fmt ,data1))
                # 对应键的值扩充为列表，索引为0的为数据格式（以便后面解析数据时进行复用），索引为1的为数据
                dic[key] = dic[key], struct.unpack(fmt , data1)
                print(dic[key])
                print("\n")
                
            output = ""
            print("------------------------")
            print(dic)

            
            for key in dic.keys ():
                output += str(key) + ":" + str(dic[key][1][0]) + ";\n"
                output = "lost : " + str(self.lost) + " index : " + str(self.index) + ";" + output + "\n"
            if self.index %10 == 0:
                # 打 印 时 间 戳
                print("时间戳")
                timestamp01_value = dic['TimeStamp'][1][0] // 1000
                timeValue = time.gmtime(int( timestamp01_value ))
                print(time.strftime ("%Y-%m-%d %H:%M:%S", timeValue ))
                #打 印 所 有 信 息
                print("所有信息")
                print(output)
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
                print(bin(dic['digital_ioInput'][1][0]) [2:]. zfill (64))
                #打 印 数 字 量 输 出 口 数 据 的 二 进 制 形 式
                print("数字量输出的二进制数据")
                print(bin(dic['digital_ioOutput'][1][0]) [2:]. zfill (64))
                # 打 印 碰 撞 报 警 状 态
                print("碰撞报警状态")
                print(dic["collision"][1][0])

            
            self.index = self.index +1
            output = ""
            dic = {}
            data = ""
            time.sleep(10)
        s.close ()


"""
b'\x00\x00\x01n\x00\x00\x01y\xa3\xc8\xee\x80\x01\xc0%\x9e\xdd\xb3\x14\xa2\x16\xc0[L\xc2\x83\xad3\xac@W\xc81\x7f\x02\x85\xb6\xc0R\x18}\xdd\xd8\xc8\xdf@V\xd1/\xcf\xd8\xd19\xc0X\xd8\xc9v^\xc9\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@v\x10\xd3>\x95\x07\x94@N\xd32\xcf\xa6\xa7\xa4@x^\xbb\x94m=Z\xc0\x08\xe0\x8e=f\xebM?\xadi\xe6\xee\x8e\xe2\xd7\xbf\x991\x97Z\x91+d@Q\x04et\n\x97\x96@f3\x98V\x0bK\xf6\xc0y\x1bh\xfa\xe0\'w?\x9d\xb7"\x8e\x0c\xbaQ\xbf\xae\x19\xddv`\xf4[\xbf\xf8\xd5e|\xa4\xed\xe2@0\x00\x00\x00\x00\x00\x00@Q\xc0\x00\x00\x00\x00\x00\xc0m\x80\x00\x00\x00\x00\x00@S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xbf\x8e\x00\x00\x00\x00\x00\x00\xbf\xa4\x00\x00\x00\x00\x00\x00?\x88\x93t\xbcj~\xfa\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x00\x0f\x00\x0c\x00\x00\x00\x00\x00\x00\x00'


machinePose01:353.05157335486115;

machinePose02:61.6499881328339;

machinePose03:389.92079584762325;

machinePose04:-3.109646300986617;

machinePose05:0.05744859373175409;

machinePose06:-0.0246032380130531;


machinePose01 11
fmtstr为8
data1:b'@v\x10\xd3>\x95\x07\x94'
('d', (353.05157335486115,))


machinePose02 12
fmtstr为8
data1:b'@N\xd32\xcf\xa6\xa7\xa4'
('d', (61.6499881328339,))


machinePose03 13
fmtstr为8
data1:b'@x^\xbb\x94m=Z'
('d', (389.92079584762325,))


machinePose04 14
fmtstr为8
data1:b'\xc0\x08\xe0\x8e=f\xebM'
('d', (-3.109646300986617,))


machinePose05 15
fmtstr为8
data1:b'?\xadi\xe6\xee\x8e\xe2\xd7'
('d', (0.05744859373175409,))


machinePose06 16
fmtstr为8
data1:b'\xbf\x991\x97Z\x91+d'
('d', (-0.0246032380130531,))


machineUserPose01 17
fmtstr为8
data1:b'@Q\x04et\n\x97\x96'
('d', (68.06869221720112,))


machineUserPose02 18
fmtstr为8
data1:b'@f3\x98V\x0bK\xf6'
('d', (177.6123457165374,))


machineUserPose03 19
fmtstr为8
data1:b"\xc0y\x1bh\xfa\xe0'w"
('d', (-401.7131298786184,))


machineUserPose04 20
fmtstr为8
data1:b'?\x9d\xb7"\x8e\x0c\xbaQ'
('d', (0.029018917007471782,))


machineUserPose05 21
fmtstr为8
data1:b'\xbf\xae\x19\xddv`\xf4['
('d', (-0.058791084957626714,))

machineUserPose06 22
fmtstr为8
data1:b'\xbf\xf8\xd5e|\xa4\xed\xe2'
('d', (-1.5520987385669902,))


"""

if __name__ == "__main__":
    pass