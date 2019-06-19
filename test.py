import re
import argparse

def main():
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

if __name__ == '__main__':
    main()