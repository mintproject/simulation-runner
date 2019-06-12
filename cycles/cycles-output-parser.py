#!/usr/bin/env python3
"""Cycles Output Parser."""

import argparse
import csv
import os

def parse_outputs(output_folder, simulation_matrix, **kwargs):
    sim_matrix = {}
    with open(simulation_matrix) as sm:
        reader = csv.reader(sm, skipinitialspace=True, quotechar="'")
        for row in reader:
            sim_matrix[row[0]] = row[1:]

    with open('cycles-output-summary.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            'unique_id',
            'crop',
            'location',
            'planting_date',
            'nitrogen_rate',
            'year',
            'yield'
        ])

        for d in os.listdir(output_folder):
            if d.startswith('cycles-'):
                with open(output_folder + '/' + d + '/output/' + d + '/season.dat') as season_file:
                    csvreader = csv.reader(season_file, delimiter='\t')
                    next(csvreader)
                    next(csvreader)
                    for row in csvreader:
                        csvwriter.writerow([
                            d,
                            sim_matrix[d][1],
                            sim_matrix[d][4].replace('.weather', '').replace('met', '').replace('x', ' x ').replace('N', ' North').replace('E', ' East'),
                            sim_matrix[d][6],
                            sim_matrix[d][9],
                            row[0][:4],
                            row[4]
                            ])


def _main():
    parser = argparse.ArgumentParser(
        description="Generate CSV file from Cycles Outputs."
    )
    parser.add_argument("output_folder", help="Cycles outputs folder")
    parser.add_argument("simulation_matrix", help="Cycles simulation matrix")
    args = parser.parse_args()
    parse_outputs(**vars(args))


if __name__ == "__main__":
    _main()
