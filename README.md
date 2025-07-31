# Ontology-based Interoperability for Industrial Data

## Why this web site

The goal of releasing this document here is to provide guidance to industry users and the semantic data modelling community about 1) the vision for the ISO 23726 Ontology-based Interoperability (OBI) series and 2) a set of principles which resources will have to comply with in order to be considered `compliant' with IDO and the ISO 23726 series. The Industrial Data Ontology (IDO) is the upper ontology in the ISO 23726 series. [IDO](https://rds.posccaesar.org/ontology/lis14/) is currently inside the ISO process and due to be published as an ISO standard in 2026. 

These organisations[1] have been supporting work to develop a proposal for ISO TC184 SC4 for a document describing an Ontology-based Interoperability ecosystem for industrial ontologies. This document will be submitted to ISO in October 2025. Once inside the ISO process only members of the ISO TC184/SC4 WG26 commmittee and the liaison groups will have access to the draft standard and any associated digital artefacts. 

[1] PoscCaesar Association, Siemens, DNV, Grundfos, The University of Western Australia, Freelance Catalyst58, Cognite, Aker Solutions, Equinor & Standards Norway

## Developers of this version of the document

Lead developers: [Professor Melinda Hodkiewicz](https://www.linkedin.com/in/melinda-hodkiewicz-b6bbba7/)  & [Andreas Neumann}(https://www.linkedin.com/in/andreas-neumann-09b267160/) 

Development team: [Pål Rylandsholm](https://www.linkedin.com/in/prylandsholm/), [Maja Milicic Brandt](https://www.linkedin.com/in/majamilicicbrandt/), [Johan W Kluwer](https://www.linkedin.com/in/johanwkluwer/), [Caitlin Woods](https://www.linkedin.com/in/caitlin-woods/), [Dirk Walter](https://www.linkedin.com/in/dirk-walther/), [Inghild Kaarstad](https://www.linkedin.com/in/inghild-kaarstad-936734a/) 

## Introduction to the OBI Part 1 document

Machine-interpretable data are a key enabler of 1) industrial automation, and 2) the application of artificial intelligence to products, plants, processes, and services. However, organizational data are often stored in digital formats that use proprietary terms, definitions, and schemas. This lack of semantic interoperability means that data exchange frequently relies on manual interpretation or custom mappings. Documents such as engineering standards, procedures, spreadsheets, and reference data libraries are prone to misinterpretation when their semantics are not formally and explicitly defined.

A semantically explicit format is key to human and machine interoperability. An ontology is a structured set of terms, their interrelationships, and associated definitions, supported by formal logic to ensure that the intended meaning is unambiguous and machine-interpretable. The use of formal representation enables consistent preservation and exchange of meaning.

Ontologies are increasingly integrated into enterprise architecture, particularly within knowledge management layers. An example is shown in Figure 1. The Ontology-Based interoperability (OBI) ecosystem comprises artefacts managed by ISO 23726 WG26, external organizations, enterprises, as well as organizational stakeholders, processes, and capabilities.

Figure 1 — Example of enterprise architecture for OBI ontology-based interoperability

![Figure 1 — Example of enterprise architecture for OBI ontology-based interoperability](https://github.com/PCA-POSC-Caesar-Association/Public_ISO23726-1/blob/main/images/OBI_ecosystem.jpeg)


At the base of the Figure 1 is a level representing the data sources created by enterprises and stored in the data storage system layer. To organize, check, and integrate data from disparate source systems, organisations are incorporating a knowledge management layer into their enterprise architecture. An ontology-based knowledge management layer provides quality controlled, interoperable data for data products, analytics and AI used by data consumers within and across organisations. IDO is the upper ontology in the OBI ecosystem knowledge management layer. In addition to IDO the knowledge management layer includes enterprise ontologies and shared artefacts such as reference ontologies, ontology modelling patterns, templates, reference data libraries, data quality rules, SHACL shapes, and SPARQL queries. Above the knowledge management layer sits in an enterprise architecture for data products, data analytics and artificial intelligence models which are accessible to data consumers.

The W3C standards Web Ontology Language (OWL) and Resource Description Framework (RDF) are foundational standards for the Semantic Web and considered normative for ontologies in the Ontology based interoperability (OBI) standards. These standards enable machine -readable, semantically interoperable representations based on shared vocabularies and logical structures. The foundation for the OBI series is ISO 23726-3, the Industrial Data Ontology (IDO).

IDO specifies an abstract representation of the industrial data domain, including a high level of conceptual abstraction and associated modelling constraints. The semantic interpretation of a concept modelled according to an IDO-aligned artefact is explicitly defined. This enables consistent interpretation and automated reasoning by both humans and machines.

IDO is implemented as an OWL 2 upper ontology. OWL 2 DL ontologies are interpreted using the Direct Semantics. DL (description logics) are a family of languages used in artificial intelligence and Semantic Web technologies for logic-based knowledge representation and reasoning. Typical ontology reasoning tasks include: (1) consistency checking, (2) automated classification (i.e. inferring implicit subclass hierarchies), and (3) derivation of implicit facts. OWL DL reasoners are software systems that perform these reasoning tasks automatically. Such automated reasoning is essential for quality assurance, semantic consistency, and knowledge inference within ontologies.

## To contact us
A copy of the draft document will be uploaded to this site in early August 2025. Please note that edits may continue to be uploaded until the draft is submitted in October. Interested readers can subscribe to this Github by clicking the 'watching' option to receive notifications.

We shall also be keeping an eye on the Issues tab. If you have questions or comments about this document and/or its progress. Please post an issue.
