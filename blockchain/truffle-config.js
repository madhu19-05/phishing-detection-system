module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545, // Port used by Ganache CLI
      network_id: "*", // Match any network id
    },
  },
  compilers: {
    solc: {
      version: "0.8.0", // Specify your Solidity version
    },
  },
};
