# 🔎 Pesquisa: llm-as-judge-revisao-automatica

> Busca: `LLM as a judge automated code review reliability rubric self-consistency verification adversarial evaluation reduce false positives best practices 2024`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## A Survey on LLM-as-a-Judge

`https://arxiv.org/html/2411.15594v1`

* These authors contributed equally to this research.

IDEA Research, International Digital Economy Academy

Institute of Computing Technology, Chinese Academy of Sciences

Department of Civil and Environmental Engineering, Imperial College London

Gaoling School of Artificial Intelligence, Renmin University of China

Accurate and consistent evaluation is crucial for decision-making across numerous fields, yet it remains a challenging task due to inherent subjectivity, variability, and scale.

Large Language Models (LLMs) have achieved remarkable success across diverse domains, leading to the emergence of "LLM-as-a-Judge," where LLMs are employed as evaluators for complex tasks. With their ability to process diverse data types and provide scalable, cost-effective, and consistent assessments, LLMs present a compelling alternative to traditional expert-driven evaluations. However, ensuring the reliability of LLM-as-a-Judge systems remains a significant challenge that requires careful design and standardization.

This paper provides a comprehensive survey of LLM-as-a-Judge, addressing the core question: How can reliable LLM-as-a-Judge systems be built? We explore strategies to enhance reliability, including improving consistency, mitigating biases, and adapting to diverse assessment scenarios. Additionally, we propose methodologies for evaluating the reliability of LLM-as-a-Judge systems, supported by a novel benchmark designed for this purpose. To advance the development and real-world deployment of LLM-as-a-Judge systems, we also discussed practical applications, challenges, and future directions. This survey serves as a foundational reference for researchers and practitioners in this rapidly evolving field.

https://github.com/IDEA-FinAI/LLM-as-Evaluator

Judgment is the faculty of thinking the particular as contained under the universal.

It involves the capacity to subsume under rules, that is, to distinguish whether something falls under a given rule.

Recently, Large Language Models (LLMs) have achieved remarkable success in numerous domains, ranging from artificial intelligence and software engineering to education and social science.

The adoption of LLMs as evaluators—commonly referred to as "LLM-as-a-Judge"

—has surged, driven by their ability to emulate human-like reasoning and decision-making processes. This capability enables LLMs to undertake roles traditionally reserved for human experts, offering a cost-effective and scalable alternative.

For instance, we usually rely on experts to evaluate the accuracy of mathematics and physics competition questions at the Olympiad level

, which can be assessed through LLM-as-a-Judge now. Additionally, in recent peer reviews of research submissions, LLM-as-a-Judge is introduced to address the rising number of paper submissions and reviewer workload

https://blog.iclr.cc/2024/10/09/iclr2025-assisting-reviewers/

, which is designed to identify potential issues in reviews and offer constructive feedback to reviewers.

These trends underscore a key motivation for adopting LLM-as-a-Judge: the potential to enhance evaluation efficiency while addressing limitations inherent in human assessments, such as scalability and consistency.

LLM-as-a-Judge presents a compelling alternative to both human evaluations and traditional automated methods, offering distinct advantages in scalability, efficiency, and adaptability.

Human evaluations, though often considered the gold standard, face challenges in scalability, cost, and consistency. They are time-consuming, require substantial expert effort, and are expensive to scale due to limited availability of qualified evaluators. Coordinating and training evaluators adds complexity, and fatigue during lengthy tasks can compromise reliability and accuracy.

In contrast, LLMs provide scalable, cost-effective, and efficient evaluations with reduced subjective variability, enhancing objectivity. Traditional automated methods, such as BLEU, ROUGE, and METEOR for software artifact summarization, often fail to align with human judgment or provide clear insights in specialized domains like software engineering.

LLMs offer flexibility to process diverse input types, including text, semi-structured data, and multi-modal content, allowing evaluations to integrate qualitative insights with quantitative rigor. This human-aligned adaptability makes LLMs effective for complex, context-aware assessments beyond the limits of conventional metrics

Despite its wide advantages, LLM-as-a-Judge poses significant challenges for reliability. This necessitates the capability of LLM-as-a-Judge framework to subsume under rules, that is, to distinguish whether something falls under a given rule

. As LLM-as-a-Judge becomes more commonly used as an effective evaluator in different areas, collecting evaluations with LLM-as-a-Judge is relatively simple. Therefore, central to this survey is the fundamental question:

How to build reliable LLM-as-a-Judge systems?

To address this question, we explore two core aspects: (1) strategies for enhancing the reliability of LLM-as-a-Judge and (2) methodologies for evaluating reliability of LLM-as-a-Judge systems themselves.

For the first aspect of enhancing LLM-as-a-Judge reliability, we review the main strategies aimed at optimizing their performance for diverse evaluation tasks. These strategies include improving consistency, mitigating biases, and refining adaptability to different assessment scenarios. For the second aspect, we examine the metrics, datasets, and methodologies used to evaluate the performance of LLM-as-a-Judge systems, discussing potential sources of bias and corresponding mitigation techniques. Building on this foundation, we introduce a novel benchmark specifically designed for LLM-as-a-Judge evaluations. Using established metrics and datasets, this benchmark provides a framework for analyzing the effectiveness of various reliability enhancement strategies. Additionally, we explore practical application scenarios, identify specific challenges unique to each context, and propose solutions to address these issues. Finally, we discuss future research directions, emphasizing key areas for advancing the reliability, scalability, and applicability of LLM-as-a-Judge systems.

This paper aims to provide a comprehensive overview of the LLM-as-a-Judge research landscape while offering insights into how reliable LLM-as-a-Judge can be constructed. We hope that this work will serve as a valuable reference for researchers and practitioners, fostering further research and facilitating the real-world deployment of LLM-as-a-Judge. The rest of this survey is organized as Figure

, we provide a comprehensive overview of the LLM-as-a-Judge field. We define LLM-as-a-Judge through formal and informal definitions, and categorize existing methods and approaches for its use. For a quick guide on implementing an LLM-as-a-Judge for specific scenarios, you can find answers in Quick Practice (

). Then, we discuss the problems of "How to improve" and "how to evaluate" LLM-as-a-Judge in n Section

. Next, we show the applications of LLM-as-a-Judge in Section

. The discussions of the challenges and future directions come at last in Section

In evaluative tasks, especially those that are subjective, human assessment is often considered the gold standard due to its reliable and open-ended nature

. However, this approach is typically slow and costly

. To address these challenges, LLMs are increasingly employed as substitutes for human evaluators. Since these models are frequently trained using Reinforcement Learning from Human Feedback (RLHF), they demonstrate strong alignment with human perspectives, leading to the approach known as "LLM-as-a-Judge".

In general, LLM-as-a-Judge is a process that uses LLM to evaluate different objects in various scenarios for diverse tasks. For instance, roles such as "Assessors", "Critics," and "Verifiers" utilize LLMs to facilitate evaluation at different stages of the process, whether during intermediate steps or throughout the entire workflow. To date, definition of how to effectively use LLM-as-a-Judge for evaluation tasks has been largely informal or vague, lacking clear and formal expression. Therefore, we will provide a formal definition of LLM-as-Evaluator as follows:

\displaystyle\left(x\oplus\mathcal{C}\right)

: The final evaluation obtained from the whole LLM-as-a-Judge process in the expected manner. It could be a score, a choice, or a sentence, etc.

: The probability function defined by the corresponding LLM, and the generation is an auto-regressive process.

: The input data in any available types (text, image, video), which waiting to be evaluated.

, which is often prompt template or combined with history information in dialogue.

: The combination operator combines the input

, and this operation can vary depending on the context, such as being placed at the beginning, middle, or end.

The formulation of LLM-as-a-Judge reflects that LLM is a type of auto-regressive generative model, which generates subsequent content based on the context then obtain target evaluation from it. The form of LLM-as-a-Judge illustrates how we utilize LLM for evaluation tasks, encompassing input design, model selection and training, as well as output post-processing.

The different basic approaches of implementing LLM-as-a-Judge can be classified according to the formulation: In-Context Learning, Model Selection, Post-processing Method and Evaluation Pipeline, which concluded in Figure

