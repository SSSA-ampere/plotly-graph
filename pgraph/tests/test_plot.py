import pytest
import networkx as nx
import pgraph as pg


@pytest.fixture(scope="function")
def G():
    G = nx.random_geometric_graph(100, 0.125)
    nx.set_node_attributes(G, 3, "prop")

    return G


def test_plot_graph(G):

    pg.plot_graph(G)

    assert True


def test_plot_graph_fixed_size_color(G):

    pg.plot_graph(G, sizing_method="static", color_method="#ffffff")

    assert True


def test_plot_graph_property(G):

    pg.plot_graph(G, sizing_method="prop", color_method="prop")

    assert True