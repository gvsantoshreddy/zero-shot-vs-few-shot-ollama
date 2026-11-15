# Zero-Shot vs. Few-Shot Prompting Using Ollama and Python

### A Practical Comparison of Prompt Engineering Techniques Using Gemma 3:4B

## Project Overview

This project compares two popular prompt engineering techniques: **Zero-Shot Prompting** and **Few-Shot Prompting**.

The experiment uses Python, Ollama, and the Gemma 3:4B language model to understand how different prompting techniques affect AI-generated responses.

Both techniques are tested using the same dataset to compare accuracy, consistency, token usage, and response time.

The project was developed as part of **Assignment 1 — Topic 12: Zero-Shot vs. Few-Shot Prompting**.

## Objectives

The main objectives of this project are:

- Understand zero-shot and few-shot prompting.
- Implement both techniques using Python.
- Run an LLM locally using Ollama.
- Compare responses using identical test questions.
- Evaluate accuracy and consistency.
- Measure prompt token usage and execution time.
- Analyse the advantages and limitations of both techniques.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Experiment implementation |
| Ollama | Local LLM execution |
| Gemma 3:4B | Language model |
| Windows PowerShell | Running the experiment |
| CSV | Storing experimental data |
| HTML | Generating the results report |
| GitHub | Hosting the project |

## Understanding the Prompting Techniques

### Zero-Shot Prompting

Zero-shot prompting means asking an AI model to complete a task without providing any examples.

**Example:**

Prompt:

Classify the following sentence as positive, negative, or neutral.

"The food was delicious."

Expected Output:

Positive

### Few-Shot Prompting

Few-shot prompting means providing a small number of examples before asking the AI model to complete a new task.

**Example:**

Prompt:

Classify the sentiment of the following sentences.

Example A:

Input: The movie was amazing.

Output: Positive

Example B:

Input: The service was terrible.

Output: Negative

Now classify:

Input: The food was delicious.

Expected Output:

Positive

Few-shot prompting helps demonstrate the required pattern or output format.

## Project Architecture

```text
             START
               |
               v
       Prepare Test Dataset
          (20 Questions)
               |
               v
        Generate Prompts
               |
       +-------+-------+
       |               |
       v               v
   Zero-Shot        Few-Shot
   Prompting        Prompting
       |               |
       +-------+-------+
               |
               v
          Ollama API
               |
               v
         Gemma 3:4B
               |
               v
       Collect Responses
               |
               v
        Evaluate Results
               |
               v
      Accuracy / Consistency
      Token Usage / Time
               |
               v
       Generate CSV & HTML
               |
               v
              END
```

## Installation and Setup

### Step 1: Install Python

Download and install Python from:

https://www.python.org/downloads/

Verify the installation:

```bash
python --version
```

### Step 2: Install Ollama

Download Ollama from:

https://ollama.com/download

Verify that Ollama is installed:

```bash
ollama --version
```

### Step 3: Download the Gemma Model

Run:

```bash
ollama pull gemma3:4b
```

Check the available models:

```bash
ollama list
```

### Step 4: Download This Project

Open the GitHub repository and select:

**Code → Download ZIP**

Extract the ZIP file on your computer.

### Step 5: Run the Experiment

Open PowerShell or a terminal inside the extracted project folder.

Execute:

```bash
python run_experiment.py
```

Make sure Ollama is running locally and the model is available.

The program automatically executes the experiment and generates the output files.

## Experiment Methodology

The experiment contains two categories of tasks.

**Sentiment Classification:** 10 questions.

**Factual Question Answering:** 10 questions.

Each question is tested using zero-shot and few-shot prompting.

Each technique is repeated three times for every question.

**Total Experiments:**

20 Questions × 2 Prompting Techniques × 3 Trials = **120 Runs**

Both approaches use the same language model and generation settings.

Model: `gemma3:4b`

Temperature: `0`

Maximum predicted tokens: `80`

## Experimental Results

The following results were obtained from real local Ollama executions.

### Accuracy Comparison

| Task | Zero-Shot | Few-Shot |
|---|---|---|
| Sentiment Classification | 100% | 100% |
| Question Answering | 100% | 90% |
| Overall Accuracy | 100% | 95% |