. By following this pipeline, we can build a basic LLM-as-a-Judge for evaluation. A faster practice guide is available in section

To apply LLM-as-a-Judge, it is helpful to start by defining the evaluation task using In-Context Learning methods. This process involves two key aspects: the design of prompt and input. For input design, it is important to consider the type of variables to be evaluated (such as text, image, or video), the manner of input (e.g., individually, in pairs, or in batches), and the position of the input (e.g., at the beginning, middle, or end). As for the prompt design, four different methods can be adopted, as illustrated in Figure

. The four methods include generating scores, solving true/false questions, conducting pairwise comparisons, and making multiple-choice selections. Further details will be provided in the following sections.

It is quite intuitive to represent an evaluation using a corresponding score. What requires more careful consideration, however, is the nature and range of the score used for evaluation. The score can be discrete, with common ranges like 1-3, 1-5

. Alternatively, it can be continuous, ranging from 0 to 1 or 0 to 100

The simplest way to score is through the context, setting the range of scores and the main criteria for scoring. For example, "Please rate the helpfulness, relevance, accuracy, level of details of their responses. Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance"

. A slightly more complex way is to provide more detailed scoring criteria. More complex scoring situations can be as

, which use Likert scale scoring functions as an absolute evaluative measure showed in Figure

. The evaluator assigns scores to a given response along predefined dimensions including accuracy, coherence, factuality and comprehensiveness. Each of these dimensions is scored on a scale of 1 to 3, ranging from worst to best. The evaluator is also asked to provide an overall score ranging from 1 to 5, based on the scores assigned to the previous 4 dimensions. This score serves as an indicator of the overall quality of the answer.

Evaluate the quality of summaries written for a news article. Rate each summary on four dimensions:

. You should rate on a scale from 1 (worst) to 5 (best).

The template for Likert scale scoring from

A Yes/No question requires a judgment on a given statement, focusing solely on its accuracy. This type of question is simple and direct, providing only two fixed responses—yes or no, true or false—without any additional comparisons or choices.

This type of evaluation is often utilized in intermediate processes, creating the conditions for a feedback loop. For example, it promotes a self-optimization cycle, as seen in

, which generates verbal self-reflections to provide valuable feedback for future attempts. In scenarios with sparse reward signals, such as a binary success status (success/fail), the self-reflection model uses the current trajectory and persistent memory to generate nuanced and specific feedback.

, Yes/No questions can be employed to evaluate custom phrases, such as

, facilitating entry into the next cycle.

Moreover, these evaluations are common for testing knowledge accuracy and assessing whether statements align with established facts

, like "Given a question and the associated retrieved knowledge graph triples (entity, relation, entity), you are asked to answer whether it’s sufficient for you to answer the question with these triples and your knowledge (Yes or No)." A detailed and specific example can be seen in the Figure

Is the sentence supported by the article? Answer "Yes" or "No".

The template for Yes/No evaluation for example.

Pairwise comparison refers to comparing two options and selecting which one is superior or more aligned with a specific standard, showed in Figure

. It involves making a decision between two options rather than judgement between ’yes’ or ’no’. The comparison can be subjective or based on objective criteria. This evaluation is a relative evaluation. Pairwise comparison is often used for ranking multiple options or prioritizing them, where several comparisons are made between pairs to identify the better choice or establish a hierarchy.

Pairwise comparison is a well-established method that has significantly impacted a variety of fields

, LLM and human evaluations are more aligned in the context of pairwise comparisons compared to score-based assessments. Numerous studies have demonstrated that pairwise comparative assessments outperform other judging methods in terms of positional consistency

. Furthermore, pairwise comparisons can be extended to more complex relation-based assessment frameworks, such as list-wise comparisons, using advanced ranking algorithms

. In pairwise comparative assessments, LLM-as-a-Judge is prompted to select the response that better answers the question at hand. To accommodate the possibility of a tie, several option modes are introduced. The Two-Option mode requires judges to choose the better response from two given options. The Three-Option mode introduces an additional choice, allowing judges to indicate a tie if neither response is preferable. Evaluations typically involve determining the outcomes of win, tie, or loss for responses

through pairwise comparisons, with win rounds counted for each response. The Four-Option mode further expands the choices, allowing judges to classify responses as either a "both good tie" or a "both bad tie."

Given a new article, which summary is better? Answer "Summary 0" or "Summary 1". You do not need to explain the reason.

The template for pairwise comparison from

Multiple-choice selections involve providing several options, not giving relative choices in pairwise comparison, nor making a yes/no judgment.

The evaluator must choose the most appropriate or correct one. This method allows for a broader range of responses compared to true/false questions and can assess deeper understanding or preferences and an example is showed in Figure

. However, this kind of prompt design is more rare than the first three.

You are given a summary and some semantic content units. For each semantic unit, choose those can be inferred from the summary, return their number.

The template for multiple-choice for example.

To automate evaluation by LLM-as-a-Judge, one effective approach is to employ advanced language models such as GPT-4

created a test set with 805 questions and assessed the performance by comparing it to text-davinci-003 using GPT-4. Additionally,

designed 80 multi-round test questions across eight common areas and used GPT-4 to automatically score the model’s responses. The accuracy of the GPT-4-based evaluator has been demonstrated to be high compared to professional human evaluators, showing superior consistency and stability in evaluations. At the same time, if the general LLM used has limitations in instruction-following or reasoning abilities, the effectiveness of the LLM-as-a-Judge method may be significantly affected.

However, relying on external API for evaluation may introduce consideration about privacy leakage, and the opacity of API models also challenges the evaluation reproducibility. Therefore, follow-up works suggest fine-tuning language models specialized in evaluations. For instance, PandaLM

constructs data based on Alpaca instructions and GPT-3.5 annotation, and then fine-tunes LLaMA-7B

constructs data from diversified instruction sets and GPT-4 annotations, and fine-tunes Vicuna

constructs evaluation data upon multiple scenarios to train a generative evaluator model, which can provide both evaluation and critical opinion. Prometheus

defines thousands of evaluation criteria and construct a feedback dataset based on GPT-4, and fine-tunes a fine-grained evaluator model.

The typical process for fine-tuning a judge model involves three main steps.

The training data generally consists of three components: instructions, the objects to be evaluated, and evaluations. Instructions are typically sourced from instruction datasets, while evaluations can come from either GPT-4 or human annotations.

The structure of the prompt template can vary based on the evaluation scheme, which already detailed in §

Using the designed prompts and collected data, the fine-tuning process for the evaluator model typically adheres to the instruction fine-tuning paradigm

. The model receives an instruction along with one or more responses to generate output that includes evaluation results and possibly explanations.

After fine-tuning, the evaluator model can be employed to evaluate the target object. While these fine-tuned models often demonstrate superior performance on self-designed test sets, they are identified several limitations in their evaluation capabilities, which detailed in Section

Post-processing refines the probability distributions generated by LLM-as-a-Judge to provide accurate evaluations. The evaluation format should align with our In-Context Learning design. Additionally, post-processing may involve procedures to enhance the reliability of extracted evaluations, closely linked to the In-Context Learning framework and consistently applied. There are three main methods of post-processing, which are extracting specific tokens, normalizing the output logits, and selecting sentences with high returns.

As showed in In-context Learning (Section

), when the evaluation target take the form of a score, selecting specific options, or responding with Yes/No, applying rule-match to extract the corresponding token from the response generated during probability distribution iteration is common used. It is worth noting that Yes/No is a broad definition, including custom statements involving judgment.

Considering a Yes/No question for evaluation in custom phrases

"Does the above answer need to be further modified?"

When the input sample is put through the template, it might have outputs such as "Modification needed.", "Conclusion: Modification needed." or "Yes". This variance in response formats is difficult to parse consistently. The corresponding post-processing with the response is necessary. Using rules to extract specific tokens for our designed prompts and input content, as well as the backbone model used for the evaluator, all have higher requirements as we discussed in Section

In contextual learning, if there is no clear indication of the output format for response, there may be various expressions of evaluation, which can be seen in Figure

