
import xml.etree.ElementTree as ET

def haxe_parse_completion_list(_list):

    if _list is None:
        return []

    print(_list)

    try:
        root = ET.fromstring(str(_list))
    except ET.ParseError as e:
        #if there was a parse error, this is an error from haxe,
        #so we will show it for now as a completion with blank insert
        _error = _list.split('\n')
        return [(_error[0], '')]

        #list is completion of properties/methods on an object/Type
    if root.tag == 'list':

        members = []

        for node in root:

            _name = node.attrib['n']
            _type = node.find('t').text

            if _type is None:
                _type = "-"

            if is_function(_type):
                members.append( ( _name+'\tfunction', _name ) )
            else:
                members.append( ( _name+'\t'+_type, _name ) )

        return members

        #type is function arguments and the like
    elif root.tag == 'type':

        args = []

        parsed = parse_type(root.text.strip())
        if parsed is not None:
            args = parsed

        return args

    return []

#returns args, return_type from a <type> string
def parse_args(_type):
    _tmp = _type

    _args = []
    _result = 0
    _count = 0
    while _result != None:
        _result = _tmp.find(' -> ')
        _arg = _tmp[:_result]

            #found a () which means it's a function type
        _end = ')'
        _par = _arg.find('(')
        if(_par == -1):
            _par = _arg.find('<')
            _end = '> ->'

        if _par != -1:
            _endpar = _tmp.find(_end)
            _arg = _tmp[:_endpar+1]
            _tmp = _tmp[_endpar+1:]
        else :
            _tmp = _tmp[_result+4:]

        if _arg:
            _args.append(_arg)

        _result = _tmp.find(' -> ')

        _count += 1
        if _count > 10 or _result == -1:
            _result = None

    return _args, _tmp

#returns a single tuple parsed for legibility as function args, clamped if too long etc
def parse_type(_type):

    if _type is None:
        return None

    if _type == "":
        return []

    result = []

    _args, _return = parse_args(_type)

    for item in _args:
        node = item.split(' : ')
        _name = node[0]
        _typename = "Unknown"
        if(len(node) > 1):
            _typename = node[1]

        result.append((_name+'\t'+_typename, _name))

    return result

#returns True if the string is completion info for a function
def is_function(_str):
    if _str:
        return _str.find(' -> ') != -1
    else:
        return False