#!/usr/bin/env python3

import os
import subprocess
from string import Template

BALENA_DEVICE_UUID = os.getenv("BALENA_DEVICE_UUID")
UBIDOTS_DEVICE_LABEL = os.getenv("UBIDOTS_DEVICE_LABEL", BALENA_DEVICE_UUID)
UBIDOTS_TOKEN = os.getenv("UBIDOTS_TOKEN")


if not UBIDOTS_TOKEN:
    print("[ERROR] Please define UBIDOTS_TOKEN environment variable")
    exit(-1)


with open("mosquitto.conf.template") as src_cfg, open(
    "config/mosquitto.conf", "w"
) as dst_cfg:
    cfg = {
        "client_id": f"ubidots-balena-{UBIDOTS_DEVICE_LABEL}",
        "username": UBIDOTS_TOKEN,
        "device_label": UBIDOTS_DEVICE_LABEL,
    }
    src = Template(src_cfg.read())
    dst = src.substitute(cfg)
    dst_cfg.write(dst)


subprocess.run(["mosquitto", "-c", "config/mosquitto.conf"])