. For example, "Response 1 is better" and "The better one is response 1", which convey the same choice but differ in format leading to the difficulty of rule recognition. Simple solutions often involve providing clear instructions, such as "The last sentence should be started with ’The better response is’", or using a few-shot strategy.

Also, the general model with insufficient instruction following capability may not be able to generate the evaluation format and content of the target according to the instruction, resulting in the post-processing extracted according to the rules not as smooth as expected.

LLM-as-a-Judge in the intermediate steps with Yes/No setting often normalize the output logits to obtain the evaluation in the form of a continuous decimal between 0 and 1. This is also very common in agent methods and prompt-based optimization methods

. For example, the self-consistency and self-reflection scores

, are effectively obtained by constructing a prompt

[\left(x\oplus\mathcal{C}\right),\texttt{"Yes"}]

and acquire the probability of each token conditioned on the previous tokens

. The auto-regressive feature is leveraged, thus aggregate the probability of the relevant tokens to compute the self-consistent score

\rho_{j}=\rho_{\text{SC},j}\cdot\rho_{\text{SR},j}

\displaystyle\underrightarrow{\overbrace{\left(x\oplus\mathcal{C}\right)}^{\rho_{\text{SC}}}\overbrace{\texttt{"Yes"}}^{\rho_{\text{SR}}}}\ \Rightarrow\begin{cases}\rho_{\text{SC}}=\prod_{t_{i}\in\alpha}P(t_{i}|t_{<i})\cdot\prod_{t_{i}\in\beta}P(t_{i}|t_{<i})\\

\rho_{\text{SR}}=\prod_{t_{i}\in\texttt{"Yes"}}P(t_{i}|t_{<i})\end{cases}

is also common using this method for LLM-as-a-Judge. It can be helpful to let the LLM evaluate itself by asking, "Is this reasoning step correct?" and then reward it based on the probability of the next word being "Yes."

In addition to selecting specific tokens and normalizing the output logits, the content extracted by LLM-as-a-Judge may also be a sentence or paragraph. As showed in Figure

reasoning tree by iteratively considering the most promising reasoning steps (actions, sub-questions) by LLM-as-a-Judge.

There are three common scenarios for using LLM-as-a-Judge evaluation pipelines showed in Figure

, which are LLM-as-a-Judge for LLMs, LLM-as-a-Judge for data, and LLM-as-a-Judge for agent respectively.

It is universally known that the best way to evaluate LLMs is human judgment, but collecting human annotations can be costly, time-consuming, and laborious

. Using strong LLMs (usually closed-source ones, e.g., GPT-4, Claude, ChatGPT) as an automated proxy for assessing LLMs has become a natural choice

. With appropriate prompt design, the quality of evaluation and agreement to human judgment can be promising

However, the cost concern still exists when calling the APIs of these proprietary models, especially when there is a frequent need for model validation on large-scale data. Moreover, closed-source LLM-as-a-Judge leads to low reproducibility due to potential changes in models behind the API.

Some recent works have started to make attempts for open-source alternatives. SelFee

collects generations, feedback, and revised generations from ChatGPT and fine-tunes LLaMA models to build a critique model. Shepherd

trains a model that can output critiques for single-response with the data of feedback from online communities and human annotation. PandaLM

trains a model to conduct pairwise comparison for LLM Instruction Tuning Optimization, and

on a 20K pairwise comparison dataset to explore the potential of open-source models as a more cost-friendly proxy.

Recent advancements in using Large Multimodal Models (LMMs) as evaluators have showcased their potential to perform complex judgment tasks in vision-language scenarios. Proprietary models like GPT-4V and GPT-4o have been pivotal in benchmarks such as detailed captioning and visual chats, utilizing both pointwise and pairwise evaluation methods

. Open-source alternatives have emerged, with Prometheus-Vision

being the first vision-language model specifically trained to act as an evaluator for user-designed scoring criteria. While Prometheus-Vision introduced the concept of open-source evaluators with a focus on specialized tasks, it remains limited to predefined criteria. In contrast, LLaVA-Critic

, another open-source innovation, expands the scope by serving as a generalist evaluator. Trained on diverse and detailed datasets, LLaVA-Critic provides robust scoring and preference learning, closely aligning with human and proprietary evaluations. These models mark significant progress in democratizing and enhancing multimodal evaluation tools.

LLM-as-a-Judge appears in two common forms in the agent. The left diagram is Agent-as-a-Juge, designing a complete agent to serve as an evaluator. The right diagram shows using LLM-as-a-Judge in the process of an Agent.

Data annotation generally refers to the labeling or generating of raw data with relevant information, which could be used for improving the efficacy of machine learning models. The process, however, is labor-intensive and costly. The emergence of LLMs presents an unprecedented opportunity to automate the complicated process of data annotation by LLM-as-a-Judge.

Most of the data need to be evaluated by LLM-as-a-Judge is generated by models, or large-scale crawled data.

Language models first conduct supervised fine-tuning to imitate how to align with human instructions

After that, reinforcement learning techniques have been explored to align language models with human preferences

The most successful way is applying a RLHF framework

via training a reward model on human feedback and using PPO

to obtain the policy model for language generation.

However, in practices, the PPO training paradigm is complex in coding and hyper-parameter tuning while it needs four models that are hard for training.

This motivates us to explore simpler and more straightforward methods to align language models with human preferences. This involves how to use LLM-as-a-Judge to evaluate whether different responses are aligned with human preferences.

use general LLM (ChatGPT) to get better alignment with human preferences. The Aplaca prompts

is used as sampling queries to different models generate responses. And these data was evaluated by LLM-as-a-Judge to obtain human preference scores (reward score) to train a new language model. Other works would like to use Supervised Fine-Tuning (SFT) model itself as evaluator, like generating better-aligned datasets for SFT including hindsight-modified prompts

In addition, the lack of domain-specific model training data is a common phenomenon. In order to obtain annotated high-quality data, it is also very common to use LLM-as-a-Judge for the generation and evaluation of domain data.

would use its Instruction Reward Model (IRM) as Evaluator, aiming to judge the quality of the evolved instructions on three aspects: i) Definition, ii) Precision, and iti) Integrity. To produce the ranking list training data of IRM, for each instruction, ChatGPT and Wizard-E are used to generate 2-4 evolved instructions respectively. Then we leverage Wizard-E to rank the quality of those 4-8 instructions.

Recent research on evaluating multimodal data focuses on addressing vision-language misalignments in Multimodal Large Language Models (MLLMs), which often cause hallucinations—outputs inconsistent with visual or contextual evidence

. Techniques like Reinforcement Learning from Human Feedback (RLHF) and Factually Augmented RLHF have been employed to improve model alignment by incorporating structured ground-truth data and image captions, enhancing hallucination detection

assess these models using tasks like scoring, pair comparison, and batch ranking, revealing limitations in alignment with human preferences. Persistent issues include biases (e.g., position, verbosity) and hallucinations, with even advanced models like GPT-4V displaying challenges. While pair comparison tasks align better with human judgment, scoring and batch ranking require significant improvements for reliable deployment. These findings emphasize the need for innovative frameworks and datasets to refine MLLM evaluation and alignment.

There are two ways to apply LLM-as-a-Judge for an agent. One is to evaluate the entire process of the intelligent agent

, and the other is to evaluate it at a specific stage in the agent framework process

. Both approaches are briefly illustrated in Figure

Using LLM as the brain of agent, an agentic system

could evaluate like a human, it would reduce the need for human involvement and eliminate the trade-off between thoroughness and effort. In addition, the agent

can interact with the environment through language and receive feedback on actions through LLM to make decisions for the next action.

To effectively apply LLM-as-a-Judge design, it is more recommended to find more effective settings in the testing cycle for different scenarios. The process of quick practice for LLM-as-a-Judge involves four main stages. First, thinking, where users define the evaluation objectives by determining what needs to be evaluated, understanding how humans typically perform such evaluations, and identifying some reliable evaluation examples. Next is prompt design, detailed in Section

. The most efficient and generally effective approach involves specifying scoring dimensions, emphasizing relative comparisons for improved assessments, and creating effective examples to guide the LLM.

