from __future__ import print_function

import __main__

__main__.pymol_argv = ["pymol", "-qc"]

import pymol

pymol.finish_launching()

import argparse
import os
import sys
from pymol import cmd, stored


def compute_contact_surface(opts):
    with open(opts.output, "w") as fd:
        print(
            "{:5}{:>12}{:>12}{:>12}{:>12}{:>12}".format(
                "",
                "ligand",
                "protein",
                "complex",
                "contact",
                "ligand",
            ),
            file=fd,
        )

        print(
            "{:5}{:>12}{:>12}{:>12}{:>12}{:>12}".format(
                "frame",
                "area(Å\u00b2)",
                "area(Å\u00b2)",
                "area(Å\u00b2)",
                "area(Å\u00b2)",
                "portion(%)",
            ),
            file=fd,
        )

        for f in range(2, cmd.count_frames() + 1):
            print("Processing frame {}...".format(f - 1), flush=True)
            cmd.frame(f)
            set_selections(opts, f)
            ligand_area = cmd.get_area("ligand", f)
            protein_area = cmd.get_area("protein", f)
            complex_area = cmd.get_area("complex", f)
            contact_area = ((ligand_area + protein_area) - complex_area) / 2
            ligand_portion = (contact_area * 100) / ligand_area
            print(
                "{:5}{:12.4f}{:12.4f}{:12.4f}{:12.4f}{:12.1f}".format(
                    f - 1,
                    ligand_area,
                    protein_area,
                    complex_area,
                    contact_area,
                    ligand_portion,
                ),
                file=fd,
            )
        print("Output written to {}".format(opts.output))


def load_file(opts):
    cmd.load(opts.topology)
    cmd.load_traj(
        opts.trajectory,
        start=opts.frames[0] if opts.frames else 1,
        stop=opts.frames[1] if opts.frames else -1,
        interval=opts.frames[2] if opts.frames else 1,
        selection="{} or {}".format(opts.ligand_sel, opts.protein_sel),
    )


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "-top", dest="topology", help="Structure file (.pdb, .psf, .cms, .gro)"
    )
    parser.add_argument(
        "-traj", dest="trajectory", help="Trajectory file (.dcd, .dtr, .xtc)"
    )
    parser.add_argument(
        "-f",
        "--frames",
        help="""
            Frames to load. Can be either a single integer to specify a particular
            frame, or a range, e.g., 10:100 for frame 10 through 100, 5:1000:10 for
            every 10th frame between 5 through 1000. If not given, all frames will be
            loaded
            """,
    )
    parser.add_argument(
        "-p",
        "--protein",
        dest="protein_sel",
        required=True,
        help="Protein atom selection. Defaults to '%(default)s'",
    )
    parser.add_argument(
        "-l",
        "--ligand",
        dest="ligand_sel",
        required=True,
        help="Ligand atom selection.",
    )
    parser.add_argument(
        "-s",
        "--surface-type",
        default="sasa",
        choices=("molecular", "sasa"),
        help="""
            Calculate molecular surface ('molecular') or solvent accesible surface area
            ('sasa'). Defaults to %(default)s.
            """,
    )
    parser.add_argument(
        "-d",
        "--density",
        dest="dot_density",
        default=3,
        choices=(0, 1, 2, 3, 4),
        help="""
            Dot density in PyMOL (0-4). Higher is better but slower. Defaults to
            %(default)s.
            """,
    )
    parser.add_argument("-o", "--output", help="Output name.")

    opts = parser.parse_args(argv)

    opts.protein_sel = "{}".format(opts.protein_sel)
    opts.ligand_sel = "{}".format(opts.ligand_sel)

    filename = os.path.basename(opts.output)
    basename, ext = os.path.splitext(filename)
    if not ext:
        ext = ".dat"
        opts.output += ext

    if opts.frames is not None:
        tokens = [int(token) for token in opts.frames.split(":")]
        if len(tokens) == 1:
            start = stop = tokens[0]
        else:
            start = tokens[0]
            stop = tokens[1]
        step = tokens[2] if len(tokens) > 2 else 1
        opts.frames = (start, stop, step)

        if len(opts.frames) == 1:
            opts.output = "{}_frame_{}{}".format(basename, opts.frames[0], ext)
        elif opts.frames[2] == 1:
            opts.output = "{}_frame_{}-{}{}".format(
                basename, opts.frames[0], opts.frames[1], ext
            )
        else:
            opts.output = "{}_frame_{}-{}_every_{}{}".format(
                basename, opts.frames[0], opts.frames[1], opts.frames[2], ext
            )

    return opts


def set_options(opts):
    if opts.surface_type == "sasa":
        cmd.set("dot_solvent", 1)
    elif opts.surface_type == "molecular":
        cmd.set("dot_solvent", 0)
    cmd.set("dot_density", opts.dot_density)


def set_selections(opts, f):
    cmd.delete("ligand")
    cmd.delete("protein")
    cmd.delete("complex")
    cmd.create("ligand", opts.ligand_sel, f)
    cmd.create("protein", opts.protein_sel, f)
    cmd.create("complex", "protein or ligand", f)


def main(argv):
    opts = parse_args(argv)
    print("Selected options:", opts)

    load_file(opts)
    set_options(opts)
    compute_contact_surface(opts)


if __name__ == "__main__":
    main(sys.argv[1:])
