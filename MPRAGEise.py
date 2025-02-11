#!/usr/bin/env python3
"""
MPRAGEise.py

This script processes MP2RAGE images by either removing or reintroducing 
the bias field and then “MPRAGEises” the UNI image.

Usage:
    MPRAGEise.py -i INV2_image -u UNI_image [-r re_bias] [-o output_folder] [-v]

Examples:
    MPRAGEise.py -i /path/to/data/inv2.nii.gz -u /data/uni.nii.gz
    MPRAGEise.py -i /path/to/data/inv2+orig -u /path/to/data/uni+orig -r 1

Created by: Sriranga Kashyap (01-2025), srikashmri@gmail.com
"""

import os
import sys
import argparse
import subprocess
import datetime
import glob

# Set AFNI environment variables
os.environ["AFNI_NIFTI_TYPE_WARN"] = "NO"
os.environ["AFNI_ENVIRON_WARNINGS"] = "NO"

# Global verbose flag (default off)
VERBOSE = False

def get_afni_version():
    """Return the AFNI version string by calling 'afni -ver'."""
    try:
        result = subprocess.run(["afni", "-ver"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return result.stdout.strip()
    except Exception:
        return "Unknown"

def parse_arguments():
    # ANSI escape codes for italics; may not be supported in all terminals.
    italic_start = "\033[3m"
    italic_end = "\033[0m"
    epilog_text = (
        f"{italic_start}Nota bene:{italic_end}\n"
        f"   {italic_start}1. The default output is set to the directory of the INV2 image.{italic_end}\n"
        f"   {italic_start}2. If you're unsure why one would need the re_bias option, you probably don't need it.{italic_end}\n"
        f"   {italic_start}3. Do not use this script for the MP2RAGE T1 map.{italic_end}\n"
    )
    parser = argparse.ArgumentParser(
        description=(
            "Background denoise MP2RAGE UNI images (MPRAGEising) whilst either "
            "removing or reintroducing the bias field."
        ),
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--inv2", required=True,
                        help="MP2RAGE INV2 image (e.g. /path/to/inv2.nii.gz or file+orig)")
    parser.add_argument("-u", "--uni", required=True,
                        help="MP2RAGE UNI image (e.g. /path/to/uni.nii.gz or uni+orig)")
    parser.add_argument("-r", "--re_bias", default="0",
                        help="Reintroduce bias-field (default=0, optional).")
    parser.add_argument("-o", "--output", default=None,
                        help="Output folder for processed files.")
    parser.add_argument("--overwrite", action="store_true", default=False,
                        help="Include -overwrite flag in each AFNI command.")
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
                        help="Enable verbose logging of command execution and debug information.")
    return parser.parse_args()

def get_basename_and_extension(filename):
    """
    Determine the base name and file extension.
    
    For NIfTI files (containing ".nii"):
      - If the filename ends with '.nii.gz', remove that and set ext = '.nii.gz'
      - Otherwise, remove '.nii' and set ext = '.nii'
    
    For AFNI datasets (if filename contains a '+'):
      - Try to call '@GetAfniPrefix' if available; if not, take the substring before '+'.
      - Set ext = '+orig'
    """
    if ".nii" in filename:
        if filename.endswith(".nii.gz"):
            basename = os.path.basename(filename)[:-7]  # remove '.nii.gz'
            file_ext = ".nii.gz"
        else:
            basename = os.path.basename(filename)[:-4]  # remove '.nii'
            file_ext = ".nii"
    elif "+" in filename:
        # Assume AFNI dataset
        try:
            result = subprocess.run(["@GetAfniPrefix", filename],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                basename = result.stdout.strip()
            else:
                basename = filename.split('+')[0]
        except Exception:
            basename = filename.split('+')[0]
        file_ext = "+orig"
    else:
        basename = os.path.basename(filename)
        file_ext = ""
    return basename, file_ext

def run_command(cmd):
    """Run an external command; exit with error if it fails.
       If verbose is enabled, print the full command and its output."""
    if VERBOSE:
        print("Running command:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if VERBOSE:
        print("Command stdout:", result.stdout)
        print("Command stderr:", result.stderr)
    if result.returncode != 0:
        print("Error running command:", " ".join(cmd))
        print("Stdout:", result.stdout)
        print("Stderr:", result.stderr)
        sys.exit(1)
    return result.stdout.strip()

def cleanup_temp_files(prefix):
    """Remove temporary files that match the given prefix and common AFNI/NIfTI extensions."""
    extensions = ["", ".nii", ".nii.gz", ".BRIK", ".BRIK.gz", ".HEAD"]
    for ext in extensions:
        pattern = prefix + ext
        for f in glob.glob(pattern):
            try:
                os.remove(f)
                if VERBOSE:
                    print(f"Removed temporary file: {f}")
            except Exception as e:
                print(f"Warning: Could not remove temporary file {f}: {e}")

def main():
    global VERBOSE
    args = parse_arguments()
    VERBOSE = args.verbose
    # Build a list for the -overwrite flag if requested.
    overwrite_flag = ["-overwrite"] if args.overwrite else []
    
    if args.overwrite:
        print("\n++++ WARNING: The --overwrite option is enabled; existing output files may be overwritten.\n")

    inv2_image = args.inv2
    uni_image = args.uni
    re_bias_flag = args.re_bias.strip()

    # Print startup information.
    print()  # blank line
    print("------------------------------")
    print("  MPRAGEise v1.0 is running.")
    print("------------------------------")
    print()  # blank line
    afni_ver = get_afni_version()
    run_date = datetime.datetime.now().strftime("%c")
    print("AFNI Version:", afni_ver)
    print("Run Date:", run_date)
    print()  # blank line after run date
    print("Input files:")
    print("  INV2 image:", inv2_image)
    print("  UNI image :", uni_image)

    # Determine output folder:
    # If the user did not supply an output folder, use the directory of the INV2 image.
    if args.output is None:
        output_folder = os.path.dirname(os.path.abspath(inv2_image))
    else:
        output_folder = args.output

    # Ensure the output folder exists.
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            sys.exit(f"Error: Unable to create output folder '{output_folder}': {e}")
    if not os.access(output_folder, os.W_OK):
        sys.exit(f"Error: Output folder '{output_folder}' is not writable.")

    # Determine basenames and file extension from the INV2 and UNI images.
    inv2_basename, file_ext = get_basename_and_extension(inv2_image)
    uni_basename, _ = get_basename_and_extension(uni_image)

    # Decide on bias handling and print step message.
    if re_bias_flag != "0":
        print("\n++++ Reintroducing bias-field.")
        re_bias = True
    else:
        print("\n++++ Removing bias-field.")
        re_bias = False

    # Build full output paths using the output folder.
    if not re_bias:
        bfc_prefix = os.path.join(output_folder, f"{inv2_basename}_bfc{file_ext}")
        run_command(["3dUnifize", "-quiet"] + overwrite_flag + ["-prefix", bfc_prefix, inv2_image])
        out_name = os.path.join(output_folder, f"{uni_basename}_unbiased_clean{file_ext}")
    else:
        bfc_prefix = os.path.join(output_folder, f"{inv2_basename}_bfc{file_ext}")
        run_command(["3dcopy", inv2_image, bfc_prefix])
        out_name = os.path.join(output_folder, f"{uni_basename}_rebiased_clean{file_ext}")

    # CALCULATION: Intensity normalization and MPRAGEising.
    int_max = run_command(["3dinfo", "-dmaxus", inv2_image])
    int_min = run_command(["3dinfo", "-dminus", inv2_image])
    intnorm_prefix = os.path.join(output_folder, f"{inv2_basename}_intnorm{file_ext}")
    expr = f"( a - {int_min} ) / ( {int_max} - {int_min} )"
    run_command(["3dcalc"] + overwrite_flag + ["-a", bfc_prefix,
                 "-expr", expr, "-prefix", intnorm_prefix])
    print("\n++++ MPRAGEising the UNI image.")
    run_command(["3dcalc"] + overwrite_flag + ["-a", uni_image,
                 "-b", intnorm_prefix, "-expr", "a * b", "-prefix", out_name])

    # CLEANUP: Remove temporary files with common AFNI/NIfTI extensions.
    cleanup_temp_files(bfc_prefix)
    cleanup_temp_files(intnorm_prefix)

    print("\n++++ Done.\n")
    print(f"Output file: {out_name}")
    print()  # blank line


if __name__ == "__main__":
    main()
