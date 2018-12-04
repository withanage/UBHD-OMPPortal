# UBHD-OMPPortal
UBHD-OMPPortal is a flexible, responsive Frontend portal for [pkp](https://pkp.sfu.ca/) 's [Open Monograph Press](https://pkp.sfu.ca/omp/)  written in python programming language and  based on the python web framework [web2py](http://www.web2py.com).

  * [Installation](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/master/static/docs/INSTALL.md)
  
  * [Demo](#demo)  , [Features](#features)
  * Plugins  [Solr Search](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/master/static/docs/SOLR.md), [VGWort Pixel Import](https://github.com/UB-Heidelberg/UBHD-OMPPortal/blob/master/static/docs/VGWORT.md)
  * [License](#license) and [Credits](#Credits)

# Demo
- Heidelberg University Publishing  [Web](http://heiup.uni-heidelberg.de/)
- Customized lens based HTML Viewer [Full book](http://heiup.uni-heidelberg.de/UBHD_OMPPortal/reader/index/43/43-68-231-1-10-20151008.xml) ,  [Chapter ](http://heiup.uni-heidelberg.de/reader/index/43/43-69-209-1-10-20150717.xml) ,  [Chapter with images](http://heiup.uni-heidelberg.de/reader/index/43/43-69-220-1-10-20150723.xml#figures)
![alt tag](static/images/UBHD-OMPPortal.png)

# Features
- Responsive design (based on twitter bootstrap)
- Easy multilingual support
- Intergrated-HTML viewer (based on [lens](https://github.com/elifesciences/lens/))
- Native [JATS](http://jats.nlm.nih.gov/) XML support for OMP
- Chapter level metadata for monographs and edited volumes
- Social sharing  (without using external plugins)
- Detailed usage statistics
- Easy migration using web2py app structure
- VGWORT plugin for royalties (for Germany, requires pythonn- urllib to check if the vgwort is enabled )
- Annotation Support


# License
This software is released under the the [GNU General Public License](LICENSE.md).
See the file [LICENSE.md](LICENSE.md) included with this distribution for the terms of this license.

# Credits
The lead deveopper and software architect is
- Dulip Withanage, Heidelberg University Library

Additional contributions were made, in alphabetical order by:

- Katharina Wäschle , Heidelberg University Library
- Nils Weiher,  Heidelberg University Library
- Web-Team, University Library Heidelberg

