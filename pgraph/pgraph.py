import plotly.graph_objects as go
import networkx as nx


def plot_graph(
    G,
    title="Graph",
    sizing_method="degree",
    color_method="degree",
    titlefont_size=16,
    showlegend=False,
    annotation_text="",
    colorbar_title="",
):
    """
    Plots a Graph using Plotly.
    
    Parameters
    ----------
    G : nx.Graph
        Network Graph

    title : str, optional
        Title of the graph, by default "Graph"

    sizing_method : {'degree', 'static'} or a node property, optional
        How to size the nodes., by default "degree"

            degree: The larger the degree, the larger the node.

            static: All nodes are the same size.

            node property: A property field of the node.

    color_method : {'degree'}, hex color code, node property, optional
        How to color the node., by default "degree"

            degree: Color the nodes based on their degree.

            hex color code: Hex color code.

            node property: A property field of the node.

    titlefont_size : int, optional
        Font size of the title, by default 16

    showlegend : bool, optional
        True to show legend, by default False

    annotation_text : str, optional
        Graph annotation text, by default ""

    colorbar_title : str, optional
        Color bar axis title, by default ""
    
    Returns
    -------
    Plotly Figure
        Plotly figure of the graph
    """

    node_trace, edge_trace = _generate_scatter_trace(
        G,
        sizing_method=sizing_method,
        color_method=color_method,
        colorbar_title=colorbar_title,
    )

    fig = _generate_figure(
        node_trace,
        edge_trace,
        title=title,
        titlefont_size=titlefont_size,
        showlegend=showlegend,
        annotation_text=annotation_text,
    )

    return fig


def _generate_scatter_trace(G, sizing_method, color_method, colorbar_title):

    edge_x = []
    edge_y = []
    node_x = []
    node_y = []
    node_size = []
    color = []

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)

        if sizing_method == "degree":
            node_size.append(G.degree(node) * 2)
        elif sizing_method == "static":
            node_size.append(12)
        else:
            node_size.append(G.nodes[node][sizing_method])

        if color_method == "degree":
            color.append(G.degree(node))
        else:
            # Look for the property, otherwise look for a color code
            # If none exist, throw an error
            if color_method in G.nodes[node]:
                color.append(G.nodes[node][color_method])
            else:
                color.append(color_method)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            reversescale=True,
            color=color,
            size=node_size,
            colorbar=dict(
                thickness=15, title=colorbar_title, xanchor="left", titleside="right"
            ),
            line_width=2,
        ),
    )

    return node_trace, edge_trace


def _generate_figure(
    node_trace, edge_trace, title, titlefont_size, showlegend, annotation_text
):

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont_size=titlefont_size,
            showlegend=showlegend,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text=annotation_text,
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig