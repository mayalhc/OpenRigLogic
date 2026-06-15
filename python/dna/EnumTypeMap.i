%include <exception.i>

%include <spyus/Caster.i>

%define enum_typemap(type_name)

%inline {
    template<>
    struct Caster<type_name> {

        static type_name fromPy(PyObject* pyObject) {
            return static_cast<type_name>(PyLong_AsLong(pyObject));
        }

        static PyObject* toPy(type_name value) {
            return PyLong_FromLong(static_cast<long>(value));
        }

    };

}

%typemap(in) (type_name) {
    if (PyLong_CheckExact($input)) {
        $1 = Caster<type_name>::fromPy($input);
    } else {
        SWIG_exception(SWIG_TypeError, "long expected");
    }
}

%typemap(out) type_name {
    $result = Caster<$1_basetype>::toPy($1);
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_UINT16) type_name {
    $1 = PyLong_CheckExact($1) ? 1 : 0;
}

%enddef
