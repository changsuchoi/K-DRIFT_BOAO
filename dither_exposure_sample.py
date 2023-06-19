# Dithring and exposure script

# telescope PWI4

# camera MaximDL win32com

# after autofocus

# offset_size

# offset pattern

# camera exposure time

# file saving

# time wait

from pwi4_client import PWI4
import time 
import win32com.client

def pwi_connect():
    print("Connecting to PWI4...")
    pwi4 = PWI4()
    s = pwi4.status()
    print("Mount connected:", s.mount.is_connected)
    if not s.mount.is_connected:
        print("Connecting to mount...")
        s = pwi4.mount_connect()
        print("Mount connected:", s.mount.is_connected)

def slew(ra=rahour, dec=decdeg):
    print("Slewing...")
    pwi4.mount_goto_ra_dec_j2000(rahour, decdeg)
    while True:
        s = pwi4.status()

        print("RA: %.5f hours;  Dec: %.4f degs, Axis0 dist: %.1f arcsec, Axis1 dist: %.1f arcsec" % (
            s.mount.ra_j2000_hours, 
            s.mount.dec_j2000_degs,
            s.mount.axis0.dist_to_target_arcsec,
            s.mount.axis1.dist_to_target_arcsec
            ))
        if not s.mount.is_slewing:
            break
        time.sleep(0.2)
    print("Slew complete. Stopping...")

def offset(raoff, decoff):
    pwi4.mount_offset(axis0_add_arcsec=raoff, axis1_add_arcsec=decoff)

def spiral_new(x_step, y_step):
    pwi4.mount_spiral_offset_new(self, x_step_arcsec, y_step_arcsec)
def offset_next():
    pwi4.mount_spiral_offset_next(self)

# test script : MaximDL win32com
#--------------------------------------------------
import time
import win32com.client

ERROR = True
NOERROR = False

##------------------------------------------------------------------------------
## Class: cCamera
##------------------------------------------------------------------------------
class cCamera:
    def __init__(self):
        print "Connecting to MaxIm DL..."
        self.__CAMERA = win32com.client.Dispatch("MaxIm.CCDCamera")
        self.__CAMERA.DisableAutoShutdown = True
        try:
            self.__CAMERA.LinkEnabled = True
        except:
            print "... cannot connect to camera"
            print "--> Is camera hardware attached?"
            print "--> Is some other application already using camera hardware?"
            raise EnvironmentError, 'Halting program'
        if not self.__CAMERA.LinkEnabled:
            print "... camera link DID NOT TURN ON; CANNOT CONTINUE"
            raise EnvironmentError, 'Halting program'

    def exposeLight(self,length,filterSlot):
        print "Exposing light frame..."
        self.__CAMERA.Expose(length,1,filterSlot)
        while not self.__CAMERA.ImageReady:
            time.sleep(1)
        print "Light frame exposure and download complete!"

    def setFullFrame(self):
        self.__CAMERA.SetFullFrame()
        print "Camera set to full-frame mode"
        
    def setBinning(self,binmode):
        tup = (1,2,3)
        if binmode in tup:
            self.__CAMERA.BinX = binmode
            self.__CAMERA.BinY = binmode
            print "Camera binning set to %dx%d" % (binmode,binmode)
            return NOERROR
        else:
            print "ERROR: Invalid binning specified"
            return ERROR
            
##
##    END OF 'cCamera' Class
##
#--------------------------------------------------
import win32com.client
import time
import os
from pwi4_client import PWI4
cam=win32com.client.Dispatch("MaxIm.CCDCamera")
cam.LinkEnabled = True

def expose(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target):
    cam.Expose(exptime, 1,) # duration (sec), light=1, filter
    time.sleep(0.5)
    #if cam.ImageReady : print('done')
    while cam.ImageReady:
        time.sleep(exptime+2)
    print ("Light frame exposure and download complete!")
def saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target):
    if cam.ImageReady :
        cam.SetFITSKey(hdrkey, hdrvalue)
        cam.SetFITSKey('OBJECT', target)
        cam.SaveImage(os.getcwd()+'\\'+im_name)