### Consistency Comparison

| Prompting Technique | Consistency |
|---|---|
| Zero-Shot | 100% |
| Few-Shot | 100% |

### Average Input Token Usage

| Task | Zero-Shot | Few-Shot |
|---|---|---|
| Classification | 45.8 | 85.8 |
| Question Answering | 40.6 | 89.6 |

Both prompting methods produced consistent responses in repeated trials.

However, few-shot prompting required more input tokens because examples were included in the prompts.

## Important Observation

One interesting result occurred during factual question answering.

**Question:** Who wrote Romeo and Juliet?

**Expected Answer:** William Shakespeare

**Few-Shot Model Output:** Shakespeare

Although the generated answer was factually correct, the automatic evaluation marked it incorrect because the answer did not match the accepted full-name format.

This affected the few-shot accuracy score.

Therefore, the measured 95% few-shot accuracy should be understood in the context of the program's grading method.

## Project Files

| File | Description |
|---|---|
| `run_experiment.py` | Main Python experiment |
| `results.csv` | Individual responses and trial measurements |
| `summary.csv` | Performance comparison |
| `REPORT.html` | Generated experiment report |
| `README_START_HERE.txt` | Basic setup instructions |
| `SUBMISSION_CHECKLIST.txt` | Submission checklist |
| `README.md` | Project documentation |

## Key Findings

**Finding 1:** Zero-shot prompting achieved 100% accuracy under the automatic grading method.

**Finding 2:** Few-shot prompting achieved 95% accuracy under the same method.

**Finding 3:** Both methods achieved 100% consistency.

**Finding 4:** Few-shot prompting required substantially more input tokens.

**Finding 5:** Providing examples influenced the format of the generated responses.

**Finding 6:** Automatic answer checking can reject factually correct alternative answers.

## Challenges Faced

- Connecting Python to the locally running Ollama model.
- Preparing identical test questions for both approaches.
- Measuring response time and token usage.
- Evaluating different answer formats.
- Interpreting automatically generated accuracy scores.

These challenges helped improve my understanding of prompt engineering and AI model evaluation.

## Future Improvements

The project can be improved by:

- Testing larger datasets.
- Comparing multiple Ollama models.
- Experimenting with different numbers of examples.
- Adding more difficult classification and reasoning tasks.
- Developing a user-friendly web interface.
- Using semantic evaluation to recognise valid alternative answers.

## Conclusion

This project demonstrates how zero-shot and few-shot prompting can be compared through a practical experiment.

The results showed that zero-shot prompting performed well on simple classification and factual question-answering tasks.

Few-shot prompting used more input tokens and did not improve the automated accuracy score in this experiment.

However, one valid shortened answer was marked incorrect by the grading system, demonstrating the importance of careful evaluation.

The experiment shows that neither prompting technique is always better. The appropriate method depends on the task, model, examples, and evaluation criteria.

## Medium Articles

**Article 1 — Theoretical / Conceptual**

[Zero-Shot vs. Few-Shot Prompting: A Beginner's Guide](https://medium.com/@venkatasntsh/zero-shot-vs-few-shot-prompting-a-beginners-guide-to-smarter-ai-prompts-574093502541)

**Article 2 — Practical / Implementation**

[Zero-Shot vs. Few-Shot Prompting: A Hands-On Experiment](https://medium.com/@venkatasntsh/zero-shot-vs-few-shot-prompting-a-hands-on-experiment-using-python-ollama-and-gemma-3-2ee17ccfd37e)

## References

- [Ollama Official Documentation](https://docs.ollama.com/)
- [Ollama API Documentation](https://docs.ollama.com/api)
- [Google Gemma Documentation](https://ai.google.dev/gemma)
- [Language Models are Few-Shot Learners — Brown et al., 2020](https://arxiv.org/abs/2005.14165)

---

**Assignment:** Assignment 1 — Topic 12

**Project:** Zero-Shot vs. Few-Shot Prompting

**Model Used:** Gemma 3:4B

**Platform:** Ollama + Python
