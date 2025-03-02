require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

module.exports = {
  solidity: "0.8.28",
  networks: {
    ganache: {
      url: process.env.WEB3_PROVIDER_URL, // "http://127.0.0.1:7545"
      accounts: [process.env.PRIVATE_KEY],
      chainId: 1337  // Sử dụng chainId phù hợp với Ganache (thường là 1337 hoặc 5777)
    }
  }
};
