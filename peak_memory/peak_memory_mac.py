'''
You need to generate the output file by running:

top -l 0 -pid  [process id]  -stats pid,mem > [outputfile.txt]

'''
import argparse
parser = argparse.ArgumentParser(description='Run to find peak memory.')
parser.add_argument(
        '-f',
        '--file',
        type=str,
        default=None,
        required=True,
        help='The memory log file to search for peak memory. (*.txt)')
parser.add_argument(
        '-pid',
        '--processID',
        type=str,
        default=None,
        required=False,
        help='The id of process which is running MEIT')

args = parser.parse_args()
filename = args.file
with open(filename) as f:
    lines = f.readlines()
    target = 0
    for item in lines:
        if item.__contains__(args.processID):

            if item.split()[0] == args.processID:
                current = item.split()[1].split('M')[0]

                if current.__contains__('G'):
                    current = current.split('G')[0] +'000'
                    current = int(current)
                else:
                    current = int(item.split()[1].split('M')[0])

                if current > target:
                    target = current
print('--')
print('The peak memory is: ' + str(target))
