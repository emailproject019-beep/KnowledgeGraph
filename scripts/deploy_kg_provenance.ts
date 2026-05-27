import { ethers } from "hardhat";

async function main() {
  const KGProvenance = await ethers.getContractFactory("KGProvenance");
  const contract = await KGProvenance.deploy();

  await contract.waitForDeployment();

  console.log("KGProvenance deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
