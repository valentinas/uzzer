import sys, time, string, cStringIO, struct, glob, os, warnings, random;
from const import *;
from maxusb import maxusb;


#in order to run this need to call following methods:
#uzzer=uzzer()
#uzzer.fuzz()


class uzzer(maxusb):
    
    def fuzz(self):
    	"""Reset connection before starting fuzzing"""
        self.serInit();
        self.MAXUSBsetup();
        for i in range(0,1000):
            self.unhandled=0;
            random.seed(i);
            self.fuzzerrun();

    def fuzzerrun(self):
        """Main loop of the USB connection."""
        print "Starting a HID device.  This won't return.";
        self.reset_connection()
        while 1:
            self.service_irqs();
            if self.unhandled>20:
                return;

    def service_irqs(self):
        """Handle USB interrupt events."""
        epirq=self.rreg(rEPIRQ);
        usbirq=self.rreg(rUSBIRQ);
        
        
        #Are we being asked for setup data?
        if(epirq&bmSUDAVIRQ): #Setup Data Requested
            self.wreg(rEPIRQ,bmSUDAVIRQ); #Clear the bit
            self.do_SETUP();
            print "doing setup";
            self.unhandled=0;
        #if(epirq&bmOUT1DAVIRQ): #OUT1-OUT packet
        #    self.do_OUT1();
        #    self.wreg(rEPIRQ,bmOUT1DAVIRQ); #Clear the bit *AFTER* servicing.
        #if(epirq&bmIN3BAVIRQ): #IN3-IN packet
        #    self.do_IN3();
        #    #self.wreg(rEPIRQ,bmIN3BAVIRQ); #Clear the bit
        #if(epirq&bmIN2BAVIRQ): #IN2 packet:
        #    self.do_IN2();
        #    #self.wreg(rEPIRQ,bmIN2BAVIRQ); #Clear the bit
        else:
            print "stalling at service_IRQs Unhandled IRQ: %(irq)02x, number %(num)d" % {"irq":epirq, "num":self.unhandled};
            self.STALL_EP0();
            self.unhandled+=1;



    def do_SETUP(self):
        """Handle USB Enumeration"""
        
        #Grab the SETUP packet from the buffer.
        SUD=self.readbytes(rSUDFIFO,8);
        
        self.OsLastConfigType=ord(SUD[bmRequestType]);
        self.typepos=0;
        setuptype=(ord(SUD[bmRequestType])&0x60);
        if setuptype==0x00:
            self.std_request(SUD);
        #elif setuptype==0x20:
        #    self.class_request(SUD);
        #elif setuptype==0x40:
        #    self.vendor_request(SUD);
        else:
            print "Stalling at do_SETUP Unknown request type 0x%02x." % ord(SUD[bmRequestType])
            self.STALL_EP0(SUD);

    def std_request(self,SUD):
        """Handles a standard setup request."""
        setuptype=ord(SUD[bRequest]);
        if setuptype==SR_GET_DESCRIPTOR: 
        	self.send_descriptor(SUD);
        #elif setuptype==SR_SET_FEATURE:
        #    self.rregAS(rFNADDR);
        #    # self.feature(1);
        #elif setuptype==SR_SET_CONFIGURATION: self.set_configuration(SUD);
        #elif setuptype==SR_GET_STATUS: self.get_status(SUD);
        #elif setuptype==SR_SET_ADDRESS: self.rregAS(rFNADDR);
        #elif setuptype==SR_GET_INTERFACE: self.get_interface(SUD);
        else:
            print "Stalling at std_request Unknown standard setup request type %02x" % setuptype;
            self.STALL_EP0(SUD);
        
    def send_descriptor(self,SUD):
        """Send the USB descriptors based upon the setup data."""
        desclen=0;
        reqlen=ord(SUD[wLengthL])+256*ord(SUD[wLengthH]); #16-bit length
        desctype=ord(SUD[wValueH]);
        
        if desctype==GD_DEVICE:
            dd = self.gen_dd();
            desclen=len(dd);
            ddata=dd;
        #elif desctype==GD_CONFIGURATION:
        #    desclen=self.CD[2];
        #    ddata=self.CD;
        #elif desctype==GD_STRING:
        #    desclen=ord(self.strDesc[ord(SUD[wValueL])][0]);
        #    ddata=self.strDesc[ord(SUD[wValueL])];
        #elif desctype==GD_HID:
        #    #Don't know how to do this yet.
        #    pass;
        #elif desctype==GD_REPORT:
        #    desclen=self.CD[25];
        #    ddata=self.RepD;
        #TODO Configuration, String, Hid, and Report
        
        print "sending device descriptor:" + str(ddata);
        
        if desclen>0:
            #Reduce desclen if asked for fewer bytes.
            desclen=min(reqlen,desclen);
            #Send those bytes.
            self.writebytes(rEP0FIFO,ddata[0:desclen]);
            self.wregAS(rEP0BC,desclen);
        else:
            print "Stalling in send_descriptor() for lack of handler for %02x." % desctype;
            self.STALL_EP0(SUD);

    def gen_dd(self):
        """generates a device descriptor
        the packet is always 18 bytes long"""
        return [
        	self.fuzz_byte(18), #length = 18d = 12h
        	0x01,	#descriptor type = device descriptor = 0x01 http://www.beyondlogic.org/usbnutshell/usb5.shtml
        	self.fuzz_byte(0x00), self.fuzz_byte(0x01), #USB version that device complies to
        	self.fuzz_byte(0x00), self.fuzz_byte(0x00), self.fuzz_byte(0x00), 	# bDeviceClass, bDeviceSubClass, bDeviceProtocol
        	self.fuzz_byte(0x40),			# bMaxPacketSize0 EP0 is 64 bytes
        	self.fuzz_rand_byte(), self.fuzz_rand_byte(),		# idVendor(L/H)--Maxim is 0B6A
        	self.fuzz_rand_byte(), self.fuzz_rand_byte(),		# idProduct(L/H)--5346
        	self.fuzz_rand_byte(), self.fuzz_rand_byte(),		# bcdDevice--1234
        	self.fuzz_rand_byte(), self.fuzz_rand_byte(), self.fuzz_rand_byte(),			# iManufacturer, iProduct, iSerialNumber
        	self.fuzz_byte(1)];
        	
    def gen_cd(self):
    	"""Generates a configuration descriptor
    	
    	The device descriptor tells the host how many configurations are available.
    	
    	The whole hierarchy looks like this:
    	
    	-Device Descriptor (gen_dd) 
    	|__
    		conf descriptor 1 (get_cd)
    		|
    		|__
    		|	Interface 0 Descriptor (still part of cd)
    		|	|
    		|	|__
    		|	|	Endpoint Descriptor (still part of cd)
    		|	|__
    		|		Endpoint Descriptor (still part of cd)	
    		|
    		|__
    		|	Interface 1 Descriptor (still part of cd)
    		|	|
    		|	|__
    		|	|	Endpoint Descriptor (still part of cd)
    		|	|__
    		|		Endpoint Descriptor (still part of cd)
    		|
    		conf descriptor 2 (get_cd)
    		|
    		|__
    		|	Interface 0 Descriptor (still part of cd)
    		|	|
    		|	|__
    		|	|	Endpoint Descriptor (still part of cd)
    		|	|__
    		|
    		
    		.....
    	
    	"""
    	return [
    		self.fuzz_byte(0x09),			# bLength
    	
    	];
    
        
    def fuzz_byte(self, value):
    	"""fuzz a bit. 1=leave as is, 2=bitflip, 3=generate new"""
    	action = random.randint(1,10);
    	if action==1:
    		return random.randint(0,255);
    	elif action==2:
    		return self.bitflip_byte(value);
    	else:
    		return value;
    		
    def fuzz_rand_byte(self):
    	return self.fuzz_byte(random.randint(0,255));
    
    def bitflip_byte(self, value):
        order = 8; #the more order, the less fuzzy. with order=8 it will flip about one bit in eight
        for i in range(0,8):
        	if random.randint(1,8)==1:
        		value=value ^ 2**i; #flip the bit
        return value;
    	
fuzzer=uzzer();
fuzzer.fuzz();   	
