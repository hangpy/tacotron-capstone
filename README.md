# Single-Speaker Tacotron in TensorFlow

The cloned project actually include multi-speaker model with deep-voice of Baidu. However, for the time being, we decided to use only Single-Speaker model because it is enough to proceed project.

<br>

<br>

## 1. Construct virtual environment

You must activate venv environment for running python library with tensorflow and so on.

With supposing you installed venv on project's root directory with naming 'venv', you can use below command script on bash shell

```
#window
source venv/Script/activate

#mac
source venv/bin/activate
```

<br>

<br>

## 2. Checking mode (en, kor)

In hparams.py, search 'kor' and follow the above comments. Just select one.

```python
basic_params = {
    # 'cleaners': 'korean_cleaners',
    'cleaners': 'english_cleaners', #can be substitued
}

basic_params.update({
    # Eval
    'min_tokens': 50, #originally 50, this is for english
    # 'min_tokens': 30, # this is for korean
})
```

<br>

<br>

## 3. Preprocessing and Training

The `datasets` directory should look like:

```
datasets
├── kss
│   ├── data (training data is here)
│   ├── alignment.json
|   ├── metadata.csv (it can be any form)
|   ├── prepare.py (customized based on downloaded dataset's structure)
│   ├── wavs
│   │   ├── -----------------
│   │   ├── 1
│   │   ├── 2
│   │   ├── ... own structure
│   │   └── -----------------
│   └── transcript.v.1.2.txt
│
├── WEB
│   ├── data (training data is here)
│   ├── alignment.json
|   ├── metadata.csv (it can be any form)
|   ├── prepare.py (customized based on downloaded dataset's structure)
│   ├── wavs
│   │   ├── -----------------
│   │   ├── Act
│   │   ├── Amos
│   │   ├── ... own structure
│   │   └── -----------------
│   └── transcript.txt
│
├── benedict
│    ├── ...
│    └── ...
│
├── LJSpeech_1_0
│    ├── ...
│    └── ...
│ 
├── __init__.py
├── datafeeder.py
└── generate_data.py
```

and `YOUR_DATASET/alignment.json` should look like:

### Benedict

(Soon) Need more data

<br>

### LJSpeech-1.1

(Soon)

<br>

### World English Bible (WEB)

[Dataset Download Link](https://www.kaggle.com/bryanpark/the-world-english-bible-speech-dataset)

The basically provided transcript has been minimally processed. So I had to manipulate original transcript's structure to can be trained by tacotron. First of all, provided transcript's quality is quite good and total duration is as much as 72 hours! so It was just all to change that transcript's form to normalized from and made it as alignment.josn which can be used to train with labeling.

So I changed a little bit, which audio file path and speech text will be split based on '\\t', and after removing not required symbol, normalized text with english_cleaner() in text utils.

1. moving directories(Act ~ ) including audio files to inside new directory in './dataset/WEB/wavs'

2. Make alignment.json file for generating training datasets. (This is a kind of metadata)

```
python -m dataset.WEB.prepare --metadata transcript.txt
```

*must be located in project's root directory*

3. Generate training dataset

```
python -m datasets.generate_data --metadata_path ./datasets/WEB/alignment.json
```

After finishing process, you can check new path on your project;s root directory './datasets/WEB/data' with many npz files.

4. Training

```
python train.py --data_path=datasets/WEB
```

<br>

### Korean Single Speaker (kss)

[Dataset Download Link](https://www.kaggle.com/bryanpark/korean-single-speaker-speech-dataset)

We trained not only english version, but also korean version to the tacotron model. Our cloned project also support training with korean speech with changing some parts a little bit. Although this dataset's each transcript is short to some extent, but sound is very clearly and has no noise at all. Very good. 

1. moving directories(1 ~ 4 ) including audio files to inside new directory in './dataset/kss/wavs'
2. Make alignment.json file (metadata)

```
python -m dataset.kss.prepare --metadata transcript.v.1.2.txt
```

3. Generate training dataset

```
python -m datasets.generate_data --metadata_path ./datasets/kss/alignment.json
```

4. Training

```
python train.py --data_path=datasets/kss
```

<br>

<br>

## 4. Synthesize

At first, locating your position on project's root directory.

```
python synthesizer.py --load_path {location which has checkpoint file} --text "Text you want to synthesize"
```

<br>

<br>

## 5. Manipulate Attention Module

Let's suppose you want to make Benedict mimic to LJ.

1. At first, you must generate LJ's voice with 0.npy, which stores LJ's attention module's weight output.

```
python synthesizer.py --load_path logs/{log_directory_what_you_genearted} --text "Text you want"
```

2. And then, you must synthesize Benedict's voice over LJ's attention output (0.npy)

```
python synthesizer.py --load_path logs/{log_directory_what_you_genearted} --text "Text you want" --manual_attention_mode=1
```

​	This `--manual_attention_mode=1` arg config part enable you to make Benedict mimic to LJ. The part you have to be cautious is that you must insert text which is same with previous text you generated.

<br>

<br>

## 6. Check result

There are some samples that you can check how each speaker mimics others. In some sample text, the phenomenon that short speech is converted to longer speech successfully. Escpecially, check two sample audio in directory sample_2, benedict_2.wav and benedict_to_web_2.wav

[Link to samples](https://drive.google.com/open?id=1Hn8qi4Rwz5AeENRZ41UilBgMwbLZm9Ak)

<br>

<br>

## 7. Issues

1. In some specific text, when short speech is converted to relatively long speech, it generate wiered noise.
2. The phenomenon that when long speech is converted to relatively shorter speech, some parts of audio get bleary

<br>

<br>

## References

- [Keith Ito](https://github.com/keithito)'s [tacotron](https://github.com/keithito/tacotron)
- [Carpedm's multispeaker-tacotron-tensorflow](https://github.com/carpedm20/multi-speaker-tacotron-tensorflow)
- [Kyubyong Park's opened WEB datasets in Kaggle](https://www.kaggle.com/bryanpark/the-world-english-bible-speech-dataset)
- [Kyubyong Park's opened Korean Single Speaker datasets in Kaggle](https://www.kaggle.com/bryanpark/korean-single-speaker-speech-dataset)

<br>

## Author

Hangbok Lee / [@hangpy](https://github.com/hangpy)