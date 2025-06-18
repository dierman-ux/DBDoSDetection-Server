# Blacklist & Blockchain Logging

## Table of Contents
- [Blacklist Manager](#blacklist-manager)
- [Blockchain Logging](#blockchain-logging)

## Blacklist Manager

Each IP is monitored for abnormal behavior. After a configurable number of warnings (e.g. 3), it is blacklisted and blocked.

## Blockchain Logging

All blacklisted IPs are logged on the VeChain testnet via smart contracts. The interaction is handled using Node.js scripts such as:

- sendAttackLog.cjs
- getAttack.cjs
- deleteAttack.cjs

This ensures immutability and public visibility of detected threats.
