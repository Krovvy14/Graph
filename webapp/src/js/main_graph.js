var endpoint = {
				url: 'http://localhost:7474',
				user: 'neo4j',
				password: 'password1!'
			},
            graph = {nodes: [], edges: []};
			s = new sigma({graph: graph, container: 'container'});

			var dragListener = sigma.plugins.dragNodes(s, s.renderers[0]);

            s.bind('overNode clickNode', function(e){
                console.log(e.data.node.label);
            });

 function customizeGraph(s){
    s.graph.nodes().forEach(function(n){
               n.label=n.neo4j_data;
               console.log(n.label);
               });
               s.refresh();
    };

sigma.neo4j.cypher(
	endpoint,
	'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100',
	s,
    customizeGraph
);