The third stage, model selection (Section

), focuses on choosing a large-scale model with strong reasoning and instruction-following abilities to ensure reliable evaluations. Finally, standardizing the evaluation process ensures that the outputs are structured (Section

). This can be achieved by using specific formats like \boxed{XX}, numerical scores, or binary responses (e.g., "Yes" or "No"). The entire process includes iterative testing with cases and refinement through retesting to enhance reliability.

When directly utilizing LLMs to conduct evaluation tasks such as scoring, selection, pairwise comparison or ranking, the inherent biases of LLMs like length bias, positional bias and concreteness bias

will lead to poor evaluation results. Addressing these inherent biases and improving the overall evaluation performance of LLMs is a critical challenge for applying LLMs as evaluators. In this section, we introduce three improvement strategy aimed at enhancing the evaluation performance of LLM-as-a-judge:

improvement strategy of LLMs’ evaluation capabilities

optimization strategy of final evaluation results

(post-processing based). Our categorization is based on the formal definition of LLM-as-Evaluator in Section

, focusing on enhancing the evaluation effectiveness by targeting three key phases of the process: the context

An evaluation prompt is an input to LLM evaluators, which is used to guide the LLMs to complete the required evaluation tasks. LLMs possess in-context learning ability to learn how to perform specified tasks through relevant examples or instructions provided in prompts without requiring weight updates or retraining

. It indicates that the design strategy of evaluation prompts will significantly impact the effectiveness of LLM-as-a-judge. Therefore, how to optimize the design of evaluation prompts, including better methods to help LLMs understand the evaluation tasks and produce evaluation results, is the most direct and effective way to improve the evaluation performance of LLM-as-a-judge.

Optimizing LLMs’ Understanding of Evaluation Tasks

In optimization methods of prompting LLMs to better understand evaluation tasks, one of the most commonly used and effective approaches is few-shot prompting

. By incorporating several high-quality evaluation examples into the evaluation prompts, LLM evaluators can effectively grasp the objectives, general processes and rough evaluation criteria of evaluation tasks. Many research works employ this prompt paradigm for evaluation, such as FActScore

In addition to providing hight-quality examples for LLMs to inference, refining the evaluation task instructions is also an effective approach to optimize LLMs’ understanding of evaluation tasks. Current methods for refining evaluation tasks mainly including the decomposition of evaluation steps and criteria:

entails breaking down the entire evaluation tasks into smaller steps, providing detailed definitions and constraints for each small step in prompts, thereby guiding LLMs comprehensively through the whole evaluation pipeline. For instance, G-Eval

employs the Socratic method to meticulously design each step to enhance evaluation performance. Saha et al. proposes Branch-Solve-Merge(BSM)

, which divides evaluation tasks into multiple parallel sub-tasks for separate evaluation and final merge.

involves breaking down coarse evaluation criteria like Fluency into finer-grained sub-criteria like Grammar, Engagingness and Readability, and then generating overall scores based on these difference dimensions. HD-Eval

iteratively aligns LLM evaluators with human preference via hierarchical criteria decomposition and thereby addressing the potential bias in LLMs. Hu and Gao et al.

summarize and clearly define an explicit hierarchical classification system encompassing 11 criteria, addressing the issue of LLMs potentially confusing different evaluation standards. These refinements specific to enable LLMs to understand the details of evaluation tasks more deeply, thereby aligning evaluation results more closely with human evaluation requirements and preferences.

Furthermore, the evaluation capabilities can be optimized based on specific shortcomings of LLMs in prompts. For instance, to address specific biases like position bias which is common in pairwise evaluations, several research efforts have optimized prompts design by randomly swapping contents to be evaluated.

analyzed and validated the impact of position bias on LLM-as-a-judge, and proposed a calibration framework to mitigate this bias by swapping the contents and averaging the scores. Auto-J

also enhance the evaluation consistency by shuffling the texts to be evaluated. In contrast to averaging scores, PandaLM

annotates the conflicting evaluation results after swapping as "Tie" to address the position bias.

To address the challenge of LLMs’ absolute scoring being less robust than relative comparing

, some research works convert scoring tasks into pairwise comparison, thereby enhancing the reliability of evaluation results.

transform the scoring evaluation to ranking evaluation and introduce Pairwise-Preference Search (PARIS), which employs LLMs to conduct pairwise comparisons locally and efficiently ranks candidate texts globally, making evaluation results more aligned with human preferences.

In summary, the design of prompts for better understanding evaluation tasks is a core method for optimizing LLMs’ in-contextual learning abilities. By refining evaluation task instructions and criteria in prompts or few-shot prompting with high-quality examples, the details of evaluation prompts can be enriched and the understanding of LLMs on evaluation tasks can be directly or indirectly enhanced. Additionally, targeted adjustments to prompts can address potential biases of LLMs such as position bias.

Directly requiring LLM evaluators to output evaluation results poses robustness problems. The response text may unexpectedly vary due to the inherent generative randomness of LLMs, such as outputting text like "low relevance" while asked to measure it with discrete scores, which hinders the automated and accurate extraction of evaluation results from LLMs’ output. An effective method to enhance the robustness of output forms is to constrain LLMs’ output in structured formats within prompts. G-Eval

perform evaluation tasks with a form-filling paradigm, constraining outputs with formats like

represents the dimension or metric to be evaluated and

denotes an identifiable output form like scores or specific tokens. LLM-EVAL

further codifies this form-filling paradigm, efficiently output evaluation results in JSON dictionary format and obtain multidimensional scores, leveraging LLMs’ high understanding and generation capabilities of code-like textural formats.

Apart from challenges in robustness, directly outputting evaluation results by LLMs also suffer from the lack of interpretability. The meaning of evaluation results from LLM evaluators is difficult to align consistently with instructions and metrics provided in prompts. To address the challenges, CLAIR

requires LLMs to output evaluation scores between 0-100 simultaneously with relevant reasons as explanations in JSON format, which enhancing the rationality and interpretability of the scores. FLEUR

utilizes LLaVA to first provide quality scores for image captions and subsequently asks with

for explanations with the images, captions and scores as inputs, offering a stepwise approach to provide interpretable scores.

In general, by constraining or guiding the output process and format of LLM evaluators within prompts, the robustness and rationality of evaluation results can be effectively improved through structured outputs. This also facilitates the automated post-processing of evaluation results in subsequent steps, thereby enhancing the overall stability of the evaluation pipeline.

The evaluation capabilities of LLMs is a reflection of their powerful general language understanding and generation abilities triggered by specific prompts. Methods for optimizing evaluation through prompt design, which focuses on LLMs’ in-contextual learning capabilities, require LLMs to fully comprehend the meaning of prompts and consistently follow the relevant evaluation instructions. However, even state-of-the-art LLMs like GPT4 face issues such as conceptual confusion

, and smaller open-source LLMs which are easier to deploy as evaluators have even more limitations in their evaluation capabilities. Therefore, how to improve the evaluation capabilities of LLMs, including how to fine-tune LLMs through meta evaluation datasets and how to iteratively optimizing models based on feedback of evaluation results, is significant for improving the fundamental evaluation performance of LLM-as-a-judge.

A straightforward approach to enhancing the evaluation capabilities of LLMs is to fine-tune them via meta evaluation datasets specifically constructed for evaluation tasks, which helps improve the LLMs’ understanding of specific evaluation prompts, boosts the evaluation performance, or addresses potential biases. The most critical step in this optimization strategy is the collection and construction of training data. A common method involves sampling evaluation questions from publicly available datasets, modifying them with certain templates, and supplementing the dataset with evaluation responses generated either manually or by powerful LLMs like GPT4. For instance, PandaLM

samples inputs and instructions from Alpaca 52K

and generate responses using GPT-3.5 to construct training data, while SALAD-Bench

builds its training data from a subset of LMSYS-Chat

To better align with the requirements of evaluation tasks, many research works further transform inputs and instructions sampled from public datasets to construct more targeted training data. OffsetBias

