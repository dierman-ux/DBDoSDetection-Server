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
var sdk_core_1 = require("@vechain/sdk-core");
var sdk_network_1 = require("@vechain/sdk-network");
var sdk_network_2 = require("@vechain/sdk-network");
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
var thorSoloClient = sdk_network_1.ThorClient.at(nodeUrl, {
    isPollingEnabled: false
});
var contract = thorSoloClient.contracts.load(CONTRACT_ADDRESS, contractABI);
var senderAccount = {
    privateKey: '418dec66cd92055c700f3b4861c5650464bd6cd66b91937d015528b310556030',
    address: '0xDfCdED32c7339247B1eb88852BFdB30310c3F6Ec'
};
var provider = new sdk_network_2.VeChainProvider(thorSoloClient, new sdk_network_2.ProviderInternalBaseWallet([
    {
        privateKey: sdk_core_1.HexUInt.of(senderAccount.privateKey).bytes,
        address: senderAccount.address
    }
]), false);
function deleteAllAttacks() {
    return __awaiter(this, void 0, void 0, function () {
        var deleteClause, transactionClauses, gasResult, txBody, signer, rawSignedTx, signedTx, sendResult, receipt;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    deleteClause = contract.clause.deleteAllAttacks();
                    transactionClauses = [{
                            to: CONTRACT_ADDRESS,
                            value: '0',
                            data: deleteClause.clause.data
                        }];
                    return [4 /*yield*/, thorSoloClient.transactions.estimateGas(transactionClauses, senderAccount.address)];
                case 1:
                    gasResult = _a.sent();
                    console.log("Estimated gas result:", gasResult);
                    return [4 /*yield*/, thorSoloClient.transactions.buildTransactionBody(transactionClauses, gasResult.totalGas)];
                case 2:
                    txBody = _a.sent();
                    return [4 /*yield*/, provider.getSigner(senderAccount.address)];
                case 3:
                    signer = _a.sent();
                    if (!signer)
                        throw new Error('Signer not found.');
                    return [4 /*yield*/, signer.signTransaction(sdk_network_2.signerUtils.transactionBodyToTransactionRequestInput(txBody, senderAccount.address))];
                case 4:
                    rawSignedTx = _a.sent();
                    signedTx = sdk_core_1.Transaction.decode(sdk_core_1.HexUInt.of(rawSignedTx.slice(2)).bytes, true);
                    return [4 /*yield*/, thorSoloClient.transactions.sendTransaction(signedTx)];
                case 5:
                    sendResult = _a.sent();
                    console.log("Transaction sent, ID:", sendResult.id);
                    return [4 /*yield*/, thorSoloClient.transactions.waitForTransaction(sendResult.id)];
                case 6:
                    receipt = _a.sent();
                    console.log("Transaction confirmed:", receipt);
                    return [2 /*return*/];
            }
        });
    });
}
deleteAllAttacks().catch(console.error);
