#!/usr/bin/env python
"""
Argus: Wifi based traffic heatmap
"""
import argparse
import os
import yaml
import json
from pprint import pprint

import packet_processor
import location

DEFAULT_CONFIG = "config.yml"


def main():
    """ Application entrypoint """
    parser = argparse.ArgumentParser(description="argus")
    parser.add_argument(
        "-c", "--config",
        type=str,
        required=False,
        default=DEFAULT_CONFIG,
        help="Config file. Defaults to config.yml"
    )

    args = parser.parse_args()
    if not args.config or not os.path.exists(args.config):
        parser.error("Must provide a valid config file")

    with open(args.config, 'r') as cfg_file:
        try:
            config = yaml.safe_load(cfg_file)
        except yaml.YAMLError as exc:
            parser.error("Config file error: {}".format(exc))

    processor = packet_processor.PacketProcessor(config['access_points'])
    processor.run()
    processor.close()

    for ap, devices in processor.location_data.items():
        for mac, q in devices.items():
            devices[mac] = list(q.queue)

    location.generate_locations(config, processor.location_data)

if __name__ == "__main__":
    main()