aims to reduce biases of LLMs by using GPT4 to generate off-topic versions of the original inputs and then having GPT-3.5 respond to the new inputs to produce bad responses. By pairing good and bad responses as training data to fine-tune the LLMs as evaluators, the biases in LLMs are significantly reduced, including length bias, concreteness bias, knowledge bias and so on. JudgeLM

enhances LLMs’ evaluation capabilities by creating different types of training data through paradigms like reference support and reference drop. CritiqueLLM

proposes a multi-path prompting approach, combining pointwise-to-pairwise and referenced-to-reference-free prompting strategies to restructure referenced pointwise grading data into four types, which helps create Eval-Instruct to fine-tune LLMs, addressing shortcomings in pointwise grading and pairwise comparison.

In summary, constructing meta evaluation training data targeted at specific evaluation tasks and fine-tuning LLMs can directly adjust the model’s internal parameterized knowledge and language abilities. This is the most straightforward method to improve the evaluation performance of LLM evaluators and address potential biases.

Iterative Optimization Based on Feedback of Evaluation Results

Fine-tuning LLMs on meta evaluation datasets give them the ability to produce evaluations which are more aligned with human preferences. However, LLM-as-a-judge may still introduce biases during evaluation process in practice, which can impact the overall evaluation quality. A natural improvement strategy is to iteratively optimize the model based on feedback of evaluation results, which mainly comes from stronger models or directly from human evaluators’ correction of the evaluation results.

. To improve model performance and further benefit the final quality score calculation, this score framework collects failure modes of metric outputs, query GPT-4 on each failure mode to gather automatic feedback, and finally selects explanations most aligned with human preferences to iteratively fine-tune the LLaMA model. Unlike INSTRUCTSCORE which directly optimizes the model, the LLM evaluator in JADE

relies on human judges to correct LLMs’ evaluation results and updates the most frequently corrected samples into the example sets for few-shot prompting. JADE utilizes this relatively low-cost method to achieve iterative updates of the evaluation capabilities.

Since the feedback is more closely aligned with human preferences, LLM evaluators can dynamically align with human when optimizing evaluation capabilities based on this feedback, leading to better evaluation results. This feedback-based iterative optimization strategy address the problem of models’ imperfect generalization and improve the evaluation capabilities through dynamic updates.

Through the optimization based on in-context learning and the model’ own capabilities, LLMs have become fairly reliable evaluators which are capable of understanding evaluation task requirements and providing rational evaluation results. However, the inherent generation randomness within the black box of LLMs still introduces significant instability to the entire evaluation pipeline, affecting the overall evaluation quality. Therefore, optimization strategies during the post-processing stage from LLM evaluators’ outputs to final evaluation results are necessary. In this survey, these optimization strategies are categorized into three types: integration of multiple evaluation results, direct optimization of LLMs’ outputs, and conversion of evaluation tasks from pointwise evaluation to pairwise comparison.

Integration of Multiple Evaluation Results

Integrating multiple evaluation results for the same content to obtain the final result is a common strategy in various experiments and engineering pipelines, which can reduce the impacts of accidental factors and random errors. The most basic optimization strategy is to perform multiple runs of evaluation on the same content with different hyper-parameters and settings, and then summarize these results. For example the work of Sottana et al.

reduces randomness in evaluations by averaging multiple scores of the same sample. Similarly, PsychoBench

takes the mean and standard deviation from ten independent runs. Auto-J

further amplifies the differences between evaluation rounds, which combine critiques with and without scenario criteria to obtain the final results.

In addition to integrating results from multiple rounds of evaluation, using multiple LLM evaluators to assess the contents simultaneously and the integrating the results is another effective method, which can reduce biases introduced by LLMs. For instance, CPAD

as evaluators to evaluate the contents and obtain the final results by voting. Bai et al.

propose a novel evaluation method called decentralized peer review of LLMs, which utilizes LLMs that generate contents to evaluate each other’s generated contents and eventually integrate the results.

---

## LLM-as-Judge: Automated Evaluation | Neel Mishra

`https://neelmishra.github.io/blog/mlops/llm-evaluation/llm-as-judge.html`

LLM-as-Judge: Automated Evaluation | Neel Mishra

Human evaluation remains the gold standard for assessing open-ended LLM outputs — but it's slow, expensive, and hard to scale.

leverages a strong language model (the "judge") to score or rank outputs from one or more candidate models, giving you human-like signal at API-call speed.

Instead of hiring annotators, you craft a

that instructs a powerful model (e.g., GPT-4o) to evaluate responses on specific criteria — returning structured scores and explanations.

paper (Zheng et al., 2023), this approach showed GPT-4 judgments agree with human preferences >80 % of the time — comparable to inter-annotator agreement. Since then, LLM-as-Judge has become a standard tool in evaluation pipelines at OpenAI, Anthropic, and across the industry.

The judge prompt is the most critical component. A well-crafted prompt includes a

You are an expert evaluator. Your task is to assess

the quality of an AI assistant's response.

: Does the response address the user's need?

: Is the response well-structured and easy to follow?

: Does it cover all aspects of the question?

Rate the response on a scale of 1-5 for each criterion.

Provide a brief justification BEFORE the score.

"helpfulness":  {"reasoning": "...", "score": N},

"accuracy":     {"reasoning": "...", "score": N},

"clarity":      {"reasoning": "...", "score": N},

"completeness": {"reasoning": "...", "score": N},

Always ask the judge to provide reasoning

the numeric score. This "chain-of-thought" approach dramatically improves score reliability and reduces random variance.

"""Score a single response using GPT-4o as judge."""

Evaluate the response according to the rubric.

ensures deterministic, parseable output. For even stricter schema enforcement, use OpenAI's

There are two fundamental paradigms for LLM-as-Judge evaluation, each suited to different scenarios.

against a rubric. Returns an absolute score (e.g., 1–5).

Regression testing, threshold-based quality gates, tracking a single model over time.

Simple, parallelizable, absolute scores allow time-series comparison.

Score calibration can drift; harder to detect subtle quality differences.

and picks the better one (A, B, or Tie). Used in MT-Bench and Chatbot Arena.

Model selection, A/B testing, comparing prompt variants.

More reliable for relative ranking; easier for the judge model.

O(n²) comparisons for n models; susceptible to position bias.

Compare two responses to the same question.

Pick the better one: output "A", "B", or "Tie".

Output JSON: {"reasoning": "...", "verdict": "A"|"B"|"Tie"}

"""Pairwise comparison with position-bias mitigation."""

# Swap order randomly to reduce position bias

# Un-swap the verdict if we reversed the order

Real-world evaluation rarely collapses to a single score. Strong judge setups evaluate across

(question: str, response: str) -> EvalResult:

"""Evaluate across 4 dimensions with structured output."""

completion = client.beta.chat.completions.

Evaluate each dimension. For overall, use:

0.3*helpfulness + 0.3*accuracy + 0.2*safety + 0.2*coherence

MT-Bench uses multi-turn evaluation with two-turn conversations. The judge sees both turns and scores them independently, capturing the model's ability to follow up and refine answers — a dimension single-turn evals miss entirely.

LLM judges inherit systematic biases. Understanding and mitigating these is critical for trustworthy automated evaluation.

In pairwise evaluation, LLMs tend to prefer whichever response appears

. The standard mitigation is to run each comparison

with swapped order, then check for agreement:

"""Run pairwise eval in both orders, flag disagreements."""

# Normalize v2 verdict (un-swap already handled in function)

"Position-dependent — flag for human review"

Research shows GPT-4 prefers GPT-4 outputs by ~10 percentage points over equally-good Claude outputs. When the candidate model and judge model share the same family, consider using a

judge model or an ensemble of multiple judge models.

Add explicit rubric instructions to counter verbosity bias:

IMPORTANT: A concise, correct answer is ALWAYS preferred over

a verbose answer that adds unnecessary detail. Penalize

responses that pad their length without adding value.

Do NOT reward length — reward information density.

Multiple studies establish strong but imperfect correlation.

~80% agreement on pairwise preferences (MT-Bench)

~81% inter-annotator agreement (same benchmark)

LLM judges often can't verify complex reasoning chains

Judges may not catch subtle hallucinations

Medical, legal, and scientific claims need specialist review

