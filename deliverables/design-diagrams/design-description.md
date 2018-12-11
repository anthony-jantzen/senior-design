## Design Description
Detailed below are three design diagrams representing the solution at varying complexities:
* [High-Level](d0-high-level.png): Basic overview of inputs and outputs to the system.
* [Mid-Level](d1-mid-level.png): Intermediate overview of modules and submodules to the system.
* [Low-Level](d2-low-level.png): Advanced overview with granular descriptions of modules/submodules in the system.

## Design Components
The following is a brief description of each component featured in the design diagrams:

* Central Server
    * A central server to process the data received from access points for device locations and house the web server for communications with the client device.
* Access Point
    * A device that creates a wireless local area network (WLAN).
* Target Device
    * Device(s) for which the user is attempting to track the location of.
* Client Device
    * Device(s) that the user administrates with and uses to view and locate target devices.
* Wireless Emittance
    * An area where a wireless internet connection is detected/emitted from a device or access point.
* Wireless Connection
    * A wireless internet connection between two computing systems.
* Message Queue
    * A submodule to queue and efficiently send updated location data to the web server.
* Web Server
    * A web server to house a web application which provides device information and locations.
