#!/usr/bin/env python3
"""Cycles Output Parser."""

import argparse
import csv
import os

def parse_outputs(output_folder, simulation_matrix, crop_name, **kwargs):
    sim_matrix = {}
    with open(simulation_matrix) as sm:
        reader = csv.reader(sm, skipinitialspace=True, quotechar="'")
        for row in reader:
            sim_matrix[row[0]] = row[1:]

    with open('output-summary.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            'unique_id',
            'crop',
            'location',
            'planting_date',
            'planting_date_fixed',
            'nitrogen_rate',
            'weed_fraction',
            'year',
            'yield',
            'forcing'
        ])

        for d in os.listdir(output_folder):
            if os.path.isdir(output_folder + '/' + d) and d.startswith('cycles-' + crop_name.lower()) and 'fertilizer_increase' not in d:
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
                            sim_matrix[d][12],
                            sim_matrix[d][9],
                            sim_matrix[d][13],
                            row[0][:4],
                            row[4],
                            sim_matrix[d][11]
                            ])


def _main():
    parser = argparse.ArgumentParser(
        description="Generate CSV file from Cycles Outputs."
    )
    parser.add_argument("output_folder", help="Cycles outputs folder")
    parser.add_argument("simulation_matrix", help="Cycles simulation matrix")
    parser.add_argument("crop_name", help="Cycles crop name")
    args = parser.parse_args()
    parse_outputs(**vars(args))


if __name__ == "__main__":
    _main()
