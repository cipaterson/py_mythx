#!/usr/bin/env python3
import os
import re
from pythx import Client
import solcx

source_code = '''
    //SPDX-License-Identifier: UNLICENSED
    /*
    * @source: https://gist.github.com/manojpramesh/336882804402bee8d6b99bea453caadd#file-odd-even-sol
    * @author: https://github.com/manojpramesh
    * Modified by Kaden Zipfel
    */

    pragma solidity ^0.5.0;

    contract OddEven {
        struct Player {
            address addr;
            uint number;
        }

        Player[2] private players;
        uint count = 0;

        function play(uint number) public payable {
                require(msg.value == 1 ether, 'msg.value must be 1 eth');
                players[count] = Player(msg.sender, number);
                count++;
                if (count == 2) selectWinner();
        }

        function selectWinner() private {
                uint n = players[0].number + players[1].number;
                (bool success, ) = players[n%2].addr.call.value(address(this).balance)("");
                require(success, 'transfer failed');
                delete players;
                count = 0;
        }
    }
'''
sol_version='latest'
for item in source_code.split("\n"):
    if "pragma" in item:
        sol_version = re.search('\d*\.\d*\.\d*', item)[0]
        break

sol_version = solcx.install_solc(version=sol_version)
solcx.set_solc_version(sol_version)
compiled_sol = solcx.compile_source(source_code, output_values=['abi', 'bin'])

contract_id, contract_interface = compiled_sol.popitem()
main_source = contract_id
bytecode = contract_interface['bin']

# Instantiate the pythx client
c = Client(api_key=os.environ.get('MYTHX_API_KEY'))

# Submit the bytecode and source for analysis
resp = c.analyze(bytecode=bytecode, main_source=main_source,
                 sources={main_source: {'source': source_code}})

# wait for the analysis to finish
while not c.analysis_ready(resp.uuid):
    time.sleep(1)

# have all your security report data at your fingertips
for issue_report in c.report(resp.uuid).issue_reports:
    for issue in issue_report.issues:
        print(issue.swc_id, issue.swc_title or "Undefined", "-", issue.description)
