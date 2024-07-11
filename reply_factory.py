
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses



def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to Django session.
    '''
    if not answer:
        return False, "Answer empty."

    session[f"answer_{current_question_id}"] = answer
    return True, ""



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    question_list = PYTHON_QUESTION_LIST

    try:
        current_index = question_list.index(current_question_id)
    except ValueError:
        return None, None  

    if current_index < len(question_list) - 1:
        next_question_id = question_list[current_index + 1]
        next_question = f"Question {next_question_id}: What is your answer?"
        return next_question, next_question_id
    else:
        return None, None  

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    question_list = PYTHON_QUESTION_LIST
    answered_count = 0

    for question_id in question_list:
        if session.get(f"answer_{question_id}"):
            answered_count += 1

    score = answered_count * 10 

    final_response = f"You have completed the quiz. Your score is {score}."
    return final_response
