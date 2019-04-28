*** Settings ***
Documentation    Tests for the location calculation of argus
Library    libraries/YamlLibrary.py    config.yml
Library    libraries/JSONLibrary.py
Library    OperatingSystem

*** Variables ***
${YAML_PATH}       config.yml
${EMPTY_PCAP01}    tests/test_caps/empty-01.cap
${EMPTY_PCAP02}    tests/test_caps/empty-02.cap
${EMPTY_PCAP03}    tests/test_caps/empty-03.cap
${VALID_PCAP01}    tests/test_caps/capture-small-01.cap
${VALID_PCAP02}    tests/test_caps/capture-small-adj-02.cap
${VALID_PCAP03}    tests/test_caps/capture-small-adj-03.cap
${CAP_TIME_VALID_START}    "Mar 14, 2019 17:09:33.000000000"
${CAP_TIME_VALID_END}      "Mar 14, 2019 17:09:33.603000000"
${MISSING_CONFIG_STRING1}    usage: argus.py [-h] [-c CONFIG]
${MISSING_CONFIG_STRING2}    argus.py: error: Must provide a valid config file
${CAP_TIME_INVALID_START01}    "Mar 14, 2019 17:09:33.000000000"
${CAP_TIME_INVALID_END01}      "Mar 14, 2019 17:09:36.000000000"
${CAP_TIME_INVALID_START02}    "Mar 14, 2019 17:09:39.000000000"
${CAP_TIME_INVALID_END02}      "Mar 14, 2019 17:09:41.000000000"
${CAP_TIME_INVALID_START03}    "Mar 14, 2019 17:09:45.000000000"
${CAP_TIME_INVALID_END03}      "Mar 14, 2019 17:09:47.603000000"


*** Test Cases ***
File Check Test
	[Documentation]    Checks that all argus files have been installed correctly
	Should Exist       argus.py
	Should Exist       config.yml
	Should Exist       install.sh
	Should Exist       location.py
	Should Exist       packet_processor.py
	Should Exist       README.md
	Should Exist       requirements.txt

Argus Missing Config Test
	[Documentation]    Verifies argus output when config file is missing
	${output}=     Run    python3 argus.py -c test.yml
	Should Contain    ${output}    ${MISSING_CONFIG_STRING1}
	Should Contain    ${output}    ${MISSING_CONFIG_STRING2}
	Remove File    test.yml

Argus Help Test
	[Documentation]    Verifies the usage output from argus
	${help_output}=    Get File    tests/test_files/usage.out
	${argus_output}=    Run    python3 argus.py --help
	Should Contain    ${help_output}    ${argus_output}

Empty Pcap Test
	[Documentation]   Checks the output from argus with empty pcaps as input
	Change AP Config File    ${EMPTY_PCAP01}    ${EMPTY_PCAP02}    ${EMPTY_PCAP03}
	Run    python3 argus.py
	File Should Exist    output.json
	File Should Not Be Empty    output.json
	Grep File    output.json    {"loc_updates": []}

Small Pcap Test
	[Documentation]   Checks the location calculation algorithms accuracy on a
	...		  small pcap file extracted from test capture on March 14th.
	...		  Checks the values computed against known test output.
	Run    tshark -r ${VALID_PCAP01} -Y '(frame.time >= ${CAP_TIME_VALID_START}) && (frame.time <= ${CAP_TIME_VALID_END})' -w tests/test_caps/small_cap_test-01.cap
	Run    tshark -r ${VALID_PCAP02} -Y '(frame.time >= ${CAP_TIME_VALID_START}) && (frame.time <= ${CAP_TIME_VALID_END})' -w tests/test_caps/small_cap_test-02.cap
	Run    tshark -r ${VALID_PCAP03} -Y '(frame.time >= ${CAP_TIME_VALID_START}) && (frame.time <= ${CAP_TIME_VALID_END})' -w tests/test_caps/small_cap_test-03.cap
	Should Exist    tests/test_caps/small_cap_test-01.cap
	Should Exist    tests/test_caps/small_cap_test-02.cap
	Should Exist    tests/test_caps/small_cap_test-03.cap
	Change AP Config File    tests/test_caps/small_cap_test-01.cap
	...                      tests/test_caps/small_cap_test-02.cap
	...                      tests/test_caps/small_cap_test-03.cap
	Run    python3 argus.py
	File Should Exist    output.json
	File Should Not Be Empty    output.json
	${output}=    Get Dict From Json File    output.json
	Should Be Equal    ${output['loc_updates'][0]['device']}    40:4e:36:22:b8:01
	Should Be Equal    ${output['loc_updates'][0]['location'][0]}    ${2.51615513578063}
	Should Be Equal    ${output['loc_updates'][0]['location'][1]}    ${-39.039146902938}
	${locations}=    Get Length    ${output['loc_updates']}
	Should Be Equal    ${84}    ${locations}
	[Teardown]    Clean Up Files

Location Time Interval Test
	[Documentation]   Verifies that the location ignores packets that have too large
	...               of a time delta.
	Run    tshark -r ${VALID_PCAP01} -Y '(frame.time >= ${CAP_TIME_INVALID_START01}) && (frame.time <= ${CAP_TIME_INVALID_END01})' -w tests/test_caps/small_cap_test-01.cap
	Run    tshark -r ${VALID_PCAP02} -Y '(frame.time >= ${CAP_TIME_INVALID_START02}) && (frame.time <= ${CAP_TIME_INVALID_END02})' -w tests/test_caps/small_cap_test-02.cap
	Run    tshark -r ${VALID_PCAP03} -Y '(frame.time >= ${CAP_TIME_INVALID_START03}) && (frame.time <= ${CAP_TIME_INVALID_END03})' -w tests/test_caps/small_cap_test-03.cap
	Should Exist    tests/test_caps/small_cap_test-01.cap
	Should Exist    tests/test_caps/small_cap_test-02.cap
	Should Exist    tests/test_caps/small_cap_test-03.cap
	Change AP Config File    tests/test_caps/small_cap_test-01.cap
	...                      tests/test_caps/small_cap_test-02.cap
	...                      tests/test_caps/small_cap_test-03.cap
	Run    python3 argus.py
	File Should Exist    output.json
	File Should Not Be Empty    output.json
	${output}=    Get Dict From Json File    output.json
	${locations}=    Get Length    ${output['loc_updates']}
	Should Be Equal    ${0}    ${locations}
	[Teardown]    Clean Up Files

*** Keywords ***
Change AP Config File
	[Documentation]    Changes the configuration files that the APs use for
	...                argus
	[Arguments]    ${config_file_1}    ${config_file_2}    ${config_file_3}

	Change Config Capture File    argus1   ${config_file_1}
	Grep File    ${YAML_PATH}    ${config_file_1}

	Change Config Capture File    argus2   ${config_file_2}
	Grep File    ${YAML_PATH}    ${config_file_2}

	Change Config Capture FIle    argus3   ${config_file_3} 
	Grep File    ${YAML_PATH}    ${config_file_3}

Clean Up Files
	[Documentation]    Removes files created in tests
	Remove File    tests/test_cap_test-01.cap
	Remove File    tests/test_cap_test-02.cap
	Remove File    tests/test_cap_test-03.cap
	Remove File    output.json


