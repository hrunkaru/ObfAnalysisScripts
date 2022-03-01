import csv
import json

# parameters
path_summaryCSV = "LOLBAS_cmd_summary.csv"
path_outputconfig = "config_for_obfstesttool.jsonl"

# open CSV summary file
with open(path_summaryCSV) as summaryCSV:
    with open(path_outputconfig, mode='w+') as outputconfig:
        csv_data = csv.DictReader(summaryCSV)

        for csv_line in csv_data:
            if(csv_line["Category"] in ["OSLibraries", "OSBinaries"]):
                output_line = {}
                output_line["command"] = csv_line["Command"]
                
                if(csv_line["Command Privileges"] != "User"):
                    output_line["elevated"] = True

                output_line["timeout"] = 5

                output_line["range"] = "full"

                outputconfig.write(json.dumps(output_line, sort_keys=True) + "\n")