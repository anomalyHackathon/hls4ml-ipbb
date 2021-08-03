#!/usr/bin/env python
import argparse
from ast import parse
import numpy as np
import bitstring

def to_fixed(x, args):
    F = args.fixed_point_bits[0] - args.fixed_point_bits[1]
    return np.round(x * 2**F)

def to_float(x, args):
    F = args.fixed_point_bits[0] - args.fixed_point_bits[1]
    return x * 2**-F

def vals_to_hex(vals, args):
    nb = args.fixed_point_bits[0] # bits of one value
    tnb = len(vals) * nb # bitwidth of N values
    assert args.link_bitwidth >= tnb, \
        "Attempting to pack {} x {} bits ({} bits) into {}".format(
            len(vals), nb, tnb, args.link_bitwidth)
    pad = args.link_bitwidth - tnb
    fmt_string = 'uint:{},'.format(pad) + 'int:{},'.format(nb) * len(vals)
    return bitstring.pack(fmt_string, 0, *vals).hex

def row_to_hex(row, args):
    # compute the packing factor
    pf = args.link_bitwidth // args.fixed_point_bits[0] if args.pack_links else 1
    N = int(np.ceil(len(row) / pf))
    y = np.array([vals_to_hex(np.flip(row[i*pf:(i+1)*pf]), args)
                  for i in range(N)])
    return y

def main():
    parser = argparse.ArgumentParser(
        description='Parse numpy file to FPGA testing for MP7 board')
    parser.add_argument('--board_name', type=str,
                        help='A string representing the name of the board')
    parser.add_argument('--generate_float_from_fix', type=bool,
                        help='Specify if you want to obtain the .npy file '
                        'obtained via to_float(to_fix(input)). It is useful to '
                        'feed to avoid casting mismatches using '
                        'hls_model.predict()')
    parser.add_argument('--link_range', choices=range(0,96), type=int, nargs=2,
                        metavar=('start','stop'), help='Start and stop values '
                        'for the range related to links')
    parser.add_argument('--link_bitwidth', choices=[32,64], type=int,
                        help='Word size in bits of each link')
    parser.add_argument('--invalid_rows', type=int,
                        help='The number of invalid that will be generate at '
                        'the beginning of the test')
    parser.add_argument('--fixed_point_bits', type=int, nargs=2,
                        metavar=('word_bits', 'integer_bits'),
                        help='The number of invalid that will be generate at '
                        'the beginning of the test')
    parser.add_argument('--pack_links', type=bool, help='Whether to pack '
                        'multiple values into one link where possible')
    parser.add_argument('--link_map', type=int, nargs='*', help='The link map')
    parser.add_argument('--input_data_path', type=str,
                        help='The path of the numpy file containing data in '
                        'floating point')
    parser.add_argument('--output_data_path', type=str,
                        help='The path of the produced .txt file containing '
                        'data in fixed point')
    args = parser.parse_args()

    fp32_data = np.load(args.input_data_path)
    # packing factor
    pf = args.link_bitwidth // args.fixed_point_bits[0] if args.pack_links else 1
    link_width = args.link_range[1] - args.link_range[0] + 1
    if fp32_data.shape[1] > link_width * pf:
        raise Exception(
            'Trying to fit {} features into {} links with packing factor {}'
            .format(fp32_data.shape[1],link_width,pf))
    if fp32_data.shape[0] > 1024:
        print('The system expect no more than 1024 rows; the original file will '
              'be truncated, keeping the first 1024 rows')
        fp32_data = fp32_data[:1024]

    output_file = open(args.output_data_path, 'w')

    fixed_data = to_fixed(fp32_data, args)
    if args.generate_float_from_fix:
        float_back_data = to_float(fixed_data, args)
        np.save('float_from_fix.npy', float_back_data)
    fixed_data = np.array([row_to_hex(row, args) for row in fixed_data])

    link_map = list(range(args.link_range[0], args.link_range[1] + 1)) \
        if args.link_map is None else args.link_map
    assert len(link_map) == link_width, \
        'Link map length ({}) does not match link range ({})'.format(
            len(link_map), link_width)

    # board section
    board_string = 'Board {}\n'.format(args.board_name)

    # channel section
    quad_chan_string = ' Quad/Chan : '
    for i in link_map:
        if args.link_bitwidth == 32:
            quad_chan_string += '   q{:02d}c{}  '.format(i // 4, i % 4)
        else:
            quad_chan_string += '      q{:02d}c{}       '.format(i // 4, i % 4)
        if i != link_map[-1]:
            quad_chan_string += ' '
        else:
            quad_chan_string += '\n'

    # link section 
    link_string = '      Link : '
    for i in link_map:
        if args.link_bitwidth == 32:
            link_string += '    {:02d}    '.format(i)
        else:
            link_string += '        {:02d}        '.format(i)
        if i != link_map[-1]:
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
