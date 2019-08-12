import re
import argparse
import matplotlib as mpl
import os

def main():
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_paths', default='datasets/kr_example')

    config = parser.parse_args()

    # p = re.compile("model.ckpt-(\d+)")

    # initial_target = re.compile("logs/(\w+)_")

    reg_new_target = re.compile("datasets/(\w+)")
    print(typeof())
    m3 = reg_new_target.search(config.data_paths)
    new_target = m3.group(1)

    # m1 = p.search("logs/LJSpeech_1_0_2019-06-16_19-21-47/model.ckpt-10000")
    # m2 = initial_target.search("logs/LJSpeech_1_0_2019-06-16_19-21-47/model.ckpt-10000")


    # reg_prev_global_step = m1.group(1)
    # reg_prev_target = m2.group(1)


    print(new_target)
    '''
    a = "[saying]"
    b = "saying"

    #print('버전: ', mpl.__version__)
    #print('설치 위치: ', mpl.__file__)
    #print('설정 위치: ', mpl.get_configdir())
    #print('캐시 위치: ', mpl.get_cachedir())
    #fm = mpl.matplotlib_fname()
    #print('설정 파일 위치: ', fm)
    #font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')

    # ttf 폰트 전체개수
    #print(len(font_list))
    #print([(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name])

    print(os.path.join(os.path.abspath(''), "abcde"))



if __name__ == '__main__':
    main()