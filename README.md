# 3dMPRAGEise [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.304074221.svg)](https://zenodo.org/badge/latestdoi/304074221)

Quick MP2RAGE UNI background cleaning script using pure **AFNI** prowess! 
Now includes option to re-introduce the bias-field to the UNI image after background cleaning if you need that for whatever reason.

# Setup
`git clone https://github.com/srikash/3dMPRAGEise.git`  
`chmod +x 3dMPRAGEise`  
`cp 3dMPRAGEise $HOME/abin`  

# Usage
`3dMPRAGEise -i INV2.nii -u UNI.nii`
or 
`3dMPRAGEize -i INV2.nii -u UNI.nii`

# Expected result
Compared to the output of [MP2RAGE Robust Background Removal MATLAB Script](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/master/DemoRemoveBackgroundNoise.m) or [MP2RAGE Robust Background Removal Python Script](https://github.com/khanlab/mp2rage_genUniDen/blob/master/mp2rage_genUniDen.py)

![Coronal](img/coronal.png)
![Axial](img/axial.png)