# micro movement
# move to target
# raoff, decoff = 1,1 arcsec
from astropy import units as u
from astropy.coordinates import SkyCoord
hdrkey='MICRO'
numb= 1
target='M101'
rahms='14:03:12.58301' 
decdms='+54:20:55.5000'
# c = SkyCoord('00 42 30 +41 12 00', unit=(u.hourangle, u.deg))
# c = SkyCoord(rad+' '+decd, unit=(u.deg, u.deg), frame='icrs')
c = SkyCoord(rahms+' '+decdms, unit=(u.hourangle, u.deg), frame='icrs')
rahour = c.ra.hour
decdeg = c.dec.deg
hdrkey='MICRO'
exptime=6
numb= 1
im_name = target+'_'+'micro'+'_'+str(numb).zfill(4)+'.fit'
slew(rahour, decdeg) # initial slew
time.sleep(10)
expose(im_name, exptime, hdrkey='MICRO', hdrvalue='INIT')
time.sleep(exptime+2)
cam.SetFITSKey('MICRO', 'INIT')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target)
offset(1, 0)
time.sleep(2)
numb+=1
im_name = target+'_'+'micro'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='MICRO', hdrvalue='E1s')
time.sleep(exptime+2)
cam.SetFITSKey('MICRO', 'E1s')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target)
offset(-2, 0)
time.sleep(2)
numb+=1
im_name = target+'_'+'micro'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='MICRO', hdrvalue='W1s')
time.sleep(exptime+2)
cam.SetFITSKey('MICRO', 'W1s')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target)
offset(1, 1)
time.sleep(2)
numb+=1
im_name = target+'_'+'micro'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='MICRO', hdrvalue='N1s')
time.sleep(exptime+2)
cam.SetFITSKey('MICRO', 'N1s')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target)
offset(0, -2)
time.sleep(2)
numb+=1
im_name = target+'_'+'micro'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='MICRO', hdrvalue='S1s')
time.sleep(exptime+2)
cam.SetFITSKey('MICRO', 'S1s')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='test',target=target)
offset(0, 1) # original position
time.sleep(2)
print('Micro stepping is done')


# spiral offset 
hdrkey = 'SPIRAL'
offset_step   = 600 # 10arcmin * 60 = 600 arcsec
target='M101'
rahms='14:03:12.58301' 
decdms='+54:20:55.5000'
# c = SkyCoord('00 42 30 +41 12 00', unit=(u.hourangle, u.deg))
# c = SkyCoord(rad+' '+decd, unit=(u.deg, u.deg), frame='icrs')
c = SkyCoord(rahms+' '+decdms, unit=(u.hourangle, u.deg), frame='icrs')
rahour = c.ra.hour
decdeg = c.dec.deg
exptime=2
numb= 1
slew(rahour, decdeg) # initial slew
time.sleep(10)

im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'INIT')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='INIT_0',target=target)
time.sleep(1)
numb+=1
print('#1', 'INIT position')

offset(offset_step, 0)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'E1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='E1_step',target=target)
time.sleep(1)
numb+=1
print('#2', 'E', offset_step)

offset(0, offset_step)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'E1N1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='E1N1_step',target=target)
time.sleep(1)
numb+=1
print('#3', 'E, N', offset_step )

offset(offset_step * -1, 0)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'N1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='N1_step',target=target)
time.sleep(1)
numb+=1
print('#4', 'N', offset_step )

offset(offset_step * -1, 0)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'W1N1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='W1N1_step',target=target)
time.sleep(1)
numb+=1
print('#5', 'W, N', offset_step )

offset(0, offset_step * -1)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'W1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='W1_step',target=target)
time.sleep(1)
numb+=1

print('#6', 'W', offset_step )

offset(0, offset_step * -1)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'W1S1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='W1S1_step',target=target)
time.sleep(1)
numb+=1

print('#7', 'W, S', offset_step )

offset(offset_step, 0)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'S1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='S1_step',target=target)
time.sleep(1)
numb+=1
print('#8', 'S', offset_step )

offset(offset_step, 0)
time.sleep(10)
im_name = target+'_'+'spiral'+'_'+str(numb).zfill(4)+'.fit'
expose(im_name, exptime, hdrkey='', hdrvalue='')
time.sleep(exptime+2)
cam.SetFITSKey('SPIRAL', 'E1S1_step')
cam.SetFITSKey('TELESCOP', 'K-DRIFT PATHFINDER')
cam.SetFITSKey('OBSERVER', 'Changsu Choi')
saveim(im_name, exptime, hdrkey='SCRIPT', hdrvalue='E1S1_step',target=target)
time.sleep(1)
numb+=1
print('#9', 'E, S', offset_step )

print('The last position', 'The 9 spiral exposure set is done')

offset(offset_step * -1, offset_step)
print('Return to INIT position')




'''
https://wt5l.wordpress.com/2016/07/23/automated-astrophotography-with-python-part-1a/
https://cdn.diffractionlimited.com/help/maximdl/Scripting.htm
https://cdn.diffractionlimited.com/help
maximDL manual
'''    

