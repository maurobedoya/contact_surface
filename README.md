# Contact surface analyzer

Python script to calculate the contact surface area between two molecular structures, e.g. ligand-protein, protein-protein, among others, in a Molecular Dynamics trajectory.


![Scheme](/assets/contact_surface_scheme.png)


## Features

It allows to carry out the analysis in the different formats supported by PyMOL, e.g., .pdb, .gro, .cms and trajectory files; .dcd, .crd, .xtc, and .trr.

It allows obtaining in a .dat file the surface area obtained by SASA of the ligand, protein, the complex, the contact area and the percentage (portion) of the ligand that makes the contact.

## Requirements

Python

PyMOL libraries

To install PyMOL libraries by console use:
```
sudo apt-get install PyMOL
```

## Usage

```
python md_contact_surface.py -top topology_file.xxx -traj trajectory_file.xxx -l "ligand_selection" -p "protein_selection" -o contact_surface_data
```

It is also possible to specify the frames of the trajectory to be analyzed. The initial and final frame can be specified as: ``-f 1:1000``, this option will analyze each frame from position 1 to 1000. But also the spacing between frames can be specified, for example the option: ``-f 1:1000:5`` will consider every 5 frames in the range 1 - 1000.

To see available options use:
```
python md_contact_surface.py -h
```

## Contributors

Be sure to thank these contributors:

* [Mauricio Bedoya](https://github.com/maurobedoya) - Creator, maintainer
* [Francisco Adasme](http://github.com/franciscoadasme) - Contributor

## License

Licensed under the MIT license, see the separate LICENSE file.

## Citing

[Contact_surface](https://github.com/maurobedoya/contact_surface)

[PyMOL](https://pymol.org/2/)

