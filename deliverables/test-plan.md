## Part I. Overall Test Plan
We will approach testing in a similar fashion as our design by splitting the tests via modules to ensure our final product is functional and efficient. We will start by setting up hardware and ensuring network connections are consistent. From there, underlying processes of our subsystems will be designed and tested. Subsystems will then be tested to ensure proper integration of processes. System-wide integration testing will then occur to ensure cohesiveness of all modules. Next, the product will undergo performance and stress testing to ensure efficiency and durability. Finally, we will conduct end user tests to gather feedback and ensure the product is intuitive.

## Part II. Test Case Descriptions

### Network Device Tests

ND1

1. This test will ensure proper setup of the wireless network.
2. This test will utilize standard network connection tools such as ping to verify the reachability and interconnectedness of each access point and the central server.
3. Inputs for this test will be the IP addresses of the access points and central server.
4. Outputs for this test will be the responses received from the destination device (if any).
5. Normal
6. Blackbox
7. Functional
8. Unit

ND2

1. This test will ensure that the access points are capturing data.
2. This test will utilize aircrack-ng to capture packets on each access point sent by nearby wireless emitters.
3. Inputs for this test will be the packets captured from the devices.
4. Outputs for this test will be the standard files created by aircrack-ng including PCAP and CSV files.
5. Normal
6. Blackbox
7. Functional
8. Unit

ND3

1. This test will ensure that the access points are sending data to the central server.
2. This test will utilize (INSERT TOOL; rsync maybe?) to send packet capture files from the access points to the central server for further processing.
3. Inputs will be the packet capture files on the access points.
4. Outputs will be the packet capture files on the central server.
5. Normal
6. Blackbox
7. Functional
8. Unit

### Data Processing Tests

DP1

1. This test will ensure that the packets captured are properly parsed.
2. This test will utilize (scapy?) and custom built programs to parse incoming packets for required information (see outputs).
3. Inputs will be the incoming packet capture files.
4. Outputs will be the timestamp, RSSI data, MAC address, and access point number in JSON format.
5. Normal
6. Blackbox
7. Functional
8. Unit

DP2

1. This test will ensure the validity of the packets captured.
2. This test will utilize custom built programs to verify that at least three access points send RSSI information for a given device within a reasonable amount of time of each other.
3. Inputs will be the parsed JSON data.
4. Outputs will be the parsed JSON data that is not discarded.
5. Normal
6. Blackbox
7. Functional
8. Unit

DP3

1. This test will ensure the accuracy of the location processing.
2. This test will utilize custom built programs to trilaterate device locations using gathered RSSI information, then validate the calculation with manually collected device location data.
3. Inputs for this test will be the RSSI information from the JSON data.
4. Outputs for this test will be an approximate X,Y coordinate based on the location map.
5. Normal
6. Blackbox
7. Functional
8. Unit

DP4

1. This test will ensure the proper storage of device data.
2. This test will run a basic query to verify that device information, including calculated location data, is inserted and stored properly in the database.
3. Inputs for this test will be the test query.
4. Outputs for this test will be the results from the database.
5. Normal
6. Blackbox
7. Functional
8. Unit

DP5

1. This test will ensure alerting on potential packet capture failure.
2. This test will utilize simple logic to alert the web server when packets are no longer being seen from a particular access point.
3. Inputs for this test will (logically) be a lack or small amount of packets from an access point.
4. Outputs for this test will be a simple alert message when the problem is identified.
5. Boundary
6. Blackbox
7. Functional
8. Integration

### Web Application Tests

WA1

1. This test will ensure communication exists between web application and server.
2. This test will utilize basic requests performed on the frontend application, observe the information received by the backend server for consistency, and return a response successfully to the application.
3. Inputs for this test will be a basic string in the request.
4. Outputs for this test will be a basic validation string in the response.
5. Normal
6. Blackbox
7. Functional
8. Unit

WA2

1. This test will ensure that the web application can communicate with the database.
2. This test will work in conjunction with DP4. A sample query will be run against the database and the results will be compared to the information listed in the table to verify that it is the same and accurate.
3. Inputs for this test will be the test query.
4. Outputs for this test will be the results from the database.
5. Normal
6. Blackbox
7. Functional
8. Unit

WA3

1. This test will ensure that the map view is displaying properly.
2. This test will utilize a controlled, dummy location value for a device that will be compared to the X,Y coordinate mapping on the map view to validate visual accuracy.
3. Inputs for this test will be sample location data for a device.
4. Outputs for this test will be the map view of the device’s location.
5. Normal
6. Blackbox
7. Functional
8. Unit

WA4

1. This test will ensure that notifications are enabled properly by the admin.
2. This test will send a dummy request to the server when the admin enables notifications, which will then send a dummy response back and trigger a frontend notification based on program logic.
3. Inputs for this test will be some form of button press by the admin to enable notifications.
4. Outputs for this test will be a dummy notification popping up on the admin’s screen.
5. Normal
6. Whitebox
7. Functional
8. Unit

### Product Performance Tests

PP1

1. This test will ensure the accuracy of the device location calculation.
2. This test will compare a manually dropped pin for a device’s location against the program’s trilateration calculation to validate location accuracy within 2 meters.
3. Inputs for this test will be the manually pinned location data and packets captured for the device by the access points.
4. Outputs for this test will be the calculated location data and map view of the device, as well as the comparison result.
5. Normal
6. Whitebox
7. Performance
8. Unit

PP2

1. This test will ensure the efficiency of the final product as a system.
2. This test will time the end to end run time of a typical workflow through the system, from packet capture to location mapping, to validate that an admin receives updated location information for a device within 1 minute.
3. Inputs for this test will be the packets captured from the device.
4. Outputs for this test will be the mapped location and the resulting time.
5. Normal
6. Whitebox
7. Performance
8. Integration
 
## Part III. Test Case Matrix
| Identifier | Normal/Abnormal | Blackbox/Whitebox | Functional/Performance | Unit/Integration |
|------------|-----------------|-------------------|------------------------|------------------|
| ND1        | Normal          | Blackbox          | Functional             | Unit             |
| ND2        | Normal          | Blackbox          | Functional             | Unit             |
| ND3        | Normal          | Blackbox          | Functional             | Unit             |
| DP1        | Normal          | Blackbox          | Functional             | Unit             |
| DP2        | Normal          | Blackbox          | Functional             | Unit             |
| DP3        | Normal          | Blackbox          | Functional             | Unit             |
| DP4        | Normal          | Blackbox          | Functional             | Unit             |
| DP5        | Boundary        | Blackbox          | Functional             | Integration      |
| WA1        | Normal          | Blackbox          | Functional             | Unit             |
| WA2        | Normal          | Blackbox          | Functional             | Unit             |
| WA3        | Normal          | Blackbox          | Functional             | Unit             |
| WA4        | Normal          | Whitebox          | Functional             | Unit             |
| PP1        | Normal          | Whitebox          | Performance            | Integration      |
| PP2        | Normal          | Whitebox          | Performance            | Integration      |
