#
# primary goal of this snippet is to get attrs-ized classes
# that uses a list type and to work it into a JSON output
# by converting it into dict-type yet JSON'able structure
# despite its heavy class nesting.
import attr
import json
import typing
import pprint


def recursive_any_to_dict(anyElement):
    """
    Recursive any nested type into a dict (so that it can be JSON'able).
    :param anyElement: Just about any 'attrs-ized' instance variable type in Python.
    :return: A dict structure
    """
    if isinstance(anyElement, dict):
        simple_dict = {}
        for key, value in anyElement.items():
            if isinstance(value, dict):
                simple_dict[key] = recursive_any_to_dict(value)
            else:
                simple_dict[key] = value

        return simple_dict
    elif isinstance(anyElement, list):  # deal with attrs' list handling
        simple_list = []
        for index in range(len(anyElement)):
            value = recursive_any_to_dict(anyElement[index])
            simple_list.append(value)
        return simple_list
    elif isinstance(anyElement, str):
        return anyElement
    elif isinstance(anyElement, bool):
        return str(anyElement)
    elif isinstance(anyElement, int):
        return str(anyElement)

    # all other types at this point here are presumably attrs-ized class-type
    simple_dict = {}
    for element in anyElement.__attrs_attrs__:
        simple_dict[element.name] = recursive_any_to_dict(getattr(anyElement, element.name))
    return simple_dict


def dumpme(title, var):
    print(title, ':', var)
    print('dir(', title, '):', dir(var))
    print(title, '.__dir__:', var.__dir__())
    if 'size' in var.__dir__():
        print(title, '.size():', var.size())
    if 'name' in var.__dir__():
        print(title, '.name:', var.name)
    if 'append' in var.__dir__():
        print(title, '.append: found!')
    if 'update' in var.__dir__():
        print(title, '.update: found!')

@attr.s(auto_attribs=True)
class AnyElement:
    not_not: bool = False
    element: typing.Any = None


@attr.s(auto_attribs=True)
class AnyElementAny:
    any_element_any: typing.Any = None


@attr.s(auto_attribs=True)
class AclElement:
    not_not: bool = False
    name: str = None
    # AnyElement, if str, use no {} pair
    # AnyElement, if object, use {} pair
    any_element: AnyElementAny = None


@attr.s(auto_attribs=True)
class MyNamedConf:
    options: typing.Dict = dict()
    acls: typing.List[AclElement] = list()


pp = pprint.PrettyPrinter(indent=4, compact=False)
tst = list()
tst.append("123")
tst.append("abc")
print(tst)
pp.pprint(tst)
nc = MyNamedConf()
pp.pprint(nc)
# = list[AclElement()]

aye1 = AnyElement(not_not=False, element='none')
ae1 = AclElement()
ae1.name = 'xfer_acl'
ae1.any_element = aye1
dumpme('ae1', ae1)

ae2 = AclElement(not_not=False, name='xfer_acl2', any_element='none')
dumpme('ae2', ae2)

nc.acls.append(ae1)
nc.acls.append(ae2)
dumpme('acls', nc.acls)

nc.options['allow_query'] = "yes"
print("nc.options:", nc.options)
print('nc:', nc)
print('nc.options:', nc.options)

print("nc.acls:", nc.acls)
print("nc.acls[0]:", nc.acls[0])
print("nc.acls[0].name:", nc.acls[0].name)
print("nc.acls[1]:", nc.acls[1])
print("nc.acls[1].name:", nc.acls[1].name)

dumpme('nc', nc)
pp.pprint(nc.acls)
instance = recursive_any_to_dict(nc)
print('instance:', instance)
print('recursive_any_to_dict:', json.dumps(instance))
print("instance['options']:", instance['options'])
print("instance['acls']:", instance['acls'])
print("instance['acls'][0]:", instance['acls'][0])
print("instance['acls'][0]['name']:", instance['acls'][0]['name'])