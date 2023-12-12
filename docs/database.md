# Database Guide

## Document Collections

The History Lab's database organizes its various texts under the broader collections they were originally a part of. Here is a list of the various accessible collections that have been digitized and can be accessed through the API:

| Collection Code | Collection Name | Document Count |
| --------------- | --------------- | -------------- |
| frus | Foreign Relations of the United States | 209,046 |
| cia | Records from the CIA Freedom of Information Act Reading Room | 935,716 |
| clinton | Hillary Clinton Emails | 54,149 |
| pdb | President's Daily Briefs | 5,011 |
| cfpf | Central Foreign Policy Files | 3,214,293 |
| kissinger | Henry Kissinger Telephone Conversations | 4,552 |
| nato | NATO Digital Archives | 46,002 |

This information can also be viewed directly through the API using the `list_collections()` function.

## Document Fields

Each individual data point in the History Lab's database represents a single text, and the fields in each data row represent different pieces of information about each text that can be extracted by users through the API. Here is a list of some of the common fields:

| Field Name | Field Description |
| ---------- | ----------------- |
| authored | Date and time stamp of when the document was authored |
| body | The full text body of the document |
| countries | A list of all the countries mentioned in the document |
| persons | A list of all the persons mentioned in the document |
| persons_id | Lists the unique IDs for all the persons that appear in the document |
| topics | A list of all the topics mentioned in the document |
| title | The text title of the document |
| doc_id | The document's unique ID, also contains information on which collection the document belongs to |

