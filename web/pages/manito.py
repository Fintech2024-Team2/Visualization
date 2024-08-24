import pandas as pd
import streamlit as st
from pyvis.network import Network
import networkx as nx
from streamlit.components.v1 import html

# Function to create the network graph
df = pd.read_csv('/Users/chaewon/Desktop/manito.csv')
def create_network_graph():
    df = pd.read_csv('/Users/chaewon/Desktop/manito.csv')
    net = Network(
        notebook=False,   # Set to False for Streamlit compatibility
        directed=True,    # Directed graph
        height="800px",   # Adjust height as needed
        width="100%"      # Fill the entire width
    )
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=300, spring_strength=0.001, damping=0.09, overlap=0)
    
    sources = df['from']
    targets = df['to']
    weights = df['power']
    
    edge_data = zip(sources, targets, weights)
    
    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        net.add_node(src, src, title=src, size=20)
        net.add_node(dst, dst, title=dst, size=20)
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
    
    # Load the graph into a NetworkX graph for searching
    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
    
    # Search functionality
    search_query = st.text_input('마니또 검색')
    if search_query:
        search_results = [node for node in G.nodes if search_query in node]
        if search_results:
            st.subheader('검색 결과:')
            for result in search_results:
                st.write(result)
        else:
            st.write('검색 결과가 없습니다.')
    
    # Additional content (optional)
    st.write("마니또 데이터프레임도 만들어야 해요")
    
if __name__ == '__main__':
    show()
