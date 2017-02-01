# -*- coding: utf-8 -*-

__version__ = "0.0.1"
__all__ = ["app",
           "es",
           "ner",
           "BREDS"]


class MyBREDS():

    def __init__(self, similarity=0.6, confidence=0.8):
        self.curr_iteration = 0
        self.patterns = list()
        self.processed_tuples = list()
        self.candidate_tuples = defaultdict(list)

        self.config = Config(config_file, seeds_file, negative_seeds,
                             similarity, confidence)
