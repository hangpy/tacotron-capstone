from pydub import AudioSegment
from util.silence import split_on_silence
from glob import glob
from tqdm import tqdm
import os
import argparse
import audioread
import datetime

'''
    This function is for splitting existing long audio file to smaller files.
'''

def remove_original_audio():
    print()


def split_smaller_operation(target, version, len_silence):

    # audio file to split
    target_dir = os.path.join(os.path.abspath(''), 'assets', target, 'wavs')

    file_pattern = 'BN*_*.wav'
    audio_list = glob(os.path.join(target_dir, file_pattern))
    long_audio_list = []

    num = 0
    gross_duration = 0
    for file in audio_list:
        file_duration = audioread.audio_open(file).duration
        if file_duration > 12.500:
            num += 1
            gross_duration += file_duration
            print(file, 'duration: ', file_duration)
            long_audio_list.append(file)
    print('The number of audio files longer than 12.5 secs: ', len(long_audio_list))
    print('The gross duration of audio files longer than 12.5 secs: ', str(datetime.timedelta(seconds=gross_duration)))

    # if all audio file is shorter than 12.5
    if len(long_audio_list) is 0:
        return

    # Each long audio file shiould be splitted again
    v_splited_num = 0
    index = 1
    for file_to_split in long_audio_list:
        audio_file = AudioSegment.from_file(file_to_split, format="wav")
        print('[V', version, ']', 'Split operation is started!')
        audio_chunks = split_on_silence(audio_file,
                                        # must be silent for at least half a second
                                        min_silence_len=len_silence,
                                        # consider it silent if quieter than -16 dBFS
                                        silence_thresh=-40, keep_silence=500)

        for i, chunk in tqdm(enumerate(audio_chunks, 1), desc='loading...'):
            out_file = os.path.join(target_dir, 'BN%02d_%05d.wav' % (version, index))
            chunk.export(out_file, format="wav")
            chunk_size = os.stat(out_file).st_size
            if chunk_size < 130000:
                os.remove(out_file)
                continue
            else:
                v_splited_num += 1
                index += 1
        print('[V', version, ']', 'Split operation is completed!')
        print('%d audio chunks were generated' % v_splited_num)

    # remove original long audio files after spliting
    for file_to_remove in long_audio_list:
        txt_file_to_remove = file_to_remove.split('.')[0] + '.txt'
        os.remove(file_to_remove)
        if os.path.exists(txt_file_to_remove):
            os.remove(txt_file_to_remove)

    # recursive! by presenting smaller length of base silence and next version to distinguish with original files
    split_smaller_operation(target, version+1, len_silence-100)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True, choices=['Test', 'Benedict'])
    parser.add_argument('--version', required=True, type=int, help='present version of audio batch file to split')
    args = parser.parse_args()

    # python split_audio.py --input [path for audio file to split] --target Benedict --version 1
    # tacotron/assets/Benedict/wavs directory will be created
    split_smaller_operation(args.target, args.version, 750)


if __name__ == '__main__':
    main()



