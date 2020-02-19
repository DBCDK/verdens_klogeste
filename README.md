# Watson Discovery

Dette er kode til indlæsning af dokumenter i Watson Discovery (se src).

Processen er:

* dokument behandles med Watson NLU for at få concepts, entities og keywords.

* dokument og metadata fra Watson NLU indlægges i Watson Discovery

Herefter kan dokumenter fremsøges ved brug af Watson Discovery's API.

# Eksempler

Vi har valgt 1000 populære Wikipedia-artikler om personer som eksempler (se data).

Herefter har vi lavet et antal søgninger (se examples, søgningen svarer til filnavnet), hvor man kan se den rå response (*.json) og en parset version med hits og de første fem entities, concepts, keywords og categories (*.md).




