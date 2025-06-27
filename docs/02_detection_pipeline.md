# Detection Pipeline

## Table of Contents
- [Feature Extraction](#feature-extraction)
- [Classification Model](#classification-model)

## Feature Extraction

Network packets are captured using Scapy. Flow-level features are calculated and aggregated over time windows. These include:

- Packet counts and lengths
- Flow duration and inter-arrival times
- TCP flag statistics (SYN, ACK, PSH, etc.)
- Byte rate and packet rate per second

## Classification Model

A model trained on pre-labeled traffic data is used for attack detection. Supported classes:

- BENIGN
- HULK
- SYNFLOOD
- UDPFLOOD
- POSTFLOOD

The model returns a label which is interpreted to determine whether an IP should be warned or blacklisted.
