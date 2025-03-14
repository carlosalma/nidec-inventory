"""Gestión de los parámetros del CLI."""

import argparse

def get_cli_parameters(resources):
    """Gestión de parámetros del CLI."""
    loc = resources['loc']
    parser = argparse.ArgumentParser(description=loc['menu']['descrip'])

    parser.add_argument('-p', '--path_repo', type=str,
                        help=loc['menu']['p'], required=True)
    parser.add_argument('-f', '--file_out', type=str,
                        help=loc['menu']['f'], required=True)
    parser.add_argument('-o', '--output_format',
                        type=str, choices=['csv', 'excel'],
                        default='csv', required=False, help=loc['menu']['o'])

    args = parser.parse_args()
    return args.path_repo, args.file_out, args.output_format
