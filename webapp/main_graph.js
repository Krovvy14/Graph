function main_graph(){
	console.log("here");
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
	  console.log("row count from customize graph: "
		 + s.graph.edges().length);

   //table creation
   function createTable(){
	   var table = document.createElement("TABLE");
	   var rowCount = s.graph.nodes().length;
	   for (var i=0; i < s.graph.nodes().length; i++){
		   console.log("s: " + String(s.graph.nodes()[i].label));
	   }
	   for (var i = 0; i < rowCount; i++){
		   var row = table.insertRow(i);
		   for (var j = 0; j < 3; j++){
			   var cell = row.insertCell(j);
			   console.log("j: " + j);
			   cell.innerHTML = String(j);
		   }
		var dvTable = document.getElementById("right-margin");
		dvTable.innerHTML = "";
		dvTable.appendChild(table);
	}

		var x = createTable();
		s.refresh();
	};

   sigma.neo4j.cypher(
			endpoint,
			'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 100',
			s,
			customizeGraph
   );
}
