# UBHD-OMPPortal
UBHD-OMPPortal is a flexible, responsive Frontend portal for [pkp's](https://pkp.sfu.ca/) [Open Monograph Press](https://pkp.sfu.ca/omp/) and [OJS](https://pkp.sfu.ca/ojs/) written in python programming language and  based on the python web framework [web2py](http://www.web2py.com).

# Demo
[Heidelberg University Publishing - Webpage] (http://heiup.uni-heidelberg.de/)
 Customized HTML Viewer [Full book](http://heiup.uni-heidelberg.de/reader/index/43/heiUP_habenstein_abwesenheit_2015.xml) [Chapter](http://heiup.uni-heidelberg.de/reader/index/43/43-69-209-1-10-20150717.xml) [Chapter with images](http://heiup.uni-heidelberg.de/reader/index/43/43-69-220-1-10-20150723.xml#figures)


# Features
- Responsive design (based on twitter bootstrap)
- Easy multilingual support
- Intergrated - HTML viewer (based on [lens](http://lens.elifesciences.org/))
- Native [JATS](http://jats.nlm.nih.gov/) XML support for OMP
- Chapter level metadata for monographs and edited volumes
- Social sharing

# Installation
1. Install Open Monograph Press. See [documentation](http://pkp.sfu.ca/omp/README)
2. Install web2py
 1. [Download] (http://web2py.com/init/default/download) web2py.
 2. Unzip it
 3. python2.7 web2py.py
3. Install UBHD-OMPPortal
 1. cd <WEB2PY_INSTALLATION_FOLDER>/applications/
 2. git clone https://github.com/UB-Heidelberg/UBHD-OMPPortal.git <PRESS_NAME>
 3. Change the settings for your local omp installation private/appconfig.ini
   1. username and password for the OMP Database
   2. press_id of the local omp press
 4. mount or link the files folder of the OMP  <WEB2PY_INSTALLATION>/applications/<PRESS_NAME>/static/monographs/
   e.g. [OMP_INSTALLATION]/files/presses/6/monographs  = <WEB2PY_INSTALL>/applications/<PRESS_NAME>/static/monographs/

# Further customization


#License
This software is released under the the [GNU General Public License](LICENSE.md).
See the file [LICENSE.md](LICENSE.md) included with this distribution for the terms of this license.











