package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/v2/contractapi"
)

// SmartContract provides functions for managing sensor data
type SmartContract struct {
	contractapi.Contract
}

// SensorData defines the structure for storing sensor information
type Asset struct {
	Node      string  `json:"node"`
	PacketID  int     `json:"packet_id"`
	Temp      float64 `json:"Temp"`
	Hum       float64 `json:"Hum"`
	Pres      string  `json:"Pres"`
	Length    int     `json:"length"`
	Iteration string  `json:"iteration"`
}

// InitLedger adds a base set of sensor data to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	data := []Asset{
		{Node: "node_01", PacketID: 0, Temp: 21.75, Hum: 27.74, Pres: "97170.78_#BAT:75#", Length: 85, Iteration: "1"},
		{Node: "node_01", PacketID: 1, Temp: 20.81, Hum: 29.82, Pres: "97176.59_#BAT:100#", Length: 86, Iteration: "2"},
	}

	for _, entry := range data {
		entryJSON, err := json.Marshal(entry)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(entry.Iteration, entryJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state: %v", err)
		}
	}

	return nil
}

// CreateAsset stores new sensor data in the world state
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, node string, packetID int, temp float64, hum float64, pres string, length int, iteration string) error {
	exists, err := s.AssetExists(ctx, iteration)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the sensor data %s already exists", iteration)
	}

	data := Asset{
		Node: node, PacketID: packetID, Temp: temp, Hum: hum, Pres: pres, Length: length, Iteration: iteration,
	}
	dataJSON, err := json.Marshal(data)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(iteration, dataJSON)
}

// ReadAsset retrieves sensor data from the world state
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, iteration string) (*Asset, error) {
	dataJSON, err := ctx.GetStub().GetState(iteration)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if dataJSON == nil {
		return nil, fmt.Errorf("the sensor data %s does not exist", iteration)
	}

	var data Asset
	err = json.Unmarshal(dataJSON, &data)
	if err != nil {
		return nil, err
	}

	return &data, nil
}

// UpdateAsset updates existing sensor data in the world state
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, node string, packetID int, temp float64, hum float64, pres string, length int, iteration string) error {
	exists, err := s.AssetExists(ctx, iteration)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the sensor data %s does not exist", iteration)
	}

	data := Asset{
		Node: node, PacketID: packetID, Temp: temp, Hum: hum, Pres: pres, Length: length, Iteration: iteration,
	}
	dataJSON, err := json.Marshal(data)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(iteration, dataJSON)
}

// DeleteAsset removes sensor data from the world state
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, iteration string) error {
	exists, err := s.AssetExists(ctx, iteration)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the sensor data %s does not exist", iteration)
	}

	return ctx.GetStub().DelState(iteration)
}

// AssetExists checks if sensor data exists in the world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, iteration string) (bool, error) {
	dataJSON, err := ctx.GetStub().GetState(iteration)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return dataJSON != nil, nil
}

func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	const pageSize = 100
	var allData []*Asset
	startKey := ""

	for {
		resultsIterator, responseMetadata, err := ctx.GetStub().GetStateByRangeWithPagination(startKey, "", pageSize, "")
		if err != nil {
			return nil, err
		}
		for resultsIterator.HasNext() {
			queryResponse, err := resultsIterator.Next()
			if err != nil {
				resultsIterator.Close()
				return nil, err
			}

			var data Asset
			err = json.Unmarshal(queryResponse.Value, &data)
			if err != nil {
				resultsIterator.Close()
				return nil, err
			}
			allData = append(allData, &data)
		}

		if responseMetadata.Bookmark == "" {
			break
		}
		startKey = responseMetadata.Bookmark
		resultsIterator.Close()
	}

	return allData, nil
}
