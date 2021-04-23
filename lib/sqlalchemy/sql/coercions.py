# sql/coercions.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

import numbers
import re

from . import operators
from . import roles
from . import visitors
from .base import Options
from .traversals import HasCacheKey
from .visitors import Visitable
from .. import exc
from .. import inspection
from .. import util
from ..util import collections_abc

if util.TYPE_CHECKING:
    from types import ModuleType

elements = None  # type: ModuleType
lambdas = None  # type: ModuleType
schema = None  # type: ModuleType
selectable = None  # type: ModuleType
sqltypes = None  # type: ModuleType
traversals = None  # type: ModuleType


def _is_literal(element):
    """Return whether or not the element is a "literal" in the context
    of a SQL expression construct.

    """

    return (
        not isinstance(
            element,
            (Visitable, schema.SchemaEventTarget),
        )
        and not hasattr(element, "__clause_element__")
    )


def _deep_is_literal(element):
    """Return whether or not the element is a "literal" in the context
    of a SQL expression construct.

    does a deeper more esoteric check than _is_literal.   is used
    for lambda elements that have to distinguish values that would
    be bound vs. not without any context.

    """

    if isinstance(element, collections_abc.Sequence) and not isinstance(
        element, str
    ):
        for elem in element:
            if not _deep_is_literal(elem):
                return False
        else:
            return True

    return (
        not isinstance(
            element,
            (
                Visitable,
                schema.SchemaEventTarget,
                HasCacheKey,
                Options,
                util.langhelpers._symbol,
            ),
        )
        and not hasattr(element, "__clause_element__")
        and (
            not isinstance(element, type)
            or not issubclass(element, HasCacheKey)
        )
    )


def _document_text_coercion(paramname, meth_rst, param_rst):
    return util.add_parameter_text(
        paramname,
        (
            ".. warning:: "
            "The %s argument to %s can be passed as a Python string argument, "
            "which will be treated "
            "as **trusted SQL text** and rendered as given.  **DO NOT PASS "
            "UNTRUSTED INPUT TO THIS PARAMETER**."
        )
        % (param_rst, meth_rst),
    )


def _expression_collection_was_a_list(attrname, fnname, args):
    if args and isinstance(args[0], (list, set, dict)) and len(args) == 1:
        util.warn_deprecated_20(
            'The "%s" argument to %s() is now passed as a series of '
            "positional "
            "elements, rather than as a list. " % (attrname, fnname)
        )
        return args[0]
    else:
        return args


def expect(
    role,
    element,
    apply_propagate_attrs=None,
    argname=None,
    post_inspect=False,
    **kw
):
    if (
        role.allows_lambda
        # note callable() will not invoke a __getattr__() method, whereas
        # hasattr(obj, "__call__") will. by keeping the callable() check here
        # we prevent most needless calls to hasattr()  and therefore
        # __getattr__(), which is present on ColumnElement.
        and callable(element)
        and hasattr(element, "__code__")
    ):
        return lambdas.LambdaElement(
            element,
            role,
            lambdas.LambdaOptions(**kw),
            apply_propagate_attrs=apply_propagate_attrs,
        )

    # major case is that we are given a ClauseElement already, skip more
    # elaborate logic up front if possible
    impl = _impl_lookup[role]

    original_element = element

    if not isinstance(
        element,
        (elements.ClauseElement, schema.SchemaItem, schema.FetchedValue),
    ):
        resolved = None

        if impl._resolve_literal_only:
            resolved = impl._literal_coercion(element, **kw)
        else:

            original_element = element

            is_clause_element = False

            while hasattr(element, "__clause_element__"):
                is_clause_element = True
                if not getattr(element, "is_clause_element", False):
                    element = element.__clause_element__()
                else:
                    break

            if not is_clause_element:
                if impl._use_inspection:
                    insp = inspection.inspect(element, raiseerr=False)
                    if insp is not None:
                        if post_inspect:
                            insp._post_inspect
                        try:
                            resolved = insp.__clause_element__()
                        except AttributeError:
                            impl._raise_for_expected(original_element, argname)

                if resolved is None:
                    resolved = impl._literal_coercion(
                        element, argname=argname, **kw
                    )
            else:
                resolved = element
    else:
        resolved = element

    if (
        apply_propagate_attrs is not None
        and not apply_propagate_attrs._propagate_attrs
        and resolved._propagate_attrs
    ):
        apply_propagate_attrs._propagate_attrs = resolved._propagate_attrs

    if impl._role_class in resolved.__class__.__mro__:
        if impl._post_coercion:
            resolved = impl._post_coercion(
                resolved,
                argname=argname,
                original_element=original_element,
                **kw
            )
        return resolved
    else:
        return impl._implicit_coercions(
            original_element, resolved, argname=argname, **kw
        )


