const PhishingLog = artifacts.require("PhishingLog");

module.exports = function (deployer) {
  deployer.deploy(PhishingLog);
};
