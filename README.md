# Guru-workflow

To apply **centrality analysis** on the **Author Collaboration** and **Author Citation Networks**, a series of steps are required to create these networks using the Open Citation data which provide the Article Citation Network. All scripts were executed on Windows Server machine having **Quad-Core AMD Opteron(TM) Processor 6272** with **`128 GB RAM`** installed. It is interesting to note that only the initial processing of data requires heavy computation and memory, once. Later, the data is converted to a compressed binary format using libraries for processing large networks and thus can run on any standard laptop machine. Below we provide details of the workflow to create Scientific Networks for a specific journal. This was selected for two primary reasons. Firstly, we wanted to replicate a study on **SCIM** done using **WoS data**. Secondly, a generic 5/34query on CrossRef provided a huge amount of data and its analysis was outside the scope of this current
article. 

We aim to provide details of our extended analysis in an upcoming publication and not clutter this workflow with unnecessary details. Although this case study is limited to data of SCIM, we have made every effort to keep the process automated, such that applying the same script to other journals or set of journals, require minimum changes. 
Overview of the process is depicted in `Figure 1`, and further details about each of the following step are provided separately. Each step is distributed with three sub-steps for clarity and batch execution.

1. The first step is to download the Citation Index provided as COCI.
2. The second step is to download the CrossRef Data, for provided ISSN through CrossRef.
3. The third step is to fetch Ego Network from COCI data, for the DOIs of respective ISSN.
4. The fourth step is to merge these data to create different Scientific Network(s).
5. Finally, the last step is to apply the centrality analysis on these networks.

![Image of Pyramid](https://github.com/bilal-dsu/Guru-workflow/blob/main/index.jpg)
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

![Image of steps](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figure2.jpg)
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
After this step Edge list file is approx 35 GB. `Script 1` converts the COCI from comma-separated-values
(CSV) to space-separated-values having only citing and cited column. This is the only format supported
by SNAP. Some formatting corrections are also made for removing extra CR/LF and quotes since it
hampers the loading process of SNAP. We have tried to load the same files with other libraries which are
relatively more intuitive but not as powerful as SNAP (Leskovec and Sosicˇ, 2016). However, we later
discuss how this data can be used with other libraries and provide scripts to convert data to a format that
is supported by the majority of network processing libraries.

#### Save COCI as Binary
Loading 35 GB edge list in-memory using SNAP takes approx 5.5 hours. Since
the edge labels are DOI in the COCI data, therefore they are saved as strings. However, this slows down
further processing, so strings are converted to a hash file. There are two binary files generated when
loading the COCI data in SNAP. First is DOIDirected.graph file which contains the directed citation
network of COCI, with integer node labels. Second is DOIMapping.hash which maps the integer node
label to respective DOI. `Script 2` saves loaded graph as Binary files for further computations. Loading
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

![ImageFetching CrossRef metadata](https://github.com/bilal-dsu/Guru-workflow/blob/main/Figure3.jpg)
`Figure 3.` Step 2 of the workflow with details of fetching metadata from CrossRef API. Sub-steps are
applied sequentially.

#### Create CrossRef API string
CrossRef limits a one time query to 1000 records for a single ISSN. For
queries with more than 1000 records, multiple API strings are needed which are created automatically by
the code in `script 3.` Crossref Data of SCIM is fetched from Crossref API which contains total 1857
records. These records are fetched by two API requests to create JSON of SCIM Journal.

#### Fetch Author(s) list from Data
Once data is fetched from CrossRef as JSON, we populate the list of
authors. In `script 4`, Authors are extracted from the previous created JSON dump from `script 3`. It
is important to note that we do not apply any technique for author name disambiguation and rely on
CrossRef to provide correct author names. Although this is problematic for further analysis, in the long
run, corrected data from a single source is much efficient than using different methods of cleaning.
