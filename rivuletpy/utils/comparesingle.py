from rivuletpy.utils.io import *
from rivuletpy.utils.compareswc import *
import argparse
parser = argparse.ArgumentParser(description='Arguments for comparing two swc files.')
parser.add_argument(
        '--target',
        type=str,
        default=None,
        required=True,
        help='The input target swc file.')
parser.add_argument(
        '--groundtruth',
        type=str,
        default=None,
        required=True,
        help='The input ground truth swc file.')

args = parser.parse_args()
swc2 = loadswc(args.groundtruth)  # ground true
swc3 = loadswc(args.target) # target file

prf_3_2, swc_compare_3_2 = precision_recall(swc3, swc2)
saveswc(args.target + '_compare_gt.swc', swc_compare_3_2)
print(str(prf_3_2))
