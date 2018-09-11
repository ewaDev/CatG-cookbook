# CatG-cookbook

Scripts in this thesis were used to achive 2 things:

1. Compare the performance of API vs Web scraping for the KEGG databases:
  * blast_result_format.py was used to format old thesis data depending on requirements.
  * agilent text data / final_blast_Table was used to retrieve primary acession assigned to the probes
  * getWebsiteInfoPartial.py was used to select the link and then scrape data from the KEGG result page
  * keggAPI.py was used to select the link call the KEGG API
  * beautifulSoup.py was used to retrieve SiganlP data based on the results of the KEGG (either scrape of api )
  * result formatting scripts are not included in here


2. Creating an information matching tool (CatG) which would map the microarray file with the relevant potencial Ecs gene (old thesis data )
and retrieved information on the potencial ECs gene - SignalP.
  * dataProcess.py - script which matches files together
  * CatG.py - CatG GUI script
  * setup.py - script used to convert CatG.py into an exe

P.S This project used phantomJS which is no longer mentained.
