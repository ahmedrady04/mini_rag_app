# mini_rag 

this progect is minmal implemeantaion of the rag modele for qustion answering 

## requirments 
 
python=3.8 or later 

### install python with miniconda 

1) download and install miniconda from [here](site)
2) create enviroment using the following command:
```bash
$ conda create -n mini_rag python=3.8
```
3) Activate the enviroment:
```bach
$ conda activate mini_rag 
```
### (Optional) Setup you command line interface for better readability
```bash
export PS1="\[\033[01;32m\]\u@\h: \w\n\[\033[00m\]\$"
```
## INSTALLATION

### INSTALL REQUIRED PACHAGE 

```bash
$  pip install -r requirements.
```
### setup the enviroment varibles

```bash
$ cp .env.example .env
```
set your enviroment varible in the ".env" file .like 'OPENAI_API_KEY' value.

## Run the Fastapi server 
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
## POSTMAN COLLECTION 

Download the POSTMAN COLECTION FROM[/Users/a1/mini_rag_app/assets/mini-rag-app.postman_collection.json](/Users/a1/mini_rag_app/assets/mini-rag-app.postman_collection.json)