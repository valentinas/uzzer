from GoodFET import GoodFET;
from const import *;

class maxusb(GoodFET):
    OsLastConfigType=-1;
    MAXUSBAPP=0x40
    usbverbose=False;
    
    def wreg(self,reg,value):
        """Poke 8 bits into a register."""
        data=[(reg<<3)|2,value];
        self.writecmd(self.MAXUSBAPP,0x00,len(data),data);        
        return value;
        
    def MAXUSBsetup(self):
        """Move the FET into the MAXUSB application."""
        self.writecmd(self.MAXUSBAPP,0x10,0,self.data); #MAXUSB/SETUP
        self.writecmd(self.MAXUSBAPP,0x10,0,self.data); #MAXUSB/SETUP
        self.writecmd(self.MAXUSBAPP,0x10,0,self.data); #MAXUSB/SETUP
        print "Connected to MAX342x Rev. %x" % (self.rreg(rREVISION));
        self.wreg(rPINCTL,0x18); #Set duplex and negative INT level.
        
    def usb_disconnect(self):
        """Disconnect the USB port."""
        self.wreg(rUSBCTL,bmVBGATE);

    def usb_connect(self):
        """Connect the USB port.""" 
        #disconnect D+ pullup if host turns off VBUS
        self.wreg(rUSBCTL,bmVBGATE|bmCONNECT);
        
    def readbytes(self,reg,length):
        """Peek some bytes from a register."""
        data=[(reg<<3)]+range(0,length);
        self.writecmd(self.MAXUSBAPP,0x00,len(data),data);
        toret=self.data[1:len(self.data)];
        ashex="";
        for foo in toret:
            ashex=ashex+(" %02x"%ord(foo));
        if self.usbverbose: print "GET   %02x==%s" % (reg,ashex);
        return toret;
        
    def reset_connection(self):
    	"""The USB is soft disconnected and then connected back
    	again in order to get a clean slate for fuzzing"""
        self.usb_disconnect();
        self.usb_connect();
    
    def rreg(self,reg):
        """Peek 8 bits from a register."""
        data=[reg<<3,0];
        self.writecmd(self.MAXUSBAPP,0x00,len(data),data);
        return ord(self.data[1]);
        
    def STALL_EP0(self,SUD=None):
        """Stall for an unknown SETUP event."""
        if SUD==None:
            print "Stalling EP0.";
        else:
            print "Stalling EP0 for %s" % self.setup2str(SUD);
        self.wreg(rEPSTALLS,0x23); #All three stall bits.
        
    def writebytes(self,reg,tosend):
        """Poke some bytes into a register."""
        data="";
        if type(tosend)==str:
            data=chr((reg<<3)|3)+tosend;
            if self.usbverbose: print "PUT %02x:=%s (0x%02x bytes)" % (reg,tosend,len(data))
        else:
            data=[(reg<<3)|3]+tosend;
            ashex="";
            for foo in tosend:
                ashex=ashex+(" %02x"%foo);
            if self.usbverbose: print "PUT %02x:=%s (0x%02x bytes)" % (reg,ashex,len(data))
        self.writecmd(self.MAXUSBAPP,0x00,len(data),data);
        
    def wregAS(self,reg,value):
        """Poke 8 bits into a register, setting AS."""
        data=[(reg<<3)|3,value];
        self.writecmd(self.MAXUSBAPP,0x00,len(data),data);        
        return value;
        
    def setup2str(self,SUD):
        """Converts the header of a setup packet to a string."""
        return "bmRequestType=0x%02x, bRequest=0x%02x, wValue=0x%04x, wIndex=0x%04x, wLength=0x%04x" % (
                ord(SUD[0]), ord(SUD[1]),
                ord(SUD[2])+(ord(SUD[3])<<8),
                ord(SUD[4])+(ord(SUD[5])<<8),
                ord(SUD[6])+(ord(SUD[7])<<8)
                );