# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 20:32:10 2021
Helper functions
@author: crisj
"""
import sys
#sys.path.append('C:\Users\vaak\.snap\auxdata\snaphu-v1.4.2_win64\bin')
#sys.path.append('C:\\Users\\vaak\\.snap\\snap-python\snappy')
sys.path.append('C:\\Users\\crisj\\.snap\\snap-python\\snappy')
sys.path.append('C:\\Users\\crisj\\.conda\\envs\\snap_env\\Lib') # anaconda environment created for this script was 'snap_env'
from snappy import jpy
from snappy import GPF
from snappy import ProductIO
from snappy import HashMap
import os
import glob

def read(filename):
    print('Reading...')
    return ProductIO.readProduct(filename)
#%% Explore operators
def listParams(operator_name):
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    op_spi = GPF.getDefaultInstance().getOperatorSpiRegistry().getOperatorSpi(operator_name)
    print('Op name:', op_spi.getOperatorDescriptor().getName())
    print('Op alias:', op_spi.getOperatorDescriptor().getAlias())
    param_Desc = op_spi.getOperatorDescriptor().getParameterDescriptors()
    for param in param_Desc:
        print(param.getName())
    
#listParams(\"TOPSAR-Split\") # change the operator here\n",
#print(listParams("Terrain-correction")) # change the operator here
#listParams(\"Enhanced-Spectral-Diversity\") # change the operator here"
#print(listParams("Multilook")) # change the operator here
#print(listParams("snaphu-unwrapping"))
#print(listParams("SnaphuExport"))
#print(listParams("ToolAdapterOp"))
print(listParams("PhaseToDisplacement"))
#%% Print reader and writer formats
# e.g. ProductIO.writeProduct(product, filename + '.dim', 'BEAM-DIMAP')
# e.g. ProductIO.writeProduct(output, SNAPHU_exp_folder, 'Snaphu')
ProductIOPlugInManager = jpy.get_type('org.esa.snap.core.dataio.ProductIOPlugInManager')
ProductReaderPlugIn = jpy.get_type('org.esa.snap.core.dataio.ProductReaderPlugIn')
ProductWriterPlugIn = jpy.get_type('org.esa.snap.core.dataio.ProductWriterPlugIn')

read_plugins = ProductIOPlugInManager.getInstance().getAllReaderPlugIns()
write_plugins = ProductIOPlugInManager.getInstance().getAllWriterPlugIns()

print('Writer formats')
while write_plugins.hasNext():
    plugin = write_plugins.next()
    print('  ', plugin.getFormatNames()[0])

print('Reader formats')
while read_plugins.hasNext():
    plugin = read_plugins.next()
    print('  ', plugin.getFormatNames()[0])

#%%
"""
Doing phase unwrapping with snappy is tricky. You need to configure your python to recognise shaphu exe file first as follows.

snaphu_dir = 'C:\\Users\\vaak\\.snap\\auxdata\\snaphu-v1.4.2_win64\\bin\\snaphu.exe'


