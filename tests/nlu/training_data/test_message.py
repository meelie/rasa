from typing import Optional, Text, List

import pytest
import numpy as np
import scipy.sparse

from rasa.nlu.featurizers.featurizer import Features
from rasa.nlu.constants import TEXT, FEATURE_TYPE_SEQUENCE, FEATURE_TYPE_SENTENCE
from rasa.nlu.training_data import Message


@pytest.mark.parametrize(
    "features, attribute, sequence_featurizers, sentence_featurizers, "
    "expected_seq_features, expected_sen_features",
    [
        (None, TEXT, [], [], None, None),
        (
            [Features(np.array([1, 1, 0]), FEATURE_TYPE_SEQUENCE, TEXT, "test")],
            TEXT,
            [],
            [],
            [1, 1, 0],
            None,
        ),
        (
            [
                Features(np.array([1, 1, 0]), FEATURE_TYPE_SEQUENCE, TEXT, "c2"),
                Features(np.array([1, 2, 2]), FEATURE_TYPE_SENTENCE, TEXT, "c1"),
                Features(np.array([1, 2, 1]), FEATURE_TYPE_SEQUENCE, TEXT, "c1"),
            ],
            TEXT,
            [],
            [],
            [1, 2, 1, 1, 1, 0],
            [1, 2, 2],
        ),
        (
            [
                Features(np.array([1, 1, 0]), FEATURE_TYPE_SEQUENCE, TEXT, "c1"),
                Features(np.array([1, 2, 1]), FEATURE_TYPE_SENTENCE, TEXT, "test"),
                Features(np.array([1, 1, 1]), FEATURE_TYPE_SEQUENCE, TEXT, "test"),
            ],
            TEXT,
            ["c1"],
            ["c1"],
            [1, 1, 0],
            None,
        ),
    ],
)
def test_get_dense_features(
    features: Optional[List[Features]],
    attribute: Text,
    sequence_featurizers: List[Text],
    sentence_featurizers: List[Text],
    expected_seq_features: Optional[List[Features]],
    expected_sen_features: Optional[List[Features]],
):

    message = Message("This is a test sentence.", features=features)

    actual_seq_features, actual_sen_features = message.get_dense_features(
        attribute, sequence_featurizers, sentence_featurizers
    )

    assert np.all(actual_sen_features == expected_sen_features)
    assert np.all(actual_seq_features == expected_seq_features)


@pytest.mark.parametrize(
    "features, attribute, sequence_featurizers, sentence_featurizers, "
    "expected_seq_features, expected_sen_features",
    [
        (None, TEXT, [], [], None, None),
        (
            [
                Features(
                    scipy.sparse.csr_matrix([1, 1, 0]),
                    FEATURE_TYPE_SEQUENCE,
                    TEXT,
                    "test",
                )
            ],
            TEXT,
            [],
            [],
            [1, 1, 0],
            None,
        ),
        (
            [
                Features(
                    scipy.sparse.csr_matrix([1, 1, 0]),
                    FEATURE_TYPE_SEQUENCE,
                    TEXT,
                    "c2",
                ),
                Features(
                    scipy.sparse.csr_matrix([1, 2, 2]),
                    FEATURE_TYPE_SENTENCE,
                    TEXT,
                    "c1",
                ),
                Features(
                    scipy.sparse.csr_matrix([1, 2, 1]),
                    FEATURE_TYPE_SEQUENCE,
                    TEXT,
                    "c1",
                ),
            ],
            TEXT,
            [],
            [],
            [1, 2, 1, 1, 1, 0],
            [1, 2, 2],
        ),
        (
            [
                Features(
                    scipy.sparse.csr_matrix([1, 1, 0]),
                    FEATURE_TYPE_SEQUENCE,
                    TEXT,
                    "c1",
                ),
                Features(
                    scipy.sparse.csr_matrix([1, 2, 1]),
                    FEATURE_TYPE_SENTENCE,
                    TEXT,
                    "test",
                ),
                Features(
                    scipy.sparse.csr_matrix([1, 1, 1]),
                    FEATURE_TYPE_SEQUENCE,
                    TEXT,
                    "test",
                ),
            ],
            TEXT,
            ["c1"],
            ["c1"],
            [1, 1, 0],
            None,
        ),
    ],
)
def test_get_sparse_features(
    features: Optional[List[Features]],
    attribute: Text,
    sequence_featurizers: List[Text],
    sentence_featurizers: List[Text],
    expected_seq_features: Optional[List[Features]],
    expected_sen_features: Optional[List[Features]],
):

    message = Message("This is a test sentence.", features=features)

    actual_seq_features, actual_sen_features = message.get_sparse_features(
        attribute, sequence_featurizers, sentence_featurizers
    )

    if expected_seq_features is None:
        assert actual_seq_features is None
    else:
        assert np.all(actual_sen_features.toarray() == expected_sen_features)

    if expected_sen_features is None:
        assert actual_sen_features is None
    else:
        assert np.all(actual_seq_features.toarray() == expected_seq_features)
