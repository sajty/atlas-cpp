#This file is distributed under the terms of 
#the GNU Lesser General Public license (See the file COPYING for details).
#Copyright (C) 2000 Stefanus Du Toit and Aloril

from common import *

class AttributeInfo:
    attr_enum = {"_free":1 }
    def __init__(self, name, value, type=None):
        if not type: type = get_atlas_type(value)
        self.name = name
        self.cname = classize(name)
        self.flag_name = string.upper(name) + "_FLAG"
        self.value = value
        self.type = type
        self.ctype = classize(self.type)
        self.enum = self.get_num()
        self.cpp_type = cpp_type[type]
        self.cpp_param_type = cpp_param_type[type]
        self.cpp_param_type2 = cpp_param_type2[type]
        self.as_object = ""
        self.ctype_as_object = self.ctype

    def get_num(self):
        if self.attr_enum.has_key(self.name):
            return self.attr_enum[self.name]
        num = self.attr_enum['_free']
        self.attr_enum['_free'] = num + 1
        self.attr_enum[self.name] = num
        return num

    def set_if(self):
        res = doc(4, 'Set the "%s" attribute.' % self.name)+\
              "    inline void set%(cname)s(%(cpp_param_type)s val);\n" % \
              self.__dict__
        if self.as_object:
            res = res + doc(4, 'Retrieve the "%s" attribute %s.' % \
                            (self.name, self.as_object)) + \
               "    inline void set%(cname)s%(as_object)s(%(cpp_param_type_as_object)s val);\n" % self.__dict__
        return res

    def get_if(self):
        res = doc(4, 'Retrieve the "%s" attribute.' % self.name)+\
              "    inline %(cpp_param_type)s get%(cname)s() const;\n" % self.__dict__ +\
              doc(4, 'Retrieve the "%s" attribute as a non-const reference.' % self.name)+\
              "    inline %(cpp_param_type2)s modify%(cname)s();\n" % self.__dict__
        if self.as_object:
            res = res + doc(4, 'Retrieve the "%s" attribute %s.' % \
                            (self.name, self.as_object)) + \
               "    inline %(cpp_param_type_as_object)s get%(cname)s%(as_object)s() const;\n" % self.__dict__
        return res

    def is_default_if(self):
        return doc(4, 'Is "%s" value default?' % self.name)+\
               "    inline bool isDefault%(cname)s() const;\n" % self.__dict__

    def inline_set(self, classname):
        self.classname = classname
        return """void %(classname)s::set%(cname)s(%(cpp_param_type)s val)
{
    attr_%(name)s = val;
    m_attrFlags |= %(flag_name)s;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def inline_get(self, classname):
        self.classname = classname
        return """%(cpp_param_type)s %(classname)s::get%(cname)s() const
{
    if(m_attrFlags & %(flag_name)s)
        return attr_%(name)s;
    else
        return ((%(classname)s*)m_defaults)->attr_%(name)s;
}

