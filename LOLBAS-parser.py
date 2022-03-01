import os
from pathlib import Path
import yaml
# pip3 install pyyml to install module 'yaml'
import csv

def cleanYAMLlastline(data):
    if (data[-1:][0] == "---\n"):
            newdata = data[:-1]
    return newdata

def createFilepaths(pathToYamls):
    filepaths = []
    subdir_list = os.listdir(pathToYamls)
    for dir in subdir_list:
        filenames = os.listdir(Path(pathToYamls, dir))
        for filename in filenames:
            filepaths.append(str((Path(dir, filename))))
    return filepaths

def createCSVsummary(filepaths_list):
    with open (pathToOutputCSV, 'w') as csv_out:

        #Create CSV header
        writer = csv.writer(csv_out)
        writer.writerow(["Category", "Name", "Description", "Created", "Command", "Command Description", "Command Category", "Command Usecase", "Command Privileges", "Command OperatingSystem", "Command MitreID"])

        for file in filepaths_list:
            splitname = file.split(".")

            with open(Path(pathToYAMLs, file), 'r') as yaml_in:
                lines = yaml_in.readlines()
                # Clean YAML files from appended '---' when no item is following
                yaml_data = cleanYAMLlastline(lines)
                data = yaml.load(''.join(yaml_data), Loader=yaml.FullLoader)

                recordtype = file.split("/")[-2]

                common_values = []
                common_values.append(recordtype)
                common_values.append(data['Name'])
                common_values.append(data['Description'])
                common_values.append(data['Created'])
                
                for command in data['Commands']:
                    #print(command)
                    write_values = []
                    write_values.extend(common_values)
                    write_values.append(command['Command'])
                    write_values.append(command['Description'])
                    write_values.append(command['Category'])
                    write_values.append(command['Usecase'] if ('Usecase' in command) else "N/A")
                    #write_values.append(command['Usecase'])
                    write_values.append(command['Privileges'])
                    write_values.append(command['OperatingSystem'] if ('OperatingSystem' in command) else "N/A")
                    #write_values.append(command['OperatingSystem'])
                    write_values.append(command['MitreID'])
                    writer.writerow(write_values)




if __name__ == "__main__":

    # TODO: Add commandline argument parsing to replace hardcoded parameters

    # path to local copy of LOLBAS project files from this project:
    # https://github.com/LOLBAS-Project/LOLBAS
    pathToLOLBAS = "LOLBAS-data/LOLBAS-master"
    pathToYAMLs = Path(pathToLOLBAS, "yml")
    pathToOutputCSV = 'LOLBAS_cmd_summary.csv'
    
    # create list of filepaths to iterate
    filepaths = createFilepaths(pathToYAMLs)

    # create CSV summary of LOLBAS yaml files
    createCSVsummary(filepaths)
