import astropy.io.fits as fits
import astropy.io.ascii as ascii
import os, sys
import glob
import numpy as np


s_ext_config_dir = '/data0/pathfinder/OBS/'
config_file      = s_ext_config_dir+ 'KPF_simplephot.sex'
param_file       = s_ext_config_dir+ 'KPF_simplephot.param'
conv_file        = s_ext_config_dir+ 'default.conv'
nnw_file         = s_ext_config_dir+ 'default.nnw'

inlist = sorted(glob.glob('*KPF*.fit'))

for j,i in enumerate(inlist):
    print('#'*80)
    print(j, len(inlist),'\n',i)
    fn=os.path.splitext(i)[0]
    s_ext_line='sex '+i+' -c '+ config_file+ ' -CATALOG_NAME '+fn+'_simple_phot.cat' + ' -FILTER_NAME '+conv_file + ' -STARNNW_NAME '+nnw_file + ' -PARAMETERS_NAME '+param_file
    s_ext_line='sex '+i+' -c '+ config_file+ ' -CATALOG_NAME '+fn+'_simple_phot.cat' +' -PSF_NAME '+fn+'.psf' + ' -FILTER_NAME '+conv_file + ' -STARNNW_NAME '+nnw_file + ' -PARAMETERS_NAME '+param_file
    os.system(s_ext_line)

#options will be added later