def expect_as_key(role, element, **kw):
    kw["as_key"] = True
    return expect(role, element, **kw)


def expect_col_expression_collection(role, expressions):
    for expr in expressions:
        strname = None
        column = None

        resolved = expect(role, expr)
        if isinstance(resolved, util.string_types):
            strname = resolved = expr
        else:
            cols = []
            visitors.traverse(resolved, {}, {"column": cols.append})
            if cols:
                column = cols[0]
        add_element = column if column is not None else strname
        yield resolved, column, strname, add_element


class RoleImpl(object):
    __slots__ = ("_role_class", "name", "_use_inspection")

    def _literal_coercion(self, element, **kw):
        raise NotImplementedError()

    _post_coercion = None
    _resolve_literal_only = False

    def __init__(self, role_class):
        self._role_class = role_class
        self.name = role_class._role_name
        self._use_inspection = issubclass(role_class, roles.UsesInspection)

    def _implicit_coercions(self, element, resolved, argname=None, **kw):
        self._raise_for_expected(element, argname, resolved)

    def _raise_for_expected(
        self,
        element,
        argname=None,
        resolved=None,
        advice=None,
        code=None,
        err=None,
    ):
        if resolved is not None and resolved is not element:
            got = "%r object resolved from %r object" % (resolved, element)
        else:
            got = repr(element)

        if argname:
            msg = "%s expected for argument %r; got %s." % (
                self.name,
                argname,
                got,
            )
        else:
            msg = "%s expected, got %s." % (self.name, got)

        if advice:
            msg += " " + advice

        util.raise_(exc.ArgumentError(msg, code=code), replace_context=err)


class _Deannotate(object):
    __slots__ = ()

    def _post_coercion(self, resolved, **kw):
        from .util import _deep_deannotate

        return _deep_deannotate(resolved)


class _StringOnly(object):
    __slots__ = ()

    _resolve_literal_only = True


class _ReturnsStringKey(object):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if isinstance(original_element, util.string_types):
            return original_element
        else:
            self._raise_for_expected(original_element, argname, resolved)

    def _literal_coercion(self, element, **kw):
        return element


class _ColumnCoercions(object):
    __slots__ = ()

    def _warn_for_scalar_subquery_coercion(self):
        util.warn(
            "implicitly coercing SELECT object to scalar subquery; "
            "please use the .scalar_subquery() method to produce a scalar "
            "subquery.",
        )

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if not getattr(resolved, "is_clause_element", False):
            self._raise_for_expected(original_element, argname, resolved)
        elif resolved._is_select_statement:
            self._warn_for_scalar_subquery_coercion()
            return resolved.scalar_subquery()
        elif resolved._is_from_clause and isinstance(
            resolved, selectable.Subquery
        ):
            self._warn_for_scalar_subquery_coercion()
            return resolved.element.scalar_subquery()
        elif self._role_class.allows_lambda and resolved._is_lambda_element:
            return resolved
        else:
            self._raise_for_expected(original_element, argname, resolved)


def _no_text_coercion(
    element, argname=None, exc_cls=exc.ArgumentError, extra=None, err=None
):
    util.raise_(
        exc_cls(
            "%(extra)sTextual SQL expression %(expr)r %(argname)sshould be "
            "explicitly declared as text(%(expr)r)"
            % {
                "expr": util.ellipses_string(element),
                "argname": "for argument %s" % (argname,) if argname else "",
                "extra": "%s " % extra if extra else "",
            }
        ),
        replace_context=err,
    )


class _NoTextCoercion(object):
    __slots__ = ()

    def _literal_coercion(self, element, argname=None, **kw):
        if isinstance(element, util.string_types) and issubclass(
            elements.TextClause, self._role_class
        ):
            _no_text_coercion(element, argname)
        else:
            self._raise_for_expected(element, argname)