%(cpp_param_type2)s %(classname)s::modify%(cname)s()
{
    if(!(m_attrFlags & %(flag_name)s))
        set%(cname)s(((%(classname)s*)m_defaults)->attr_%(name)s);
    return attr_%(name)s;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def inline_is_default(self, classname):
        self.classname = classname
        return """bool %(classname)s::isDefault%(cname)s() const
{
    return (m_attrFlags & %(flag_name)s) == 0;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def inline_send(self, classname):
        res = 'void %s::send%s' % (classname, self.cname)
        res = res + '(Atlas::Bridge & b) const\n'
        res = res + '{\n'
        if self.name not in ["parents", "objtype"]:
            res = res + '    if(m_attrFlags & %s) {\n' % self.flag_name
            indent = "    "
        else:
            indent = ""

        if self.type == "int":
            res = res + indent + '    b.mapIntItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        elif self.type == "float":
            res = res + indent + '    b.mapFloatItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        elif self.type == "string":
            res = res + indent + '    b.mapStringItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        elif self.type == "list":
            res = res + indent + '    Atlas::Message::Encoder e(b);\n'
            res = res + indent + '    e.mapElementListItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        elif self.type == "map":
            res = res + indent + '    Atlas::Message::Encoder e(b);\n'
            res = res + indent + '    e.mapElementMapItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        elif self.type == "string_list":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::list<std::string> & l = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::list<std::string>::const_iterator I = l.begin();\n'
            res = res + indent + '    for(; I != l.end(); ++I) {\n'
            res = res + indent + '        b.listStringItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        elif self.type == "int_list":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::list<std::string> & l = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::list<std::string>::const_iterator I = l.begin();\n'
            res = res + indent + '    for(; I != l.end(); ++I) {\n'
            res = res + indent + '        b.listIntItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        elif self.type == "float_list":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::list<double> & l = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::list<double>::const_iterator I = l.begin();\n'
            res = res + indent + '    for(; I != l.end(); ++I) {\n'
            res = res + indent + '        b.listFloatItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        elif self.type == "string_list_length":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::vector<std::string> & v = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::vector<std::string>::const_iterator I = v.begin();\n'
            res = res + indent + '    for(; I != v.end(); ++I) {\n'
            res = res + indent + '        b.listStringItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        elif self.type == "int_list_length":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::vector<std::string> & v = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::vector<std::string>::const_iterator I = v.begin();\n'
            res = res + indent + '    for(; I != v.end(); ++I) {\n'
            res = res + indent + '        b.listIntItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        elif self.type == "float_list_length":
            res = res + indent + '    b.mapListItem("%s");\n' % (self.name)
            res = res + indent + '    const std::vector<double> & v = get%s();\n' \
                  % (self.cname)
            res = res + indent + '    std::vector<double>::const_iterator I = v.begin();\n'
            res = res + indent + '    for(; I != v.end(); ++I) {\n'
            res = res + indent + '        b.listFloatItem(*I);\n'
            res = res + indent + '    }\n'
            res = res + indent + '    b.listEnd();\n'
        else:
            res = res + indent + '    Atlas::Message::Encoder e(b);\n'
            res = res + indent + '    e.mapElementListItem("%s", get%s%s());\n' \
                  % (self.name, self.cname, self.as_object)
        if self.name not in ["parents", "objtype"]:
            res = res + '    }\n'
        return res + '}\n\n'
        

#[gs]etattr_im: convert to use get/set'Attrname'

    def check_obj(self, name, obj):
        if not isinstance(obj, AttributeInfo):
            obj = AttributeInfo(name, obj)
        return obj

    def default_map(self, name, obj):
        obj = self.check_obj(name, obj)
        res = "        Element::MapType " + name + ";\n"
        for (sub_name, sub_value) in obj.value.items():
            sub = AttributeInfo(sub_name, sub_value)
            if sub.type == "list":
                res = res + self.default_list("%s_%s" % (name, sub.name), sub)
            if sub.type == "map":
                res = res + self.default_map("%s_%s" % (name, sub.name), sub)
            res = res + "        %s.push_back(" % name
            if sub.type == "list" or sub.type == "map":
                res = res + "%s_%s" % (name, sub.name)
            elif sub.type == "string":
                res = res + 'std::string("%s")' % sub.value
            else:
                res = res + "%s" % sub.value
            res = res + ");\n"
        return res

    def default_list(self, name, obj):
        obj = self.check_obj(name, obj)
        i = 0
        res = "        Element::ListType " + name + ";\n"
        for sub in obj.value:
            sub_type = type2str[type(sub)]
            if sub_type == "list":
                res  = res + self.default_list("%s_%d" % (name, ++i), sub)
            elif sub_type == "map":
                res = res + self.default_map("%s_%d" % (name, ++i), sub)
            res = res + "        %s.push_back(" % name
            if sub_type == "list" or sub_type == "map":
                res = res + "%s_%d" % (name, i)
            elif sub_type == "string":
                res = res + 'std::string("%s")' % sub
            else:
                res = res + '%s' % sub
            res = res + ");\n"
        return res

    def constructors_im(self):
        if self.type == "map": return ""
        res = ""
        if self.type == "list":
            res = res + self.default_list(self.name, self)
        if self.type == "map":
            res = res + self.default_map(self.name, self)
        res = res + '        set' + self.cname + '('
        if self.type == "string":
            res = res + 'std::string("' + self.value + '")'
        elif self.type == "list" or self.type == "map":
            res = res + self.name
        else:
            res = res + '%s' % self.value
        return res + ');\n'

    def getattr_im(self):
        return '    if (name == "%(name)s") return get%(cname)s%(as_object)s();\n' \
               % self.__dict__

    def setattr_im(self):
        return '    if (name == "%(name)s") { set%(cname)s%(as_object)s(attr.as%(ctype_as_object)s()); return; }\n' % self.__dict__



#Element::ListType vs vector<BaseObject>
#vector<BaseObject> -> Element::ListType: use asElement to convert
#Element::ListType -> vector<BaseObject>: use BaseObjectData and make all dynamic?

class ArgsRootList(AttributeInfo):
    def __init__(self, name, value, type):
        AttributeInfo.__init__(self, name, value, "RootList")
        self.as_object = "AsList"
        self.cpp_param_type_as_object = cpp_param_type["list"][:-1]
        self.ctype_as_object = "List"

    def set_if(self):
        return AttributeInfo.set_if(self) + \
               "    inline void set%(cname)s1(Root& val);\n" % self.__dict__

    def inline_set(self, classname):
        return AttributeInfo.inline_set(self, classname) + \
               """void %(classname)s::set%(cname)s%(as_object)s(%(cpp_param_type_as_object)s val)
{
    m_attrFlags |= %(flag_name)s;
    attr_%(name)s.resize(0);
    for(Message::Element::ListType::const_iterator I = val.begin();
        I != val.end();
        I++)
    {
        if (I->isMap()) {
            attr_%(name)s.push_back(messageElement2ClassObject(I->asMap()));
        }
    }
}

void %(classname)s::set%(cname)s1(Root& val)
{
    m_attrFlags |= %(flag_name)s;
    if(attr_%(name)s.size()!=1) attr_%(name)s.resize(1);
    attr_%(name)s[0] = val;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def inline_get(self, classname):
        return AttributeInfo.inline_get(self, classname) + \
               """%(cpp_param_type_as_object)s %(classname)s::get%(cname)s%(as_object)s() const
{
    %(cpp_param_type)s args_in = get%(cname)s();
    Atlas::Message::Element::ListType args_out;
    for(%(cpp_type)s::const_iterator I = args_in.begin();
        I != args_in.end();
        I++)
    {
        args_out.push_back(Atlas::Message::Element::MapType());
        (*I)->addToMessage(args_out.back().asMap());
    }
    return args_out;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def constructors_im(self):
        return ""

#typed list: string_list, int_list, float_list
#Element::ListType vs list<foo>
#list<foo> -> Element::ListType: just add
#Element::ListType -> list<foo>: check type and ignore not matching types

class TypedList(AttributeInfo):
    def __init__(self, name, value, type):
        AttributeInfo.__init__(self, name, value, type)
        self.as_object = "AsList"
        self.cpp_param_type_as_object = cpp_param_type["list"][:-1]
        self.ctype_as_object = "List"
        element_type = string.split(type,"_")[0]
        self.cpp_element_type = cpp_type[element_type]
        if element_type == "string":
            self.cpp_element_type_begin = "std::string("
            self.cpp_element_type_end = ")"
        else:
            self.cpp_element_type_begin = ""
            self.cpp_element_type_end = ""
        self.element_type_as_object = classize(element_type)

    def inline_set(self, classname):
        return AttributeInfo.inline_set(self, classname) + \
               """void %(classname)s::set%(cname)s%(as_object)s(%(cpp_param_type_as_object)s val)
{
    m_attrFlags |= %(flag_name)s;
    attr_%(name)s.resize(0);
    for(Atlas::Message::Element::ListType::const_iterator I = val.begin();
        I != val.end();
        I++)
    {
        if((*I).is%(element_type_as_object)s())
            attr_%(name)s.push_back((*I).as%(element_type_as_object)s());
    }
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def inline_get(self, classname):
        return AttributeInfo.inline_get(self, classname) + \
               """%(cpp_param_type_as_object)s %(classname)s::get%(cname)s%(as_object)s() const
{
    %(cpp_param_type)s lst_in = get%(cname)s();
    Atlas::Message::Element::ListType lst_out;
    for(%(cpp_type)s::const_iterator I = lst_in.begin();
        I != lst_in.end();
        I++)
    {
        lst_out.push_back(%(cpp_element_type_begin)s*I%(cpp_element_type_end)s);
    }
    return lst_out;
}

""" % self.__dict__ #"for xemacs syntax highlighting

    def constructors_im(self):
        return ""

#typed list with fixed length: 
#string_list_length, int_list_length, float_list_length
#Element::ListType vs vector<foo>
#vector<foo> -> Element::ListType: just add
#Element::ListType -> vector<foo>: check type and ignore not matching types
#                    also check length and ignore all extra elements and 
#                    fill missing elements with defaults

class TypedVector(TypedList): pass
#add length check later
#(and take into account possibility of settting default values using AsList versions)

attr_name2class = {'map': [AttributeInfo],
                   'list': [AttributeInfo],
                   'string': [AttributeInfo],
                   'int': [AttributeInfo],
                   'float': [AttributeInfo],
                   'args': [ArgsRootList],
                   'string_list': [TypedList],
                   'int_list': [TypedList],
                   'float_list': [TypedList],
                   'string_list_length': [TypedVector],
                   'int_list_length': [TypedVector],
                   'float_list_length': [TypedVector]}
