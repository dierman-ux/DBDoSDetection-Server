/**
 * @file vechain_logAttack.ts
 * @description
 * This script interacts with a smart contract deployed on the VeChain testnet.
 * It demonstrates how to log a DoS attack record by sending a transaction
 * to the `logAttack` method of the contract.
 * 
 * The process includes:
 * 1. Setting up the Thor client and contract instance.
 * 2. Preparing the transaction clauses.
 * 3. Estimating gas required for the transaction.
 * 4. Building and signing the transaction.
 * 5. Sending the transaction and waiting for confirmation.
 * 
 * Requirements:
 * - Node.js environment with '@vechain/sdk-core' and '@vechain/sdk-network' installed.
 * - Private key and address of the sender account with testnet funds.
 */


import { Address, Clause, HexUInt, Transaction} from '@vechain/sdk-core';
import { THOR_SOLO_URL, ThorClient} from '@vechain/sdk-network';
import {VeChainProvider,ProviderInternalBaseWallet,signerUtils} from '@vechain/sdk-network';
import { expect } from 'expect';

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
];

const nodeUrl = 'https://testnet.veblocks.net';

const CONTRACT_ADDRESS = '0x3503543A2dAD949457deC8CEBf09F9d28Ec42416';

// 1 - Build the thor client and load the contract

const thorSoloClient = ThorClient.at(nodeUrl, {
    isPollingEnabled: false
});

const contract = thorSoloClient.contracts.load(
    CONTRACT_ADDRESS,
    contractABI as unknown as any
);

// Sender account with private key
const senderAccount = {
    privateKey:
        '418dec66cd92055c700f3b4861c5650464bd6cd66b91937d015528b310556030',
    address: '0xDfCdED32c7339247B1eb88852BFdB30310c3F6Ec'
};

// Create the provider (used in this case to sign the transaction with getSigner() method)
const provider = new VeChainProvider(
    // Thor client used by the provider
    thorSoloClient,

    // Internal wallet used by the provider (needed to call the getSigner() method)
    new ProviderInternalBaseWallet([
        {
            privateKey: HexUInt.of(senderAccount.privateKey).bytes,
            address: senderAccount.address
        }
    ]),

    // Disable fee delegation (BY DEFAULT IT IS DISABLED)
    false
);

const ipAddress = '1.1.1.1';
const attackType = 'Prueba';

const logAttackClause = contract.clause.logAttack(ipAddress, attackType);

// Convert ContractClause to TransactionClause
const transactionClauses = [{
  to: CONTRACT_ADDRESS,
  value: '0',
  data: logAttackClause.clause.data // Ensure this is a string (hex data)
}];

// 2 - Create the transaction clauses
const transaction = {
  clauses: transactionClauses,
  simulateTransactionOptions: {
    caller: senderAccount.address
  }
};

async function main() {
// 3 - Estimate gas
const gasResult = await thorSoloClient.transactions.estimateGas(
    transaction.clauses,
    transaction.simulateTransactionOptions.caller
);

console.log("Estimated gas result:", gasResult);

// 4 - Build transaction body
const txBody = await thorSoloClient.transactions.buildTransactionBody(
    transaction.clauses,
    gasResult.totalGas
);

// 4 - Sign the transaction
const signer = await provider.getSigner(senderAccount.address);

if (!signer) {
    throw new Error('Signer not found for the provided address.');
}

const rawSignedTransaction = await signer.signTransaction(
    signerUtils.transactionBodyToTransactionRequestInput(
        txBody,
        senderAccount.address
    )
);

const signedTransaction = Transaction.decode(
    HexUInt.of(rawSignedTransaction.slice(2)).bytes,
    true
);

// 5 - Send the transaction
const sendTransactionResult =
    await thorSoloClient.transactions.sendTransaction(signedTransaction);

// 6 - Wait for transaction receipt
const txReceipt = await thorSoloClient.transactions.waitForTransaction(
    sendTransactionResult.id
);

}

main().catch(console.error);