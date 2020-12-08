# Wrapper service

DBC har lavet en wrapper service der:

* sender en søgning videre mod Watson Discovery

* laver clustering: resultaterne opdeles i tre klasser baseret på metadata

* tilføjer Gale-metadata

Eksempel (hvor `key` er en token der udleveres af DBC):
 
```
curl -X POST https://vk-cluster.ai.dbc.dk/query -d '{"query": "trump", "key": "xxxxxxxx"}'
```

Dette vil give json retur, svarende til Watson Discoverys API, men hvor der for hvert resultat i `results` under `metadata` er tilføjet:

* "cluster_id" som angiver hvilket cluster resultatet tilhører.

* `gale` som indeholder:

  * `gale-collection` der angiver hvilken Gale-collection dokumentet kommer fra

  * `gale-fake-level` der er en int 0-99 der kan bruges til at simulere niveau (fx folkeskole/gymnasium)
  
  * `gale-fake-waiting` der er en int 0-99 der kan bruges til at simulere hvor lang tid der går før materialet kan leveres

Eksempel:
```
...
           "title" : "Donald John Trump",
            "gale" : {
               "gale-fake-level" : 88,
               "gale-collection" : "Student",
               "gale-fake-waiting" : 41
            },
            "docid" : "EJ1667000175",
           "cluster_id" : 0
 ...
 ```
 
# Similar endpoint

Der er implementeret endnu et endpoint oven på Watson Discovery query, som finder andre dokumenter der ligner det/de givne dokument(er).

Endpointet tager en komma-separeret liste (uden mellemrum) af Watson Discovery document-id'er og returnere et output som svarer til outputet fra query-endpointet.

Eksempel (hvor `key` er en token der udleveres af DBC):
 
```
curl -X POST https://vk-cluster.ai.dbc.dk/similar -d '{"similar-document-ids": "127517a4-9111-49a3-ac6e-f70848cbfec9", "key": "xxxxxxxx"}'
```

Der kan optionelt gives en parameter `similar-fields` med som gives til Watson Discovery similar.fields. Dette er en komma-separeret liste af felter (uden 
mellemrum).

Eksempel (hvor `key` er en token der udleveres af DBC):

```
curl -X POST https://vk-cluster.ai.dbc.dk/similar -d '{"similar-document-ids": "127517a4-9111-49a3-ac6e-f70848cbfec9", "similar-fields": "text,title", "key": "xxxxxxxx"}'
```
Similar fields har næppe nogen stor praktisk betydning da `text` er hele artiklens tekst og `title` indeholder 'no title'. Dokumentets title findes i `metadata.title`.

Dokument-id'er findes i `id` feltet pr resultat.

# Data

Dokumenterne der er lagt i Discovery er taget fra Gale og udvalgt udfra størrelse, dvs. kun dokumenter over en vis størrelse er lagt ind (for at systemet har tekst at arbejde på).

Dokumenterne er taget fra følgende Gale collections ("used" er det antal der er lagt ind i Discovery):

|*collection*|*total*|*used*|*used percentage*|
| --- | --- | --- | --- |
|Biography|763176|77779|10.2%|
|Science|66703|16124|24.2%|
|Student|161841|45451|28.1%|
|GlobalIssues|107199|12040|11.2%|


# Watson Discovery

Dette er kode til indlæsning af dokumenter i Watson Discovery (se src).

Processen er:

* dokument behandles med Watson NLU for at få concepts, entities og keywords.

* dokument og metadata fra Watson NLU indlægges i Watson Discovery

Herefter kan dokumenter fremsøges ved brug af Watson Discovery's API.



