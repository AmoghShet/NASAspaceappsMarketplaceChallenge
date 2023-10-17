# NASAspaceappsOpenMarketPlaceSol
The following is our solution to the open marketplace problem from the NASAspaceapps challenge 2023

# Uses (prerequisites):
1) Python
2) Sunbird-RC

# Instructions:

1) Up the RC service by going into the back-end folder and running the following command: "docker-compose up -d"
2) Run the python script (with your API key in the code) to get your bot running 

# High-Level Summary:
In the current world, with an abundancy of fake resumes & certificates/credentials, there exists 2 problems: 1) The genuine profiles get drowned out in a sea of fakes 2) The onus of weeding through the hundreds of profiles falls on the project providers This problem arises due to: 1) Most profiles/resumes being copied from a common template (all resumes/profiles are homogenized). This problem is only an exasperated by the fact that: 2) Most fake certificates, and achievements of skill, look the same as the genuine ones (no credibility) Our solution aims to solve this issue by introducing a system that automatically signs and ensures every entry, every certificate issued on the database is digitally signed and stored in a secure registry, while making this open source and interoperable with nearly any data format/schema (via the use of Sunbird-RC)

# Project Summary:
As mentioned, our solution aims to solve this issue by introducing a system that automatically signs and ensures every entry, every certificate issued on the database is digitally signed and stored in a secure registry, while making this open source and interoperable with nearly any data format/schema (via the use of Sunbird-RC)


Sunbird-RC (https://docs.sunbirdrc.dev/learn/readme) is an Indian DPG Registry & Credentials framework by Sunbird/Ek Step. Based on schemas designed by programmers via the JSON format, the framework creates & sets up a registry+credentials system with the appropriate REST APIs. All transactions with these APIs are via the JSON file format. In our implementation, we've created 4 different schemas: Seeker, Provider, Endorsement & Project. These tables are interlinked, and each digitally signed in the RSA cryptographic format (but modifiable to work with other cryptographic algorithms) , however these fields can be easily changed, and registries populated from data from external NASA repos via APIs. Thus:

1) Each certificate issued with the RC system can easily be validated and verified (as demonstrated by CoWIN, which runs on Sunbird RC).

2) As profiles now only contain genuine credentials, they hold lot more weight. The minimal profile design also ensure to make each resume that cuts the crap out


The front end telegram we've thrown together isn't the main product, but the back-end. The front end is there to demonstrate how this system can be used in any format or system, as long as they can call and receive JSON objects via REST APIs
