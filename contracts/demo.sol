pragma solidity >=0.5.8;

contract Demo {
    event Echo(string message);

    function echo(string calldata message) internal {
        emit Echo(message);
    }
}

contract Hello is Demo {
  function hello(string calldata name) external {
    echo(name);
  }
}