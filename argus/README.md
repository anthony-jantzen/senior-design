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
5. Follow OpenWRT USB drive setup (see References and Resources below).

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
   * *output.json* will be written to *processing* directory.

#### Packet Processing
Packet processing is all performed under [packet_processor.py](argus-dev/packet_process.py).

It utilizes Python's Scapy library to parse the packets into objects. The Scapy objects are then iterated through to extract important information for location processing. Output is in the following format:

```
item = {
    'MAC' : device mac address,
    'AP' : ap device communicated with (argus1, argus2, argus3),
    'RSSI' : signal strength of that device,
    'TIME' : timestamp of when the packet sent
}
```

#### Location Processing
Location processing is all performed under [location.py](argus-dev/location.py).

It utilizes trilateration algorithms in conjunction with Python's SciPy and NumPy libraries to calculate locations. Specifically, it trilaterates a location on a cartesion grid given the location of known locations (access points) and the desired point's distance from those locations using the free space path loss algorithm. Mean standard error is implemented to minimize the error in estimations. Location updates are then written to a list in the following format before being dumped to json:

```
data["loc_updates"].append({
    "timestamp": timestamp,
    "location": location,
    "device": device
})
```

Locations are in the form of an x,y coordinate to be plotted by the heatmap logic on the frontend application.

#### Testing
Testing was conducted using the Robot Framework. Robot Framework tests consist of test suites, test cases, and test keywords. A test keyword tests an indivudal element from argus. A test case insures that individual keywords integrate together. A test suite is composed of multiple test cases that verifies the integrity of the program. To run the tests, install Robot Framework with:

```pip3 install robotframework```

Then move to the argus-dev directory and execute the tests with:

```robot -d tests/output/Argus tests/Argus.robot```

This will output a log.html file that shows Argus as a test suite and the results from the tests.


## User Interface Setup

#### Notes
* Preact-CLI was utilized to establish the frontend user interface. The installation has been optimized, but more details surrounding Preact-CLI can be found using the References and Resources link.

#### Setup
1. Git clone [argus-ui](argus-ui/) to the central repository.
2. Follow the installation and setup guide located in the [README](argus-ui/README.md).
   * Web application will be running locally on central repository.
   * *output.json* will be grabbed from the *processing* directory and used to graph the heatmap.

## References and Resources
* [Free Space Path Loss Algorithm](https://en.wikipedia.org/wiki/Free-space_path_loss)
* [GL.iNet](https://www.gl-inet.com/)
* [Preact-CLI](https://github.com/developit/preact-cli)
* [Python3](https://www.python.org/download/releases/3.0/)
  * [Download](https://www.python.org/downloads/)
  * [Documentation](https://www.python.org/doc/)
* [Robot Framework](https://robotframework.org/)
* [Scapy Library](https://scapy.net/)
* [SciPy Library (with NumPy)](https://www.scipy.org/)

## FAQ

#### What packets does argus take into account for location calculation?

Argus' packet processing module ignores 802.11 Beacon Packets and 802.11 Probe Response packets as these packets do not originate from devices but rather other access points. 

#### How do I change what packets are ignored?

If you want to ignore additional packets, you can either add the [scapy 802.11 protocol](https://github.com/secdev/scapy/blob/master/scapy/layers/dot11.py) to the list of [ignored packets](https://github.com/anthony-jantzen/senior-design/blob/master/argus/argus-dev/packet_processor.py#L16) or filter the pcap file prior to input on argus using [tshark](https://www.wireshark.org/docs/man-pages/tshark.html).

#### Can I use my own mesh network with Argus?

Any mesh network can be applied to Argus. However, there are a few things to note when doing this. First, the setup process for the network and your access points to perform a packet capture may differ slightly than our guide. Additionally, the trilateration algorithm is optimized for three access points, so slight modifications will need to be made to the code when using four or more.

#### Can I use Python 2 with Argus?

It is highly recommended to use Python3 when installing and running Argus as that is what it was written in. Dependencies may be lost and conflicts may arise if you attempt to use Python 2.

