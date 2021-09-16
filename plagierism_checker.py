# Plagierism_checker
# Made by Jaedong Hwang
import pycode_similar
import pdb
import os
import argparse

class ArgParser(argparse.ArgumentParser):
    """
    A simple ArgumentParser to print help when got error.
    """
    def error(self, message):
        self.print_help()
        from gettext import gettext as _
        self.exit(2, _('\n%s: error: %s\n') % (self.prog, message))

def parsing():
    parser = ArgParser(description='A simple plagiarism detection tool for python code')
    parser.add_argument('-l', type=int, default=4,
                        help='if AST line of the function >= value then output detail (default: 4)')
    parser.add_argument('-p', type=float, default=0.5,
                        help='if plagiarism percentage of the function >= value then output detail (default: 0.5)')
    parser.add_argument('--verbose', default=False, action='store_true')
    parser.add_argument('--path', type=str, default='./',
                        help='path')
    args = parser.parse_args()
    return args

def add_main(path):
    f = open(path, 'r')
    try:
        lines = f.readlines()
    except :
        pdb.set_trace()
    new_lines = ['def main():\n']
    for line in lines:
        new_lines.append(' '+line)
    return ''.join(new_lines)

if __name__ == '__main__':
    args = parsing()
    PATH = args.path
    ldir = sorted(os.listdir(PATH))
    strs = []
    names = []
    print("start checking")
    for filename in ldir:
        if '.py' == filename[-3:]:
            strs.append(add_main(os.path.join(PATH,filename)))
            names.append(filename) #filename.split('_')[0])
    
    copy_checker = {}
    
    similarities = []
    most_similar = []
    for i in range(len(strs)-1):
#        new_strs = strs[i:i+1] + strs[:i] + strs[i+1:]
#        new_names = names[i:i+1] + names[:i] + names[i+1:]
        new_strs = strs[i:]
        new_names = names[i:]
        try:
            results = pycode_similar.detect(new_strs,  diff_method=pycode_similar.UnifiedDiff)
        except :
            print(new_names)
            continue
        max_sim = -1
        for index, func_ast_diff_list in results:
            sum_total_count = sum(func_diff_info.total_count for func_diff_info in func_ast_diff_list)
            sum_plagiarism_count = sum(func_diff_info.plagiarism_count for func_diff_info in func_ast_diff_list)
            similarity = sum_plagiarism_count / float(sum_total_count)
            if max_sim < similarity:
                max_sim = similarity
                max_sim_name = new_names[index]
            if similarity < args.p:
                continue
            print('ref: {}\t\tcandidates: {}\t\tsimilarity: {:.2f} % ({}/{}) '.format(names[i], new_names[index],
                    sum_plagiarism_count / float(sum_total_count) * 100,
                    sum_plagiarism_count,
                    sum_total_count))
            if args.verbose:
                print('details (AST lines >= {} and plagiarism percentage >= {}):'.format(
                        args.l,
                        args.p,
                ))
                output_count = 0
                for func_diff_info in func_ast_diff_list:
                    if len(func_diff_info.info_ref.func_ast_lines) >= args.l and func_diff_info.plagiarism_percent >= args.p:
                        output_count = output_count + 1
                        print(func_diff_info)
                if output_count == 0:
                    print('<empty results>')
        most_similar.append((max_sim_name, max_sim))
   
    print()
    print("MAX_SIMILARITY (> {}) for each file".format(args.p))
    print()
    for ref, (candidate, sim) in zip(names, most_similar):
        if args.verbose or sim > args.p:
            print('ref: {}\t\tcandidates: {}\t\tsimilarity: {:.2f}'.format(ref,
                                                    candidate, sim))