You need to specify your temporary folder where the unrwapping files will be stored. 
SNAP has some default folder for phase unwrapping.
You can make your own, but remember to change it inside SNAP where you want to have this temporary folder.
You can then export snaphu using snappy paramters as follows. The input file is a filtered interferogram.
"""    
snaphu_dir = 'C:\\Users\\crisj\\.snap\\auxdata\\snaphu-v1.4.2_win64\\bin\\snaphu.exe'
# Snaphu export
#Fname='subset_0_of_InSAR_pipeline_II'
#TempFolder = 'D:\\PhD Info\\InSAR\\Examples\\SNAPPY_Ecuador_Galapagos\\exp_subset\\'
#Product = read(os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos',Fname+'.dim')) # reads .dim 
#Fpath = 'D:\PhD Info\InSAR\Examples\Hawai Earthquake - RUS video\Test2'
#Fname='Orb_Stack_Ifg_Deb_Flt_ML_DInSAR'
#TempFolder = 'D:\PhD Info\InSAR\Examples\Hawai Earthquake - RUS video\Test2\exp_snappy'

       
# exp
Fpath = 'D:\PhD Info\InSAR\Examples\Japan Earthquake - Alaska tutorial\Test2\Smaller'
Fname = 'subset_0_of_Orb_Stack_ifg_deb_dinsar_ML_flt'
TempFolder = 'D:\PhD Info\InSAR\Examples\Japan Earthquake - Alaska tutorial\Test2\Smaller\exp_snappy'


Product = read(os.path.join(Fpath,Fname+'.dim')) # reads .dim 
params      = HashMap()
params.put("targetFolder", TempFolder)
params.put("statCostMode", "DEFO")
params.put("initMethod", "MCF")
params.put("numberOfTileRows", 10)
params.put("numberOfTileCols", 10)
params.put("numberOfProcessors", 4)
params.put("rowOverlap", 0)
params.put("colOverlap", 0)
params.put("tileCostThreshold", 500)
#Vahid
#params.put("numberOfTileRows", 1)
#params.put("numberOfTileCols", 1)
#params.put("numberOfProcessors", 4)
#params.put("rowOverlap", 0)
#params.put("colOverlap", 0)
#params.put("tileCostThreshold", 500)
Product     =  GPF.createProduct("SnaphuExport", params, Product)
ProductIO.writeProduct(Product, TempFolder, "Snaphu")
print("Snaphu export performed successfully .................................")
#%%
# Phase unwrapping
"""
----------------------------------------------------------------------------------------------------------------
After that snaphu is exported, you can do phase unrwapping in the terminal which is not desirable.
But I call the snaphu to do this in python as follows.

It needs three files for this operation: filtered wrapped interferogram, and two files inside this temp folder.-

---------------------------------------------------------------------------------------
"""       
TempFolder = 'D:\PhD Info\InSAR\Examples\Japan Earthquake - Alaska tutorial\Test2\Smaller\exp_hybrid'
bandList = os.listdir(TempFolder)
for item in bandList:
    if item.endswith('.img') and item[0:5] == 'Phase':
        phasen = item  
#print(Fname+'\\'+TempFolder + '\\' + phasen)
print(phasen)
Product     = read(TempFolder+'\\' + phasen) # reads .dim 
width = Product.getSceneRasterWidth()
os.chdir (TempFolder)
os.system(snaphu_dir + ' -f snaphu.conf ' + phasen + ' ' + str(width))
print("Phase unwrapping performed successfully ..............................")
#%%
# Snaphu import
bandList = os.listdir(TempFolder)
for item in bandList:
    if item.endswith('.hdr') and item[0:8] == 'UnwPhase':
        upha = item
print(upha)

#working_dir='D:\\PhD Info\\InSAR\\Examples\\SNAPPY_Ecuador_Galapagos'
#os.chdir (working_dir + '\\' + Fname)
#
Files       = jpy.array('org.esa.snap.core.datamodel.Product', 2)
#Files[0]    = ProductIO.readProduct(os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos','subset_0_of_InSAR_pipeline_II.dim'))
Files[0]    = read(os.path.join(Fpath,Fname+'.dim')) # reads .dim 
Files[1]    = ProductIO.readProduct(glob.glob(TempFolder + '\\' + upha)[0])
HashMap     = jpy.get_type("java.util.HashMap")
params      = HashMap()
Product     = GPF.createProduct("SnaphuImport", params, Files)
os.chdir (Fpath)
ProductIO.writeProduct(Product, Fname + "_ifg_ml_fit_unwph.dim", "BEAM-DIMAP")
print("Snaphu import performed successfully .................................")
# Phase To Displacement
#Product = read(os.path.join(r'D:\PhD Info\InSAR\Examples\SNAPPY_Ecuador_Galapagos\exp_subset','subset_0_of_InSAR_pipeline_II_ifg_ml_fit_unwph.dim')) # reads .dim 
params      = HashMap()
Product     = GPF.createProduct("PhaseToDisplacement", params, Product)
os.chdir (Fpath)
ProductIO.writeProduct(Product, Fname +'_ifg_ml_fit_unwph_disp.dim', "BEAM-DIMAP")
print("Phase To Displacement performed successfully .................................")