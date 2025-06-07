/**
 * logAttack.js
 * 
 * This script interacts with a VeChain smart contract deployed on the testnet to log Denial-of-Service (DoS) attacks.
 * It uses the VeChain SDK Core and Network libraries to build, sign, and send transactions to the blockchain.
 * 
 * Usage:
 *   node logAttack.js <ip_address> <attack_type>
 * 
 * Example:
 *   node logAttack.js 192.168.1.100 SYN_FLOOD
 * 
 * The script sends a transaction calling the `logAttack` function of the smart contract,
 * which records the IP address and attack type with a timestamp on the blockchain.
 */

"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};

Object.defineProperty(exports, "__esModule", { value: true });

// Import necessary classes and functions from VeChain SDK Core and Network libraries
var sdk_core_1 = require("@vechain/sdk-core");
var sdk_network_1 = require("@vechain/sdk-network");
var sdk_network_2 = require("@vechain/sdk-network");

// ABI of the deployed smart contract to interact with
var contractABI = [
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
var nodeUrl = 'https://testnet.veblocks.net';
var CONTRACT_ADDRESS = '0x3503543A2dAD949457deC8CEBf09F9d28Ec42416';
// Build the thor client and load the contract
var thorSoloClient = sdk_network_1.ThorClient.at(nodeUrl, {
    isPollingEnabled: false
});
var contract = thorSoloClient.contracts.load(CONTRACT_ADDRESS, contractABI);
// Sender account with private key
var senderAccount = {
    privateKey: '418dec66cd92055c700f3b4861c5650464bd6cd66b91937d015528b310556030',
    address: '0xDfCdED32c7339247B1eb88852BFdB30310c3F6Ec'
};
// Create the provider (used in this case to sign the transaction with getSigner() method)
var provider = new sdk_network_2.VeChainProvider(
// Thor client used by the provider
thorSoloClient, 
// Internal wallet used by the provider (needed to call the getSigner() method)
new sdk_network_2.ProviderInternalBaseWallet([
    {
        privateKey: sdk_core_1.HexUInt.of(senderAccount.privateKey).bytes,
        address: senderAccount.address
    }
]), 
// Disable fee delegation (BY DEFAULT IT IS DISABLED)
false);


/**
 * Sends a logAttack transaction to the smart contract, recording an attack on-chain.
 * @param ipAddress The IP address of the attacker (string)
 * @param attackType The type of attack (string)
 */
function sendAttack(ipAddress, attackType) {
    var logAttackClause = contract.clause.logAttack(ipAddress, attackType);
    // Convert ContractClause to TransactionClause
    var transactionClauses = [{
            to: CONTRACT_ADDRESS,
            value: '0',
            data: logAttackClause.clause.data // Ensure this is a string (hex data)
        }];
    // Create the transaction clauses
    var transaction = {
        clauses: transactionClauses,
        simulateTransactionOptions: {
            caller: senderAccount.address
        }
    };

    return __awaiter(this, void 0, void 0, function () {
        var gasResult, txBody, signer, rawSignedTransaction, signedTransaction, sendTransactionResult, txReceipt;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, thorSoloClient.transactions.estimateGas(transaction.clauses, transaction.simulateTransactionOptions.caller)];
                case 1:
                    gasResult = _a.sent();
                    console.log("Estimated gas result:", gasResult);
                    return [4 /*yield*/, thorSoloClient.transactions.buildTransactionBody(transaction.clauses, gasResult.totalGas)];
                case 2:
                    console.log("Building transaction body...");
                    txBody = _a.sent();
                    console.log("Transaction body:", txBody);
                    return [4 /*yield*/, provider.getSigner(senderAccount.address)];
                case 3:
                    console.log("Getting signer for address:", senderAccount.address);
                    signer = _a.sent();
                    console.log("Signer retrieved:", signer);
                    if (!signer) {
                        throw new Error('Signer not found for the provided address.');
                    }
                    return [4 /*yield*/, signer.signTransaction(sdk_network_2.signerUtils.transactionBodyToTransactionRequestInput(txBody, senderAccount.address))];
                case 4:
                    console.log("Signing transaction...");
                    rawSignedTransaction = _a.sent();
                    signedTransaction = sdk_core_1.Transaction.decode(sdk_core_1.HexUInt.of(rawSignedTransaction.slice(2)).bytes, true);
                    console.log("Signed transaction:", signedTransaction);
                    return [4 /*yield*/, thorSoloClient.transactions.sendTransaction(signedTransaction)];
                case 5:
                    console.log("Sending transaction...");
                    sendTransactionResult = _a.sent();
                    console.log("Transaction sent, ID:", sendTransactionResult.id);
                    return [2 /*return*/];
            }
        });
    });
}

module.exports = { sendAttack };

// If the script is run directly, parse arguments and call sendAttack
if (require.main === module) {
  const [, , ip, type] = process.argv;

  if (!ip || !type) {
    console.error("Uso: node logAttack.js <ip> <tipo_ataque>");
    process.exit(1);
  }

  sendAttack(ip, type)
    .then(() => console.log("Ataque registrado correctamente"))
    .catch((err) => console.error("Error:", err));
}
