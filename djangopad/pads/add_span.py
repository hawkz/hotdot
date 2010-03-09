'''
This module will take two strings that contain html and find the difference.
Upon finding the difference, we will determine if we are in a span owned by the
user argument.  If not, we shall wrap the extraneous characters in such a span.
import difflib
s = difflib.SequenceMatcher()
txt0 = """<span class="foo">fo</span><span class="bar">ar</span>"""
txt1 = """<span class="foo">foo</span><span class="bar">ar</span>"""
txt2 = """<span class="foo">foo</span>b<span class="bar">ar</span>"""
txt3 = """<span class="foo">foo</span><span class="bar">bar</span>"""
u0 = 'foo'
u1 = 'bar'
s = difflib.SequenceMatcher()
s.set_seqs(txt0, txt1)
'''

import difflib
import re

opn = r'<span class="{user}">'
cls = r'</span>'
regex = re.compile(r'<span class="(\w+)">')

def process(old, new, user):
    s = difflib.SequenceMatcher()
    s.set_seqs(old, new)
    for d in s.get_opcodes():
        if not regex.findall( new ):
            new1 = opn.format(user=user)+new+cls
            pass
        if not regex.findall( new[:d[3]]):
            new1 = opn.format(user=user)+new[0:d[4]]+cls+new[d[4]:]
            pass
        if d[0] == 'equal':
            print 'equal between {0}:{1} and {2}:{3}'.format(d[1],d[2],d[3],d[4])
            pass
        if d[0] == 'replace':
            print 'REPLACE, {0}:{1} with {2}:{3}'.format(d[1],d[2],d[3],d[4])
            pass
        if d[0] == 'delete':
            print 'DELETE'
            pass
        if d[0] == 'insert':
            print 'insert at {0} with {1}:{2}'.format(d[1],d[3],d[4])
            if not regex.findall(new):
                print 'there are no spans, make the first'
                #new = opn.format(user=user)+new+cls
            elif not regex.findall( new[0:d[3]] ):
                print 'NO SPANS BEFORE'
                #new = opn.format(user=user)+new[0:d[4]]+cls+new[d[4]:]
            elif new.rfind(opn.format(user=user), 0, d[3]) > new.rfind(cls, 0, d[3] ):
                print 'we are in the correct span'
                pass
            else:
                if regex.findall( new[0:d[3]] ):
                    other = regex.findall( new[0:d[3]] ).pop()
                    if new.rfind(opn.format(user=other), 0,d[3])\
                            > new.rfind(cls,0,d[3]):
                        print 'we are in somebody else\'s span'
                        new1 = new[0:d[3]]+\
                            cls+opn.format(user=user)+\
                            new[d[3]:d[4]]+\
                            cls+opn.format(user=other)+\
                            new[d[4]:]
                    else:
                        print 'no man\'s land'
                        new1 = new[0:d[3]]+\
                            opn.format(user=user)+\
                            new[d[3]:d[4]]+\
                            cls + new[d[4]:]
    return new1

