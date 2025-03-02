const hre = require("hardhat");

async function main() {
  // Lấy factory của smart contract
  const DataProvenance = await hre.ethers.getContractFactory("DataProvenance");
  // Deploy contract
  const contract = await DataProvenance.deploy();
  // Chờ cho đến khi contract được deploy hoàn tất (ethers v6)
  await contract.waitForDeployment();
  console.log("Contract deployed to:", contract.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
