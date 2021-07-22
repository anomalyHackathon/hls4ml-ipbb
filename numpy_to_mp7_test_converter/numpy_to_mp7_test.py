import argparse
from ast import parse
import numpy as np
from rig.type_casts import NumpyFixToFloatConverter, NumpyFloatToFixConverter
import bitstring

def c2(val):
    if args.link_bitwidth == 32:
        return bitstring.pack('uint:16, int:16', 0, val).hex
    else:
        return bitstring.pack('uint:16, uint:16, uint:16, int:16', 0, 0, 0, val).hex

parser = argparse.ArgumentParser(description='Parse numpy file to FPGA testing for MP7 board')
parser.add_argument('--board_name', type=str, help='A string representing the name of the board')
parser.add_argument('--generate_float_from_fix', type=bool, help='Specify if you want to obtain the .npy file obtained via to_float(to_fix(input)). It is useful to feed to avoid casting mismatches using hls_model.predict()')
parser.add_argument('--link_range', choices=range(0,96), type=int, nargs=2, metavar=('start','stop'), help='Start and stop values for the range related to links')
parser.add_argument('--link_bitwidth', choices=[32,64], type=int, help='Word size in bits of each link')
parser.add_argument('--invalid_rows', type=int, help='The number of invalid that will be generate at the beginning of the test')
parser.add_argument('--fixed_point_bits', type=int, nargs=2, metavar=('word_bits', 'integer_bits'), help='The number of invalid that will be generate at the beginning of the test')
parser.add_argument('--input_data_path', type=str, help='The path of the numpy file containing data in floating point')
parser.add_argument('--output_data_path', type=str, help='The path of the produced .txt file containing data in fixed point')
args = parser.parse_args()
fp32_data = np.load(args.input_data_path)
if fp32_data.shape[1] > args.link_range[1] - args.link_range[0] + 1:
    raise Exception('You must set a link range value greather or equal to the number of features')
if fp32_data.shape[0] > 1024:
    print('The system expect no more than 1024 rows; the original file will be truncated, keeping the first 1024 rows')
    fp32_data = fp32_data[:1024]
output_file = open(args.output_data_path, 'w')
to_fixed = NumpyFloatToFixConverter(signed=True, n_bits=args.fixed_point_bits[0], n_frac=args.fixed_point_bits[0] - args.fixed_point_bits[1])
fixed_data = to_fixed(fp32_data)
if args.generate_float_from_fix:
    to_float = NumpyFixToFloatConverter(n_frac=args.fixed_point_bits[0] - args.fixed_point_bits[1])
    float_back_data = to_float(fixed_data)
    np.save('float_from_fix.npy', float_back_data)
c2_numpy = np.vectorize(c2)
fixed_data = c2_numpy(fixed_data)

# board section
board_string = 'Board {}\n'.format(args.board_name)

# channel section
quad_chan_string = ' Quad/Chan : '
for i in range(args.link_range[0], args.link_range[1] + 1):
    if args.link_bitwidth == 32:
        quad_chan_string += '   q{:02d}c{}  '.format(i // 4, i % 4)
    else:
        quad_chan_string += '      q{:02d}c{}       '.format(i // 4, i % 4)
    if i != args.link_range[1]:
        quad_chan_string += ' '
    else:
        quad_chan_string += '\n'

# link section 
link_string = '      Link : '
for i in range(args.link_range[0], args.link_range[1] + 1):
    if args.link_bitwidth == 32:
        link_string += '    {:02d}    '.format(i)
    else:
        link_string += '        {:02d}        '.format(i)
    if i != args.link_range[1]:
        link_string += ' '
    else:
        link_string += '\n'

# frame section
frame_start = 'Frame {:04d} : '
frame = ''
if args.invalid_rows > 0:
    for i in range(0,args.invalid_rows):
        frame += frame_start.format(i)
        for j in range(0, args.link_range[1] - args.link_range[0] + 1):
            if args.link_bitwidth == 32:
                frame += '0v00000000'
            else:
                frame += '0v0000000000000000'
            if j != args.link_range[1] - args.link_range[0]:
                frame += ' '
            else:
                frame += '\n'
dummy_cols = args.link_range[1] - args.link_range[0] - fp32_data.shape[1]
for i, v in enumerate(fixed_data):
    frame += frame_start.format(i + args.invalid_rows)
    for j, k in enumerate(v):
        frame += '1v' + k
        frame += ' '
    if dummy_cols > 0:
        for s in range(0, dummy_cols + 1):
            if args.link_bitwidth == 32:
                frame += '0v00000000'
            else:
                frame += '0v0000000000000000'
            if s + j != args.link_range[1] - args.link_range[0] - 1:
                frame += ' '
    frame += '\n'
       
l = [board_string, quad_chan_string, link_string, frame]
output_file.writelines(l)
output_file.close()
print('Done!')
