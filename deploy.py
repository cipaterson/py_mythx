#!/usr/bin/env python
import time
import os
import sys
from pythx import Client
import solcx

if len(sys.argv) < 2:
    print('Usage:  Provide contract filename:')
    print(f'{sys.argv[0]} contract.sol')
    exit(1)

# solidity source
sol_file_path = sys.argv[1]

# Instantiate the pythx client
c = Client(api_key=os.environ.get('MYTHX_API_KEY'))

# Read the Solidity file
with open(sol_file_path, "r") as f:
    source_code = f.read()

out = solcx.compile_source(source_code, output_values=['bin', 'srcmap']) ##, solc_version="0.7.0")
print(out)
exit()
for k,v in out.items():
    print(k)
    bytecode = v['bin']
    break       # we're only processing the first contract in the file today