Humor, tone, and style are poorly evaluated

"""Compute correlation metrics between human and judge scores."""

If your LLM judge achieves a Spearman ρ > 0.7 with human annotations on a calibration set of 100–200 examples, it's reliable enough for automated use. Below 0.6, invest in prompt tuning or switch judge models.

Moving LLM-as-Judge from notebooks to production requires batching, cost management, logging, and fail-safes.

"""Score one item with concurrency control."""

"""Run judge over a dataset with controlled concurrency."""

Judging 1,000 responses with GPT-4o at ~800 tokens per judge call costs roughly $4–8. For large-scale eval, consider using GPT-4o-mini for initial screening (10× cheaper) and reserving GPT-4o for borderline cases. Always log token usage per evaluation.

Every judge call should log: the item ID, judge model, prompt version hash, raw scores, token usage, latency, and timestamp. This enables:

— track mean scores over time after model or prompt changes

— alerting on parse errors or judge refusals

An uncalibrated judge may consistently rate too high or too low, or compress the score range. Calibration aligns judge scores with human expectations.

Collect 100–200 examples with human scores covering the full quality spectrum (including intentionally bad responses). This is your ground truth.

Score all calibration examples with your judge prompt. Compute Spearman ρ, Kendall τ, and pairwise agreement against human labels.

Adjust rubric wording, add few-shot examples of scored responses, and modify the scale (e.g., 1–5 vs 1–10). Re-run until correlation exceeds your threshold.

Periodically sample judge outputs for human review. Track score distributions — sudden shifts indicate model updates or prompt drift.

Including scored examples in the judge prompt significantly improves calibration. These "anchor" examples define what each score level means concretely:

Response: Seasons are caused by Earth's ~23.5° axial tilt.

As Earth orbits the Sun, different hemispheres receive

more direct sunlight. This tilt — not distance from the

Reasoning: Accurate, concise, addresses common misconception.

Response: Seasons happen because the Earth moves closer to

and farther from the Sun during its orbit.

Reasoning: Contains a common factual error. Distance from

the Sun is not the primary cause of seasons.

Response: The tilt of the Earth causes seasons.

Reasoning: Correct but too brief. Lacks explanation of the

mechanism (axial tilt relative to orbital plane).

The best judge prompts combine a clear rubric, chain-of-thought reasoning, structured output, and 3–5 few-shot examples with diverse score levels. This combination achieves the highest correlation with human evaluators — often within 2–3 percentage points of human inter-annotator agreement.

Open-ended text quality (summarization, Q&A)

Rapid iteration during prompt engineering

Exact-match tasks (use string metrics instead)

Mathematical correctness (use code-based verification)

Security/safety critical decisions (always include humans)

Tasks requiring real-world verification (fact-checking)

High-stakes deployment gates (use as signal, not sole decider)

---

## [2412.05579] LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods

`https://arxiv.org/abs/2412.05579`

[2412.05579] LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods

Computer Science > Computation and Language

), last revised 10 Dec 2024 (this version, v2)]

LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods

View a PDF of the paper titled LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods, by Haitao Li and 7 other authors

The rapid advancement of Large Language Models (LLMs) has driven their expanding application across various fields. One of the most promising applications is their role as evaluators based on natural language responses, referred to as ''LLMs-as-judges''. This framework has attracted growing attention from both academia and industry due to their excellent effectiveness, ability to generalize across tasks, and interpretability in the form of natural language. This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations. We begin by providing a systematic definition of LLMs-as-Judges and introduce their functionality (Why use LLM judges?). Then we address methodology to construct an evaluation system with LLMs (How to use LLM judges?). Additionally, we investigate the potential domains for their application (Where to use LLM judges?) and discuss methods for evaluating them in various contexts (How to evaluate LLM judges?). Finally, we provide a detailed analysis of the limitations of LLM judges and discuss potential future directions. Through a structured and comprehensive analysis, we aim aims to provide insights on the development and application of LLMs-as-judges in both research and practice. We will continue to maintain the relevant resource list at

60 pages, comprehensive and continuously updated

https://doi.org/10.48550/arXiv.2412.05579

View a PDF of the paper titled LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods, by Haitao Li and 7 other authors

Code, Data and Media Associated with this Article

arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community?

Which authors of this paper are endorsers?

---

## LLM-as-a-judge

`https://llm-as-a-judge.github.io/`

This is an initiative survey and paper list aiming to employ LLM as the judge for various applications

- In this work, we introduce ToolPRMBench, a benchmark for evaluating process reward models on tool-use reasoning.

Who's Your Judge? On the Detectability of LLM-Generated Judgments

- In this work, we propose and formalize the task of judgment detection and systematically investigate the detectability of LLM-generated judgments.

Preference Leakage: A Contamination Problem in LLM-as-a-judge

- In this work, we expose preference leakage, a contamination problem in LLM-as-a-judge caused by the relatedness of data generator and evaluator LLMs.

From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge

- In this survey, we delve into the details of LLM-as-a-judge, aiming to provide a comprehensive overview of LLM-based judgment, including judgment attributes, methodologies, applications and benchmarks.

ToolPRMBench: Evaluating and Advancing Process Reward Models for Tool-using Agents

Reward-guided search methods have demonstrated strong potential in enhancing tool-using agents by effectively guiding sampling and exploration over complex action spaces. As a core design, those search methods utilize process reward models (PRMs) to provide step-level rewards, enabling more fine-grained monitoring. However, there is a lack of systematic and reliable evaluation benchmarks for PRMs in tool-using settings. In this paper, we introduce ToolPRMBench, a large-scale benchmark specifically designed to evaluate PRMs for tool-using agents. ToolPRMBench is built on top of several representative tool-using benchmarks and converts agent trajectories into step-level test cases. Each case contains the interaction history, a correct action, a plausible but incorrect alternative, and relevant tool metadata. We respectively utilize offline sampling to isolate local single-step errors and online sampling to capture realistic multi-step failures from full agent rollouts. A multi-LLM verification pipeline is proposed to reduce label noise and ensure data quality. We conduct extensive experiments across large language models, general PRMs, and tool-specialized PRMs on ToolPRMBench. The results reveal clear differences in PRM effectiveness and highlight the potential of specialized PRMs for tool-using.

title={ToolPRMBench: Evaluating and Advancing Process Reward Models for Tool-using Agents},

author={Li, Dawei and Yao, Yuguang and Tan, Zhen and Liu, Huan and Guo, Ruocheng},

journal={arXiv preprint arXiv:2601.12294},

Who's Your Judge? On the Detectability of LLM-Generated Judgments

Large Language Model (LLM)-based judgments leverage powerful LLMs to efficiently evaluate candidate content and provide judgment scores. However, the inherent biases and vulnerabilities of LLM-generated judgments raise concerns, underscoring the urgent need for distinguishing them in sensitive scenarios like academic peer reviewing. In this work, we propose and formalize the task of judgment detection and systematically investigate the detectability of LLM-generated judgments. Unlike LLM-generated text detection, judgment detection relies solely on judgment scores and candidates, reflecting real-world scenarios where textual feedback is often unavailable in the detection process. Our preliminary analysis shows that existing LLM-generated text detection methods perform poorly given their incapability to capture the interaction between judgment scores and candidate content---an aspect crucial for effective judgment detection. Inspired by this, we introduce J-Detector, a lightweight and transparent neural detector augmented with explicitly extracted linguistic and LLM-enhanced features to link LLM judges' biases with candidates' properties for accurate detection. Experiments across diverse datasets demonstrate the effectiveness of J-Detector and show how its interpretability enables quantifying biases in LLM judges. Finally, we analyze key factors affecting the detectability of LLM-generated judgments and validate the practical utility of judgment detection in real-world scenarios.

