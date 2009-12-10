'''
This module will take two strings that contain html and find the difference.
Upon finding the difference, we will determine if we are in a span owned by the
user argument.  If not, we shall wrap the extraneous characters in such a span.
'''


def process(newstring, oldstring, owner):

    # if there are no spans, wrap
    if not '''<span class=["']? ''' in 


def get_addition(newstring, oldstring):
    '''If it is addition, return the index of the first changed character

    '''
    if len(newstring) < len(oldstring):
        return None
    else:
        for i, (newChar, oldChar) in enumerate( zip(newstring, oldstring) ):
            if newChar != oldChar:
                return i

    return len(oldstring)

def see_has_span(i, newstring, username):
    '''See if the character in question is already wrapped with span

    The span classes will be the username represented with:

        <span class="{{username}}">

    This implementation will cause highly strange results if the text itself
    contains the strings ``span>`` of ``span class``

    '''

    span_index = newstring[:i].rfind('span class')

    if span_index == newstring[:i].rfind('span>'):
        return False

    if newstring[span_index+11:span_index+11+len(username)] == username:
        return True

    else:
        return False


def wrap_span(i, newstring, username):
    return ''.join([
            newstring[:i],
            '<span class="{0}">'.format(username),
            newstring[i],
            '</span>',
            newstring[i+1:]
    ])

def diff_and_span(newstring, oldstring, username):
    if newstring == oldstring:
        return newstring

    i = get_addition(newstring, oldstring)
    print i

    if i and not see_has_span(i, newstring, oldstring):
        return wrap_span(i, newstring, username)

    else:
        return newstring




