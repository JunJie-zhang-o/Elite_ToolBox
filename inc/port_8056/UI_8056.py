
from PyQt5.QtWidgets import QMessageBox, QWidget
from loguru import logger
from inc.ui2py.port_8056 import Ui_Widget_8056
from inc.port_8056.Qthread_8056 import Port_8056
import math


class UI_8056(Ui_Widget_8056,QWidget):

    
    def __init__(self) -> None:
        super().__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect_init()
        # 初始化变量,默认为弧度-False
        self.show_deg_or_rad = False

        
    def connect_init(self):
        self.btn_start_recv.toggled.connect(self.slot_recv)
        self.Rbtn_rad.clicked.connect(self.solt_radio_btn)
        self.Rbtn_deg.clicked.connect(self.solt_radio_btn)

        
    def slot_recv(self):
        logger.info("UI_8056 start recv btn clicked")
        if self.btn_start_recv.isChecked() == True:
            self.btn_start_recv.setText("停止监控")
            self.port_8056 = Port_8056()
            self.port_8056.dic_8056.connect(self.dic_2_ui)
            self.port_8056.sign_except.connect(self.except_msgbox)
            self.port_8056.start()
        else:
            self.btn_start_recv.setText("开始监控")
            self.port_8056.stop()


    def dic_2_ui(self,dic):
        # 关节坐标
        self.LE_joint1.setText(format(dic["machinePos01"][1][0],"4.5f"))
        self.LE_joint2.setText(format(dic["machinePos02"][1][0],"4.5f"))
        self.LE_joint3.setText(format(dic["machinePos03"][1][0],"4.5f"))
        self.LE_joint4.setText(format(dic["machinePos04"][1][0],"4.5f"))
        self.LE_joint5.setText(format(dic["machinePos05"][1][0],"4.5f"))
        self.LE_joint6.setText(format(dic["machinePos06"][1][0],"4.5f"))
        
        # 带工具直角坐标
        self.LET_world_x.setText(format(dic["machinePose01"][1][0],"4.5f"))
        self.LET_world_y.setText(format(dic["machinePose02"][1][0],"4.5f"))
        self.LET_world_z.setText(format(dic["machinePose03"][1][0],"4.5f"))
        if self.show_deg_or_rad == False:
            self.LET_world_rx.setText(format(dic["machinePose04"][1][0],"4.5f"))
            self.LET_world_ry.setText(format(dic["machinePose05"][1][0],"4.5f"))
            self.LET_world_rz.setText(format(dic["machinePose06"][1][0],"4.5f"))
        else:
            self.LET_world_rx.setText(format(math.degrees(dic["machinePose04"][1][0]),"4.5f"))
            self.LET_world_ry.setText(format(math.degrees(dic["machinePose05"][1][0]),"4.5f"))
            self.LET_world_rz.setText(format(math.degrees(dic["machinePose06"][1][0]),"4.5f"))
        # 带工具用户坐标
        self.LET_user_x.setText(format(dic["machineUserPose01"][1][0],"4.5f"))
        self.LET_user_y.setText(format(dic["machineUserPose02"][1][0],"4.5f"))
        self.LET_user_z.setText(format(dic["machineUserPose03"][1][0],"4.5f"))
        if  self.show_deg_or_rad == False:
            self.LET_user_rx.setText(format(dic["machineUserPose04"][1][0],"4.5f"))
            self.LET_user_ry.setText(format(dic["machineUserPose05"][1][0],"4.5f"))
            self.LET_user_rz.setText(format(dic["machineUserPose06"][1][0],"4.5f"))
        else:
            self.LET_user_rx.setText(format(math.degrees(dic["machineUserPose04"][1][0]),"4.5f"))
            self.LET_user_ry.setText(format(math.degrees(dic["machineUserPose05"][1][0]),"4.5f"))
            self.LET_user_rz.setText(format(math.degrees(dic["machineUserPose06"][1][0]),"4.5f"))
        if self.port_8056.data_len > 366 :
            # 法兰中心直角坐标
            self.LE_world_x.setText(format(dic["machineFlangePose01"][1][0],"4.5f"))
            self.LE_world_y.setText(format(dic["machineFlangePose02"][1][0],"4.5f"))
            self.LE_world_z.setText(format(dic["machineFlangePose03"][1][0],"4.5f"))
            if  self.show_deg_or_rad == False:
                self.LE_world_rx.setText(format(dic["machineFlangePose04"][1][0],"4.5f"))
                self.LE_world_ry.setText(format(dic["machineFlangePose05"][1][0],"4.5f"))
                self.LE_world_rz.setText(format(dic["machineFlangePose06"][1][0],"4.5f"))
            else:
                self.LE_world_rx.setText(format(math.degrees(dic["machineFlangePose04"][1][0]),"4.5f"))
                self.LE_world_ry.setText(format(math.degrees(dic["machineFlangePose05"][1][0]),"4.5f"))
                self.LE_world_rz.setText(format(math.degrees(dic["machineFlangePose06"][1][0]),"4.5f"))
            # 法兰坐标用户坐标
            self.LE_user_x.setText(format(dic["machineUserFlangePose01"][1][0],"4.5f"))
            self.LE_user_y.setText(format(dic["machineUserFlangePose02"][1][0],"4.5f"))
            self.LE_user_z.setText(format(dic["machineUserFlangePose03"][1][0],"4.5f"))
            if  self.show_deg_or_rad == False:
                self.LE_user_rx.setText(format(dic["machineUserFlangePose04"][1][0],"4.5f"))
                self.LE_user_ry.setText(format(dic["machineUserFlangePose05"][1][0],"4.5f"))
                self.LE_user_rz.setText(format(dic["machineUserFlangePose06"][1][0],"4.5f"))
            else:
                self.LE_user_rx.setText(format(math.degrees(dic["machineUserFlangePose04"][1][0]),"4.5f"))
                self.LE_user_ry.setText(format(math.degrees(dic["machineUserFlangePose05"][1][0]),"4.5f"))
                self.LE_user_rz.setText(format(math.degrees(dic["machineUserFlangePose06"][1][0]),"4.5f"))
            
        # 关节力矩
        self.LB_force1.setText(format(dic["torque01"][1][0],"4.3f"))
        self.LB_force2.setText(format(dic["torque02"][1][0],"4.3f"))
        self.LB_force3.setText(format(dic["torque03"][1][0],"4.3f"))
        self.LB_force4.setText(format(dic["torque04"][1][0],"4.3f"))
        self.LB_force5.setText(format(dic["torque05"][1][0],"4.3f"))
        self.LB_force6.setText(format(dic["torque06"][1][0],"4.3f"))
        # 电机速度
        self.LB_speed1.setText(format(dic["motor_speed01"][1][0],"6.1f"))
        self.LB_speed2.setText(format(dic["motor_speed02"][1][0],"6.1f"))
        self.LB_speed3.setText(format(dic["motor_speed03"][1][0],"6.1f"))
        self.LB_speed4.setText(format(dic["motor_speed04"][1][0],"6.1f"))
        self.LB_speed5.setText(format(dic["motor_speed05"][1][0],"6.1f"))
        self.LB_speed6.setText(format(dic["motor_speed06"][1][0],"6.1f"))
        # 模拟量
        self.LB_AI01.setText(format(dic["analog_ioInput01"][1][0],"4.5f"))
        self.LB_AI02.setText(format(dic["analog_ioInput02"][1][0],"4.5f"))
        self.LB_AI03.setText(format(dic["analog_ioInput03"][1][0],"4.5f"))
        self.LB_AO01.setText(format(dic["analog_ioOutput01"][1][0],"4.5f"))
        self.LB_AO02.setText(format(dic["analog_ioOutput02"][1][0],"4.5f"))
        self.LB_AO03.setText(format(dic["analog_ioOutput03"][1][0],"4.5f"))
        self.LB_AO04.setText(format(dic["analog_ioOutput04"][1][0],"4.5f"))
        self.LB_AO05.setText(format(dic["analog_ioOutput05"][1][0],"4.5f"))

        self.robot_state(dic)
        self.di_do(dic)


        if self.port_8056.data_len > 462 :
            self.LE_joint1_speed.setText(format(dic["jointSpeed01"][1][0],"4.5f"))
            self.LE_joint2_speed.setText(format(dic["jointSpeed02"][1][0],"4.5f"))
            self.LE_joint3_speed.setText(format(dic["jointSpeed03"][1][0],"4.5f"))
            self.LE_joint4_speed.setText(format(dic["jointSpeed04"][1][0],"4.5f"))
            self.LE_joint5_speed.setText(format(dic["jointSpeed05"][1][0],"4.5f"))
            self.LE_joint6_speed.setText(format(dic["jointSpeed06"][1][0],"4.5f"))
            
            self.LE_speed_TCP.setText(format(dic["tcpSpeed01"][1][0],"4.3f"))

        pass
    
    # @logger.catch
    def robot_state(self,dic,*args):
        """解析机器人状态相关信息
        """
        # 机器人状态
        robotState = ("停止","暂停","急停","运行","报警")
        if dic["robotState"][1][0] >=0 and dic["robotState"][1][0] <=4:
            self.LB_running_state.setText(robotState[dic["robotState"][1][0]])
        # 伺服使能状态
        servoReady = ("未使能","使能中")
        if dic["servoReady"][1][0] >=0 and dic["servoReady"][1][0] <= 1:
            self.LB_brake_state.setText(servoReady[dic["servoReady"][1][0]])
        # 同步状态
        can_motor_run = ("未同步","同步")
        if dic["can_motor_run"][1][0] >=0 and dic["can_motor_run"][1][0] <= 1:
            self.LB_synch_state.setText(can_motor_run[dic["can_motor_run"][1][0]])
        # 循环模式
        autorun_cycleMode = ("单步","单循环","连续循环")
        if dic["autorun_cycleMode"][1][0] >=0 and  dic["autorun_cycleMode"][1][0] <= 2:
            self.LB_cyclical_mode.setText(autorun_cycleMode[dic["autorun_cycleMode"][1][0]])
        # 机器人模式
        robotMode = ("示教模式","自动模式","远程模式")   
        if dic["robotMode"][1][0]>=0 and dic["robotMode"][1][0] <= 2:
            self.LB_robot_mode.setText(robotMode[dic["robotMode"][1][0]])     
        # 碰撞报警状态
        collision = ('未报警','碰撞报警')
        if dic["collision"][1][0] >=0 and dic["collision"][1][0] <= 1:
            self.LB_crash_state.setText(collision[dic["collision"][1][0]])
        if self.port_8056.data_len > 462 :
            emergencyStopState = ("未急停","已急停")
            if dic["emergencyStopState"][1][0] >= 0 and dic["emergencyStopState"][1][0] <=1 :
                self.LB_stop_state.setText(emergencyStopState[dic["emergencyStopState"][1][0]])
        
    
    
    def di_do(self,dic):
        """解析数字量信息
        """
        #打 印 数 字 量 输 入 口 数 据 的 二 进 制 形 式
        # print("数字量输入的二进制数据")
        # print(bin(dic['digital_ioInput'][1][0])[2:].zfill(64))
        di = bin(dic['digital_ioInput'][1][0])[2:].zfill(64)
        #打 印 数 字 量 输 出 口 数 据 的 二 进 制 形 式
        # print("数字量输出的二进制数据")
        # print(bin(dic['digital_ioOutput'][1][0])[2:].zfill(64))
        do = bin(dic['digital_ioOutput'][1][0])[2:].zfill(64)
        
        # 
        d_input = [self.LB_DI04,self.LB_DI05,self.LB_DI06,self.LB_DI07,
                   self.LB_DI08,self.LB_DI09,self.LB_DI10,self.LB_DI11,
                   self.LB_DI12,self.LB_DI13,self.LB_DI14,self.LB_DI15,
                   self.LB_DI16,self.LB_DI17,self.LB_DI18,self.LB_DI19]
        for i in range(len(d_input)):
            d_input[i].setText(str(di)[-(i+5)])
        d_output = [self.LB_DO01,self.LB_DO02,self.LB_DO03,self.LB_DO04,
                    self.LB_DO05,self.LB_DO06,self.LB_DO07,self.LB_DO08,
                    self.LB_DO09,self.LB_DO10,self.LB_DO11,self.LB_DO12,
                    self.LB_DO13,self.LB_DO14,self.LB_DO15,self.LB_DO16,
                    self.LB_DO17,self.LB_DO18,self.LB_DO19,self.LB_DO20]
        for i in range(len(d_output)):
            d_output[i].setText(str(do)[-(i+1)])

    
    def solt_radio_btn(self):
        # 获取发送对象
        sender = self.sender()
        logger.info("UI_8056 radio btn clicked param="+sender.text())
        # 角度
        if sender.text() == self.Rbtn_deg.text():
            self.show_deg_or_rad = True
        # 弧度
        else:
            self.show_deg_or_rad = False
            
            
    def except_msgbox(self,except_sign):
        # print(except_sign+"111111111")
        if except_sign == "ConnectionRefusedError":
            msg = "请检查网络连接或8056远程端口是否正常打开"
        if except_sign == "8056 recv timeout" or except_sign == "ConnectionResetError":
            msg = "请检查网络连接是否中断"
        QMessageBox.warning(self,"监控失败",msg)
        self.btn_start_recv.setText("开始监控")
        self.btn_start_recv.setChecked(False)
