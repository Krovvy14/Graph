#################################################
#ingester.py									#
#################################################
#! /usr/bin/python
from neo4j.v1 import GraphDatabase, basic_auth


def create_database(infile):
	driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password1!"))
	session = driver.session()

	#cypher query to create unique source MAC address nodes
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`eth.src` IS NOT NULL MERGE (n:Node {eth: row.`eth.src`}) ON CREATE SET n.eth=row.`eth.src`")
	#cypher query to create unique source IP address nodes
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "'AS row FIELDTERMINATOR ';' WITH row WHERE row.`ip.src` IS NOT NULL MERGE (n:IP {ip: row.`ip.src`}) ON CREATE SET n.ip=row.`ip.src`") 
	#cypher query to create unique destination MAC address nodes
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`eth.dst` IS NOT NULL MERGE (n:Node {eth: row.`eth.dst`}) ON CREATE SET n.eth=row.`eth.dst`")
	#cypher query to create unique destination IP address nodes
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`ip.dst` IS NOT NULL MERGE (n:IP {ip: row.`ip.dst`}) ON CREATE SET n.ip=row.`ip.dst`")
	#cypher query to create relationship between source MAC address and source IP address in the PCAP file
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`eth.src` IS NOT NULL AND row.`ip.src` IS NOT NULL MATCH (n:Node) MATCH (m:IP) WHERE n.eth=row.`eth.src` AND m.ip=row.`ip.src` MERGE (m)-[:HAS_MAC]->(n)")
	#cypher query to create relationship between destination MAC address and destination IP address in PCAP file
	session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`eth.src` IS NOT NULL AND row.`ip.src` IS NOT NULL MATCH (n:Node) MATCH (m:IP) WHERE n.eth=row.`eth.dst` AND m.ip=row.`ip.dst` MERGE (m)-[:HAS_MAC]->(n)")
	#cypher query to draw relationship between source and destination nodes in the PCAP file
        session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM 'http://localhost:8080/" + infile + "' AS row FIELDTERMINATOR ';' WITH row WHERE row.`eth.src` IS NOT NULL AND row.`eth.dst` IS NOT NULL MATCH (n:Node) WHERE n.eth=row.`eth.src` MATCH (m:Node) WHERE m.eth=row.`eth.dst` CREATE (n)-[:TALKS_TO {protocol: row.`_ws.col.Protocol`, info: row.`_ws.col.Info`, data: row.`data`, length: row.`frame.len`}]->(m)")
	
	session.close()

