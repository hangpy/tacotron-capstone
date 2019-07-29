[The World English Bible](https://en.wikipedia.org/wiki/World_English_Bible) is a public domain update of the American Standard Version of 1901 into modern English. Its original audios are freely available [here](http://www.audiotreasure.com/webindex.htm). I split each chapter by verse manually and aligned the segmented audio clips to the text so they can be used as a training dataset for speech tasks. They are 72 hours in total. You can download them at [Kaggle Dataset](the-world-english-bible-speech-dataset). Also, you may want to check my project using this dataset [here](https://github.com/Kyubyong/tacotron).

This dataset is composed of the following:
  * README.md
  * wav files sampled at 12,000 KHZ
  * transcript.txt.

`transcript.txt` is in a tab-delimited format. The first column is the audio file paths. The second one is the script. Finally, the rightmost column is the duration of the audio file.

February, 2018. Kyubyong Park (kbpark.linguist@gmail.com)