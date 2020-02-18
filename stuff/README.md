Setup env xpdev-p01:

```
cd ~damkjaer/git/gitlab.dbc.dk/ai/verdens_klogeste/
. env/bin/activate
. watson.sh
```

Then setup query:
```
export Q=filibuster
python ~/GIT/verdens_klogeste/src/verdens_klogeste/query-cbo.py > /home/cbo/GIT/verdens_klogeste/stuff/${Q}.json
```

Parse with (verdens_klogeste/stuff):
```
./parse-response.py < filibuster.json
Ted_Cruz.txt
Bernie_Sanders.txt
Steve_Bannon.txt
Nancy_Pelosi.txt
Britney_Spears.txt
George_W._Bush.txt
Hillary_Clinton.txt
```
