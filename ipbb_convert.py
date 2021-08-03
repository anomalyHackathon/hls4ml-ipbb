#!/usr/bin/env python
import argparse
import traceback


PROG_NAME = 'ipbb_convert'


def error(msg):
    print(f'{PROG_NAME}: error: {msg}')
    exit(1)


try:
    from hls4ml_ipbb import Project, IP, VHDLWrapper
    from hls4ml_ipbb.backend import VivadoBackend
    from hls4ml_ipbb.exception import ToolException
except ImportError:
    error('hls4ml_ipbb could not be imported, please install it in your '
          'environment if you do not have it')


def run(src, dest, solution, hls_project_name):
    try:
        project = Project(src, backend=VivadoBackend(),
                          hls_project_name=hls_project_name)

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
    except (FileNotFoundError, ToolException) as ex:
        error(str(ex)[0].lower() + str(ex)[1:])
    except Exception:
        print(traceback.format_exc())
        error('an error has occurred, the details are above')


def main():
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description='Convert the solution in an '
                                     'hls4ml project to a VHDL ipbb component.',
                                     epilog='Before using ipbb_convert, you '
                                     'MUST export the IP in your solution by '
                                     'running an appropriate feature in your '
                                     'HLS software.')
    parser.add_argument('src', metavar='SOURCE',
                        type=str, help='the path to an hls4ml project directory')
    parser.add_argument('dest', metavar='DESTINATION',
                        type=str, help='the path to a directory where an ipbb '
                        'component should be exported to')
    parser.add_argument('--hls-name', metavar='NAME', dest='hls_project_name',
                        type=str, help='the name of an HLS project directory in '
                        'the hls4ml project (required when there is more than 1 '
                        'HLS project directory)')
    parser.add_argument('-s', '--solution', metavar='NAME', dest='solution',
                        type=str, help='the name of a solution in the project '
                        'to be converted (required when there is more than '
                        '1 solution)')
    
    args = parser.parse_args()
    run(args.src, args.dest, args.solution, args.hls_project_name)
