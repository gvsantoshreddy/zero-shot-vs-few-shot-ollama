"""Topic 12: Zero-shot vs Few-shot, using local Ollama. Python standard library only."""
import csv, json, time, urllib.request, urllib.error, pathlib, statistics, html, collections
ROOT=pathlib.Path(__file__).resolve().parent
MODEL='gemma3:4b'; API='http://127.0.0.1:11434/api/generate'; REPEATS=3
TESTS=[
('classification','I loved the friendly service and delicious food.','positive'),
('classification','The package arrived broken and late.','negative'),
('classification','The meeting starts at 10 AM tomorrow.','neutral'),
('classification','This app is easy to use and very helpful.','positive'),
('classification','The battery dies after only one hour.','negative'),
('classification','The book contains twelve chapters.','neutral'),
('classification','The concert was amazing and unforgettable.','positive'),
('classification','Customer support never answered my request.','negative'),
('classification','The train departs from platform four.','neutral'),
('classification','The room was clean and comfortable.','positive'),
('qa','What is the capital of France?','paris'),
('qa','How many days are in a leap year?','366'),
('qa','What planet is known as the Red Planet?','mars'),
('qa','What gas do plants absorb during photosynthesis?','carbon dioxide'),
('qa','How many sides does a hexagon have?','6'),
('qa','What is 12 multiplied by 8?','96'),
('qa','What is the largest ocean on Earth?','pacific ocean'),
('qa','What is the chemical symbol for gold?','au'),
('qa','Who wrote Romeo and Juliet?','william shakespeare'),
('qa','What is the freezing point of water in Celsius at standard pressure?','0'),
]
CLASS_EXAMPLES=[('The movie was fantastic.','positive'),('The service was terrible.','negative'),('The office opens on Monday.','neutral')]
QA_EXAMPLES=[('What is the capital of Italy?','rome'),('What is 5 times 7?','35'),('Which planet is closest to the Sun?','mercury')]
def prompt(task, question, mode):
 if task=='classification':
  rule='Classify the sentiment as exactly one word: positive, negative, or neutral. Reply with the label only.'
  examples=CLASS_EXAMPLES
 else:
  rule='Answer the factual question briefly. Reply with only the short answer, no explanation.'
  examples=QA_EXAMPLES
 parts=[rule]
 if mode=='few-shot':
  parts.append('Examples:')
  for q,a in examples: parts.append(f'Input: {q}\nAnswer: {a}')
 parts.append(f'Input: {question}\nAnswer:')
 return '\n\n'.join(parts)
def generate(text):
 data=json.dumps({'model':MODEL,'prompt':text,'stream':False,'options':{'temperature':0,'num_predict':80}}).encode()
 req=urllib.request.Request(API,data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=120) as r: return json.load(r)
def norm(s): return ' '.join(s.lower().strip().strip(' .,!?:;\"\'').split())
def correct(task, answer, expected):
 a=norm(answer); e=norm(expected)
 if task=='classification': return a==e
 if e=='6': return a in ('6','six')
 if e=='0': return a in ('0','zero','0°c','0 c','0 degrees celsius')
 return a==e or (task=='qa' and e in ('paris','mars','366','96','pacific ocean','carbon dioxide','william shakespeare') and e in a and len(a)<65)
