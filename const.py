#Handy registers.
rEP0FIFO=0
rEP1OUTFIFO=1
rEP2INFIFO=2
rEP3INFIFO=3
rSUDFIFO=4
rEP0BC=5
rEP1OUTBC=6
rEP2INBC=7
rEP3INBC=8
rEPSTALLS=9
rCLRTOGS=10
rEPIRQ=11
rEPIEN=12
rUSBIRQ=13
rUSBIEN=14
rUSBCTL=15
rCPUCTL=16
rPINCTL=17
rREVISION=18
rFNADDR=19
rIOPINS=20
rIOPINS1=20  #Same as rIOPINS
rIOPINS2=21
rHIRQ=25
rHIEN=26
rMODE=27
rPERADDR=28
rHCTL=29
rHXFR=30
rHRSL=31

#Host mode registers.
rRCVFIFO =1
rSNDFIFO =2
rRCVBC   =6
rSNDBC   =7
rHIRQ    =25


# R11 EPIRQ register bits
bmSUDAVIRQ =0x20
bmIN3BAVIRQ =0x10
bmIN2BAVIRQ =0x08
bmOUT1DAVIRQ= 0x04
bmOUT0DAVIRQ= 0x02
bmIN0BAVIRQ =0x01

# R12 EPIEN register bits
bmSUDAVIE   =0x20
bmIN3BAVIE  =0x10
bmIN2BAVIE  =0x08
bmOUT1DAVIE =0x04
bmOUT0DAVIE =0x02
bmIN0BAVIE  =0x01




# ************************
# Standard USB Requests
SR_GET_STATUS       =0x00   # Get Status
SR_CLEAR_FEATURE    =0x01   # Clear Feature
SR_RESERVED     =0x02   # Reserved
SR_SET_FEATURE      =0x03   # Set Feature
SR_SET_ADDRESS      =0x05   # Set Address
SR_GET_DESCRIPTOR   =0x06   # Get Descriptor
SR_SET_DESCRIPTOR   =0x07   # Set Descriptor
SR_GET_CONFIGURATION    =0x08   # Get Configuration
SR_SET_CONFIGURATION    =0x09   # Set Configuration
SR_GET_INTERFACE    =0x0a   # Get Interface
SR_SET_INTERFACE    =0x0b   # Set Interface

# Get Descriptor codes  
GD_DEVICE       =0x01   # Get device descriptor: Device
GD_CONFIGURATION    =0x02   # Get device descriptor: Configuration
GD_STRING       =0x03   # Get device descriptor: String
GD_HID                  =0x21   # Get descriptor: HID
GD_REPORT           =0x22   # Get descriptor: Report

# SETUP packet header offsets
bmRequestType           =0
bRequest                =1
wValueL         =2
wValueH         =3
wIndexL         =4
wIndexH         =5
wLengthL        =6
wLengthH        =7

# HID bRequest values
GET_REPORT      =1
GET_IDLE        =2
GET_PROTOCOL            =3
SET_REPORT      =9
SET_IDLE        =0x0A
SET_PROTOCOL            =0x0B
INPUT_REPORT            =1

# PINCTL bits
bmEP3INAK   =0x80
bmEP2INAK   =0x40
bmEP1INAK   =0x20
bmFDUPSPI   =0x10
bmINTLEVEL  =0x08
bmPOSINT    =0x04
bmGPXB      =0x02
bmGPXA      =0x01

# rUSBCTL bits
bmHOSCSTEN  =0x80
bmVBGATE    =0x40
bmCHIPRES   =0x20
bmPWRDOWN   =0x10
bmCONNECT   =0x08
bmSIGRWU    =0x04

# USBIRQ bits
bmURESDNIRQ =0x80
bmVBUSIRQ   =0x40
bmNOVBUSIRQ =0x20
bmSUSPIRQ   =0x10
bmURESIRQ   =0x08
bmBUSACTIRQ =0x04
bmRWUDNIRQ  =0x02
bmOSCOKIRQ  =0x01

# MODE bits
bmHOST          =0x01
bmLOWSPEED      =0x02
bmHUBPRE        =0x04
bmSOFKAENAB     =0x08
bmSEPIRQ        =0x10
bmDELAYISO      =0x20
bmDMPULLDN      =0x40
bmDPPULLDN      =0x80

# PERADDR/HCTL bits
bmBUSRST        =0x01
bmFRMRST        =0x02
bmSAMPLEBUS     =0x04
bmSIGRSM        =0x08
bmRCVTOG0       =0x10
bmRCVTOG1       =0x20
bmSNDTOG0       =0x40
bmSNDTOG1       =0x80

# rHXFR bits
# Host XFR token values for writing the HXFR register (R30).
# OR this bit field with the endpoint number in bits 3:0
tokSETUP  =0x10  # HS=0, ISO=0, OUTNIN=0, SETUP=1
tokIN     =0x00  # HS=0, ISO=0, OUTNIN=0, SETUP=0
tokOUT    =0x20  # HS=0, ISO=0, OUTNIN=1, SETUP=0
tokINHS   =0x80  # HS=1, ISO=0, OUTNIN=0, SETUP=0
tokOUTHS  =0xA0  # HS=1, ISO=0, OUTNIN=1, SETUP=0 
tokISOIN  =0x40  # HS=0, ISO=1, OUTNIN=0, SETUP=0
tokISOOUT =0x60  # HS=0, ISO=1, OUTNIN=1, SETUP=0

# rRSL bits
bmRCVTOGRD   =0x10
bmSNDTOGRD   =0x20
bmKSTATUS    =0x40
bmJSTATUS    =0x80
# Host error result codes, the 4 LSB's in the HRSL register.
hrSUCCESS   =0x00
hrBUSY      =0x01
hrBADREQ    =0x02
hrUNDEF     =0x03
hrNAK       =0x04
hrSTALL     =0x05
hrTOGERR    =0x06
hrWRONGPID  =0x07
hrBADBC     =0x08
hrPIDERR    =0x09
hrPKTERR    =0x0A
hrCRCERR    =0x0B
hrKERR      =0x0C
hrJERR      =0x0D
hrTIMEOUT   =0x0E
hrBABBLE    =0x0F

# HIRQ bits
bmBUSEVENTIRQ   =0x01   # indicates BUS Reset Done or BUS Resume     
bmRWUIRQ        =0x02
bmRCVDAVIRQ     =0x04
bmSNDBAVIRQ     =0x08
bmSUSDNIRQ      =0x10
bmCONDETIRQ     =0x20
bmFRAMEIRQ      =0x40
bmHXFRDNIRQ     =0x80