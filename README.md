# Environment Setup

To run all scripts you need to setup python environment, first you need to install `python3` and all its dependencies

Install `python3` and its dependencies

#### Windows
To install `python3` on windows go to the link
[Install Python on windows!](https://www.python.org/downloads/)

#### Ubuntu
By default python is installed on ubuntu, if not follow the link 
[Install Python on ubuntu!](https://www.python.org/downloads/source/)

#### Install Dependencies
After installing python on your machine install dependencies from `requirements.txt`


`pip install -r requirements.txt`


Once you install `python3` and all its dependcies, follow the Guru workflow guide.

#### Batch Execution
All python scripts can be executed through a sample batch file in `AllScripts.bat` by modifying the
ISSN and date range. This batch processing will also be useful for developing a front-end tool, as well as,
modifying the sequence as per need.


# Guru-workflow

To apply **centrality analysis** on the **Author Collaboration** and **Author Citation Networks**, a series of steps are required to create these networks using the Open Citation data which provide the Article Citation Network. All scripts were executed on Windows Server machine having **Quad-Core AMD Opteron(TM) Processor 6272** with **`128 GB RAM`** installed. It is interesting to note that only the initial processing of data requires heavy computation and memory, once. Later, the data is converted to a compressed binary format using libraries for processing large networks and thus can run on any standard laptop machine. Below we provide details of the workflow to create Scientific Networks for a specific journal. This was selected for two primary reasons. Firstly, we wanted to replicate a study on **SCIM** done using **WoS data**. Secondly, a generic 5/34query on CrossRef provided a huge amount of data and its analysis was outside the scope of this current
article. 

We aim to provide details of our extended analysis in an upcoming publication and not clutter this workflow with unnecessary details. Although this case study is limited to data of SCIM, we have made every effort to keep the process automated, such that applying the same script to other journals or set of journals, require minimum changes. 
Overview of the process is depicted in `Figure 1`, and further details about each of the following step are provided separately. Each step is distributed with three sub-steps for clarity and batch execution.

1. The **first step** is to download the Citation Index provided as COCI.
2. The **second step** is to download the CrossRef Data, for provided ISSN through CrossRef.
3. The **third step** is to fetch Ego Network from COCI data, for the DOIs of respective ISSN.
4. The **fourth step** is to merge these data to create different Scientific Network(s).
5. Finally, the **last step** is to apply the centrality analysis on these networks.

![Image of Pyramid](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure2.jpg)
`Figure 1.` Workflow to Identify Gurus of any Field. A pyramid shows the refinement of data at every
step. COCI contains approx. 625 M edges, which is refined to Ego Network for subset nodes fetched for
respective ISSN. Finally, the top of the pyramid shows the output in form of few nodes identified with
high centrality.

Relevant python scripts are explained and described below, for not only replication
of the current study, but also, reuse of this study for other ISSN or other network types for bibliometric
analyses.

### Fetching Citation Network

Details of the step are shown in `Figure 2.` Below we define the sub-steps to convert the COCI data to be
used in Python libraries for network processing. This step is computation and memory intensive but needs
to be performed once.

![Image of steps](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure3.jpg)
`Figure 2.` Step 1 of the workflow with details of creating the citation network. Sub-steps are applied
sequentially.

#### Download COCI Data 

Citation Index is manually downloaded from (OpenCitations, 2020). The 15 GB
Zip file extracts to 98 GB set of files. Loading this data in-memory resulted in memory-overflow, even
when using 128 GB RAM. Therefore, in the next step, we remove the columns other than citing and cited,
which are used to create the Article Citation Network.

#### Convert COCI Data to Edge List 
This step is needed to convert the COCI Data to an edge list format.
It is an easy to process format, with two nodes on each row signifying an edge. This format is supported
by SNAP (Leskovec and Sosicˇ, 2016), which is used for processing huge network data, such as COCI.
After this step Edge list file is approx 35 GB. `Edge_List.py` converts the COCI from comma-separated-values
(CSV) to space-separated-values having only citing and cited column. This is the only format supported
by SNAP. Some formatting corrections are also made for removing extra CR/LF and quotes since it
hampers the loading process of SNAP. `Edge_List.py` takes two arguments. First is the name of directory containing COCI data. Second is the name of CSV file to be generated as output. We have tried to load the same files with other libraries which are 
relatively more intuitive but not as powerful as SNAP (Leskovec and Sosicˇ, 2016). However, we later
discuss how this data can be used with other libraries and provide scripts to convert data to a format that
is supported by the majority of network processing libraries.

#### Save COCI as Binary
Loading 35 GB edge list in-memory using SNAP takes approx 5.5 hours. Since
the edge labels are DOI in the COCI data, therefore they are saved as strings. However, this slows down
further processing, so strings are converted to a hash file. There are two binary files generated when
loading the COCI data in SNAP. First is DOIDirected.graph file which contains the directed citation
network of COCI, with integer node labels. Second is DOIMapping.hash which maps the integer node
label to respective DOI. `SNAP_Binary.py` saves loaded graph as Binary files for further computations. `SNAP_Binary.py` takes four arguments. First is the name of CSV file that was generated in previous step. Second and third are the names of graph and hash files, respectively. Fourth is the location of files to be saved for further processing. Loading
binary file in-memory takes a few minutes as compared to a few hours for loading CSV data, with the
downside that additional columns of COCI are currently not being utilised. To keep things simple for
novice and non-technical user, DOIMapping.hash is simply a node list where node number corresponds
to its label (DOI), while the DOIDirected.graph is an edge list on node number. This is the part which
makes SNAP less intuitive but more powerful since computations are much faster when integer labels are
used but for human consumption, a mapping to string labels is also provided.

#### Fetching CrossRef metadata
Details of the step are shown in `Figure 3.` Below we define the sub-steps to fetch the citation metadata and
converting it to list of authors and DOIs. Although the following scripts only provide API string to fetch
data for a single journal, however, it is possible to fetch data with other filters and query using CrossRef.
Details are provided in its documentation, and the metadata downloaded via different filters is in a similar
format which makes this script reusable for a variety of tasks.

![ImageFetching CrossRef metadata](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure4.jpg)
`Figure 3.` Step 2 of the workflow with details of fetching metadata from CrossRef API. Sub-steps are
applied sequentially.

#### Create CrossRef API string
CrossRef limits a one time query to 1000 records for a single ISSN. For
queries with more than 1000 records, multiple API strings are needed which are created automatically by
the code in `JsonDump.py`. `JsonDump.py` takes four arguments. First two are the date range. Third is the ISSN of journal to fetch data. Fourth is the location of files to be saved for further processing which is generated by appending the date range and ISSN. Crossref Data of SCIM is fetched from Crossref API which contains total 1857
records. These records are fetched by two API requests to create JSON of SCIM Journal.

#### Fetch Author(s) list from Data
Once data is fetched from CrossRef as JSON, we populate the list of
authors. In `Extraction.py`, Authors are extracted from the previous created JSON dump from `JsonDump.py`. `Extraction.py` takes two arguments. First is the name of author DOI file. Second is the folder location. Both are appended with date range and ISSN. It
is important to note that we do not apply any technique for author name disambiguation and rely on
CrossRef to provide correct author names. Although this is problematic for further analysis, in the long
run, corrected data from a single source is much efficient than using different methods of cleaning.

#### Fetch DOI list from Data
Once data is fetched from CrossRef as JSON, we populate the list of DOI.
`DOIList.py` shows how DOIs are extracted from the previously created JSON dump from `JsonDump.py`. Although the
purpose of fetching DOI is also completed in `Extraction.py`, but it’s replica is created in `DOIList.py` to suggest
that analysis with only provided DOI list is also possible. `DOIList.py` takes two arguments. First is the name of CSV containing the DOIs. Second is the folder name containing the file. So the previous two sub-steps can be ignored if
analysing a specific journal is not needed. If the list of DOIs is fetched from an external source, then it
can be easily incorporated in this workflow.

#### Creating Ego Network
Details of the step are shown in `Figure 4`. Below we define the sub-steps to create Ego Network. This step
can be iterated zero or more times to grow the network as desired. This step is not used in Comparative
Analysis, however, we provide the details in this section to show that with Publicly accessible metadata it
is relatively easier to scale our approach. Further, this step justifies our approach of using SNAP over
other network processing libraries since the process of creating the Ego Network is not only fast but
intuitive to code, due to a variety of functions available in the extensive library documentation that makes
it easier to access the nodes in both directions of an edge. Also the integer labels makes the computation
faster than using string labels. This step was coded using python 2.7.

![Creating Ego Network](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure5.jpg)
`Figure 4.` Step 3 of the workflow with details of creating the Ego Network. Sub-steps are applied
sequentially, and may be iterated over to create next level of Ego Network.

#### Load COCI Binary to Fetch Subgraph
`EgoNetCode.py` shows the loading of the network and the
fetching of individual node labels. `EgoNetCode.py` takes five arguments. First two are the names of hash and graph file of COCI. Last three are the names of file, parent folder and sub folder of article citation network.  After loading a binary file of COCI a subset of the graph is fetched
with nodes linked at one level apart i.e. they either cite or are cited-by the existing articles. Processing a
subgraph from 625M edges takes a few minutes on a Core i5 laptop with 16 GB RAM. To confine the
discussion in this article related to the workflow we have omitted detailed analysis of time calculation, but
provide enough details so that this work is reused by other researchers.

#### Crossref Dump For EgoNet
`CrossrefDumpForEgoNet.py` shows the fetching of CrossRef data for all DOI of Article
Ego Network created in the previous step. `CrossrefDumpForEgoNet.py` takes the name of parent folder as single argument to save the details of all DOIs. This way first we download all data and then process it to
create the network. Depending on the size of the network and the number of Ego Network levels, as well
as, internet speed this process can take from a few hours to days to complete. Once a local copy of data is
available this delay can be reduced. Since we do not have access to complete dump of CrossRef, we could
not identify whether these same script can be reused but we assume that there would be few changes
required to access the data locally.

#### DOI and Author List Extraction
`DOIAUthorExtractionForEgoNet.py` shows the creation of the Ego Network for Authors. This
is similar to `Extraction.py` and `DOIList.py` for nodes of Journal data downloaded earlier. However, here we add the
connecting nodes fetched in subgraph above and download their respective Author details. `DOIAUthorExtractionForEgoNet.py` takes the name of parent folder as single argument to append the author details.

#### Creating Scientific Network(s)
Details of the step are shown in `Figure 5.` Once all the data is pre-processed, this step created different
types of network. We can also add Bibliographic coupling and Co-citation network within the list, but
they are ignored for two reasons. First, we did not find much evidence of centrality analysis on these
networks. Secondly, the processing time for creating these networks for a very large citation network is
relatively much longer than creating Author collaboration or Author Citation Network. These networks
are simply created by creating an edge list for authors who have collaborated or cited each other.

![Fig5](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure6.jpg)
`Figure 5.` Step 4 of the workflow with details of creating different Scientific Networks. Sub-steps are
applied sequentially.

#### Create Article Citation Network
Once the list of DOI is available, it is used to fetch subgraph of Article
Citation Network for these DOIs. `ArticleCit.py` shows details of fetching article citation network as a
subgraph from COCI. `ArticleCit.py` takes six arguments. First two are the names of hash and graph file of COCI. Third is the name of CSV containing DOIs. Fourth is the name of CSV to save network. Last two are the names of parent folder and sub folder to save network. Further, it saves the same graph as a binary file for further analysis. Also, the CSV
file can be used with any graph processing library (such as NetworkX) while binary file can be read using
SNAP.

#### Create Author Collaboration Network
Author collaboration is identified via a list of co-authors from
JSON Data fetched from CrossRef. Author Collaboration network is created as shown in `CollaborationNet.py`. `CollaborationNet.py` takes five arguments. First is the CSV to save network. Second is the CSV to get details of authors. Last three are the names of file, parent folder and sub folder to save network.
This refined data is further used for Comparative Analysis in the subsequent section. It is important to
note that the count of Authors at this sub-step may vary from next sub-step of creating Author Citation
Network since the list of co-authors in CrossRef is provided as a list of names and we do not include
further metadata about these authors.

#### Create Author Citation Network
Using the subgraph of Article Citation Network, respective edges are
made for Authors to create Author Citation Network, as shown `AuthorCit.py`. `AuthorCit.py` takes seven argument. First is the article citation network previously generated. Second is the name of file to save network. Third is the CSV to get details of authors. Subsequent three are the names of file, parent folder and sub folder to save network. Last is the node list hash file. All co-authors are linked to
use full counting method. In case method of partial counting is to be utilised then this script needs to
be modified. However, our workflow is not affected by the use of a partial or full counting method and
hence we have picked simpler one for brevity. In any case, this network shall supplement the analysis on
a collaboration network that was constructed in the previous step, as well as, Article Citation network that
is originally provided.

#### Centrality Analysis
Details of the step are shown in `Figure 6.` Below we define the sub-steps to apply different centrality
measures on the Scientific Networks. This is one of the common method employed in the bibliometric
analysis, however, other methods of SNA can also be applied at this step. Any tool or wrapper API may
restrict the functionality at this point, however, this work can be extended to use any functions in existing
network processing libraries. Since using tools is easier than the script, a future application of this study
could be about creating a front end tool for ease of use. Below we provide details about how the different
centrality measures applied by different studies discussed above can be done. Each of the measures is
separated in the different listing, along with loading and initialisation.

![Fig6](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figures/Figure7.jpg)
`Figure 6.` Step 5 of the workflow with details of centrality measures that are applied on different
Scientific Networks. Sub-steps may be applied as required, as there is no dependency within steps.

#### Applying centrality measures on Article citation network
The article citation network is a Directed Acyclic Graph (DAG). Most centrality analyses are not meaningful on DAG. Two measures are presented
in `ArticleCentrality.py`. `ArticleCentrality.py` takes the name of parent folder as single argument to save centrality scores. Degree Centrality provides highly cited articles. Finding authors of these articles is also possible. Influence definition in DAG is captured via the recursive definition of Katz Centrality.

#### Applying centrality measures on Author citation network
The author citation network is a cyclic graph. Three measures are presented in `AuthorCitCentr.py`, namely, Highly cited authors (degree centrality), Influential authors (Eigen centrality), Authors working in multiple domains (betweenness centrality). `AuthorCitCentr.py` takes the name of parent folder as single argument to save centrality scores.

#### Applying centrality measures on Author Collaboration network 
The author collaboration network is a cyclic graph and most centrality analyses are possible. Five measures are presented in `CollaborationCent.py`, namely, Highly collaborative authors (degree centrality), Influential collaborators (Eigen centrality), Authors working in multiple groups (betweenness centrality), Well knitted authors (closeness centrality), Solo authors (farness centrality). `CollaborationCent.py` takes the name of parent folder as single argument to save centrality scores.
