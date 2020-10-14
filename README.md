# 3dMPRAGEise/ize

Quick MP2RAGE UNI background cleaning script using only **AFNI**. 

No other dependencies. IMO out-performs the [MP2RAGE Robust Background Removal MATLAB Script](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/master/DemoRemoveBackgroundNoise.m)

# Setup
`git clone https://github.com/srikash/3dMPRAGEise.git`  
`chmod +x 3dMPRAGEise`  
`cp 3dMPRAGEise $HOME/abin`  

# Usage
`3dMPRAGEise -i INV2.nii -u UNI.nii`

# Expected result
![Coronal](img/coronal.png)
![Axial](img/axial.png)