class _CoerceLiterals(object):
    __slots__ = ()
    _coerce_consts = False
    _coerce_star = False
    _coerce_numerics = False

    def _text_coercion(self, element, argname=None):
        return _no_text_coercion(element, argname)

    def _literal_coercion(self, element, argname=None, **kw):
        if isinstance(element, util.string_types):
            if self._coerce_star and element == "*":
                return elements.ColumnClause("*", is_literal=True)
            else:
                return self._text_coercion(element, argname, **kw)

        if self._coerce_consts:
            if element is None:
                return elements.Null()
            elif element is False:
                return elements.False_()
            elif element is True:
                return elements.True_()

        if self._coerce_numerics and isinstance(element, (numbers.Number)):
            return elements.ColumnClause(str(element), is_literal=True)

        self._raise_for_expected(element, argname)


class LiteralValueImpl(RoleImpl):
    _resolve_literal_only = True

    def _implicit_coercions(
        self, element, resolved, argname, type_=None, **kw
    ):
        if not _is_literal(resolved):
            self._raise_for_expected(
                element, resolved=resolved, argname=argname, **kw
            )

        return elements.BindParameter(None, element, type_=type_, unique=True)

    def _literal_coercion(self, element, argname=None, type_=None, **kw):
        return element


class _SelectIsNotFrom(object):
    __slots__ = ()

    def _raise_for_expected(self, element, argname=None, resolved=None, **kw):
        if isinstance(element, roles.SelectStatementRole) or isinstance(
            resolved, roles.SelectStatementRole
        ):
            advice = (
                "To create a "
                "FROM clause from a %s object, use the .subquery() method."
                % (resolved.__class__ if resolved is not None else element,)
            )
            code = "89ve"
        else:
            advice = code = None

        return super(_SelectIsNotFrom, self)._raise_for_expected(
            element,
            argname=argname,
            resolved=resolved,
            advice=advice,
            code=code,
            **kw
        )


