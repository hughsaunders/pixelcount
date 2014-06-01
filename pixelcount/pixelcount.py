#!/usr/bin/env python

# Standard Library imports
import argparse
import sys

# 3rd Party Imports
from PIL import Image
from prettytable import PrettyTable


class PixelCount:

    # Dictionary to convert channel letters to their equivalent number.
    channel_indexes = {
        'r': 0,
        'g': 1,
        'b': 2
    }

    def __init__(self, image_file, channel, threshold):

        # Arguments
        self.image_file = image_file
        self.channel_letter = channel
        self.channel_num = self.channel_indexes[channel]
        self.threshold = threshold

        # Read image file into self.image
        self.image = Image.open(self.image_file)

    def count(self):
        """ Split image into channels, count the pixels that are above
        a threshold in the selected channel (self.channel_num)
        """

        # Split image into R,G,B channels
        channels = self.image.split()

        # Get pixels as a vector (single dimension array)
        channel_data = channels[self.channel_num].getdata()

        total_pixels = len(channel_data)

        # Loop over channel data, count pixels above threshold
        above_threshold_count = 0
        for pixel in channel_data:
            if pixel >= self.threshold:
                above_threshold_count += 1

        above_threshold_percentage = \
            (float(above_threshold_count) / total_pixels) * 100

        # Return dictionary of values
        return {
            "total_pixels": total_pixels,
            "above_threshold_count": above_threshold_count,
            "above_threshold_percentage": above_threshold_percentage
        }


class PixelCountCLI:
    """ This class provides a command line interface for pixelcount
    """

    def main(self, input_args):
        """ The main method - this will be executed with pixelcount is run
        from the command line
        """

        # Deal with command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--channel', '-c', choices=['r', 'g', 'b'],
                            required=True)
        parser.add_argument('--threshold', '-t', type=int, required=True)
        parser.add_argument('--file', '-f', type=argparse.FileType('rb'),
                            required=True)
        args = parser.parse_args(input_args)

        # Initialise PixeCount
        pc = PixelCount(image_file=args.file,
                        channel=args.channel,
                        threshold=args.threshold)

        # Count!
        results = pc.count()

        # Print results in a table
        table = PrettyTable(["Item", "Value"])
        table.add_row(["Total Pixels", results["total_pixels"]])
        table.add_row(["Channel", pc.channel_letter])
        table.add_row(["Threshold", pc.threshold])
        table.add_row(["Pixels in channel %s Above Threshold" %
                       pc.channel_letter, results["above_threshold_count"]])
        table.add_row(["Above Threshold Percentage",
                      "%.2f%%" % results["above_threshold_percentage"]])
        print table

# Run PixeCountCLI if this module is run as a script
if __name__ == '__main__':
    cli = PixelCountCLI()
    cli.main(sys.argv[1:])
