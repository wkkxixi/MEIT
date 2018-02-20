'''
In memory_log.sh, you need to specify the job id and output file name and
the time interval to monitor the job.

You need to generate the output file by running:

sh memory_log.sh

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

args = parser.parse_args()
filename = args.file
with open(filename) as f:
    lines = f.readlines()
    target = 0
    for item in lines:
        if item.__contains__('resources_used.mem'):
            current = item.split()[-1]
            current = current[:-2]
            current = int(current)
            #print(str(current))
            if current > target:
                target = current
print('--')
print('The peak memory is: ' + str(target))
