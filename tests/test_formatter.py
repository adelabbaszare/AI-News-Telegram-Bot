from src.utils.formatter import generate_hashtags


def test_generate_hashtags_from_strings() -> None:
    assert generate_hashtags(["Artificial Intelligence", "Machine-Learning"]) == (
        "#Artificial_Intelligence #Machine_Learning"
    )


def test_generate_hashtags_handles_invalid_topics() -> None:
    assert generate_hashtags([None, {}, {"name": "Data Science"}]) == "#Data_Science"