def main():
 print('Using',MODEL,'via',API)
 try: generate('Reply OK')
 except Exception as exc:
  print('ERROR: Cannot connect to Ollama or model not installed:',exc)
  print('Run: ollama pull '+MODEL+'  then: ollama serve (if not already running)')
  return
 rows=[]
 for mode in ('zero-shot','few-shot'):
  for i,(task,q,gold) in enumerate(TESTS,1):
   for trial in range(1,REPEATS+1):
    p=prompt(task,q,mode); start=time.perf_counter()
    try:
     result=generate(p); answer=result.get('response','').strip(); error=''
    except Exception as exc: answer=''; result={}; error=str(exc)
    elapsed=round(time.perf_counter()-start,3)
    row={'mode':mode,'test_id':i,'task':task,'question':q,'expected':gold,'trial':trial,'response':answer,'correct':int(correct(task,answer,gold)) if not error else 0,'prompt_tokens':result.get('prompt_eval_count',''),'output_tokens':result.get('eval_count',''),'elapsed_seconds':elapsed,'error':error}
    rows.append(row); print(f'{mode:9} {i:02} trial {trial}: {answer[:55]}')
 with (ROOT/'results.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for mode in ('zero-shot','few-shot'):
  for task in ('classification','qa'):
   subset=[r for r in rows if r['mode']==mode and r['task']==task]
   bytest=collections.defaultdict(list)
   for r in subset: bytest[r['test_id']].append(norm(r['response']))
   consistent=sum(len(set(v))==1 for v in bytest.values())/len(bytest)
   avg=lambda key:round(statistics.mean(float(r[key]) for r in subset if r[key]!=''),2) if any(r[key]!='' for r in subset) else None
   summary.append({'mode':mode,'task':task,'accuracy_percent':round(100*sum(r['correct'] for r in subset)/len(subset),1),'consistency_percent':round(100*consistent,1),'avg_prompt_tokens':avg('prompt_tokens'),'avg_output_tokens':avg('output_tokens'),'avg_seconds':avg('elapsed_seconds'),'runs':len(subset)})
 with (ROOT/'summary.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
 report(summary,rows)
 print('\nDONE: results.csv, summary.csv, REPORT.html created. Open REPORT.html in Chrome.')
def report(summary,rows):
 esc=html.escape
 table=''.join('<tr>'+''.join(f'<td>{esc(str(v))}</td>' for v in r.values())+'</tr>' for r in summary)
 details=''.join('<tr>'+''.join(f'<td>{esc(str(r[k]))}</td>' for k in ('mode','task','question','expected','response','correct','prompt_tokens','output_tokens','elapsed_seconds'))+'</tr>' for r in rows if r['trial']==1)
 bars=''.join(f'<div class="barrow"><span>{esc(r["mode"])} / {esc(r["task"])}</span><div class="track"><div class="fill" style="width:{r["accuracy_percent"]}%"></div></div><b>{r["accuracy_percent"]}%</b></div>' for r in summary)
 template='''<!doctype html><html><head><meta charset="utf-8"><title>Topic 12 Experiment Report</title><style>body{font:16px/1.6 Arial,sans-serif;max-width:1100px;margin:35px auto;padding:0 20px;color:#243047}h1,h2{color:#123b69}h1{border-bottom:5px solid #2d8dc7;padding-bottom:15px}.subtitle{color:#52657d}.panel{background:#eef6fc;padding:18px;border-radius:10px}table{width:100%;border-collapse:collapse;font-size:13px;margin:15px 0}th{background:#123b69;color:white}th,td{padding:9px;border:1px solid #cbd5e1;text-align:left;vertical-align:top}tr:nth-child(even){background:#f1f5f9}.barrow{display:flex;gap:12px;align-items:center;margin:12px 0}.barrow span{width:225px}.track{height:22px;flex:1;background:#e2e8f0;border-radius:5px;overflow:hidden}.fill{height:100%;background:#2183b8}.barrow b{width:55px}pre{background:#edf2f7;padding:18px;white-space:pre-wrap;border-radius:8px}@media print{body{margin:0}table{font-size:10px}h2{break-after:avoid}}</style></head><body><h1>Zero-Shot vs Few-Shot Prompting: Which Approach Works Better?</h1><p class="subtitle">Assignment 1 · Topic 12 · Local Ollama experiment · Model: MODEL</p><h2>1. Abstract</h2><p>This project compares zero-shot and few-shot prompting for sentiment classification and factual question answering. The same 20 test questions are evaluated with both approaches using a local language model. Three runs per question assess consistency, while reference answers support accuracy measurement. The experiment also records prompt tokens, output tokens and wall-clock response time.</p><h2>2. Problem and Objectives</h2><p>Choosing an effective prompt format can improve model answers, but examples add input tokens and require careful selection. The goal is to compare correctness, stability, speed and token costs on identical cases without sending data to a cloud API.</p><h2>3. Methodology</h2><p><b>Model:</b> MODEL via local Ollama. <b>Dataset:</b> 10 sentiment texts (positive/negative/neutral) and 10 short-answer factual questions. <b>Trials:</b> 3 for each prompt type and question, 120 runs total. <b>Settings:</b> temperature=0; num_predict=80. <b>Fairness:</b> same model, tasks, ground truth, and decoding settings; only the prompt examples differ. Test data and examples are separated.</p><h2>4. Prompt Templates</h2><h3>Zero-shot</h3><pre>Classify the sentiment as exactly one word: positive, negative, or neutral. Reply with the label only.\n\nInput: The battery dies after only one hour.\nAnswer:</pre><h3>Few-shot</h3><pre>Classify the sentiment as exactly one word: positive, negative, or neutral. Reply with the label only.\n\nExamples:\n\nInput: The movie was fantastic.\nAnswer: positive\n\nInput: The service was terrible.\nAnswer: negative\n\nInput: The office opens on Monday.\nAnswer: neutral\n\nInput: The battery dies after only one hour.\nAnswer:</pre><p>Question-answering uses the same structure but includes three separate factual Q&A examples for few-shot prompting.</p><h2>5. Workflow Diagram</h2><pre>                  SAME TEST DATASET (20 items)\n                            |\n                 +----------+----------+\n                 |                     |\n             ZERO-SHOT              FEW-SHOT\n          instruction + input     instruction + 3 examples + input\n                 |                     |\n                 +----------+----------+\n                            |\n                   LOCAL OLLAMA MODEL\n                            |\n                  Record 3 runs / item\n                            |\n             Accuracy / Consistency / Tokens / Time\n                            |\n                     Compare & conclude</pre><h2>6. Results</h2><div class="panel"><b>Accuracy by task and prompt</b>CHART</div><table><thead><tr><th>Mode</th><th>Task</th><th>Accuracy %</th><th>Consistency %</th><th>Avg prompt tokens</th><th>Avg output tokens</th><th>Avg seconds</th><th>Runs</th></tr></thead><tbody>SUMMARY</tbody></table><p><b>Accuracy</b> = exact/accepted matches divided by all trials × 100. <b>Consistency</b> = percentage of test questions with identical normalized answers across 3 trials. Token figures are reported by Ollama; time includes local request overhead. Consistency does not guarantee correctness.</p><h2>7. Sample Model Outputs (first trial per question)</h2><table><thead><tr><th>Mode</th><th>Task</th><th>Input</th><th>Expected</th><th>Model output</th><th>Correct (1/0)</th><th>Prompt tokens</th><th>Output tokens</th><th>Seconds</th></tr></thead><tbody>DETAILS</tbody></table><h2>8. Discussion</h2><p>Compare the measured accuracy and consistency across tasks. Few-shot prompting may clarify output format or task boundaries, but uses more prompt tokens because examples are included. Zero-shot prompting is shorter and may be sufficient for familiar, unambiguous tasks. Small local models can make mistakes even with examples.</p><h2>9. Example Selection Challenges</h2><p>Examples must be representative, correctly labeled, concise, and different from the test questions. Too many examples can waste tokens, bias answers, or exceed context limits. A poor or misleading example may reduce performance. The three sentiment examples deliberately cover all three labels; Q&A examples cover geography, arithmetic, and science.</p><h2>10. Limitations</h2><p>The dataset is small and hand-written, results depend on the local Ollama model and hardware, exact matching can underestimate correct paraphrases, and temperature 0 does not always guarantee identical answers. A broader dataset, additional models, human grading and multiple random seeds would improve reliability.</p><h2>11. Conclusion</h2><p>The experiment shows how to choose a prompting method using evidence rather than assumptions. Use the results table to determine which method performed better for each task. Prefer zero-shot for simple tasks when brevity matters; try few-shot when labels, style or response format need demonstrations. Any final performance claim should be based on the recorded measurements above.</p><h2>12. References</h2><p>Ollama API documentation: https://docs.ollama.com/api<br>Brown et al. (2020), Language Models are Few-Shot Learners, NeurIPS.<br>Wei et al. (2022), Finetuned Language Models Are Zero-Shot Learners, ICLR.</p><p><i>Generated from actual local model runs. Export to PDF using Chrome → Print → Save as PDF.</i></p></body></html>'''
 page=template.replace('MODEL',esc(MODEL)).replace('CHART',bars).replace('SUMMARY',table).replace('DETAILS',details)
 (ROOT/'REPORT.html').write_text(page,encoding='utf-8')
if __name__=='__main__': main()