title={Who's Your Judge? On the Detectability of LLM-Generated Judgments},

author={Li, Dawei and Tan, Zhen and Zhao, Chengshuai and Jiang, Bohan and Huang, Baixiang and Ma, Pingchuan and Alnaibari, Abdullah and Shu, Kai and Liu, Huan},

journal={arXiv preprint arXiv:2509.25154},

Preference Leakage: A Contamination Problem in LLM-as-a-judge (Accepted by ICLR 2026)

Large Language Models (LLMs) as judges and LLM-based data synthesis have emerged as two fundamental LLM-driven data annotation methods in model development. While their combination significantly enhances the efficiency of model training and evaluation, little attention has been given to the potential contamination brought by this new model development paradigm. In this work, we expose preference leakage, a contamination problem in LLM-as-a-judge caused by the relatedness between the synthetic data generators and LLM-based evaluators. To study this issue, we first define three common relatednesses between data generator LLM and judge LLM: being the same model, having an inheritance relationship, and belonging to the same model family. Through extensive experiments, we empirically confirm the bias of judges towards their related student models caused by preference leakage across multiple LLM baselines and benchmarks. Further analysis suggests that preference leakage is a pervasive issue that is harder to detect compared to previously identified biases in LLM-as-a-judge scenarios. All of these findings imply that preference leakage is a widespread and challenging problem in the area of LLM-as-a-judge.

title={Preference Leakage: A Contamination Problem in LLM-as-a-judge},

author={Dawei Li and Renliang Sun and Yue Huang and Ming Zhong and Bohan Jiang and Jiawei Han and Xiangliang Zhang and Wei Wang and Huan Liu},

From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge (Accepted by EMNLP 2025)

Assessment and evaluation have long been critical challenges in artificial intelligence (AI) and natural language processing (NLP). However, traditional methods, whether matching-based or embedding-based, often fall short of judging subtle attributes and delivering satisfactory results. Recent advancements in Large Language Models (LLMs) inspire the "LLM-as-a-judge" paradigm, where LLMs are leveraged to perform scoring, ranking, or selection across various tasks and applications. This paper provides a comprehensive survey of LLM-based judgment and assessment, offering an in-depth overview to advance this emerging field. We begin by giving detailed definitions from both input and output perspectives. Then we introduce a comprehensive taxonomy to explore LLM-as-a-judge from three dimensions: what to judge, how to judge and where to judge. Finally, we compile benchmarks for evaluating LLM-as-a-judge and highlight key challenges and promising directions, aiming to provide valuable insights and inspire future research in this promising research area.

title   = {From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge},

author  = {Dawei Li and Bohan Jiang and Liangjie Huang and Alimohammad Beigi and Chengshuai Zhao and Zhen Tan and Amrita Bhattacharjee and Yuxuan Jiang and Canyu Chen and Tianhao Wu and Kai Shu and Lu Cheng and Huan Liu},

journal = {arXiv preprint arXiv: 2411.16594}

---

## GitHub - rajavavek/RELIAB-J-LLM-as-a-Judge-is-Not-Enough: A reproducibility toolkit and benchmark framework for evaluati

`https://github.com/rajavavek/RELIAB-J-LLM-as-a-Judge-is-Not-Enough/tree/main`

GitHub - rajavavek/RELIAB-J-LLM-as-a-Judge-is-Not-Enough: A reproducibility toolkit and benchmark framework for evaluating the reliability of LLM-as-a-Judge systems across accuracy, consistency, bias, calibration, robustness, domain transfer, and rubric adherence. · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

You must be signed in to change notification settings

RELIAB-J: A Reliability Benchmark for LLM-as-a-Judge Evaluation

RELIAB-J is a reproducibility toolkit and benchmark framework for evaluating the reliability of large language models used as automated judges. The project supports systematic testing of LLM judges beyond aggregate accuracy by measuring multiple reliability dimensions, including accuracy, consistency, bias sensitivity, domain transfer, rubric adherence, adversarial robustness, and calibration.

This repository accompanies the manuscript “LLM-as-a-Judge is Not Enough: A Reliability Benchmark for AI Evaluation.” It provides the code, benchmark schema, sample data, prompt templates, perturbation operators, parser rules, metric implementations, bootstrap confidence-interval scripts, and reproducibility files needed to audit and reproduce RELIAB-J-style evaluations.

A reproducibility toolkit and benchmark framework for evaluating the reliability of LLM-as-a-Judge systems across accuracy, consistency, bias, calibration, robustness, domain transfer, and rubric adherence.

You can’t perform that action at this time.

---

## LLM-as-a-Judge Evaluation

`https://www.emergentmind.com/topics/llm-as-a-judge-evaluations`

LLM-as-a-Judge evaluations are a scalable paradigm that uses advanced language models to automatically assess and benchmark generative outputs.

These systems employ methodologies such as pairwise comparisons, rubric-based grading, and multi-agent debates to capture semantic and contextual nuances.

Challenges like bias, robustness, and reliability require improved calibration strategies and human-in-the-loop approaches to enhance operational performance.

) paradigm refers to the practice of deploying advanced LLMs to automatically evaluate, grade, or benchmark the outputs of other LLMs or generative systems. The paradigm has rapidly gained traction across natural language processing, code generation, multi-agent evaluation, and privacy-preserving NLP as an alternative to traditional reference-based or human annotation-based evaluation. Despite its scalability and cost-effectiveness, LLM-as-a-Judge introduces multifaceted challenges in terms of alignment, bias, robustness, generalizability, scoring reliability, and operational best practices.

1. Core Principles and Evaluation Frameworks

are conceived to provide scalable, consistent, and cost-efficient alternatives to manual human evaluation for diverse tasks where traditional metrics (like BLEU or ROUGE) fail to capture semantic, stylistic, or context-dependent nuances (

). The standard operating procedure involves:

