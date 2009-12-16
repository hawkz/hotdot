'''
This module will take two strings that contain html and find the difference.
Upon finding the difference, we will determine if we are in a span owned by the
user argument.  If not, we shall wrap the extraneous characters in such a span.

import difflib
s = difflib.SequenceMatcher()
txt0 = """<span class='foo'>fo</span><span class='bar'>ar</span>"""
txt1 = """<span class='foo'>foo</span><span class='bar'>ar</span>"""
txt2 = """<span class='foo'>foo</span>b<span class='bar'>ar</span>"""
txt3 = """<span class='foo'>foo</span><span class='bar'>bar</span>"""
u0 = 'foo'
u1 = 'bar'
s = difflib.SequenceMatcher()
s.set_seqs(txt0, txt1)
'''

import difflib

class StrExt(str):
    '''Extensions to the Python String to add greater diffing convenience'''
    def right_before_wrong(self, right, wrong, reverse=False,
            start=None, end=None):
        '''Returns True if the right string is before the wrong string'''
        if not reverse:
            #print 'going forward'
            if self.find(wrong, start, end) == -1 and\
                    self.find(right, start, end) != -1:
                #print 'we found a right but not a wrong'
                return True
            if self.find(right, start, end) != -1:
                #print self.find(right, start, end), self.find(wrong, start, end)
                return self.find(right, start, end) <\
                        self.find(wrong, start, end)
            else:
                #print 'we have no right'
                return False
        else:
            #print 'going in reverse'
            if self.rfind(right, start, end) != -1 and\
                    self.rfind(wrong, start, end) == -1:
                #print 'we have found ``right`` and not ``wrong``'
                return True
            #print self.rfind(right, start, end), self.rfind(wrong, start, end)
            return self.rfind(right, start, end) > self.rfind(wrong, start, end)
    def has_match_before(self, text, from_index):
        if self.rfind(text, 0, from_index) != -1:
            return True
        else:
            return False
    def has_match_after(self, text, from_index):
        if self.find(text, from_index) != -1:
            return True
        else:
            return False
    def get_prev_index(self, from_index, text):
        '''Returns first index of text in StrExt going back from_index'''
        return self[:from_index].rfind(text) # -1 if can't find
    def get_next_index(self, from_index, text):
        '''Returns first index of text in StrExt going forward from_index'''
        if self[from_index+1:].find(text) != -1:
            return self[from_index+1:].find(text) + from_index+1
        else:
            return -1 # if can't find
    def rm_str_sli(self, start, end):
        '''Returns a StrExt object with the slice self[start:end] removed'''
        return StrExt( "".join( (self[:start], self[end:]) ) )
    def add_str_before(self, string, before):
        return StrExt( "".join( (self[:before], string, self[before:]) ))


def process(oldstring, newstring, owner):
    '''Take two strings and ``preserve ownership`` with span tags'''
    old = StrExt(oldstring)
    new = StrExt(newstring)
    #TODO: make regex to accept " or ' ?
    opn = "<span class='{0}'>".format(owner)
    cls = '</span>'
    print old,'\n', new
    print opn, cls
    s = difflib.SequenceMatcher()
    s.set_seqs(old,new)
    print s.get_opcodes()
    for oc in s.get_opcodes():
        if oc[0] == 'insert':
            print 'we have insert'
            if new.right_before_wrong(opn, cls, reverse=True, start=0,
                    end=oc[3]):
                #print 'correct before'
                
            if new.right_before_wrong(opn, cls, start=oc[3]-1, end=len(txt1) ):
                #print 'next is right'
                tmp = new.rm_str_sli( oc[4], oc[4]+len(opn) )
                #print tmp
                ret = tmp.add_str_before( opn, oc[3] )
                return ret




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




