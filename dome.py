# %%
import serial
from threading import Thread, Lock
import time


# %% [markdown]
# 먼저 RS232드라이버를 설치하고 선을 연결한 후 port를 검색해야함
# window 11, rs232-usb converter를 활용해 테스트 하였음
# 2023.05.16 현재 남쪽 돔은 케이블 연결이 되어 있으나 북쪽은 아직 되어 있지 않음
# 윤요라 선생님의 컨트롤러 제어 프로토콜을 따름
# 메인 파워는 ON, 두 돔 스위치는 중립으로 놓기

# %%
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports: print (p)

# %%
port='COM6'
baud=19200 #(통신속도)
bitnum=8
parity = 'NONE'
stop_bit=1
new_line='\r'


# %%
ser = serial.Serial(
    port = 'COM6', 
    baudrate=baud, 
    parity='N',
    stopbits=1,
    bytesize=bitnum,
    timeout=1
    )

# %%
# 포트접속, 열려있는지 확인
ser.isOpen()

#print(ser.name)

# %%
# 명령어 실행 예제
command='status\r'
en_command=str.encode(command)
print(en_command)
ser.write(en_command)

if ser.readable():
    res=ser.readline()

    print(res[:len(res)-1].decode())

# %%
command01='status\r'

command02='domeopen-all\r'

command03='domeclose-all\r'

command04='domeopen-south\r'

command05='domeopen-north\r'

command06='domeclose-south\r'

command07='domeclose-north\r'

command08='domestop\r'

command09='light-on\r'

command10='light-off\r'

command11='led-on\r'

command12='led-off\r'


# %%
def run_command(command):
    res=ser.readline()
    print(res[:len(res)-1].decode())
    en_command=str.encode(command)
    print(en_command,'\n')
    ser.write(en_command)
    print( 'executing command ...', command, '\n')
    #time.sleep(1)

    if ser.readable():
        res=ser.readline()
        print(res[:len(res)-1].decode())
        print('Job is done.')

# %%
res=ser.readline()
print(res[:len(res)-1].decode())
run_command(command06)

# %% [markdown]
# 명령어 전부 테스트 완료, LED 작동은 확인 불가


