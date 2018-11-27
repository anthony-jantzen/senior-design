## Milestones
### 1. Set up hardware
Determine hardware requirements for the project and implement basic set up of components from project design including access points, central server, and possibly a client device for testing purposes.

### 2. Create modules
Create modules defined in the project design. Define classes for each stage of the data processing module. Set up web server to communicate with message queue, client device, and data processing module. Set up web framework to be used for user interface on client device.

### 3. Collect and extract data
Write class to monitor, capture, and filter packets received from access points. Write algorithm to scan packets and parse out relevant data for location processing.

### 4. Process location
Research methods of efficient device location triangulation/trilateration. Write algorithm to use RSSI and ToF to calculate target device's location from extracted data.

### 5. Set up communications
Establish message queue and in-memory data management system to prepare and store location data on web server. Implement communication pathways between web server and client device.

### 6. Implement user interface
Design and develop the user interface for the client device, including features listed previously like device location and information listing. Create configurable notification system based on status of target devices or access points. Generate a method for setting up facility map of access points for end user.

### 7. Test and document project
Perform unit and integration tests of all modules in the project design. Document project according to course assignments. Conduct end user tests to gather feedback, document necessary instructions, and adjust implementation accordingly.