Instructing an LLM to evaluate outputs (e.g., candidate answers, summaries, code, or privacy sensitivity labels), either by binary scoring, grade assignments, or pairwise preference comparison (

Utilizing various prompting methodologies: few-shot, chain-of-thought (CoT) elicitation, structured rubrics, or multi-dimensional personas (

Aggregating outputs into quantitative (numeric score) or qualitative (rationale/CoT explanation) feedback.

LLM-as-a-Judge frameworks are typically divided into:

: Judges compare multiple candidate responses, selecting the preferred output (

: Assigning a numerical grade or category to a single output.

: Instantiating several evaluator agents, each simulating a distinct

or evaluative dimension, often with an in-group debate for richer, multidimensional feedback (

A distinguishing feature is the scalability to large evaluation sets and the ability to create customized, human-aligned rubrics in domains where high-quality references are limited.

2. Reliability, Generalizability, and Judge Alignment

A central challenge in LLM-as-a-Judge is achieving reliable alignment with human evaluators across a variety of settings.

In domains with high inter-human agreement, only the largest and best models (e.g.,

, Llama-3 70B, Llama-3.1 70B) produce reasonable alignment scores with humans (e.g., Scott’s Pi ≈ 0.88), yet even these can diverge by up to 5 points on absolute rating scales (

). This effect is compounded in complex, open-ended, or subjective tasks.

achieve high in-domain accuracy (on data and protocols they were directly trained for) but dramatically underperform in out-of-domain evaluation scenarios, indicating overfitting to specific distributional or prompt patterns (

GPT-4 consistently displays higher robustness, adaptability, and generalizability across grading protocols, scoring schemes, and multi-turn dialogue, suggesting that adaptation to diverse evaluation tasks remains a major obstacle for fine-tuned or specialized judge models.

In expert domains (e.g., dietetics, mental health), agreement rates between

and human subject matter experts range from 60–68%, demonstrating a significant gap for specialized or knowledge-intensive evaluation (

). Notably, LLM judgement is often more closely aligned with lay user preferences than

yields Pearson correlation coefficients up to 0.85 versus humans—substantially outperforming traditional exact match and F1 metrics (0.17 and 0.36, respectively), while showing minimal

when the same model serves as generator and judge (

A plausible implication is that while LLM judges are viable complements to human evaluation and conventional metrics on well-specified tasks, expert-in-the-loop hybrid workflows are essential for high-fidelity or domain-critical applications.

3. Biases: Position, Length, Self-Preference, and Scoring

Bias is a pervasive concern in LLM-as-a-Judge systems. Empirical studies reveal:

: Judges may systematically favor responses based on order (primacy/recency preference), with the magnitude modulated by model family, context window, and candidate quality gap (

). Metrics such as repetition stability, position consistency, and preference fairness quantitatively characterize this [formulas specified in the original]. In pairwise code judging, simply swapping the presentation order of responses can lead to accuracy shifts exceeding 10% (

: LLM judges often prefer verbose, formal, or fluent outputs regardless of substantive quality—an artifact of

: An LLM-as-a-Judge may assign higher scores to outputs more "familiar" to its own policy, as measured by lower perplexity, creating bias towards its own generations—quantified by a fairness-inspired metric based on equal opportunity (

: Score sensitivity arises when changing prompt components such as rubric order, ID type (numeric vs. Roman), or reference answer quality. Even state-of-the-art judges (e.g., GPT-4o) exhibit fluctuations in correlation with human judgments (typically within 0.03, but up to 0.2 for smaller models) depending on these perturbations (

: Bandwagon effects, chain-of-thought biases, and verbosity amplify in collaborative debates but are somewhat mitigated in meta-judge aggregation schemes; explicit debiasing through normalization (e.g., PINE) shows promise in reducing scoring artifacts (

These findings collectively require practitioners to implement careful prompt design, rigorous pre- and post-processing (e.g., order randomization, rubric shuffling, explicit debiasing terms), and consider ensemble approaches to mitigate individual model or prompt-induced bias.

4. Robustness, Uncertainty Quantification, and Adversarial Vulnerability

Recent work reveals persistent vulnerabilities in LLM-as-a-Judge systems, particularly when facing

can be easily manipulated by adversarial prompt modifications such as

(escape characters, context ignoring, injected completions) or optimization-based attacks such as PAIR, which achieves high

(ASR) and large deviations from correct scores (

Robustness is highly sensitive to choice of prompt template—decomposed into discrete components such as role, instructions, evaluation criterion, and response format. Minor changes in phrasing or structure can swing vulnerability metrics and attack success rates (

Defense mechanisms include re-tokenization (e.g., BPE-dropout) and LLM-based detectors; each carries trade-offs in computational overhead and effectiveness, with JudgeLM-13B highlighted as a high-performing robust, open-source judge.

quantification via confusion matrices (analyzing log token probabilities over n² assessments) can yield a per-instance reliability indicator: judgments marked with "low uncertainty" correspond to notably higher accuracy—even up to 100% in some benchmarks—than baseline assessments or high-uncertainty cases (

Robustness in practical deployment is an open concern; for instance, composite attacks targeting commercial platforms (Alibaba PAI-Judge) can force severe misjudgment even with built-in defenses (

Statistical robustness to adversarial perturbations, variance in prompt component influence, and computationally efficient defenses remain central research questions for production-grade judge deployments.

5. Methodological Innovations: Human-Centric, Quantitative, and Multi-Agent Strategies

Contemporary directions extend LLM-as-a-Judge beyond naive model prompting:

: Structuring and visualizing evaluation rubrics, providing interactive iteration on small samples for criterion refinement, and maintaining transparency around LLM decision processes are essential for trust and reliability (

: Post-hoc regression or classification models (e.g., Least-Squares, Multinomial, Bradley-Terry-Luce) trained on LLM outputs and human scores offer statistically efficient and computationally light calibration, often outperforming supervised LLM fine-tuning while avoiding overfitting (

f(e, b; \theta) = (\phi(e) \oplus b)^\top \theta + c

combines base judge's qualitative embedding and score into calibrated predictions.

: Introducing synthetic "crowd" responses for deeper

and distillation produces more comprehensive chain-of-thought (CoT) explanations, boosting average evaluation accuracy by 6.7% across multiple benchmarks, and improving downstream

: Automated generation of domain-grounded personas (from external documents) and orchestrated debate with multiple

in frameworks like MAJ-EVAL enables multidimensional, stakeholder-aligned feedback. This outperforms both simple automated metrics and single-judge LLM evaluations in human-expert alignment on complex, real-world tasks (

: Varying rubric order, score IDs, and full-mark reference inclusion demonstrably affects score stability; nonstandard prompt designs occasionally outperform conventional templates (

in math, code, and instruction provide robust environments for stress-testing judge reliability, bias, and best practices (

6. Domain-Specific and Multilingual Considerations

Adoption of LLM-as-a-Judge in specialized or multilingual contexts is limited by further complications:

In software engineering, output-based LLM-judge methods obtain Pearson R up to 81.32 for code translation but perform poorly in code summarization, indicating task-dependent reliability (

). Pairwise pointwise comparisons are prone to order bias.

Multilingual evaluation is characterized by weak consistency across languages. Even state-of-the-art judges average

≈ 0.3, with much poorer performance in low-resource languages, and neither

nor scaling solves this; ensemble strategies provide moderate improvements in cross-language judgment consistency (

In privacy-preserving NLP, LLM judges can model global human privacy perception (high agreement with average human ratings), but outcomes are dependent on prompt structure and tend to skew toward more privacy-conservative ratings compared to diverse (and less consistent) human judgments (

This suggests that reliability, fairness, and calibration for LLM-as-a-Judge remain open areas in high-stakes, expert, and multilingual settings.

7. Best Practices and Future Research Directions

The emerging consensus is that LLM-as-a-Judge systems are most effective when used in conjunction with:

Rigorous prompt engineering, including order randomization, explicit rubric specification, and voting/ensemble aggregation across model families.

to adjust LLM-assigned scores, identify unreliable judgments, and align with human ratings (

Active mitigation of biases through debiasing frameworks (e.g., PINE), prompt perturbation analysis, and comprehensive benchmark testing (

Deployment of hybrid human-in-the-loop workflows for domain-specific or expert-level evaluation (

Integrated support for transparency, user-driven criterion refinement, and customizable evaluation pipelines (

analysis and continual benchmarking under attack and

Expanding and diversifying high-quality, task-specific evaluation datasets across domains, modalities, and languages (

Continued investigation into adversarial robustness, multidimensional and multi-agent approaches, cross-lingual consistency, and

is needed for the maturation of LLM-as-a-Judge as a reliable, general-purpose evaluation framework.

Definition Search Book Streamline Icon: https://streamlinehq.com

An Empirical Study of LLM-as-a-Judge for LLM Evaluation: Fine-tuned Judge Model is not a General Substitute for GPT-4

LLM-as-a-Judge: Reassessing the Performance of LLMs in Extractive QA

Human-Centered Design Recommendations for LLM-as-a-Judge

Multi-Agent-as-Judge: Aligning LLM-Agent-Based Automated Evaluation with Multi-Dimensional Human Evaluation

CodeJudgeBench: Benchmarking LLM-as-a-Judge for Coding Tasks

Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges

Limitations of the LLM-as-a-Judge Approach for Evaluating LLM Outputs in Expert Knowledge Tasks

Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge

Judging with Many Minds: Do More Perspectives Mean Less Prejudice?

Evaluating Scoring Bias in LLM-as-a-Judge

LLMs Cannot Reliably Judge (Yet?): A Comprehensive Assessment on the Robustness of LLM-as-a-Judge

Black-box Uncertainty Quantification Method for LLM-as-a-Judge

Crowd Comparative Reasoning: Unlocking Comprehensive Evaluations for LLM-as-a-Judge

Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as Test-Time Scaling Evaluators

Can LLMs Replace Human Evaluators? An Empirical Study of LLM-as-a-Judge in Software Engineering

How Reliable is Multilingual LLM-as-a-Judge?

LLM-as-a-Judge for Privacy Evaluation? Exploring the Alignment of Human and LLM Perceptions of Privacy in Textual Data

No one has generated a video about this topic yet.

No one has generated a whiteboard explanation for this topic yet.

Get notified by email when new papers are published related to

How does the LLM-as-a-Judge paradigm compare to traditional human evaluation methods?

What techniques are used to mitigate biases such as position and verbosity bias in these systems?

How do multi-agent evaluation frameworks improve the reliability of LLM-as-a-Judge assessments?

What are the primary challenges in aligning LLM-based judgments with expert human evaluations?

Find recent papers about adversarial robustness in LLM-as-a-Judge systems.

---