class HasCacheKeyImpl(RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if isinstance(original_element, traversals.HasCacheKey):
            return original_element
        else:
            self._raise_for_expected(original_element, argname, resolved)

    def _literal_coercion(self, element, **kw):
        return element


class ExpressionElementImpl(_ColumnCoercions, RoleImpl):
    __slots__ = ()

    def _literal_coercion(
        self, element, name=None, type_=None, argname=None, is_crud=False, **kw
    ):
        if element is None:
            return elements.Null()
        else:
            try:
                return elements.BindParameter(
                    name, element, type_, unique=True, _is_crud=is_crud
                )
            except exc.ArgumentError as err:
                self._raise_for_expected(element, err=err)

    def _raise_for_expected(self, element, argname=None, resolved=None, **kw):
        if isinstance(element, roles.AnonymizedFromClauseRole):
            advice = (
                "To create a "
                "column expression from a FROM clause row "
                "as a whole, use the .table_valued() method."
            )
        else:
            advice = None

        return super(ExpressionElementImpl, self)._raise_for_expected(
            element, argname=argname, resolved=resolved, advice=advice, **kw
        )


class BinaryElementImpl(ExpressionElementImpl, RoleImpl):

    __slots__ = ()

    def _literal_coercion(
        self, element, expr, operator, bindparam_type=None, argname=None, **kw
    ):
        try:
            return expr._bind_param(operator, element, type_=bindparam_type)
        except exc.ArgumentError as err:
            self._raise_for_expected(element, err=err)

    def _post_coercion(self, resolved, expr, **kw):
        if resolved.type._isnull and not expr.type._isnull:
            resolved = resolved._with_binary_element_type(expr.type)
        return resolved


class InElementImpl(RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if resolved._is_from_clause:
            if (
                isinstance(resolved, selectable.Alias)
                and resolved.element._is_select_statement
            ):
                self._warn_for_implicit_coercion(resolved)
                return self._post_coercion(resolved.element, **kw)
            else:
                self._warn_for_implicit_coercion(resolved)
                return self._post_coercion(resolved.select(), **kw)
        else:
            self._raise_for_expected(original_element, argname, resolved)

    def _warn_for_implicit_coercion(self, elem):
        util.warn(
            "Coercing %s object into a select() for use in IN(); "
            "please pass a select() construct explicitly"
            % (elem.__class__.__name__)
        )

    def _literal_coercion(self, element, expr, operator, **kw):
        if isinstance(element, collections_abc.Iterable) and not isinstance(
            element, util.string_types
        ):
            non_literal_expressions = {}
            element = list(element)
            for o in element:
                if not _is_literal(o):
                    if not isinstance(o, operators.ColumnOperators):
                        self._raise_for_expected(element, **kw)
                    else:
                        non_literal_expressions[o] = o
                elif o is None:
                    non_literal_expressions[o] = elements.Null()

            if non_literal_expressions:
                return elements.ClauseList(
                    *[
                        non_literal_expressions[o]
                        if o in non_literal_expressions
                        else expr._bind_param(operator, o)
                        for o in element
                    ]
                )
            else:
                return expr._bind_param(operator, element, expanding=True)

        else:
            self._raise_for_expected(element, **kw)

    def _post_coercion(self, element, expr, operator, **kw):
        if element._is_select_statement:
            # for IN, we are doing scalar_subquery() coercion without
            # a warning
            return element.scalar_subquery()
        elif isinstance(element, elements.ClauseList):
            assert not len(element.clauses) == 0
            return element.self_group(against=operator)

        elif isinstance(element, elements.BindParameter):
            if not element.expanding:
                # coercing to expanding at the moment to work with the
                # lambda system.  not sure if this is the right approach.
                # is there a valid use case to send a single non-expanding
                # param to IN? check for ARRAY type?
                element = element._clone(maintain_key=True)
                element.expanding = True

            return element
        else:
            return element


class OnClauseImpl(_CoerceLiterals, _ColumnCoercions, RoleImpl):
    __slots__ = ()

    _coerce_consts = True

    def _implicit_coercions(
        self, original_element, resolved, argname=None, legacy=False, **kw
    ):
        if legacy and isinstance(resolved, str):
            return resolved
        else:
            return super(OnClauseImpl, self)._implicit_coercions(
                original_element,
                resolved,
                argname=argname,
                legacy=legacy,
                **kw
            )

    def _text_coercion(self, element, argname=None, legacy=False):
        if legacy and isinstance(element, str):
            util.warn_deprecated_20(
                "Using strings to indicate relationship names in "
                "Query.join() is deprecated and will be removed in "
                "SQLAlchemy 2.0.  Please use the class-bound attribute "
                "directly."
            )
            return element

        return super(OnClauseImpl, self)._text_coercion(element, argname)

    def _post_coercion(self, resolved, original_element=None, **kw):
        # this is a hack right now as we want to use coercion on an
        # ORM InstrumentedAttribute, but we want to return the object
        # itself if it is one, not its clause element.
        # ORM context _join and _legacy_join() would need to be improved
        # to look for annotations in a clause element form.
        if isinstance(original_element, roles.JoinTargetRole):
            return original_element
        return resolved


class WhereHavingImpl(_CoerceLiterals, _ColumnCoercions, RoleImpl):
    __slots__ = ()

    _coerce_consts = True

    def _text_coercion(self, element, argname=None):
        return _no_text_coercion(element, argname)


class StatementOptionImpl(_CoerceLiterals, RoleImpl):
    __slots__ = ()

    _coerce_consts = True

    def _text_coercion(self, element, argname=None):
        return elements.TextClause(element)


class ColumnArgumentImpl(_NoTextCoercion, RoleImpl):
    __slots__ = ()


class ColumnArgumentOrKeyImpl(_ReturnsStringKey, RoleImpl):
    __slots__ = ()


class StrAsPlainColumnImpl(_CoerceLiterals, RoleImpl):
    __slots__ = ()

    def _text_coercion(self, element, argname=None):
        return elements.ColumnClause(element)


class ByOfImpl(_CoerceLiterals, _ColumnCoercions, RoleImpl, roles.ByOfRole):

    __slots__ = ()

    _coerce_consts = True

    def _text_coercion(self, element, argname=None):
        return elements._textual_label_reference(element)


class OrderByImpl(ByOfImpl, RoleImpl):
    __slots__ = ()

    def _post_coercion(self, resolved, **kw):
        if (
            isinstance(resolved, self._role_class)
            and resolved._order_by_label_element is not None
        ):
            return elements._label_reference(resolved)
        else:
            return resolved


class GroupByImpl(ByOfImpl, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if isinstance(resolved, roles.StrictFromClauseRole):
            return elements.ClauseList(*resolved.c)
        else:
            return resolved


class DMLColumnImpl(_ReturnsStringKey, RoleImpl):
    __slots__ = ()

    def _post_coercion(self, element, as_key=False, **kw):
        if as_key:
            return element.key
        else:
            return element


class ConstExprImpl(RoleImpl):
    __slots__ = ()

    def _literal_coercion(self, element, argname=None, **kw):
        if element is None:
            return elements.Null()
        elif element is False:
            return elements.False_()
        elif element is True:
            return elements.True_()
        else:
            self._raise_for_expected(element, argname)


class TruncatedLabelImpl(_StringOnly, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if isinstance(original_element, util.string_types):
            return resolved
        else:
            self._raise_for_expected(original_element, argname, resolved)

    def _literal_coercion(self, element, argname=None, **kw):
        """coerce the given value to :class:`._truncated_label`.

        Existing :class:`._truncated_label` and
        :class:`._anonymous_label` objects are passed
        unchanged.
        """

        if isinstance(element, elements._truncated_label):
            return element
        else:
            return elements._truncated_label(element)


class DDLExpressionImpl(_Deannotate, _CoerceLiterals, RoleImpl):

    __slots__ = ()

    _coerce_consts = True

    def _text_coercion(self, element, argname=None):
        # see #5754 for why we can't easily deprecate this coercion.
        # essentially expressions like postgresql_where would have to be
        # text() as they come back from reflection and we don't want to
        # have text() elements wired into the inspection dictionaries.
        return elements.TextClause(element)


class DDLConstraintColumnImpl(_Deannotate, _ReturnsStringKey, RoleImpl):
    __slots__ = ()


class DDLReferredColumnImpl(DDLConstraintColumnImpl):
    __slots__ = ()


class LimitOffsetImpl(RoleImpl):
    __slots__ = ()

    def _implicit_coercions(self, element, resolved, argname=None, **kw):
        if resolved is None:
            return None
        else:
            self._raise_for_expected(element, argname, resolved)

    def _literal_coercion(self, element, name, type_, **kw):
        if element is None:
            return None
        else:
            value = util.asint(element)
            return selectable._OffsetLimitParam(
                name, value, type_=type_, unique=True
            )


class LabeledColumnExprImpl(ExpressionElementImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if isinstance(resolved, roles.ExpressionElementRole):
            return resolved.label(None)
        else:
            new = super(LabeledColumnExprImpl, self)._implicit_coercions(
                original_element, resolved, argname=argname, **kw
            )
            if isinstance(new, roles.ExpressionElementRole):
                return new.label(None)
            else:
                self._raise_for_expected(original_element, argname, resolved)


class ColumnsClauseImpl(_SelectIsNotFrom, _CoerceLiterals, RoleImpl):
    __slots__ = ()

    _coerce_consts = True
    _coerce_numerics = True
    _coerce_star = True

    _guess_straight_column = re.compile(r"^\w\S*$", re.I)

    def _text_coercion(self, element, argname=None):
        element = str(element)

        guess_is_literal = not self._guess_straight_column.match(element)
        raise exc.ArgumentError(
            "Textual column expression %(column)r %(argname)sshould be "
            "explicitly declared with text(%(column)r), "
            "or use %(literal_column)s(%(column)r) "
            "for more specificity"
            % {
                "column": util.ellipses_string(element),
                "argname": "for argument %s" % (argname,) if argname else "",
                "literal_column": "literal_column"
                if guess_is_literal
                else "column",
            }
        )


class ReturnsRowsImpl(RoleImpl):
    __slots__ = ()


class StatementImpl(_CoerceLiterals, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if resolved._is_lambda_element:
            return resolved
        else:
            return super(StatementImpl, self)._implicit_coercions(
                original_element, resolved, argname=argname, **kw
            )

    def _text_coercion(self, element, argname=None):
        util.warn_deprecated_20(
            "Using plain strings to indicate SQL statements without using "
            "the text() construct is  "
            "deprecated and will be removed in version 2.0.  Ensure plain "
            "SQL statements are passed using the text() construct."
        )
        return elements.TextClause(element)


class SelectStatementImpl(_NoTextCoercion, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if resolved._is_text_clause:
            return resolved.columns()
        else:
            self._raise_for_expected(original_element, argname, resolved)


class HasCTEImpl(ReturnsRowsImpl):
    __slots__ = ()


class JoinTargetImpl(RoleImpl):
    __slots__ = ()

    def _literal_coercion(self, element, legacy=False, **kw):
        if isinstance(element, str):
            return element

    def _implicit_coercions(
        self, original_element, resolved, argname=None, legacy=False, **kw
    ):
        if isinstance(original_element, roles.JoinTargetRole):
            return original_element
        elif legacy and isinstance(resolved, str):
            util.warn_deprecated_20(
                "Using strings to indicate relationship names in "
                "Query.join() is deprecated and will be removed in "
                "SQLAlchemy 2.0.  Please use the class-bound attribute "
                "directly."
            )
            return resolved
        elif legacy and isinstance(resolved, roles.WhereHavingRole):
            return resolved
        elif legacy and resolved._is_select_statement:
            util.warn_deprecated(
                "Implicit coercion of SELECT and textual SELECT "
                "constructs into FROM clauses is deprecated; please call "
                ".subquery() on any Core select or ORM Query object in "
                "order to produce a subquery object.",
                version="1.4",
            )
            # TODO: doing _implicit_subquery here causes tests to fail,
            # how was this working before?  probably that ORM
            # join logic treated it as a select and subquery would happen
            # in _ORMJoin->Join
            return resolved
        else:
            self._raise_for_expected(original_element, argname, resolved)


class FromClauseImpl(_SelectIsNotFrom, _NoTextCoercion, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self,
        original_element,
        resolved,
        argname=None,
        explicit_subquery=False,
        allow_select=True,
        **kw
    ):
        if resolved._is_select_statement:
            if explicit_subquery:
                return resolved.subquery()
            elif allow_select:
                util.warn_deprecated(
                    "Implicit coercion of SELECT and textual SELECT "
                    "constructs into FROM clauses is deprecated; please call "
                    ".subquery() on any Core select or ORM Query object in "
                    "order to produce a subquery object.",
                    version="1.4",
                )
                return resolved._implicit_subquery
        elif resolved._is_text_clause:
            return resolved
        else:
            self._raise_for_expected(original_element, argname, resolved)

    def _post_coercion(self, element, deannotate=False, **kw):
        if deannotate:
            return element._deannotate()
        else:
            return element


class StrictFromClauseImpl(FromClauseImpl):
    __slots__ = ()

    def _implicit_coercions(
        self,
        original_element,
        resolved,
        argname=None,
        allow_select=False,
        **kw
    ):
        if resolved._is_select_statement and allow_select:
            util.warn_deprecated(
                "Implicit coercion of SELECT and textual SELECT constructs "
                "into FROM clauses is deprecated; please call .subquery() "
                "on any Core select or ORM Query object in order to produce a "
                "subquery object.",
                version="1.4",
            )
            return resolved._implicit_subquery
        else:
            self._raise_for_expected(original_element, argname, resolved)


class AnonymizedFromClauseImpl(StrictFromClauseImpl):
    __slots__ = ()

    def _post_coercion(self, element, flat=False, name=None, **kw):
        assert name is None

        return element._anonymous_fromclause(flat=flat)


class DMLTableImpl(_SelectIsNotFrom, _NoTextCoercion, RoleImpl):
    __slots__ = ()

    def _post_coercion(self, element, **kw):
        if "dml_table" in element._annotations:
            return element._annotations["dml_table"]
        else:
            return element


class DMLSelectImpl(_NoTextCoercion, RoleImpl):
    __slots__ = ()

    def _implicit_coercions(
        self, original_element, resolved, argname=None, **kw
    ):
        if resolved._is_from_clause:
            if (
                isinstance(resolved, selectable.Alias)
                and resolved.element._is_select_statement
            ):
                return resolved.element
            else:
                return resolved.select()
        else:
            self._raise_for_expected(original_element, argname, resolved)


class CompoundElementImpl(_NoTextCoercion, RoleImpl):
    __slots__ = ()

    def _raise_for_expected(self, element, argname=None, resolved=None, **kw):
        if isinstance(element, roles.FromClauseRole):
            if element._is_subquery:
                advice = (
                    "Use the plain select() object without "
                    "calling .subquery() or .alias()."
                )
            else:
                advice = (
                    "To SELECT from any FROM clause, use the .select() method."
                )
        else:
            advice = None
        return super(CompoundElementImpl, self)._raise_for_expected(
            element, argname=argname, resolved=resolved, advice=advice, **kw
        )


_impl_lookup = {}


for name in dir(roles):
    cls = getattr(roles, name)
    if name.endswith("Role"):
        name = name.replace("Role", "Impl")
        if name in globals():
            impl = globals()[name](cls)
            _impl_lookup[cls] = impl
