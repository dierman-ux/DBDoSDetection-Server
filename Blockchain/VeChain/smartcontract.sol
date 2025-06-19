// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title DoSAttackRegistry
/// @notice Registro descentralizado de ataques DoS en VeChain
/// @dev Esta implementación no requiere control de acceso y asume un entorno abierto

contract DoSAttackRegistry {

    // ------------------------
    // 1. Estructura del registro
    // ------------------------

    /// @dev Cada ataque registrado contiene la IP atacante, el tipo de ataque y un timestamp
    struct AttackRecord {
        string ipAddress;
        string attackType;
        uint256 timestamp;
    }

    // ------------------------
    // 2. Variables de estado
    // ------------------------

    /// @dev Lista dinámica de ataques registrados
    AttackRecord[] public records;

    // ------------------------
    // 3. Eventos públicos para trazabilidad
    // ------------------------

    event AttackLogged(string ipAddress, string attackType, uint256 timestamp);
    event AttackDeleted(uint256 index);
    event AllAttacksDeleted();
    event AttacksByTypeDeleted(string attackType);

    // ------------------------
    // 4. Funciones de escritura
    // ------------------------

    /// @notice Registra un nuevo ataque en la lista
    /// @param _ipAddress Dirección IP atacante
    /// @param _attackType Tipo de ataque detectado
    function logAttack(string memory _ipAddress, string memory _attackType) public {
        AttackRecord memory record = AttackRecord(_ipAddress, _attackType, block.timestamp);
        records.push(record);
        emit AttackLogged(_ipAddress, _attackType, block.timestamp);
    }

    /// @notice Elimina un ataque específico por índice
    /// @param index Índice del ataque a borrar
    function deleteAttack(uint256 index) public {
        require(index < records.length, "Index out of bounds");

        // Mueve el último registro a la posición eliminada y borra el final
        records[index] = records[records.length - 1];
        records.pop();

        emit AttackDeleted(index);
    }

    /// @notice Elimina todos los registros de ataques
    function deleteAllAttacks() public {
        delete records;
        emit AllAttacksDeleted();
    }

    /// @notice Elimina todos los ataques de un tipo específico
    /// @param _attackType Tipo de ataque a eliminar
    function deleteAttacksByType(string memory _attackType) public {
        uint256 i = 0;
        while (i < records.length) {
            if (keccak256(bytes(records[i].attackType)) == keccak256(bytes(_attackType))) {
                records[i] = records[records.length - 1];
                records.pop();
            } else {
                i++;
            }
        }
        emit AttacksByTypeDeleted(_attackType);
    }

    // ------------------------
    // 5. Funciones de lectura
    // ------------------------

    /// @notice Retorna un ataque por su índice
    function getAttack(uint256 index) public view returns (string memory, string memory, uint256) {
        require(index < records.length, "Index out of bounds");
        AttackRecord memory record = records[index];
        return (record.ipAddress, record.attackType, record.timestamp);
    }

    /// @notice Retorna el número total de ataques registrados
    function getTotalAttacks() public view returns (uint256) {
        return records.length;
    }

    /// @notice Retorna todos los ataques de un tipo determinado
    function getAllAttacksByType(string memory _attackType) public view returns (AttackRecord[] memory) {
        // Cuenta los registros coincidentes
        uint256 count = 0;
        for (uint256 i = 0; i < records.length; i++) {
            if (keccak256(bytes(records[i].attackType)) == keccak256(bytes(_attackType))) {
                count++;
            }
        }

        // Construye un array con los resultados
        AttackRecord[] memory filtered = new AttackRecord[](count);
        uint256 j = 0;
        for (uint256 i = 0; i < records.length; i++) {
            if (keccak256(bytes(records[i].attackType)) == keccak256(bytes(_attackType))) {
                filtered[j] = records[i];
                j++;
            }
        }

        return filtered;
    }
}
