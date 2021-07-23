# Scout

## Description

Scout is python + solid project intenteded to survey several open crypto exchange platforms looking for the best buy or sell opportunity for a given pair (e.g USDT/USDC).

## What it does

Once it finds the best option, it allows the user to executes a smart contract using a given wallet address and the proper api keys for the selected platform.

## Purpose

This is the practical part of an investigation project made for the University of Belgrano where we explore, the arbitrage strategy on the crypto environment, more specifically DeFi.

## Stack

* Python3 with FastAPI
* Docker + Docker-compose
* AlpineLinux (SO of the docker images)
* Solid + Etherum testnet
* VueJS


## Progress

- [x] BE, Create base boilderplate.
- [ ] BE, Add hooks to the exchanges APIS.
- [ ] BE, Add endpoint that accepts a certain crypto pair.
- [ ] BE, Modify previous endpoint as to receive settings such as: wallet address, dry run, api keys.
- [ ] BE, Create Smart contract that handles the transaction.
- [ ] FE, Add interface that allows easy user input.
