# Understanding LC BIBFRAME graphs

Consider and instance of Kafka's "The Trial": <https://id.loc.gov/resources/instances/1006621.html>

The data is available in many forms, including JSON-LD: <https://id.loc.gov/resources/instances/1006621.cbd.json>

A picture of this can be obtained through the <https://www.ldf.fi/service/rdf-grapher?rdf=https://id.loc.gov/resources/instances/1006621.cbd.rdf&from=xml&to=pdf> and there is copy locally <1006621_cbd_rdf.pdf>.

# What does the `.cbd` in the URL mean?

This is not a Concise Bounded Description (CBD) for an entity as defined by <https://www.w3.org/submissions/CBD/>. For example, the `bf:Instance` description in <> includes:

```
<http://id.loc.gov/resources/instances/1006621> a bf:Instance ;
  ...
  bf:instanceOf <http://id.loc.gov/resources/works/1006621> ;
  bf:issuance <http://id.loc.gov/vocabulary/issuance/mono> ;
  ...
```

which is what would be expected in a CBD, but then also includes informtation about the entities <http://id.loc.gov/resources/works/1006621> (the `bf:Work`) and <http://id.loc.gov/vocabulary/issuance/mono>:

```
<http://id.loc.gov/resources/works/1006621> a bf:Monograph,
        bf:Text,
        bf:Work ;
    bflc:aap "Kafka, Franz, 1883-1924. The trial" ;
    bflc:aap-normalized "kafkafranz18831924thetrial" ;
   ...

   <http://id.loc.gov/vocabulary/issuance/mono> a bf:Issuance ;
       rdfs:label "single unit" ;
       bf:code "mono" .
```

Neither of these additional descriptions are part of the CBD for the instance.

It seems that OCLC documentation suggests that the LC response is a CBD (<https://help.oclc.org/Metadata_Services/WorldShare_Collection_Manager/Data_sync_collections/Prepare_your_data/Structure_BIBFRAME_data>).

We can use Python's RDFLib to extract a CBD for the `bf:Instance` within this graph:

```
> python cbd.py

Number of statements in graph from 1006621.cbd.json is 224

Number of statements in CBD sub-graph for node http://id.loc.gov/resources/instances/1006621 is 65
@prefix bf: <http://id.loc.gov/ontologies/bibframe/> .
@prefix bflc: <http://id.loc.gov/ontologies/bflc/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix lclocal: <http://id.loc.gov/ontologies/lclocal/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://id.loc.gov/resources/instances/1006621> a bf:Instance ;
    bf:adminMetadata [ a bf:AdminMetadata ;
            bf:agent <http://id.loc.gov/vocabulary/organizations/dlcmrc> ;
            bf:date "2024-07-30T18:19:41.932016-04:00"^^xsd:dateTime ;
            bf:generationProcess <https://github.com/lcnetdev/marc2bibframe2/releases/tag/v2.7.0> ;
            bf:status <http://id.loc.gov/vocabulary/mstatus/c> ],
        [ a bf:AdminMetadata ;
            bflc:encodingLevel <http://id.loc.gov/vocabulary/menclvl/f> ;
            bf:descriptionConventions <http://id.loc.gov/vocabulary/descriptionConventions/aacr> ;
            bf:descriptionLevel <http://id.loc.gov/ontologies/bibframe-2-3-0/> ;
            bf:identifiedBy [ a bf:Local ;
                    bf:assigner <http://id.loc.gov/vocabulary/organizations/dlc> ;
                    rdf:value "1006621" ] ;
            lclocal:d906 "=906     $a 7 $b cbc $c orignew $d 1 $e ocip $f 19 $g y-gencatlg" ],
        [ a bf:AdminMetadata ;
            bf:agent <http://id.loc.gov/vocabulary/organizations/dlc> ;
            bf:date "1987-11-23"^^xsd:date ;
            bf:status <http://id.loc.gov/vocabulary/mstatus/n> ],
        [ a bf:AdminMetadata ;
            bf:date "1988-08-25T09:44:08"^^xsd:dateTime ;
            bf:descriptionModifier <http://id.loc.gov/vocabulary/organizations/dlc> ;
            bf:status <http://id.loc.gov/vocabulary/mstatus/c> ] ;
    bf:dimensions "21 cm" ;
    bf:editionStatement "Definitive ed." ;
    bf:extent [ a bf:Extent ;
            rdfs:label "281 p." ] ;
    bf:identifiedBy [ a bf:Lccn ;
            rdf:value "   87032345 " ],
        [ a bf:Isbn ;
            bf:acquisitionTerms "$5.95" ;
            bf:qualifier "pbk" ;
            rdf:value "0805208488" ] ;
    bf:instanceOf <http://id.loc.gov/resources/works/1006621> ;
    bf:issuance <http://id.loc.gov/vocabulary/issuance/mono> ;
    bf:media <http://id.loc.gov/vocabulary/mediaTypes/n> ;
    bf:note [ a bf:Note,
                <http://id.loc.gov/vocabulary/mnotetype/physical> ;
            rdfs:label "ill." ],
        [ a bf:Note ;
            rdfs:label "Translation of: Der Prozess" ] ;
    bf:provisionActivity [ a bf:ProvisionActivity,
                bf:Publication ;
            bflc:simpleAgent "Schocken Books" ;
            bflc:simpleDate "c1988" ;
            bflc:simplePlace "New York" ;
            bf:date "1988"^^<http://id.loc.gov/datatypes/edtf> ;
            bf:place <http://id.loc.gov/vocabulary/countries/nyu> ] ;
    bf:publicationStatement "New York: Schocken Books, c1988" ;
    bf:responsibilityStatement "Franz Kafka ; translated from the German by Willa and Edwin Muir ; revised, and with additional material translated by E.M. Butler ; with excerpts from Kafka's diaries ; drawings by Franz Kafka" ;
    bf:title [ a bf:Title ;
            bflc:nonSortNum "4" ;
            bf:mainTitle "The trial" ] ;
    dcterms:isPartOf <http://id.loc.gov/resources/instances> .
```

Note that while the CBD includes the statements referring to the related `bf:instanceOf` and `bf:issuance` entities, the descriptions of these entities are not included.
