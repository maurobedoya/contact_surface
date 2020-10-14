# Contact surface analyzer

Python script to calculate the contact surface area between two molecular structures e.g ligand-protein, protein-protein, etc, in a molecular dynamics trajectory.


![Scheme](/assets/contact_surface_scheme.png)


## Features

It allows to carry out the analysis in the different formats supported by Pymol, for example, .pdb, .gro, .cms and path files; .dcd, .crd, .xtc, and .trr.

It allows obtaining in a .dat file the surface area obtained by SASA of the ligand, protein, the complex, the contact area and the percentage (portion) of the ligand that makes the contact.

## Requirements

Python

Pymol libraries

To install Pymol libraries by console use:
```
sudo apt-get install pymol
```

## Usage

```
python md_contact_surface.py -top file.xxx -traj trajectory_file.xxx -l "ligand_seletion" -p "protein_selection" -o contact_surface_data
```

## Contributors

[Francisco Adasme](http://github.com/franciscoadasme)