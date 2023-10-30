# Convert JSON files to CSV files (if original file is CSV then relocate).
# the original data is always placed in the folder: ./data/origin

# Written by: Zhiwei Chang
# Last modified: 2023-10-17

import os
import shutil
import re
import json
import datetime
import pandas as pd
from bs4 import BeautifulSoup

current_datetime = datetime.datetime.now()
current_date_string = current_datetime.strftime("%Y%m%d")
current_date_string

data_path = "./data/generated/"
isExist = os.path.exists(data_path)
if not isExist:
    os.makedirs(data_path)


def main():

    path = './data/origin'
    isPath = os.path.exists(path)
    if not isPath:
        print("The path is not exist! Please place the original JSON/csv files in the folder: ./data/origin")

    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]

        if ext == '.json':
            json_name = os.path.splitext(f)[0]
            filename = re.split('_', json_name)[0] + '_' + current_date_string + '.csv'
            with open(os.path.join(path, f)) as file:
                json_data = json.load(file)
            df = pd.DataFrame(json_data)

            content_txt = []
            for i in range(len(df)):
                txt = df[df.columns[-1]][i] # always assume the last column is the content.  
                soup = BeautifulSoup(txt, 'html.parser')
                content = soup.get_text()
                content_txt.append(content)

            df['content_txt'] = content_txt
            
            df.to_csv(data_path + filename,index=False)
            print("converting " + json_name + " to " + filename + " ..." )

        elif ext == '.csv':
            shutil.copy(os.path.join(path, f), data_path)
            os.rename(data_path +f, data_path +os.path.splitext(f)[0]+"_"+current_date_string+".csv")
            print("copying " + f + " to " + data_path + " ..." )

if __name__ == "__main__":
    main() 