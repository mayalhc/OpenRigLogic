#-*- coding: utf-8 -*-
import argparse
import random
import os

import dna
import riglogic


def loadDNA(path):
    stream = dna.FileStream(path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
    reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
    reader.read()
    if not dna.Status.isOk():
        raise RuntimeError("Error loading DNA")
    return reader


def runRigLogic(dnaReader):
    rl = riglogic.RigLogic(dnaReader)
    ri = riglogic.RigInstance(rl)

    for i in range(ri.getRawControlCount()):
        ri.setRawControl(i, random.random())

    rl.calculate(ri)
    print(ri.getJointOutputs())


def main():
    parser = argparse.ArgumentParser(description="RigLogic demo")
    parser.add_argument('dna',
                        metavar='dna',
                        help='Path to DNA file to load')

    args = parser.parse_args()

    dnaReader = loadDNA(args.dna)
    runRigLogic(dnaReader)
    print("Done.")

if __name__ == '__main__':
    main()
