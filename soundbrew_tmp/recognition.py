#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import json
import argparse
from tqdm import tqdm
from contextlib import closing
from multiprocessing import Pool
from glob import glob
from functools import partial
from text.cleaners import english_cleaners

def text_recognition(path, config):
    root, ext = os.path.splitext(path)
    txt_path = root + ".txt"

    if os.path.exists(txt_path):
        with open(txt_path) as f:
            out = json.loads(open(txt_path).read())
            return out

    # if new api account is used, do resetting env file for google credential
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    out = {}
    error_count = 0

    tmp_path = os.path.splitext(path)[0] + ".wav"
    client = speech.SpeechClient() # Fixed

    while True:
        try:
            # client= speech.SpeechClient() # Causes 10060 max retries exceeded -to OAuth -HK
            content = path[0]

            with io.open(tmp_path, 'rb') as f:
                audio = types.RecognitionAudio(content=f.read())

            config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code='en-GB')

            response = client.recognize(config, audio)

            if len(response.results) > 0:
                alternatives = response.results[0].alternatives

                #results = 실제 음성인식된 text
                results = [alternative.transcript for alternative in alternatives]
                assert len(results) == 1, "More than 1 results: {}".format(results)

                #실질적으로 txt
                out = { os.path.basename(path): "" if len(results) == 0 else results[0] ,
                        "normalized_text": english_cleaners(results[0])}
                print(path, results[0], english_cleaners(results[0]))
                break
            break
        except Exception as err:
            raise Exception("OS error: {0}".format(err))

            error_count += 1
            print("Skip warning for {} for {} times".
                    format(path, error_count))

            if error_count > 5:
                break
            else:
                continue

    global removed
    if len(out) is 0:
        # remove file that only has instrument sound.
        os.remove(root + '.wav')
        print(root, '.wav file is removed!')

    else:
        with open(txt_path, 'w') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)

    return out

#콘솔창에 진행률 히스토그램 찍어주는 함수
def parallel_run(fn, items, desc="", parallel=True):
    results = []

    if parallel:
        with closing(Pool()) as pool:
            for out in tqdm(pool.imap_unordered(
                    fn, items), total=len(items), desc=desc):
                if out is not None:
                    results.append(out)
    else:
        for item in tqdm(items, total=len(items), desc=desc):
            out = fn(item)
            if out is not None:
                results.append(out)

    return results

def text_recognition_batch(paths, config):

    num_of_removed_file = [0]

    paths.sort()

    results = {}
    items = parallel_run(
            partial(text_recognition, config=config), paths,
            desc="text_recognition_batch", parallel=True)
    for item in items:
        results.update(item)

    print('Recognition process is successfully completed!')
    return results

def main():

    parser = argparse.ArgumentParser()
    # input: wav파일들이 위치한 디렉토리 이름 (예: ./test_audio/ )
    parser.add_argument('--target', required=True, choices=['Benedict', 'Test'])
    parser.add_argument('--recognition_filename', default="recognition.json")
    config, unparsed = parser.parse_known_args()

    # audio 파일이 있는 디렉토리
    audio_dir = os.path.join(os.path.abspath(''), 'assets', config.target, 'wavs')

    # 디렉토리내에 있는 wav파일들을 담는 배열
    paths = []
    for tmp_path in glob(os.path.join(audio_dir, "*.wav")):
        paths.append(tmp_path)

    text_recognition_batch(paths, config)



if __name__ == '__main__':
    main()
