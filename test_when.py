from datetime import date

import pytest
from pydantic import ValidationError

from when_is_it import Answer, get_answer


@pytest.mark.vcr(record_mode='new_episodes')
def test_shortest_night():
    expected_answer = Answer(answer_date=date(2001, 7, 4))
    actual_answer = get_answer(question = "What date was the Independence day in USA in 2001?")
    assert expected_answer == actual_answer


#@pytest.mark.skip(reason="Uncomment when asked in the tasklist")
@pytest.mark.vcr(record_mode='new_episodes')
def test_meetup_date():
    expected_answer = Answer(answer_date=date(2023, 4, 24))
    actual_answer = get_answer(question = "The meetup is on 24 April. and today is 21 April 2023. Soon it will be summer. When is the meetup?")
    assert expected_answer == actual_answer