"""
All of this needs to be burned in a fire


import difflib
import re

class StrExt(str):
    '''Extensions to the Python String to add greater diffing convenience'''
    def right_before_wrong(self, right, wrong, reverse=False,
            start=None, end=None):
        '''Returns True if the right string is before the wrong string'''
        if not reverse:
            ##print 'going forward'
            if self.find(wrong, start, end) == -1 and\
                    self.find(right, start, end) != -1:
                ##print 'we found a right but not a wrong'
                return True
            if self.find(right, start, end) != -1:
                ##print self.find(right, start, end), self.find(wrong, start, end)
                return self.find(right, start, end) <\
                        self.find(wrong, start, end)
            else:
                ##print 'we have no right'
                return False
        else:
            ##print 'going in reverse'
            if self.rfind(right, start, end) != -1 and\
                    self.rfind(wrong, start, end) == -1:
                ##print 'we have found ``right`` and not ``wrong``'
                return True
            ##print self.rfind(right, start, end), self.rfind(wrong, start, end)
            return self.rfind(right, start, end) > self.rfind(wrong, start, end)
    def indices_match(self, right, other, reverse=False,
            start=None, end=None):
        if reverse:
            return self.rfind(right,start,end)!=-1 and self.rfind(right,start,end) == self.rfind(other,start,end)
        else:
            return self.find(right,start,end)!=-1 and self.find(right,start,end) == self.find(other,start,end)
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


def get_other_opn(newstring, rawgex, start=None, end=None):
    r = re.compile(rawgex)
    if r.findall( newstring[start:end] ):
        return r.findall( newstring[start:end] ).pop()
    else:
        return []

def process(oldstring, newstring, owner):
    '''Take two strings and ``preserve ownership`` with span tags'''
    old = StrExt(oldstring)
    new = StrExt(newstring)
    #TODO: make regex to accept " or ' ?
    opn = '<span class="{0}">'.format(owner)
    opn_gen= '<span'
    cls = '</span>'
    regx = r'<span class="(\w+)">'
    ##print old,'\n', new
    ##print opn, cls
    s = difflib.SequenceMatcher()
    s.set_seqs(old,new)
    #print s.get_opcodes()
    for oc in s.get_opcodes():
        ##print oc
        if not new[oc[3]:oc[4]] or new[oc[3]:oc[4]].isspace():
            return newstring
        if oc[0] == 'insert':
            #print 'we have insert'
            if oc[3] == 0:
                #print 'insert at 0'
                tmp = new.add_str_before(cls, oc[4])
                ret = tmp.add_str_before(opn, 0)
                return ret
            elif not any(x in new for x in [opn, opn_gen, cls]):
                #print 'no spans yet'
                #print 'with string,', new, opn, opn_gen, cls
                if not new and not opn_gen and not cls:
                    #print 'our strings are lost'
                    pass
                tmp = new.add_str_before(cls, len(new))
                ret = tmp.add_str_before(opn, 0)
                return ret
            elif new.right_before_wrong(opn, cls, reverse=True, start=0,
                    end=oc[3]):
                #print 'correct before'
                if new.right_before_wrong(cls, opn_gen, start=oc[3], end=len(new)):
                    #print 'correct tags'
                    return new
                else:
                    #print 'we are borked'
                    return 'we are borked'
            elif new.right_before_wrong(opn, cls, start=oc[3]-1, end=len(new) ):
                ##print 'next is right'
                tmp = new.rm_str_sli( oc[4], oc[4]+len(opn) )
                ##print tmp
                ret = tmp.add_str_before( opn, oc[3] )
                return ret
            elif new.rfind(opn, 0, oc[3]) != -1 and new.rfind(opn,0,oc[3]) == new.rfind(opn_gen,0,oc[3]):
                #print 'the previous span is correct'
                before = new.rfind(cls, 0, oc[3])
                #print before
                #print oc[3], oc[4], len(new)
                s = new[oc[3]:oc[4]]
                #print s
                tmp = new.rm_str_sli( oc[3], oc[4] )
                #print tmp
                ret = tmp.add_str_before(s, before)
                #print ret
                return ret
            elif not new.indices_match(opn,opn_gen,reverse=True,start=0,end=oc[3]) and ( not new.indices_match(opn,opn_gen,start=oc[3],end=len(new)) or not new.right_before_wrong(opn,cls,start=oc[3],end=len(new)) ):
                #print 'not adjacent to correct, wrap with span'
                if not new.right_before_wrong(cls,opn_gen,start=oc[3], end=len(new) ):
                    #print 'but we are not in a span, make a new one'
                    tmp = new.add_str_before(cls, oc[4])
                    #print tmp
                    ret = tmp.add_str_before(opn, oc[3]-1)
                    return ret
                else:
                    #print 'we are in a span, the wrong one'
                    #t = new.rm_str_slice(new.find(cls),oc[3],len(new)
                    #print new, 0, oc[3]
                    #print 'the length of new is', len(new)
                    other = get_other_opn(new,regx,0,oc[3])
                    #print other
                    '''
                    r = re.compile(r'(<span class="\w+">)')
                    if r.findall(r'<span class="{0}">'.format(other)):
                        opn_other = r.findall(r'<span class="{0}">'.format(other)).pop()
                    else:
                        opn_other = ''
                    '''
                    opn_other = '<span class="{0}">'.format(other)
                    tmp = new.add_str_before(opn_other, oc[4])
                    i = tmp.add_str_before(cls, oc[4])
                    ret = i.add_str_before(opn, oc[3])
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
    #print i

    if i and not see_has_span(i, newstring, oldstring):
        return wrap_span(i, newstring, username)

    else:
        return newstring



"""
