# under yyyy-mm-dd directory
# move bias, dark, flat to 'calib'
# file header summary
import os,sys
import pwd
import astropy.io.fits as fits
import glob
import numpy as np
from pyraf import iraf
iraf.noao()
iraf.imred()
iraf.ccdred()

datestr=os.getcwd().split('/')[-1]
gethead='gethead *.fit IMAGETYP OBJECT DATE-OBS EXPTIME > file_header_summary_'+datestr+'.txt'
os.system(gethead)
os.system('cat file_header_summary_'+datestr+'.txt') # object image file summary

os.chdir('calib_HDR')
##=====================================================================================
def hdrfix(im, key, val, comment=''):
    fits.setval(im,key,value=val,comment=comment)
    '''
    fits.setval(
    filename,
    keyword,
    *args,
    value=None,
    comment=None,
    before=None,
    after=None,
    savecomment=False,
    **kwargs,)
    '''
##=====================================================================================


def imcombine(flist, outname, mode='median'):
    # iraf.imcombine.lParam() check
    print(str(len(flist)) ,'files will be stacked')
    iraf.imcombine(input=','.join(flist),
                    output=outname,
                    combine='median',
                    reject='crreject',
                    scale='none', 
                    zero='mode',
                    )
    print(outname, 'is created')

##=====================================================================================
def darkcom(dlist, exptime):
    flist=[]
    flist=[s for s in dlist if fits.getheader(s)['EXPTIME']==exptime]
    print(len(flist),'files','\n',flist)
    outname='master_dark_'+str(exptime)+'_'+datestr+'.fit'
    imcombine(flist, outname)
    print(outname, 'created')
##=====================================================================================
def imarith(im1,op,im2,result):
    iraf.imarith(operand1=im1,
                op=op,
                operand2=im2,
                result=result,
                verbose='yes')

##=====================================================================================
caliblist=glob.glob('*.fit')
darklist= [s for s in caliblist if fits.getheader(s)['IMAGETYP']=='Dark Frame']
print(darklist)
expt=[]
for i in darklist:
    expt.append(fits.getheader(i)['EXPTIME'])
print(expt)
set(expt)
darkexpt=list(set(expt))
print('dark exptimes are','\n',sorted(darkexpt))

for i in darkexpt:
	darkcom(darklist,i)
mdarklist=sorted(glob.glob('master_dark*.fit')) 
for i in mdarklist:
    print(i, np.mean(fits.getdata(i)))                   

##=====================================================================================
twflatlist=glob.glob('tw*.fit')
masterdark='../calib_MRG/master_dark_1.0_2023-05-31.fit'
for i in twflatlist:
    print(i, np.mean(fits.getdata(i)))
expt=[]
for i in twflatlist:
    expt.append(fits.getheader(i)['EXPTIME'])
print(expt)
set(expt)
twflatexpt=list(set(expt))
print('twillight flat exptimes are','\n',sorted(twflatexpt))    
print(len(twflatlist), 'twillight flat files')

for i in twflatlist:
    imarith(i,'-',masterdark,'d'+i)
twflatlist=glob.glob('dtw*.fit')
imcombine(twflatlist,'master_twflat_'+datestr+'.fit')
imarith('master_twflat_'+datestr+'.fit',
        '/',
        np.mean(fits.getdata('master_twflat_'+datestr+'.fit')),
        'n_master_twflat_'+datestr+'.fit')
print ('n_master_twflat_'+datestr+'.fit', 'std value is', 
        np.std(fits.getdata('n_master_twflat_'+datestr+'.fit')))

##=====================================================================================
# object pre-processing
#os.chdir('../')
objlist=glob.glob("*.fit")
#objlist=glob.glob("M3*.fit")
#objlist=glob.glob("moon*HDR*.fit")
#objlist=glob.glob("NGC*.fit")

expt=[]
for i in objlist:
    expt.append(fits.getheader(i)['EXPTIME'])
set(expt)
objexpt=sorted(list(set(expt)))
print(objexpt)

def imarith(f1, op, f2, r):
	iraf.imarith(operand1=f1,op=op,operand2=f2, result=r+f1, verbose='yes')

calib_directory='calib/'
twflat_directory='twflat_HDR/'
mdarklist=sorted(glob.glob(calib_directory+'master_dark*.fit')) 
for t in objexpt:
    olist=sorted([s for s in objlist if fits.getheader(s)['EXPTIME']==t])
    darkim=[d for d in mdarklist if fits.getheader(d)['EXPTIME']==t][0]
    for i in olist:
    	imarith(i, '-', darkim, 'd_')


objlist=sorted(glob.glob("d_*.fit"))
twflat='calib/n_master_twflat_2023-05-31_HDR.fit'
for i in objlist:
	imarith(i,'/', twflat,'f')


# astrometry
############################################################

import os, sys
ra, dec = 210.798123, 54.369925 # M101

def solveim(inim):
    #solve='solve-field '+ inim + ' --scale-low 1.8 --scale-high 2.0 --scale-unit app'+ ' --no-plot' + ' --overwrite' + ' --fits-image'+ ' --new-fits a'+inim + ' --ra '+str(ra)+' --dec '+str(dec) + ' --use-source-extractor' + ' --source-extractor-config ../default.sex'+ ' --source-extractor-path /usr/local/bin/sex'+' --crpix-center' +' --x-column X_IMAGE --y-column Y_IMAGE --sort-column MAG_AUTO --sort-ascending' + ' --radius 1' 
    solve='solve-field '+ inim + ' --scale-low 1.8 --scale-high 2.0 --scale-unit app'+ ' --no-plot' + ' --overwrite' + ' --fits-image'+ ' --new-fits a'+inim + ' --use-source-extractor' + ' --source-extractor-config /data0/pathfinder/OBS/default.sex'+ ' --source-extractor-path /usr/local/bin/sex'+' --crpix-center' +' --x-column X_IMAGE --y-column Y_IMAGE --sort-column MAG_AUTO --sort-ascending' + ' --radius 1' 
    os.system(solve)

objlist=glob.glob('fd*.fit')


for n,i in enumerate(objlist) : 
	print(n+1,'of',len(objlist), i)
	solveim(i)    
os.system('rm *.xyls *.corr *.match *.wcs *.axy *.rdls *.solved')
############################################################
# file name change
# object_pathfinder_exptime_filter_yyyymmdd-hhmmss.fit
# move to RED data dirctory
redlist=glob.glob('afd*.fit')

for i in redlist:
    newname=i.split('-')[0][4:]+'_KPF_'+str(fits.getheader(i)['exptime'])+'_L_'+fits.getheader(i)['DATE-OBS'][:-3]+'.fit'
    print(i, 'to', newname)
    os.system('cp '+i+' '+newname)


############################################################
# simple PSF + photometry + catalog + zero point + limit mag




