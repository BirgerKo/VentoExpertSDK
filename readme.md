# Introduction

This is a Python module for making a connection to a Blauberg Vento Expert room ventilationsystem with a heat exchanger. Developer documentation is [here](
https://blaubergventilatoren.de/uploads/download/b133_4_1en_01preview.pdf). 

This SDK is forked from forked from dingusdk/dukaonesdk and is heavily based upon the work there.

The primary goal for this module is to make an interface from Home Assistant to Blauberg Vento Expert systems. There are also other suppliers branding these systems under their own name.
OEMs:
 * Duka One

The module implements:

* On/Off 
* Set/Get speed
* Set/Get Mode
* Notification when a state changes. 
 
## Example

See the examples.py file

This blog http://www.dingus.dk/ has  good information.

## Other compatible devices

There are several one "bands" of the duka one ventilator.
* Blauberg Vento
* Siku With several models.

These should also work - I don't know which one is the orginal manufacture. Both Blauberg and Siku has documentation for the interface.

[You can see the documentation from Blauberg here](https://blaubergventilatoren.de/uploads/download/b133_4_1en_01preview.pdf)

# License

VentoExpertSDK is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VentoExpertSDK is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this library.  If not, see <http://www.gnu.org/licenses/>.

