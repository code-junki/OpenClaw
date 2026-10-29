from typing_stats import count_words, wpm, accuracy


def test_count_words_handles_extra_spaces():
    # split(" ") produces empty strings on double/leading/trailing spaces
    assert count_words("hello  world") == 2
    assert count_words("  the quick brown fox  ") == 4


def test_wpm_is_per_minute():
    # 10 words typed in 30 seconds == 20 words per minute
    assert wpm("a b c d e f g h i j", 30) == 20


def test_accuracy_full_match_is_100():
    assert accuracy("hello", "hello") == 100.0


def test_accuracy_partial_match():
    # one wrong character out of five == 80% accuracy
    assert accuracy("hxllo", "hello") == 80.0
