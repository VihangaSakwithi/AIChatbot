import re
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message: #Count the recognised words in the user message
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words)) # Recognised words as a %

    for word in required_words: #Check required words in the user message
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response: #Check response rate
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]): #Map responses to a dict
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True) #Basic responses
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('You can find them on services section', ['i', 'want', 'hire', 'worker'], required_words=['worker', 'hire'])
    response('Our latest plumbing services:', ['plumber'], required_words=['plumber'])

    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice']) #Contact long response

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

while True:
    print('Bot: ' + get_response(input('You: ')))