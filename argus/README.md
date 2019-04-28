# Overview

Argus is a tool for estimating the locations of devices positioned on or nearby a mesh network utilizing RSSI information obtained from packet capture. To do this, it employs the use of various technologies and algorithms. This user manual is meant as a guide to understanding each of these technologies and setting up Argus as a workable product in your own environment.

## Network Setup

#### Notes
* Network setup may be skipped for pre-existing mesh networks with packet capture. Simply send packet capture to central repository and continue on to the data processing setup.
* The access point we utilized for this project was the GL.iNet 150M Mini Smart Router (see References and Resources). Setup may differ slightly when using other products.

#### Hardware Requirements
* (3x) Wireless Access Points

#### Setup
For each access point (AP):
1. Set AP in router mode.
2. Plug AP into power source.
3. Connect AP to a switch that has internet access.
4. Install *tcpdump* on the AP.
5. Install *lsblk* on the AP.
6. Follow OpenWRT USB drive setup (see References and Resources below).

Once the above are completed, find a power source for each AP. Ping each of them to verify connectivity, then ssh into them. *tcpdump* will be ready to use, and *rsync* can be utilized to periodically transfer packet capture files to your central repository.

## Data Processing Setup

#### Notes
* Python3 was utilized for nearly all of the data processing. Please see References and Resources for downloads and docs.

#### Setup
On the central repository:
1. Git clone [argus-dev](argus-dev/) to the central repository.
2. Run [install.sh](argus-dev/install.sh).
   * This will set up the python virtual environment and install all library dependencies.
3. Edit [config.yml](argus-dev/config.yml) to align with your project.
   * Here, you will define the drive locations of the packet capture files sent periodically by each AP, as well as the approximate x,y plane coordinate of the APs.
   * This file will be fed into the main controller.
4. Execute [argus.py](argus-dev/argus.py).
   * The main controller of the project.
   * This will utilize the config file above to gather the packet capture files, then call the packet and location processor (see below for details).

#### Packet Processing


## User Interface Setup

#### Notes
* Preact-CLI was utilized to establish the frontend user interface. The installation has been optimized, but more details surrounding Preact-CLI can be found using the References and Resources link.

#### Setup
1. Git clone [argus-ui](argus-ui/) to the central repository.
2. Follow the install guide located in the [README](argus-ui/README.md).

## References and Resources
* [GL.iNet](https://www.gl-inet.com/)
* [Preact-CLI](https://github.com/developit/preact-cli)
* [Python3](https://www.python.org/download/releases/3.0/)
  * [Download](https://www.python.org/downloads/)
  * [Documentation](https://www.python.org/doc/)
* [Scapy Library](https://scapy.net/)
* [SciPy Library (with NumPy)](https://www.scipy.org/)

## FAQ