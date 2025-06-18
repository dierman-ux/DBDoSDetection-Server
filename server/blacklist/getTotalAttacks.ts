/**
 * @file vechain_callTotalAttacks.ts
 * @description
 * Script to read attack data from a smart contract deployed on the VeChain testnet
 * using a read-only call to `getTotalAttacks` (sin gas ni firma).
 */

import { ThorClient } from '@vechain/sdk-network';

const contractABI= [
	{
		"anonymous": false,
		"inputs": [],
		"name": "AllAttacksDeleted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "AttackDeleted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "ipAddress",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "attackType",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "AttackLogged",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "attackType",
				"type": "string"
			}
		],
		"name": "AttacksByTypeDeleted",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "deleteAllAttacks",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "deleteAttack",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_attackType",
				"type": "string"
			}
		],
		"name": "deleteAttacksByType",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_attackType",
				"type": "string"
			}
		],
		"name": "getAllAttacksByType",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "ipAddress",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "attackType",
						"type": "string"
					},
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					}
				],
				"internalType": "struct DoSAttackRegistry.AttackRecord[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "index",
				"type": "uint256"
			}
		],
		"name": "getAttack",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTotalAttacks",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ipAddress",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_attackType",
				"type": "string"
			}
		],
		"name": "logAttack",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ipAddress",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_attackType",
				"type": "string"
			}
		],
		"name": "logAttackWithTypeTracking",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "records",
		"outputs": [
			{
				"internalType": "string",
				"name": "ipAddress",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "attackType",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] as const;



const nodeUrl = 'https://testnet.veblocks.net';
const CONTRACT_ADDRESS = '0x3503543A2dAD949457deC8CEBf09F9d28Ec42416';

async function getTotalAttacks() {
  // 1 - Inicializa el cliente Thor
  	const thorSoloClient = ThorClient.at(nodeUrl, { isPollingEnabled: false });

  // 2 - Carga el contrato
  	const contract = thorSoloClient.contracts.load(CONTRACT_ADDRESS, contractABI);

	const attacks = await contract.read.getTotalAttacks();
  
	const countNum = Number(attacks[0]);
	console.log(`Number of Registered Attacks: ${countNum}`);
}

getTotalAttacks().catch(console.error);