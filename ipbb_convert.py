#!/usr/bin/env python
import argparse
import traceback


PROG_NAME = 'ipbb_convert'


def error(msg):
    print(f'{PROG_NAME}: error: {msg}')
    exit(1)


try:
    import hls4ml_ipbb
    from hls4ml_ipbb import Project, IP, VHDLWrapper
except ImportError:
    error('hls4ml_ipbb is not present in your environment, please install it '
          'before using the program')


def run(src, dest, solution):
    try:
        project = Project(src)

        if solution is None:
            if len(project.solutions) > 1:
                error('the specified hls4ml project has more than '
                      '1 solution, please run the program again with '
                      f'-s/--solution and one of {project.solutions}')
            else:
                solution = project.solutions[0]
        elif solution not in project.solutions:
            error('the specified hls4ml project does not have a solution '
                  f"called '{solution}', please use one of "
                  f'{project.solutions}')

        ip = project.get_ip(solution)
        wrapper = VHDLWrapper(ip)
        wrapper.save(dest)

        print(f'{PROG_NAME}: the solution has been converted successfully!')
    except FileNotFoundError:
        error('the specified hls4ml project does not exist')
    except hls4ml_ipbb.NoHDLError:
        error('the solution does not have an exported IP')
    except hls4ml_ipbb.NoHLSProjectError:
        error('the specified hls4ml project does not have any '
              'Vivado HLS project directory inside')
    except hls4ml_ipbb.InvalidHLSProjectError:
        print(traceback.format_exc())
        error('the Vivado HLS project inside the specified '
              'hls4ml project could not be processed, the details '
              'are above')
    except hls4ml_ipbb.NoVHDLError:
        error('the solution does not have an exported VHDL IP '
              '(but it may have an IP exported in a different HDL)')
    except hls4ml_ipbb.UnknownPortEncounteredError as ex:
        error(f"the solution has an unknown port '{ex.port_name}'")
    except Exception:
        print(traceback.format_exc())
        error('an error has occurred, the details are above')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description='Convert the solution in an '
                                     'hls4ml project to a VHDL ipbb component.',
                                     epilog='Before using ipbb_convert, you '
                                     'MUST export the IP in your solution by '
                                     'running an appropriate feature in Vivado '
                                     'HLS.')
    parser.add_argument('src', metavar='SOURCE',
                        type=str, help='the path to an hls4ml project directory')
    parser.add_argument('dest', metavar='DESTINATION',
                        type=str, help='the path to a directory where an ipbb '
                        'component should be exported to')
    parser.add_argument('-s', '--solution', metavar='NAME', dest='solution',
                        type=str, help='the name of a solution in the project '
                        'to be converted (required when there is more than '
                        '1 solution)')
    
    args = parser.parse_args()
    run(args.src, args.dest, args.solution)
