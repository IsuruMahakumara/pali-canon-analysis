// Create top-level categories 

CREATE (:Category {name: 'Sutta'}); 
CREATE (:Category {name: 'Abhidhamma'}); 
CREATE (:Category {name: 'Vinaya'}); 

// Create Sutta children 

MATCH (s:Sutta:Category {name: 'Sutta'}) 
CREATE (s)-[:HAS_CHILD]->(:Category {name: 'Dīghanikāya'}), 
(s)-[:HAS_CHILD]->(:Category {name: 'Majjhimanikaya'}), 
(s)-[:HAS_CHILD]->(:Category {name: 'Anguttaranikaya'}), 
(s)-[:HAS_CHILD]->(:Category {name: 'Samyuttanikaya'}),
(s)-[:HAS_CHILD]->(:Category {name: 'Khuddakanikaya'}); 


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