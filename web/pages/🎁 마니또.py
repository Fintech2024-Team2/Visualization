import pandas as pd
import streamlit as st
from pyvis.network import Network
from streamlit.components.v1 import html

# Function to create the network graph
def create_network_graph():
    df = pd.read_csv('/Users/chaewon/Desktop/manito.csv')
    net = Network(
        notebook=False,   # Set to False for Streamlit compatibility
        directed=True,    # Directed graph
        height="800px",   # Adjust height as needed
        width="100%"      # Fill the entire width
    )
    net.barnes_hut(gravity=-30000, central_gravity=0.3, spring_length=100, spring_strength=0.01, damping=0.09, overlap=0)
    
    sources = df['from']
    targets = df['to']
    weights = df['power']
    
    edge_data = zip(sources, targets, weights)
    
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        net.add_node(src, src, title=src, size=25)
        net.add_node(dst, dst, title=dst, size=25)
        net.add_edge(src, dst, value=w, title=w, arrows="to")

    # Customize edge colors based on weight values
    for n in net.edges:
        if n["value"] == '음료':
            n['color'] = 'blue'
        elif n["value"] == '과자':
            n['color'] = 'green'
        elif n["value"] == '응원':
            n['color'] = 'red'
        else:
            n['color'] = 'black'
    
    net.show_buttons(filter_=['physics'])
    return net

# Streamlit app
def show():
    st.title("마니또")
    st.write("당신의 마니또를 검색하세요!")
    
    # Create and display the network graph
    net = create_network_graph()
    net.save_graph('pyvis_net_graph.html')
    
    # Embed the graph in the Streamlit app
    html_file = open('pyvis_net_graph.html', 'r', encoding='utf-8')
    source_code = html_file.read()
    html_file.close()
    html(source_code, height=800)

if __name__ == '__main__':
    show()
