# InSAR_Snappy
Automatic generation of Interferograms, displacement and interferometric coherence maps for Sentinel-1 data in python. It uses the Snappy python API to automatically generate these outputs.
It takes as input the image names and follows the following pre-processing steps:
* S1 Tops Corregistration with enhanced spectral diversity
* Interferogram formation
* Deburst
* Topographic phase removal
* Multilook
* (Subset - coming up)
* Goldstein filtering
* Shaphu export
* Phase unwrapping
* Phase to displacement maps
* Terrain correction
* Export

Note: Use the InSAR_User.py script to run the main code.
