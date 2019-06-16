#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from glob import glob
import pandas as pd
import argparse
import json
from tqdm import tqdm

def generate_metadata(args):

    speaker = args.target
    in_dir = os.path.join(os.path.abspath(''), 'assets', speaker, 'wavs')

    paths=[]
    for tmp_path in glob(os.path.join(in_dir, "*.txt")):
        paths.append(tmp_path)

    f_filter = ["txt"] # a list containing the desired file extensions to be matched
    m = [] # final match list
    # out_dir = os.path.join(os.path.abspath(''), args.output, args.target)

    print('Started writing metadata.csv operation')
    for file in tqdm(paths, desc='Writing metadata...'):
        file_name = os.path.basename(file) # 파일 이름 추출

        file_ext = file_name.split(".")[-1].lower() # 파일 확장자 추출


        if file_ext in f_filter:
            with open(file) as json_file:
                json_data = json.load(json_file)
                original_text = json_data[file_name.replace(file_ext, "wav")]
                normalized_text = json_data["normalized_text"]
            label = os.path.splitext(file_name)[0]+"|"+original_text+"|"+normalized_text
            #label = f_name[0] + f_ext[-1] # as per your example, first char of file_name and last of file_ext
            #m.append([f_path, f_name, f_ext, label]) # append to match list
            print(label)
            m.append(label)

    df = pd.DataFrame(m, columns=['label']) # create a dataframe from match list
    #metadata_dir = os.path.pardir
    #print(metadata_dir)
    df.to_csv(os.path.join(os.path.abspath(''), 'assets', args.target, 'metadata.csv'), index=False, header=False) # create csv from df
    print("metadata.csv is successfully created!")

def main():
    parser = argparse.ArgumentParser()
    #input: wav와 txt파일들이 위치한 디렉토리 이름 (예: ./test_audio/ )
    parser.add_argument('--target', required=True, choices=['Benedict', 'Test'])
    args = parser.parse_args()

    #print(paths)
    generate_metadata(args)



if __name__ == '__main__':
  main()
