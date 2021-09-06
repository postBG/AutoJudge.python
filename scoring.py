import argparse
import csv
import os
from subprocess import Popen, PIPE, STDOUT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--assignment_dir', type=str, required=True)
    parser.add_argument('--num_problems', type=int, required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.assignment_dir):
        raise Exception('{} does not exist'.format(args.assignment_dir))

    # prepare directories
    input_dir = os.path.join(args.assignment_dir, 'input')
    configs = []
    for n, input_path in enumerate(os.listdir(input_dir)):
        configs.append(get_arg_from_txt(os.path.join(input_dir, input_path)))

    answer_dir = os.path.join(args.assignment_dir, 'answer')
    score_dir = os.path.join(args.assignment_dir, 'scores')
    if not os.path.exists(score_dir):
        os.mkdir(score_dir)

    for problem_number in range(1, args.num_problems + 1):
        # prepare student codes, inputs and answer codes
        student_dir = os.path.join(args.assignment_dir, '{}'.format(problem_number))
        student_codes = os.listdir(student_dir)
        student_codes.sort()

        # prepare .csv files
        csv_path = os.path.join(score_dir, '{}.csv'.format(problem_number))
        f = open(csv_path, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow(["student id", "score"])

        for i, student_file in enumerate(student_codes):
            # if not student_file.endswith('{}.py'.format(problem_number)):
            #    print("Not py file: {}".format(student_file))
            #    continue
            print(student_file)

            # get student_id
            student_file_s = student_file.split('_')
            if len(student_file_s[0]) == 10:
                student_id = student_file_s[0]
            elif len(student_file_s[0]) < 10:
                student_id = student_file_s[0] + '-' + student_file_s[1]
            else:
                raise Exception("Wrong student id")

            # init score for each problem
            score = 0

            # @TODO: manage codes
            #            for i, arg in enumerate(configs[args.num_problems-1]):
            arg = configs[problem_number - 1][0]
            arg = arg.replace(b'\r', b'').lstrip(b'\n')
            answer = get_python_output(os.path.join(answer_dir, str(problem_number) + '.py'), arg)
            cand = get_python_output(os.path.join(student_dir, student_file), arg)
            if answer.strip() == cand.strip():
                score = 1
            else:
                print(answer)
                print(cand)
            wr.writerow([student_id, score, answer.strip(), cand.strip()])
        f.close()


def get_python_output(file_path, inputs):
    p = Popen(['python', file_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate(input=inputs)[0]
    return grep_stdout


def get_arg_from_input():
    ret = ''
    while True:
        inp = input()
        if inp == 'EOS':
            break
        ret += inp + '\n'
    return ret.encode()


def get_arg_from_txt(txt_path):
    stream = open(txt_path, 'rb')
    args = stream.read().split(b'EOS')
    return args


if __name__ == '__main__':
    main()
