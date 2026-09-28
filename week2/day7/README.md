#### Issues
 - the current model #model="openai/gpt-oss-20b" cannot be used in ReAct
 - this openai model calls its native tools if we try to implement it manually
 - since we are manually implementing the tools we dont want that 
 - to fix this problem use this model #model="qwen/qwen3.8-27b"