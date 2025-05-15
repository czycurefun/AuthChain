# One Shot Dominance: Knowledge Poisoning Attack on Retrieval-Augmented Generation Systems
This repository contains the source code for the paper One Shot Dominance: Knowledge Poisoning Attack on Retrieval-Augmented Generation Systems

# Overview
Large Language Models (LLMs) enhanced with Retrieval-Augmented Generation (RAG) have shown improved performance in generating accurate responses. However, the dependence on external knowledge bases introduces potential security vulnerabilities, particularly when these knowledge bases are publicly accessible and modifiable.
Poisoning attacks on knowledge bases for RAG systems face two fundamental challenges: the injected malicious content must compete with multiple authentic documents retrieved by the retriever, and LLMs tend to trust retrieved information that aligns with their internal memorized knowledge. Previous works attempt to address these challenges by injecting multiple malicious documents, but such saturation attacks are easily detectable and impractical in real-world scenarios.
To enable the effective single document poisoning attack, we propose AuthChain, a novel knowledge poisoning attack method that leverages Chain-of-Evidence theory and authority effect to craft more convincing poisoned documents. AuthChain generates poisoned content that establishes strong evidence chains and incorporates authoritative statements, effectively overcoming the interference from both authentic documents and LLMs' internal knowledge.
Extensive experiments across six popular LLMs demonstrate that AuthChain achieves significantly higher attack success rates while maintaining superior stealthiness against RAG defense mechanisms compared to state-of-the-art baselines.

The overview of Authchain:
<p align="center">
  <img src="https://github.com/czycurefun/AuthChain/blob/main/fig/method_revise.png" width="900"/>
</p>

# Environment
- pip install requirements.txt



# Running
**Information Extraction**
```
python extract_information.py
```   

**Poisoned Document Generation**
```
python AuthChain.py
```   

