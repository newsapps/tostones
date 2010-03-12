#!/bin/env python

import os
import shutil

SKIP = [
    'favicon.ico',
    'images',
    'javascripts',
    'stylesheets',
    ]

try:
    os.remove('out/tables/index.html')
except:
    pass

for i in os.listdir('out/tables'):    
    if i in SKIP:
        continue
        
    folder = os.path.join('out/tables', i)
    index = os.path.join(folder, 'index.html')
    shutil.copyfile(index, 'out/tables/%s.html' % i)
    
    os.remove(index)
    os.rmdir(folder)
