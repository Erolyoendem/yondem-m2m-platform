import json
from solcx import compile_standard, install_solc
from pathlib import Path

install_solc("0.8.19")

def compile_contract(contract_name):
    contract_path = Path(f"/Users/haksystems/Yondem-M2M-Platform/03-Implementation/mcp-server/blockchain/contracts/{contract_name}.sol")
    
    with open(contract_path, "r") as f:
        source = f.read()
    
    compiled = compile_standard({
        "language": "Solidity",
        "sources": {f"{contract_name}.sol": {"content": source}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        }
    }, solc_version="0.8.19")
    
    contract_data = compiled["contracts"][f"{contract_name}.sol"][contract_name]
    
    abi_path = contract_path.with_suffix(".abi")
    bin_path = contract_path.with_suffix(".bin")
    
    with open(abi_path, "w") as f:
        json.dump(contract_data["abi"], f, indent=2)
    
    with open(bin_path, "w") as f:
        f.write(contract_data["evm"]["bytecode"]["object"])
    
    print(f"✅ {contract_name} kompiliert")
    print(f"   ABI: {abi_path}")
    print(f"   BIN: {bin_path}")

if __name__ == "__main__":
    compile_contract("YDMToken")
    compile_contract("PublisherContract")
    print("\\n🎉 Alle Contracts kompiliert!")
