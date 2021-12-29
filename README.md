#SMOD-3

## Client and Server
New updated version of SMOD (https://github.com/0x0mar/smod) fully compatible with Python 3.x
Actually tested and working on Python 3.9

Also a simple Modbus Server script is provided in order to simplify testing Modbus protocol.

Smod is a modular framework with every kind of diagnostic 
and offensive feature you could need in order to pentest 
modbus protocol.
It is a full Modbus protocol implementation using Python and Scapy. 
This software can be run on Linux/OSX. 

##Summary
SCADA (Process Control Networks) based systems have moved from proprietary closed networks to open source solutions and TCP/IP enabled networks steadily over recent years. This has made them vulnerable to the same security vulnerabilities that face our traditional computer networks.

The Modbus/TCP protocol was used as the reference protocol to display the effectiveness of the test bed in carrying out cyber attacks on a power system protocol. Modbus/TCP was chosen specifically for these reasons:
+ modbus is still widely used in power systems.
+ modbus/TCP is simple and easy to implement.
+ modbus protocol libraries are freely available for utilities to implement smart grid applications.

You can use this tool to vulnerability assessment a modbus protocol.
##Install
If you wish, create a virtual env:
```
python -m venv venv
```
In order to run the tool you need to install requirements:
```
pip install -r requirements.txt
```
##Server
If you need, included with SMOD there is a simple Modbus server to let you easly test attacks.

Server HOST ip is set to default 127.0.0.1 and port, of course, is 502

In order to run you will need root privileges!
```
sudo python server.py
```
##Demo
Just a little demo showing off the basics
```
> python3 smod3.py 
 _______ 
< SMOD-3 >
 ------- 
        \   ^__^
         \  (xx)\_______
            (__)\       )\/\
             U  ||----w |
SMOD-3 > help
 Command  Description                                      
 -------  -----------                                      
 back     Move back from the current context               
 exit     Exit the console                                 
 exploit  Run module                                       
 help     Help menu                                        
 modules  Displays modules of a given type, or all modules 
 options  Displays all options of a given module  
 set      Sets a variable to a value                       
 use      Selects a module by name
                         
SMOD-3 > modules
 Modules                              Description                             
 -------                              -----------                             
 modbus/function/readCoils            Fuzzing Read Coils Function             
 modbus/function/readDiscreteInput    Fuzzing Read Discrete Inputs Function   
 modbus/function/readHoldingRegister  Fuzzing Read Holding Registers Function 
 modbus/function/readInputRegister    Fuzzing Read Input Registers Function   
 modbus/function/writeSingleCoils     Fuzzing Write Single Coil Function      
 modbus/function/writeSingleRegister  Fuzzing Write Single Register Function  
 modbus/scanner/discover              Check Modbus Protocols                  
 modbus/scanner/getfunc               Enumeration Function on Modbus           
 modbus/scanner/uid                   Brute Force UID                         
SMOD-3 >
```
Brute Force Modbus UID
```
SMOD-3 > use modbus/scanner/uid
SMOD-3 modbus(uid) > options
 Name      Current Setting  Required  Description                                 
 ----      ---------------  --------  -----------                                 
 Function  1                False     Function code, Defualt:Read Coils.          
 Output    True             False     The stdout save in output directory         
 RHOSTS                     True      The target address range or CIDR identifier 
 RPORT     502              False     The port number for modbus protocol         
 Threads   1                False     The number of concurrent threads            
SMOD-3 modbus(uid) >set RHOSTS 192.168.1.6
SMOD-3 modbus(uid) >exploit 
[+] Module Brute Force UID Start
[+] Start Brute Force UID on : 192.168.1.6
[+] UID on 192.168.1.6 is : 10
SMOD-3 modbus(uid) >
```
Enumeration Function on Modbus
```
SMOD-3 >use modbus/scanner/getfunc
SMOD-3 modbus(getfunc) > options
 Name     Current Setting  Required  Description                                 
 ----     ---------------  --------  -----------                                 
 Output   True             False     The stdout save in output directory         
 RHOSTS                    True      The target address range or CIDR identifier 
 RPORT    502              False     The port number for modbus protocol         
 Threads  1                False     The number of concurrent threads            
 UID      None             True      Modbus Slave UID.                           
SMOD-3 modbus(getfunc) >set RHOSTS 192.168.1.6
SMOD-3 modbus(getfunc) >set UID 10
SMOD-3 modbus(getfunc) >exploit 
[+] Module Get Function Start
[+] Looking for supported function codes on 192.168.1.6
[+] Function Code 1(Read Coils) is supported.
[+] Function Code 2(Read Discrete Inputs) is supported.
[+] Function Code 3(Read Multiple Holding Registers) is supported.
[+] Function Code 4(Read Input Registers) is supported.
[+] Function Code 5(Write Single Coil) is supported.
[+] Function Code 6(Write Single Holding Register) is supported.
[+] Function Code 7(Read Exception Status) is supported.
[+] Function Code 8(Diagnostic) is supported.
[+] Function Code 15(Write Multiple Coils) is supported.
[+] Function Code 16(Write Multiple Holding Registers) is supported.
[+] Function Code 17(Report Slave ID) is supported.
[+] Function Code 20(Read File Record) is supported.
[+] Function Code 21(Write File Record) is supported.
[+] Function Code 22(Mask Write Register) is supported.
[+] Function Code 23(Read/Write Multiple Registers) is supported.
SMOD-3 modbus(getfunc) >
```
