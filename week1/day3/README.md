# Day 3 CMD Responses



(day2) PS E:\Learning_AI\week1> uv init day3
Initialized project `day3` at `E:\Learning_AI\week1\day3`
(day2) PS E:\Learning_AI\week1> cd day3
(day2) PS E:\Learning_AI\week1\day3> uv venv python 3.14
error: unexpected argument '3.14' found

Usage: uv.exe venv [OPTIONS] [PATH]

For more information, try '--help'.
(day2) PS E:\Learning_AI\week1\day3> uv venv --python 3.14
Using CPython 3.14.3 interpreter at: C:\Users\dadia\AppData\Local\Python\pythoncore-3.14-64\python.exe
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
(day2) PS E:\Learning_AI\week1\day3> .\.venv\Scripts\activate.ps1
(day3) PS E:\Learning_AI\week1\day3> uv add groq python-dotenv
Resolved 16 packages in 428ms
      Built day3 @ file:///E:/Learning_AI/week1/day3                                                                                                                                                                                                                                                                         
Prepared 1 package in 65ms
░░░░░░░░░░░░░░░░░░░░ [0/16] Installing wheels...                                                                                                                                                                                                                                                                             warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 16 packages in 1.21s
 + annotated-types==0.8.0
 + anyio==4.15.1
 + certifi==2026.7.22
 + day3==0.1.0 (from file:///E:/Learning_AI/week1/day3)
 + distro==1.9.0
 + groq==1.7.0
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + idna==3.20
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + python-dotenv==1.2.3
 + sniffio==1.3.1
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
(day3) PS E:\Learning_AI\week1\day3> code understand-token.py
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py                      
############ RESPONSE ##################
Here are **seven one‑word brand names** that feel fresh, memorable, and versatile for a clothing company. I’ve included a short note on why each could work:

| # | Name | Why it Works |
|---|------|--------------|
| 1 | **Velora** | A smooth blend of “velvet” and a melodic ending that feels luxurious and approachable. |
| 2 | **Threadly** | Combines “thread” (the core of any garment) with a playful suffix that suggests ease and style. |
| 3 | **Silkline** | Evokes the elegance of silk and the idea of a cohesive collection. |
| 4 | **Moda** | The Italian word for fashion, short, global, and instantly recognizable. |
| 5 | **Wardra** | A modern twist on “wardrobe,” hinting at curated, stylish pieces. |
| 6 | **Trendify** | Implies turning ordinary items into trend‑setting apparel. |
| 7 | **Clothet** | A playful spin on “clothes” that feels tech‑savvy and forward‑thinking. |

Feel free to mix, match, or tweak any of these to suit your brand’s personality and target audience.
(day3) PS E:\Learning_AI\week1\day3> uv add groq
Resolved 16 packages in 1ms
Checked 16 packages in 50ms
(day3) PS E:\Learning_AI\week1\day3> uv pip list
Package           Version   Editable project location
----------------- --------- -------------------------
annotated-types   0.8.0
anyio             4.15.1
certifi           2026.7.22
day3              0.1.0     E:\Learning_AI\week1\day3
distro            1.9.0
groq              1.7.0
h11               0.16.0
httpcore          1.0.9
httpx             0.28.1
idna              3.20
pydantic          2.13.5
pydantic-core     2.46.5
python-dotenv     1.2.3
sniffio           1.3.1
typing-extensions 4.16.0
typing-inspection 0.4.4
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
############ RESPONSE ##################
Traceback (most recent call last):
  File "E:\Learning_AI\week1\day3\understand-token.py", line 51, in <module>
    answer = response.choices[0].message.content
             ^^^^^^^^
NameError: name 'response' is not defined
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
Traceback (most recent call last):
  File "E:\Learning_AI\week1\day3\understand-token.py", line 29, in <module>
    response=client.chat.completion.create(model=model, messages=messages)
             ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Chat' object has no attribute 'completion'. Did you mean: 'completions'?
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
propmt:Hi1 ---> your tokens:73 completion_token:40 total Token:113
propmt:Explain time travel in detail ---> your tokens:76 completion_token:2048 total Token:2124
propmt:Write a 1000 word essay on Machine learning ---> your tokens:81 completion_token:1618 total Token:1699
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
propmt:Hi1 ---> your tokens:73 completion_token:56 total Token:129
propmt:Explain time travel in detail under 100 words ---> your tokens:80 completion_token:773 total Token:853
propmt:Write a 500 word essay on Machine learning ---> your tokens:80 completion_token:1064 total Token:1144
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
propmt:Hi1 ---> your tokens:73 completion_token:50 total Token:123 Finish Reason:length
propmt:Explain time travel in detail under 100 words ---> your tokens:80 completion_token:50 total Token:130 Finish Reason:length
propmt:Write a 500 word essay on Machine learning ---> your tokens:80 completion_token:50 total Token:130 Finish Reason:length
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
propmt:Hi1 ---> your tokens:73 completion_token:51 total Token:124 Finish Reason:stop
propmt:Explain time travel in detail under 100 words ---> your tokens:80 completion_token:500 total Token:580 Finish Reason:length
propmt:Write a 500 word essay on Machine learning ---> your tokens:80 completion_token:500 total Token:580 Finish Reason:length
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> python .\understand-token.py
propmt:Hi1 ---> your tokens:73 completion_token:45 total Token:118 Finish Reason:stop
propmt:Explain time travel in detail under 100 words ---> your tokens:80 completion_token:529 total Token:609 Finish Reason:stop
propmt:Write a 500 word essay on Machine learning ---> your tokens:80 completion_token:1043 total Token:1123 Finish Reason:stop
############ RESPONSE ##################
(day3) PS E:\Learning_AI\week1\day3> deaactivate
deaactivate : The term 'deaactivate' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:1
+ deaactivate
+ ~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (deaactivate:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 
(day3) PS E:\Learning_AI\week1\day3> deactivate 
PS E:\Learning_AI\week1\day3> 