![aricma Knowledge Graph wallpaper](documentation/aricma-knowledge-graph-wallpaper.png)

# The aricma Knowledge Graph

The aricma Knowledge Graph is an innovative data management solution designed to address the challenges of changing file storage methods, data search and retrieval, featuring a flexible storage structure, and intelligent indexing.

## Index
1. [About The Problem](documentation/about-the-problem.md): Overview of the challenges related to data storage and retrieval.
2. [Our Solution Finding Strategy](documentation/our-solution-strategy.md): Explanation of the strategic approach to discovering solutions.
3. [Possible User Stories](documentation/possible-user-stories.md): User stories outlining various functionalities and requirements.

```mermaid
flowchart LR
    subgraph clients 
        web
        mobile
        cli
    end
    subgraph business logic 
        add-data
    end
    subgraph data storage 
        S3
        RDS
        vectorDB
    end
    mobile --> add-data
    add-data -- store the file for long term --> S3
    add-data -- store the token with related file path --> RDS
    add-data -- store vector for each token --> vectorDB
```

```mermaid
flowchart LR
    subgraph clients 
        web
        mobile
        cli
    end
    subgraph business logic 
        get-data
    end
    subgraph data storage 
        S3
        RDS
        vectorDB
    end
    web --> get-data

    get-data -- get all tokens near the query vector --> vectorDB
    get-data -- get file paths for each tokens --> RDS
    get-data -- get all files --> S3
```
