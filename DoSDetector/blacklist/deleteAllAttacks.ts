import { Address, Clause, HexUInt, Transaction } from '@vechain/sdk-core';
import { THOR_SOLO_URL, ThorClient } from '@vechain/sdk-network';
import {
  VeChainProvider,
  ProviderInternalBaseWallet,
  signerUtils
} from '@vechain/sdk-network';

const contractABI = [
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

const thorSoloClient = ThorClient.at(nodeUrl, {
  isPollingEnabled: false
});

const contract = thorSoloClient.contracts.load(
  CONTRACT_ADDRESS,
  contractABI as any
);

const senderAccount = {
  privateKey: '418dec66cd92055c700f3b4861c5650464bd6cd66b91937d015528b310556030',
  address: '0xDfCdED32c7339247B1eb88852BFdB30310c3F6Ec'
};

const provider = new VeChainProvider(
  thorSoloClient,
  new ProviderInternalBaseWallet([
    {
      privateKey: HexUInt.of(senderAccount.privateKey).bytes,
      address: senderAccount.address
    }
  ]),
  false
);

async function deleteAllAttacks() {
  // 1. Construir la cláusula para llamar a deleteAllAttacks
  const deleteClause = contract.clause.deleteAllAttacks();

  const transactionClauses = [{
    to: CONTRACT_ADDRESS,
    value: '0',
    data: deleteClause.clause.data
  }];

  // 2. Estimar gas
  const gasResult = await thorSoloClient.transactions.estimateGas(
    transactionClauses,
    senderAccount.address
  );

  console.log("Estimated gas result:", gasResult);

  // 3. Crear el cuerpo de la transacción
  const txBody = await thorSoloClient.transactions.buildTransactionBody(
    transactionClauses,
    gasResult.totalGas
  );

  // 4. Firmar la transacción
  const signer = await provider.getSigner(senderAccount.address);
  if (!signer) throw new Error('Signer not found.');

  const rawSignedTx = await signer.signTransaction(
    signerUtils.transactionBodyToTransactionRequestInput(
      txBody,
      senderAccount.address
    )
  );

  const signedTx = Transaction.decode(
    HexUInt.of(rawSignedTx.slice(2)).bytes,
    true
  );

  // 5. Enviar la transacción
  const sendResult = await thorSoloClient.transactions.sendTransaction(signedTx);

  console.log("Transaction sent, ID:", sendResult.id);

  // 6. Esperar recibo
  const receipt = await thorSoloClient.transactions.waitForTransaction(sendResult.id);
  console.log("Transaction confirmed:", receipt);
}

deleteAllAttacks().catch(console.error);
