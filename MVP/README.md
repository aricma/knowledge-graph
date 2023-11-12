# MVP

This document details how our Minimum Viable Product (MVP) functions, focusing on the processes for adding files and querying stored data. It includes flowcharts to illustrate how data moves through the different parts of our system, providing a clear understanding of the MVP's business logic. 

## Add File
```mermaid
flowchart TD
    client -- send file to the server --> endpoint
    endpoint -- store the original blobs --> file_storage
    endpoint --> file_loader -- turn blobs into plain text --> text_file_reader
    text_file_reader -- split the file into logical chunks --> file_splitter
    
%%    text_file_reader -- load the file into plain text --> file_loader
    file_splitter -- store the chunks --> chunk_storage
    chunk_storage -- create and store embeddings to the chunks --> vector_db
    vector_db -- return the original file ids --> client
```

## Get File


## Query
```mermaid
flowchart TD
    client -- ask for the nearest data points --> vector_db
    vector_db -- get the chunks for the found matches --> chunk_storage
    chunk_storage -- get the original files for the chunks --> file_storage
    file_storage -- format and return the query results --> client 
```
