// Create top-level categories 

CREATE (:Category {name: 'Sutta'}); 
CREATE (:Category {name: 'Abhidhamma'}); 
CREATE (:Category {name: 'Vinaya'}); 

// Create Sutta children with indempotent merge

MATCH (s:Sutta:Category {name: 'Sutta'})

MERGE (d:Category {name: 'Dīghanikāya'})
MERGE (m:Category {name: 'Majjhimanikaya'})
MERGE (a:Category {name: 'Anguttaranikaya'})
MERGE (sy:Category {name: 'Samyuttanikaya'})
MERGE (k:Category {name: 'Khuddakanikaya'})

MERGE (s)-[:HAS_CHILD]->(d)
MERGE (s)-[:HAS_CHILD]->(m)
MERGE (s)-[:HAS_CHILD]->(a)
MERGE (s)-[:HAS_CHILD]->(sy)
MERGE (s)-[:HAS_CHILD]->(k);



// Create Abhidhamma children 
MATCH (a:Category {name: 'Abhidhamma'}) 
CREATE (a)-[:HAS_CHILD]->(:Category {name: 'Dhammasangani'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Vibhanga'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Dhatukatha'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Kathavatthu'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Puggalapannatti'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Yamaka'}), 
(a)-[:HAS_CHILD]->(:Category {name: 'Patthana'}); 


//Create Vinaya children (generic) 
MATCH (v:Category {name: 'Vinaya'}) 
CREATE (v)-[:HAS_CHILD]->(:Category {name: 'Parajikapali'}), 
(v)-[:HAS_CHILD]->(:Category {name: 'Pacittiyapali'}), 
(v)-[:HAS_CHILD]->(:Category {name: 'Mahavaggapali'}), 
(v)-[:HAS_CHILD]->(:Category {name: 'Cullavaggapali'}), 
(v)-[:HAS_CHILD]->(:Category {name: 'Parivarapali'});