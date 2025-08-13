# Avoiding duplication

Section 6 of the https://pca-posc-caesar-association.github.io/Public_ISO23726-1/latest/ lists the principles for ontology artefacts to be compliant with OBI.

## Clauses from Section 6

Clause 6.4 Axiomisation

Resources in an OBI series ontology should be axiomised to constrain the meaning of that resource by specifying rules, properties and relationships it shall satisfy in order **to make the resource semantically distinct from all the other resources.** 

**Constraints should define criteria for an individual's membership in classes, for being related by object or data property, and for the purpose of any individual.**

Clause 6.5 Annotation

Ontology models should be documented with metadata (3.4.3) described in Clause 8.

Other annotations can be included but these are as an addition to the ones listed in Clause 8 and should be governed by a documented process.
Classes and properties in an ontology should be documented with metadata listed in Clause 9.

## Clauses from Section 8

8.3 Sub-directory structure

Reference ontologies will have the following URL structure http://rds.posccaesar.org/ontology/XXX/ont/core

EXAMPLE 1
For the Schedule Data Ontology (SDO) the following URL is proposed: http://rds.posccaesar.org/ontology/sdo/ont/core

SWRL Rules, SHACL shapes and property chains shall be in dedicated directories under the ontology with which they are associated.

EXAMPLE 2
1. https://rds.posccaesar.org/ontology/lis14/ont/core/swrl/ 
2. https://rds.posccaesar.org/ontology/lis14/ont/core/shacl/ 
3. https://rds.posccaesar.org/ontology/lis14/ont/core/propertychain/

8.5 Class names

Class name in the IRI (3.4.2) and the annotation label without language tag shall be a noun group in singular, given in Pascal Case (also known as Upper Camel Case), each word capitalized, and no separation or punctuation between words. Class names should not use numeric identifiers for classes. No acronyms should be used except those in the dictionary, such as RADAR.

EXAMPLE

The class physical object is written as PhysicalObject with an example IRI (3.4.2) as follows.
1. http://rds.posccaesar.org/ontology/lis14/rdl/PhysicalObject

## What does this mean in practice?

In practice all classes, object and data properties in any ontology managed by the PCA maintenance agency and considered part of the ISO 23726 series MUST be stored in the rdl folder available at http://rds.posccaesar.org/ontology/lis14/rdl/ and NOT in the home ontology address.

For example the lis:Information class in `ise:Schedule subClassOf lis:InformationObject' has the following iri:

lis:InformationObject

http://rds.posccaesar.org/ontology/lis14/rdl/InformationObject and NOT 

http://rds.posccaesar.org/ontology/lis14/ont/core/InformationObject 

The IDO core ontology has its own iri http://rds.posccaesar.org/ontology/lis14/ont/core/ but this is not used for concepts in the ontology, just for the ontology itself.

All concepts in lis14 are stored in the rdl folder. 

Advantages: 

This practice stops duplication of concepts. Only one definition of each concept exists. 

Disadvantages:

Care needs to be taken with how concepts are defined as they will be used by others in the community when ontologies are imported.

## What happens if you don't do this?

This is an example from work on a reference ontology for an industrial  business vocabulary ido-ibv aligned to ido that is being explored. The ido-ibv ontology imports lis14 (IDO core), maintenance procedure ontology, and ido-maintenance. 

This results in the following namespaces for concepts

All concepts in lis14 are in /lis14/rdl (not in lis14/ont)

Taking Qualified Maintenance Person as an example

Concepts from the ido-maintenance are in: 

http://www.semanticweb.org/ontology/ido-maintenance/ont/core/QualifiedMaintenancePerson

Concepts from the maintenance procedure ontology are in:

http://spec.equonto.org/ontology/maintenance-procedure/static-procedure-ontology#QualifiedPerson

Concepts from the ido-ibv ontology are in: 

http://www.semanticweb.org/ontology/ido-ibv/ont/core/QualifiedPerson

When these are opened up in Protege we can see that there are 3 definitions and each refer to classes and object properties with different iri's across the set. 

![protegesnip](person_iri.JPG "Example from Protege for multiple versions with different namespaces and references to concepts with different namespaces")

## How does this help?


If all the concepts are in rdl folders then testing for duplication and overlap is much easier. 

Also instead of creating a new class in the above example the developer should have created a new rdl when the ido-ibv ontology was set up. Only new concepts should be stored there. Existing concepts that are fit for purpose should be reused either through ontology imports or by reuse with appropriate attribution. 



