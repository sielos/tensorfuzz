# Copyright 2018 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Fuzz a neural network to get a NaN."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
import numpy as np
import tensorflow as tf
from lib import fuzz_utils
from lib.corpus import InputCorpus
from lib.corpus import seed_corpus_from_numpy_arrays
from lib.coverage_functions import all_logit_coverage_function
from lib.fuzzer import Fuzzer
from lib.mutation_functions import do_basic_mutations
from lib.sample_functions import recent_sample_function
from lib.corpus import corpus_array
import pandas as pd


tf.flags.DEFINE_string(
    "checkpoint_dir", None, "Dir containing checkpoints of model to fuzz."
)
tf.flags.DEFINE_integer(
    "total_inputs_to_fuzz", 100, "Loops over the whole corpus."
)
tf.flags.DEFINE_integer(
    "mutations_per_corpus_item", 100, "Number of times to mutate corpus item."
)
tf.flags.DEFINE_float(
    "ann_threshold",
    1.0,
    "Distance below which we consider something new coverage.",
)
tf.flags.DEFINE_integer("seed", None, "Random seed for both python and numpy.")
tf.flags.DEFINE_boolean(
    "random_seed_corpus", False, "Whether to choose a random seed corpus."
)
FLAGS = tf.flags.FLAGS


def metadata_function(metadata_batches):
    """Gets the metadata."""
    metadata_list = [
        [metadata_batches[i][j] for i in range(len(metadata_batches))]
        for j in range(metadata_batches[0].shape[0])
    ]
    return metadata_list


def objective_function(corpus_element):
    """Checks if the metadata is inf or NaN."""
    metadata = corpus_element.metadata
    if all([np.isfinite(d).all() for d in metadata]):
        return False

    tf.logging.info("Objective function satisfied: non-finite element found.")
    return True


def main(_):
    """Constructs the fuzzer and performs fuzzing."""

    # Log more
    tf.logging.set_verbosity(tf.logging.INFO)
    # Set the seeds!
    if FLAGS.seed:
        random.seed(FLAGS.seed)
        np.random.seed(FLAGS.seed)

    coverage_function = all_logit_coverage_function
    image, label = fuzz_utils.basic_mnist_input_corpus(
        choose_randomly=FLAGS.random_seed_corpus
    )
    numpy_arrays = [[image, label]]

    with tf.Session() as sess:

        tensor_map = fuzz_utils.get_tensors_from_checkpoint(
            sess, FLAGS.checkpoint_dir
        )

        fetch_function = fuzz_utils.build_fetch_function(sess, tensor_map)

        size = FLAGS.mutations_per_corpus_item
        mutation_function = lambda elt: do_basic_mutations(elt, size)
        seed_corpus = seed_corpus_from_numpy_arrays(
            numpy_arrays, coverage_function, metadata_function, fetch_function
        )
        corpus = InputCorpus(
            seed_corpus, recent_sample_function, FLAGS.ann_threshold, "kdtree"
        )
        print("Corpus#########################", seed_corpus)

        tf.logging.info("Seed Corpus.", seed_corpus)
        fuzzer = Fuzzer(
            corpus,
            coverage_function,
            metadata_function,
            objective_function,
            mutation_function,
            fetch_function,
        )
        result = fuzzer.loop(FLAGS.total_inputs_to_fuzz)
        if result is not None:
            tf.logging.info("Fuzzing succeeded.")
            tf.logging.info(
                "Generations to make satisfying element: %s.",
                result.oldest_ancestor()[1],
            )
            # df = pd.DataFrame(corpus_array)
            # df.to_excel(excel_writer="/tmp/unique/test.xlsx")
        else:
            tf.logging.info("Fuzzing failed to satisfy objective function.")
            # df = pd.DataFrame(corpus_array)
            # df.to_excel(excel_writer="/tmp/unique/test.xlsx")


if __name__ == "__main__":
    tf.app.run()
