#!/usr/bin/env bash
# patch_nl round 2: the reference scan and the three detectors that read it, then the model review of references to deleted provisions
cd "$(dirname "$0")"
export LE_WORKERS=6 LE_GREP_THREADS=6 PYTHONIOENCODING=utf-8 LE_PRIORITY=idle
P="C:/Python314/python.exe -X utf8"
set -x
mkdir -p findings/run/pre-nl2 && cp findings/run/triage.jsonl findings/run/ranked_dangling_ref.parquet findings/run/placeholder_ref.jsonl findings/run/dead_fine.jsonl findings/run/pre-nl2/
rm -f index/refs/netherlands-law*.parquet
$P ingest/refscan.py --shards netherlands-law:6
$P detectors/ref_detectors.py run; $P detectors/placeholder_ref.py run; $P detectors/dead_fine.py run
source ./llm_env.sh
$P -c "import json; L=[l for l in open('findings/run/triage.jsonl',encoding='utf-8') if json.loads(l)['detector']!='dangling_ref']; open('findings/run/triage.jsonl','w',encoding='utf-8',newline='\n').writelines(L)"
$P triage/triage.py run --per 40 --workers 12 --dets dangling_ref
echo RERUN DONE
