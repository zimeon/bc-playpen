import argparse
import tarfile
import io
import os
import logging
import re

import uuid
import json
from rdflib import Graph

import uri_counter


NUM_TO_UUID = {}
TRIPLE_COUNTER = uri_counter.TripleURICounter()

def parse_jsonld(content):
    graph = Graph()
    # Parse the JSON-LD data and add it to the graph
    graph.parse(data=content, format="json-ld")
    # Print the triples in the graph
    for s, p, o in graph:
        TRIPLE_COUNTER.add(s, p, o)

def read_tar_gz_file(filename):
    """Generator to read content from files in a .tar.gz without extracting.

    Yields:
        str: name of file within .tar.gz
        str: content of file within .tar.gz
    """
    try:
        with tarfile.open(filename, "r:gz") as tar:
            logging.info(f"Contents of {filename}:")
            for member in tar.getmembers():
                if member.isfile():
                    logging.info(f"- {member.name}")
                    with tar.extractfile(member) as f:
                        content = f.read().decode('utf-8')
                        yield(member.name, content)
    except tarfile.ReadError as e:
        logging.error(f"Error reading {filename}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred with {filename}: {e}")


def read_file(filename):
    if tarfile.is_tarfile(filename):
        return read_tar_gz_file(filename)
    else:
        # Assume it is just a single file
        with open(filename, "r") as fh:
            content = fh.read()
            yield(filename, content)


def rewrite_with_uuids(content):
    pattern = re.compile(r"(resources/?(works|instances)/?)(\d+)\"")
    replacements = {}
    for m in re.finditer(pattern, content):
        prefix = m.group(1)
        num = m.group(3)
        if m.group(0) not in replacements:
            if num not in NUM_TO_UUID:
                NUM_TO_UUID[num] = str(uuid.uuid4())
            replacements[m.group(0)] = prefix + NUM_TO_UUID[num] + '"'
            #print(m.group(0) + " ---> " + replacements[m.group(0)])
    for old, new in replacements.items():
        content = content.replace(old, new)
    return content

def process_file(filename):
    with tarfile.open("out.tar.gz", "w:gz") as tout:
        num_files = 0
        total_input_size = 0
        total_output_size = 0
        for (name, content) in read_tar_gz_file(filename):
            num_files += 1
            n = len(content)
            total_input_size += n
            # Look at the JSON-LD
            parse_jsonld(content)
            #print(f"{name} has {n} bytes of content")
            #print(f"### FROM ###\n{content}")
            new = rewrite_with_uuids(content)
            # Add to tout...
            uuname = name.replace(".cbd.", ".uuid.")
            ti = tarfile.TarInfo(name=uuname)
            ti.size = len(new)
            total_output_size += ti.size
            ti.type = tarfile.REGTYPE
            #print(f"### TO ###\n{new}")
            tout.addfile(ti, fileobj=io.BytesIO(new.encode('utf-8')))
    print(f"Files processed = {num_files}")
    print(f"Total input content size = {total_input_size} bytes")
    print(f"Total output content size = {total_output_size} bytes")
    print(TRIPLE_COUNTER)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", action="store",
                        # default="24116199.cbd.jsonld",
                        default="bluecore-sample-records2_10k_extract.tar.gz",
                        help="source site")
    return parser.parse_args()


args = parse_arguments()
process_file(args.src)
