from ilikesql import Column
from ilikesql import exc as sa_exc
from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import MetaData
from ilikesql import String
from ilikesql import Table
from ilikesql import Unicode
from ilikesql.orm import backref
from ilikesql.orm import clear_mappers
from ilikesql.orm import configure_mappers
from ilikesql.orm import relationship
from ilikesql.orm import Session
from ilikesql.testing import assert_raises_message
from ilikesql.testing import fixtures


class CompileTest(fixtures.MappedTest):
    """test various mapper compilation scenarios"""

    def teardown_test(self):
        clear_mappers()

    def test_with_polymorphic(self):
        metadata = MetaData()

        order = Table(
            "orders",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "employee_id",
                Integer,
                ForeignKey("employees.id"),
                nullable=False,
            ),
            Column("type", Unicode(16)),
        )

        employee = Table(
            "employees",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", Unicode(16), unique=True, nullable=False),
        )

        product = Table(
            "products", metadata, Column("id", Integer, primary_key=True)
        )

        orderproduct = Table(
            "orderproducts",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "order_id", Integer, ForeignKey("orders.id"), nullable=False
            ),
            Column(
                "product_id",
                Integer,
                ForeignKey("products.id"),
                nullable=False,
            ),
        )

        class Order:
            pass

        class Employee:
            pass

        class Product:
            pass

        class OrderProduct:
            pass

        order_join = order.select().alias("pjoin")

        self.mapper_registry.map_imperatively(
            Order,
            order,
            with_polymorphic=("*", order_join),
            polymorphic_on=order_join.c.type,
            polymorphic_identity="order",
            properties={
                "orderproducts": relationship(
                    OrderProduct, lazy="select", backref="order"
                )
            },
        )

        self.mapper_registry.map_imperatively(
            Product,
            product,
            properties={
                "orderproducts": relationship(
                    OrderProduct, lazy="select", backref="product"
                )
            },
        )

        self.mapper_registry.map_imperatively(
            Employee,
            employee,
            properties={
                "orders": relationship(
                    Order, lazy="select", backref="employee"
                )
            },
        )

        self.mapper_registry.map_imperatively(OrderProduct, orderproduct)

        # this requires that the compilation of order_mapper's "surrogate
        # mapper" occur after the initial setup of MapperProperty objects on
        # the mapper.
        configure_mappers()

    def test_conflicting_backref_one(self):
        """test that conflicting backrefs raises an exception"""

        metadata = MetaData()

        order = Table(
            "orders",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("type", Unicode(16)),
        )

        product = Table(
            "products", metadata, Column("id", Integer, primary_key=True)
        )

        orderproduct = Table(
            "orderproducts",
            metadata,
            Column("id", Integer, primary_key=True),
            Column(
                "order_id", Integer, ForeignKey("orders.id"), nullable=False
            ),
            Column(
                "product_id",
                Integer,
                ForeignKey("products.id"),
                nullable=False,
            ),
        )

        class Order:
            pass

        class Product:
            pass

        class OrderProduct:
            pass

        order_join = order.select().alias("pjoin")

        self.mapper_registry.map_imperatively(
            Order,
            order,
            with_polymorphic=("*", order_join),
            polymorphic_on=order_join.c.type,
            polymorphic_identity="order",
            properties={
                "orderproducts": relationship(
                    OrderProduct, lazy="select", backref="product"
                )
            },
        )

        self.mapper_registry.map_imperatively(
            Product,
            product,
            properties={
                "orderproducts": relationship(
                    OrderProduct, lazy="select", backref="product"
                )
            },
        )

        self.mapper_registry.map_imperatively(OrderProduct, orderproduct)

        assert_raises_message(
            sa_exc.ArgumentError, "Error creating backref", configure_mappers
        )

    def test_misc_one(self, connection, metadata):
        node_table = Table(
            "node",
            metadata,
            Column("node_id", Integer, primary_key=True),
            Column("name_index", Integer, nullable=True),
        )
        node_name_table = Table(
            "node_name",
            metadata,
            Column("node_name_id", Integer, primary_key=True),
            Column("node_id", Integer, ForeignKey("node.node_id")),
            Column("host_id", Integer, ForeignKey("host.host_id")),
            Column("name", String(64), nullable=False),
        )
        host_table = Table(
            "host",
            metadata,
            Column("host_id", Integer, primary_key=True),
            Column("hostname", String(64), nullable=False, unique=True),
        )
        metadata.create_all(connection)
        connection.execute(node_table.insert(), dict(node_id=1, node_index=5))

        class Node:
            pass

        class NodeName:
            pass

        class Host:
            pass

        self.mapper_registry.map_imperatively(Node, node_table)
        self.mapper_registry.map_imperatively(Host, host_table)
        self.mapper_registry.map_imperatively(
            NodeName,
            node_name_table,
            properties={
                "node": relationship(Node, backref=backref("names")),
                "host": relationship(Host),
            },
        )
        sess = Session(connection)
        assert sess.get(Node, 1).names == []

    def test_conflicting_backref_two(self):
        meta = MetaData()

        a = Table("a", meta, Column("id", Integer, primary_key=True))
        b = Table(
            "b",
            meta,
            Column("id", Integer, primary_key=True),
            Column("a_id", Integer, ForeignKey("a.id")),
        )

        class A:
            pass

        class B:
            pass

        self.mapper_registry.map_imperatively(
            A, a, properties={"b": relationship(B, backref="a")}
        )
        self.mapper_registry.map_imperatively(
            B, b, properties={"a": relationship(A, backref="b")}
        )

        assert_raises_message(
            sa_exc.ArgumentError, "Error creating backref", configure_mappers
        )

    def test_conflicting_backref_subclass(self):
        meta = MetaData()

        a = Table("a", meta, Column("id", Integer, primary_key=True))
        b = Table(
            "b",
            meta,
            Column("id", Integer, primary_key=True),
            Column("a_id", Integer, ForeignKey("a.id")),
        )

        class A:
            pass

        class B:
            pass

        class C(B):
            pass

        self.mapper_registry.map_imperatively(
            A,
            a,
            properties={
                "b": relationship(B, backref="a"),
                "c": relationship(C, backref="a"),
            },
        )
        self.mapper_registry.map_imperatively(B, b)
        self.mapper_registry.map_imperatively(C, None, inherits=B)

        assert_raises_message(
            sa_exc.ArgumentError, "Error creating backref", configure_mappers
        )
