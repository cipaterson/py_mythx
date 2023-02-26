#!/usr/bin/env python3
import time
import os
import sys
from pythx import Client
import solcx

if len(sys.argv) < 2:
    print('Usage:  Provide contract filename:')
    print(f'{sys.argv[0]} contract.sol')
    exit(1)

# solidity source filename
sol_file_path = sys.argv[1]

# Instantiate the pythx client
c = Client(api_key=os.environ.get('MYTHX_API_KEY'))

# Read the Solidity file
with open(sol_file_path, "r") as f:
    source_code = f.read()

out = solcx.compile_source(source_code, output_values=['bin', 'srcmap'])

for k,v in out.items():
    bytecode = v['bin']
    break       # we're only processing the first contract in the file today

# Submit the bytecode and source for analysis
resp = c.analyze(bytecode=bytecode, main_source=sol_file_path, sources={sol_file_path: {'source': source_code}})

# wait for the analysis to finish
while not c.analysis_ready(resp.uuid):
    time.sleep(1)

# have all your security report data at your fingertips
for issue_report in c.report(resp.uuid).issue_reports:
    for issue in issue_report.issues:
        print(issue.swc_id, issue.swc_title or "Undefined", "-", issue.description)
