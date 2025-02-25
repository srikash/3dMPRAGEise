# MPRAGEise [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14926753.svg)](https://zenodo.org/badge/latestdoi/14926753)

Background denoise MP2RAGE UNI images (MPRAGEising) whilst either removing or reintroducing the bias field - Powered by **AFNI**

## **Preferred Script: [MPRAGEise.py](https://github.com/srikash/3dMPRAGEise/blob/main/MPRAGEise.py)**  
*MPRAGEise.py is the Python implementation of the original shell script and is recommended for its easier interface and better logging capabilities.*

**Setup:**

`git clone https://github.com/srikash/3dMPRAGEise.git`  
`cp 3dMPRAGEise/MPRAGEise.py $HOME/abin`  

**Usage:**

`python MPRAGEise.py -i INV2_image.nii.gz -u UNI_image.nii.gz`

*Nota bene: Do not use this script for the MP2RAGE T1 map.*


## Expected result
Compared to the output of [MP2RAGE Robust Background Removal MATLAB Script](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/master/DemoRemoveBackgroundNoise.m) or [MP2RAGE Robust Background Removal Python Script](https://github.com/khanlab/mp2rage_genUniDen/blob/master/mp2rage_genUniDen.py)

![Coronal](img/coronal.png)
![Axial](img/axial.png)



