from pydub import AudioSegment
from util.silence import split_on_silence
from glob import glob
from tqdm import tqdm
import os
import argparse

def split_operation(args):

    # audio file to split
    input_file = args.input
    target_dir = os.path.join(os.path.abspath(''), 'assets', args.target)
    # output directory splitted audio files will be stored
    out_dir = os.path.join(os.path.abspath(''), 'assets', args.target, 'wavs')

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)


    file_pattern = 'BN%02d_*.wav' % args.version
    last_index = None
    existing_audio_files = glob(os.path.join(out_dir, file_pattern))
    if len(existing_audio_files) is not 0:
        existing_audio_files.sort(reverse=True)
        last_file = os.path.basename(existing_audio_files[0])
        last_index = int(last_file.split('_')[1].split('.')[0])
    #     becuase the index is started from 0
    else:
        last_index = 0



    audio_file = AudioSegment.from_file(input_file, format="mp3")

    # 48khz -> 16khz for google speech api usage
    audio_file = audio_file.set_frame_rate(16000)
    # multiple channel -> one channel for google speech api usage
    audio_file = audio_file.set_channels(1)

    print('Split operation is started')

    audio_chunks = split_on_silence(audio_file,
                                    # must be silent for at least half a second
                                    min_silence_len=850,

                                    # consider it silent if quieter than -16 dBFS
                                    silence_thresh=-40, keep_silence=500)
    num_of_chunks = len(audio_chunks)

    # for i, chunk in tqdm(enumerate(audio_chunks, 1), desc='loading...'):
    #     out_file = os.path.join(out_dir, 'BN%02d_%05d.wav' % (args.version, i + last_index))
    #     chunk.export(out_file, format="wav")


    i = 1
    for chunk in tqdm(audio_chunks, desc='loading...'):
        out_file = os.path.join(out_dir, 'BN%02d_%05d.wav' % (args.version, i + last_index))
        chunk.export(out_file, format="wav")
        chunk_size = os.stat(out_file).st_size
        if chunk_size < 130000 or chunk_size > 1000000:
            os.remove(out_file)
            continue
        i = i + 1

    print('Split operation is successfully completed')
    print('%d audio chunks were generated' % i)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--version', required=True, type=int, help='present version of audio batch file to split')
    args = parser.parse_args()

    # python split_audio.py --input [path for audio file to split] --target Benedict --version 1
    # tacotron/assets/Benedict/wavs directory will be created
    split_operation(args)


if __name__ == '__main__':
    main()