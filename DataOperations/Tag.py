import pandas as pd


class TagFactory:

    # Separate tags out of a string
    #TODO ";" useful as a string separator?
    @staticmethod
    def process_tags(
            string_input
    ):
        return string_input.split(";")


