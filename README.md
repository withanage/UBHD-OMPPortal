# UBHD-OMPPortal
UBHD-OMPPortal is a flexible, responsive Frontend portal for [pkp's](https://pkp.sfu.ca/) [Open Monograph Press](https://pkp.sfu.ca/omp/) and [OJS](https://pkp.sfu.ca/ojs/) written in python programming language and  based on the python web framework [web2py](http://www.web2py.com).

#Demo
[Heidelberg University Publishing] (http://heiup.uni-heidelberg.de/)

#Features
- Responsive design (based on twitter bootstrap)
- Easy multilingual support
- Intergrated - HTML viewer (based on [lens](http://lens.elifesciences.org/))
- Native [JATS](http://jats.nlm.nih.gov/) XML support for OMP
- Chapter level metadata for monographs and edited volumes
- Social sharing

#Installation
1. Install Open Monograph Press. See [documentation](http://pkp.sfu.ca/omp/README)
2. Install web2py
 1. [Download] (http://web2py.com/init/default/download) web2py.
 2. Unzip it
 3. python2.7 web2py.py
3. Install UBHD-OMPPortal
 1. cd <WEB2PY_INSTALLATION_FOLDER>/applications/
 2. git clone https://github.com/UB-Heidelberg/UBHD-OMPPortal.git <PRESS_NAME>
 3. Change the username and password for the OMP Database in private/appconfig.ini
 4. mount or link the

#License
This software is released under the the [GNU General Public License](LICENSE.md).
See the file [LICENSE.md](LICENSE.md) included with this distribution for the terms of this license.











