# 🔎 Pesquisa: como-fazer-quiz-memoria-classificar

> Busca: `multiple choice distractor design, matching memory game, sorting categorization educational UX best practices children cognitive load`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Frontiers | Multiple-Choice Item Distractor Development Using Topic Modeling Approaches

`https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00825/full`

Frontiers | Multiple-Choice Item Distractor Development Using Topic Modeling Approaches

Multiple-Choice Item Distractor Development Using Topic Modeling Approaches

Centre for Research in Applied Measurement and Evaluation, Department of Educational Psychology, University of Alberta, Edmonton, AB, Canada

Writing a high-quality, multiple-choice test item is a complex process. Creating plausible but incorrect options for each item poses significant challenges for the content specialist because this task is often undertaken without implementing a systematic method. In the current study, we describe and demonstrate a systematic method for creating plausible but incorrect options, also called distractors, based on students’ misconceptions. These misconceptions are extracted from the labeled written responses. One thousand five hundred and fifteen written responses from an existing constructed-response item in Biology from Grade 10 students were used to demonstrate the method. Using a topic modeling procedure commonly used with machine learning and natural language processing called latent dirichlet allocation, 22 plausible misconceptions from students’ written responses were identified and used to produce a list of plausible distractors based on students’ responses. These distractors, in turn, were used as part of new multiple-choice items. Implications for item development are discussed.

Multiple-choice testing is one of the most enduring and successful forms of educational assessment that remains in practice today. Multiple-choice items are used in educational testing because they permit the measurement of diverse types of knowledge, skills, and competencies (

). Multiple-choice items are efficient to administer; they are easy to score objectively; they can be used to sample a wide range of content; they require a relatively short time to administer (

, claimed that selected-response items, like multiple choice, are the most appropriate item format for measuring cognitive achievement or ability, especially higher-order cognitive skills, such as problem solving, synthesis, and evaluation. He also stated that this item format is both useful and appropriate for creating exams intended to measure a broad range of knowledge, ability, or cognitive skills across many domains.

Because of these important benefits, multiple-choice items continue to have broad appeal and, hence, application in education, despite some potential disadvantages, such as guessing effects and unintentionally exposing students’ to wrong information. North American students take 100s of multiple-choice tests and answer 1000s of multiple-choice items as part of their educational experience.

reported that one-third of the United States use multiple-choice items exclusively for assessing 4th grade and 8th grade students’ math and reading skills. In higher education, a multiple-choice test is a common and widely used assessment format for measuring students’ knowledge, especially in introductory courses with a large group of students. Multiple-choice testing is also used extensively for international assessments. In the 2015 administration of The Trends in International Mathematics and Science Study (TIMSS), for example, half of the mathematics and science items used the multiple-choice format (

). In the 2015 administration of the Program for International Student Assessment (PISA), two-third of the items in reading, mathematics, and science assessments were multiple choice (

A multiple-choice item consists of a stem, options, and auxiliary information. The stem contains context, content, and/or the question the student is required to answer. The options include a set of alternative answers with one correct option and one or more incorrect options or distractors. Auxiliary information includes any additional content, in either the stem or option, required to create an item, including text, images, tables, graphs, diagrams, audio, and/or video. To answer a multiple-choice item, the student is presented with a stem and two or more options that differ in their relative correctness. Students are required to make a distinction among response options, several of which may be partially correct, in order to select the best or most correct option. Hence, the student must use her or his knowledge and problem-solving skills to identify the relationship between the content in the stem and the correct option. The incorrect options are called distractors because they are considered to be “distracting” to students with partial knowledge due to their plausibility to yield the correct option.

Creating multiple-choice items is a challenging task, particular when it comes to distractor development, because of the sheer volume of work that is required. For example, to create 100 multiple-choice items that consists of one correct option and four incorrect options, a content specialist has to create 100 stems and 100 correct options. The content specialist also needs to create 400 plausible but incorrect options. This challenge of distractor development is both daunting and, oftentimes, unsuccessful.

evaluated the distractors from four standardized multiple-choice tests. They evaluated the quality and plausibility of distractors based on the attractiveness of distractors. More specifically, they emphasized that plausible distractors should be able to attract more than 5% of the low-performing students, who failed to identify a correct answer. Based on such criteria, they found that only 8% of the items contained effective distractors.

To overcome the challenge of creating large numbers of effective distractors, researchers and practitioners have explored and implemented different strategies. The most common strategy focuses on a list of plausible but incorrect alternatives linked to common misconceptions or errors in thinking, reasoning, and problem solving (

claim that the most effective way to develop plausible distractors using misconceptions is to identify “common errors” elicited by a particular stem in the item prompt. These common errors serve as candidates for plausible distractors. Haladyna and Rodriguez state that common errors can be identified in two ways. First, they can be identified using the judgments of contents specialists who have a good understanding of teaching and learning within a specific content area and who can specify the common errors and misconceptions that arise when students learn a new topic or concept. Second, they can be identified by evaluating student answers to constructed-response item (i.e., an item that contains a stem by no options) where errors in reasoning, thinking, and problem solving are documented in the student’s responses. The second approach—extracting student responses from constructed-response items—is the preferred strategy for identifying common errors because it is based on the actual response processes from students rather than the expected response processes inferred from the judgment of content specialists about how students respond to test items. However, identifying and extracting common errors and misconceptions from the actual response processes is a daunting task because large amounts of response data must be processes and this data, in turn, must be classified accurately in order to identify outcomes that could be used as distractors.

The purpose of this study is to introduce an augmented intelligence approach for systematically identifying and classifying misconceptions from the students’ written responses that are pre-labeled for the purpose of creating distractors that can be used for multiple-choice items. Augmented intelligence is an area within artificial intelligence that deals with how computer systems can emulate and extend human cognitive abilities thereby helping to improve human task performance and to enhance human problem solving (

). It requires the interaction between a human and a computer system in order for the system to produce an output or solution. Augmented intelligence combines the human capacity for judgment with the ability of modern computing using computational analysis and data storage to solve complex and, typically, unstructured problems. Augmented intelligence can therefore be used to characterize any process or system that improves the human capacity for solving complex problems by relying on a partnership between a human and a machine (

We introduce and demonstrate an augmented intelligence method that can be used for distractor development using latent dirichlet allocation (LDA;

). LDA is a statistical model used in machine learning and natural language processing which identifies specific topics and concepts within written texts. Specific words are expected to appear in a written text more or less frequently given a particular topic. LDA can be used to capture this expected outcome in a mathematical framework by focusing on the number of times words appeared in written text for different topics. Using LDA, content specialists can identify actual misconceptions based on students’ response processes in order to create lists of plausible distractors.

Traditional Approach for Distractor Development

Distractors are one of the key components that affect the overall quality of multiple-choice items as well as the item’s statistical characteristics (

). Distractors are intended to distinguish between students who have not yet acquired the knowledge necessary to answer the item correctly from those who understand the content. Therefore, distractors in a multiple-choice item are designed to contain plausible but incorrect answers based on students’ common errors or misconceptions so that the option can measure students’ level of mastery in a specific content area (e.g.,

). Creating distractors using common errors and misconceptions result in multiple-choice items with increased diagnostic value as well as higher item quality (

claimed that common errors and misconceptions could be identified using two different approaches. In the first approach, content specialists create individual distractors by hand that contain these common errors and misconceptions.

recommended that content specialists mimic students’ problem solving processes by answering questions such as, “what is a common error for solving this problem?” and “what do students usually confuse this concept or idea with?” in order to identify plausible distractors. The most appealing aspect of this method lies in its practicality and ease of implementation. The distractors are created by content specialists familiar with the students and the content area to mimic the typical and the commons problems that are most likely to occur. While this approach is feasible, it is also based on three assumptions. First, plausible algorithms, rules, or sources of information can be specified by content specialists. Second, plausible but incorrect distractors can be produced using these sources. Third, the misconceptions identified by the content specialists from these sources are, in fact, the same misconceptions held by the students. Proper alignment of the assumptions is critical for creating distractors that measure students’ actual errors and misconceptions. Moreover, the alignment must occur for each distractor across every multiple-choice item. Using our earlier example, if a content specialist writes 100 multiple-choice items and each item contains five options (i.e., one correct option and four distractors), then the content specialist must identify 400 plausible but incorrect alternatives that satisfy these three assumptions.

In the second approach, students’ responses from existing constructed-response items are evaluated to identify common errors and misconceptions. That is, content specialists review students’ responses from constructed-response items to identify mistakes, errors, and misunderstanding and then classify these outcomes to create a compiled list of plausible distractors (e.g.,

). This approach addressed the inferential problem associated with the previous approach because it is based on actual student response data rather than judgments about expected response processes. In other words, approach two is data driven. Common errors and misconceptions identified using approach two come from the algorithms, rules, or sources of information used by students to produce incorrect answers. Unfortunately, the second approach suffers from the problem of practicality and ease of implementation because it is neither practical nor easy to use. As it is currently implemented, approach two is daunting because it entails a comprehensive review of students’ written responses using a manual process with the goal of identify common errors and misconceptions that occur consistently and systematically. It is also a process fraught with interpretive problems because identifying common errors and misconceptions that occur systematically can be a subjective task (e.g., what are the characteristics of a systematic misconception). And, despite the potential benefits of using a data-driven approach, practically also dictates that the item development process should be relatively quick and efficient, even when large number of multiple-choice items are required. This requirement is challenging to address using the second approach, especially when large amounts of written text are available from a constructed-response item.

To-date, limited research has been conducted to investigate the application of augmented intelligence for the purpose of distractor development. Researchers have explored the significance of using students’ misconceptions and common errors to create distractors. The approach used in these studies was based on identifying misconceptions using students written or verbal responses that, in turn, were manually categorize by content specialists to identify common errors and misconceptions (e.g.,

). As noted earlier, a data-drive approach using students’ responses is inherently beneficial for identifying the actual errors and misconceptions that students use when they produce incorrect answers. But it is also inherently limited because it is excessively time consuming and labor intensive to identify and classify errors from written text using a manual review process. To overcome this limitation, we introduce and illustrate a data-driven method for creating distractors based on student’s common errors and misconceptions using LDA.

Topic Modeling and Latent Dirichlet Allocation

Locating keywords and topics to understand text is a simple and effective way for humans to classify textual information. To gather information about certain topics, for example, we often start from generating one or two key words to locate relevant documents that share common topics. Unfortunately, this approach quickly becomes unmanageable for humans when the amount of textual information begins to increase. For example, having content specialists manually review 1000s of students’ responses to identify and then categorize common errors would be a time consuming and inefficient classification exercise.

To overcome this clustering challenge, topic modeling has been developed and used with machine learning and natural language processing algorithms to uncover the hidden topics in a document (

). These hidden topics can be identified without any pre-labeling, which means that topic models do not require pre-categorized or topic-labeled documents. In machine learning, these problems are described as an unsupervised learning approach, which means the structure of the problem includes targets or outputs which are unknown and hence the primary focus of learning is to understand the structure of the data. Therefore, in topic modeling, we attempt to identify hidden or unobserved target, topics, using the fully observed information, words.

If we assume that a sequence of words in a document is governed by the same unobserved topic, then we could simply compute the likelihood of a document to represent certain topic to determine the underlying topic of a document in an unsupervised setting. To find the common topics, topic modeling uses word occurrence information where certain words are expected to appear in a document more or less frequently depending on a particular topic. LDA is a generative probabilistic topic modeling algorithm (

), where each document is perceived as a mixture of several topics. Generative models take the information of how observed data was generated into account to build a model. Suppose, for instance, we have documents that were generated by complex procedures that are unknown.

Latent dirichlet allocation attempts to synthesize an approximated generation procedure and observed information (i.e., words) to uncover hidden topics, without any labels. Moreover, unlike other topic modeling approaches, LDA can not only produce interpretable topics and can handle unseen documents to assign topics. The generative process of LDA consists of three layers of sampling a topic distribution, sampling topics, and sampling words over topics. For example, after the number of words (or document length) and the number of topics are decided, a topic distribution is specified (e.g., 40% biology, 30% kinetics, and 30% psychology). Next, a topic is picked based on the topic mixture distribution and a word is picked based on the distribution over words corresponding to the topic. This process is then repeated until all the words are generated for each documents.

describes a graphical representation of the generative process of LDA.

A conceptual representation of latent dirichlet allocation (LDA).

Given this process, LDA attempts to explore the hidden topics in a document by computing a posterior distribution of the hidden variables given a document. Due to a large number of possible topic structures, computing the probability of certain words under a specific topic (i.e., the distribution over words corresponding to the topic) becomes impossible to compute. To address this problem, LDA uses a method called Gibbs sampling (

) where each word is randomly assigned in the document to one of the topics, which will provide the initial guess of the word-topic and word-document distribution. LDA assumes that all topic assignments except for the current word in question are correct, and then updates the assignment of the current word. This process is repeated to improve the assignment until a steady state is reached. Once the final assignment is identified, it is used to estimate the topic mixtures of each document.

Model Evaluation and Augmented Intelligence

While topic models can be used to extract meaningful and interpretable topic assignments, evaluating the final assignment is challenging using an unsupervised approach (

). Unsupervised learning tasks do not include pre-labeled targets. Instead human judgment is required to evaluate the practicality and usefulness of the topic modeling performance (

). For example, the practicality of the topic model could be evaluated using the “human-in-the-loop” augmented intelligence approach, where humans are asked to locate a randomly substituted word or topic (

). If the human can reliably tell which one is a random intruder, then we can say that the trained topic yields a coherent and discernible topic (

). In addition, intrinsic measures (i.e., statistical measures) should also be considered for model evaluation. Such measures help evaluate how well the model fits the observed data.

Log-likelihood evaluates the probability of the observed data, given the model (

). Thus, we can locate the best model by attempting to produce the highest log-likelihood measure. The Kullback-Leibler (KL) divergence measure focuses on measuring the divergence among the topic distributions. KL divergence explicitly focuses on evaluating how much information we lose when we choose a certain model, by computing the symmetric KL divergence between the distribution of variance in the topic-word distribution and the marginal topic distribution (

). Thus, the best model can be determined by locating the point where the KL divergence measure reaches the lowest value (

Previous research has been conducted to demonstrate the usefulness of LDA for different types of topic modeling assignments. In education, for example, LDA has been used to uncover topics for essay scoring purposes (

), implementing course recommendation systems (

). However, to our knowledge, LDA has never been used to identify students’ errors and misconceptions for the purpose of creating distractors that could be used to create multiple-choice items. Therefore, the purpose of the study is to describe a method for creating distractor by identifying students’ misconceptions using the LDA topic modeling approach. Unlike the traditional approach where content specialists were responsible for using their judgments to analyze and evaluate students’ responses in order to identify plausible misconceptions for distractors development, the current study provided a systematic and data-driven method to cluster students’ written responses with similar underlying concepts in order to locate common mistakes. Once clustered, these responses become the basis for creating plausible distractors.

An open source data set collected and released from the short-answer scoring competition called Automated Student Assessment Prize (ASAP) was used in the study

. As the data set is publicly available, ethical approval was not sought in the study. ASAP was held in 2012. The competition was designed to promote the capabilities of effective scoring system using automated essay scoring frameworks and to provide efficient classroom essay scoring tools for practitioners. The competition included two phases. The first phase focused on developing robust automated scoring frameworks for relatively long responses (up to 650 words). The second phase focused on scoring short responses (up to 50 words). Both the competitions significantly contributed to promoting open and rigors model development for automated essay scoring (

For the short-essay scoring competition, 10 data sets were released and each data set was generated from a single prompt. The responses were produced by students in grade 10. Each data set was based on a unique prompt in different disciplines, such as Language Arts, Biology, and Science. All the responses were pre-labeled, scored by two human-raters. The current study used data set six from Biology to demonstrate the proposed method. This data was chosen to demonstrate the proposed method for three reasons. Fist, the current method requires pre-labeled data set and the data set six consisted of the resolved-score (or final score) based on the agreement of the two human raters. Second, the prompt required students to respond using multiple answers thereby producing a variety of diverse responses from a single prompt. In addition, the original constructed-response prompt could be easily reformatted into a multiple-choice stem.

More specifically, we used 1,515 responses from the original training set, where students were asked to list and describe three processes used by cells to control the movement of substances across the cell membrane (see

). The particular number of training responses were selected based on the score assigned by two independent human raters. The final score corresponded to the number of correctly identified answer and we only selected the responses where students failed to identify any correct answer (i.e., score 0), as the focus of this study is on extracting common errors and misconceptions.

Distractor Development Stage 1: Data Preparation

To achieve clear and interpretable clusters of topics, pre-processing is required. First, all of the misspelled words were corrected. Second, words were converted into lower cases and lemmatized using the Python NLTK library (

). Lemmatization is the process of grouping the words together so they can be analyzed as a single item based on their dictionary form. For example, the words ‘studies’ and ‘studying’ would be lemmatized into ‘study.’ Third, digits, non-alphabetic words (e.g., #, %, &, @), and stop words (e.g., a, and, but, how) were removed and all punctuation was specified as a separate word. Fourth, responses were separated into sentences allowing each sentence to be denoted as a separate topic.

Pre-processing is also focused on spelling correction using a combination of several approaches. We used the word embedding-based model for spelling correction. Word embedding-based models use the semantic similarities of words to determine the best candidate of a misspelled word (

). We used a list of words provided in the pre-trained GloVe embedding (

), which were trained on six billion words from Wikipedia 2014 and Gigaword 5. We attempted to locate the best candidate of an incorrect word from the Glove embedding word list based on a cosine-similarity score. Using the embedding-based spell correction, we could successfully correct more than 95% of the misspelled words, while some of the remaining misspelled words that could not be fixed with the methods were correctly manually. This approach was chosen after attempting existing spell checkers in Python and the correction results were relatively lower than expected (e.g., NLTK edit-distance with 78% correction). Such cases often included words that were significantly malformed, thus, providing very limited resemblance with a correct form.

Distractor Development Stage 2: Topic Clustering and Cluster Evaluation

The LDA model was constructed using the Python library lda 1.0.5. To generate clear and interpretable clusters of topics, model training and evaluation took place simultaneously. To enable flexible and robust learning, it is necessary to identify the ranges of several model parameters so the model with the optimum range can be identified. For example, the number of topic groups must be specified before training begins. The number of Gibbs sampling iteration must also be specified to train the model. To begin, the number of topics and sample iterations ranged from 1 to 50 and up to 800 iterations, respectively. These ranges were selected so that we can extract as many potential misconceptions as possible with a stable estimation. We set our initial range of the number of topics as a relatively large number, 50, so that the model could conduct a comprehensive categorization of common errors and misconceptions. In terms of the number of iterations, we evaluated the negative log-likelihood of the model at every 10 iterations and inspected whether a significant decrease or increase in log-likelihood occurred. The significance was evaluated based on a chosen tolerance value of 0.5. The results indicated that log-likelihood stabilized around 800 iterations. The performance of our initial model was evaluated using the perplexity measure. Perplexity is a commonly used topic-model measure that is computed by dividing a negative log-likelihood by the number of words (see

). As the name suggests, perplexity provides the degree of ‘uncertainty’ or ‘confusion’ the model has in assigning probabilities to text. Therefore, we could determine the optimal number of topics by locating the model with the lowest perplexity.

Then, the topic clusters were visualized to evaluate the clustering. Topic clusters were projected in a two-dimensional space by computing the distance between topics using t-distributed stochastic neighbor embedding (t-SNE). T-SNE is a dimensionality reduction algorithm for high-dimensional data visualization. The idea of t-SNE is to find a probability distribution that is a function of the smallest number of coordinates and to create a similar distribution function to reduce the dimensionality. Assume that we want to calculate the probability of finding two points i and j at the squared Euclidean distance between the points, ||

. T-SNE attempts to match the distribution using a Student’s-

distribution, while attempting to learn the

) in the lower dimension. If the visualized clusters are significantly overlapping and malformed, then the number of topics should be adjusted. In addition, the KL divergence was used as an evaluation criterion for the visualization because it helps determine the similarity of the two distributions. The learning algorithm attempts to create a clear visualization of distinctive topic clusters while minimizing KL divergence to locate the optimal model. To do so, several adjustments were necessary to determine the number of iterations, the learning rate, and the perplexity rate. While the number of iterations and the learning rate determines the efficiency and accuracy of model learning through controlling for the weight adjustments, the perplexity rate controls for the effective number of cluster neighbors. Finally, interpretability of the clusters was evaluated by summarizing the clustered sentences using the Python library genism summarization. Gensim summarization conducts a text rank-based summarization using a variation of the TextRank algorithm (

). TextRank attempts to construct a graph from a document, where sentences (or nodes) are connected with each other via edges. Edges represent the similarity between the sentences, which are often computed based on the word overlap between the two sentences. TextRank hypothesizes that the most important sentence in a text as the one that is the most frequently connected in a graph. We chose this approach as previous studies have demonstrated relatively good performance using the method, while it does not require any manual annotation (

). The summaries were created so that content specialists could effectively evaluate the plausibility of the extracted common errors and misconceptions.

In the study, we refer to content specialists as the experts who are experienced in item writing in particular subjects. With this type of content expertise, validating the plausibility of summarized common errors and misconceptions could improve the quality of distractors which are generated from each topic cluster. To do so, content specialists could discuss and attempt to identify where each misconception originated from. For example, if the content of a cluster includes morphologically or phonetically similar words with correct answers, the specialists could conclude that the misconception originated from the confusion in recalling certain terminologies or associating a term with a correct definition. Also, content specialists could be encouraged to answer more concrete questions to evaluate the quality of clusters. Such questions could include, “How many of the clusters do you find meaningful?” and “Is the cluster describing a commonly well-identified misconception regarding the topic?” This would help content specialists to evaluate distractors thoroughly, while providing important information to evaluate the capacity of the current system.

Distractor Development Stage 3: Item and Distractor Formation

In stage 3, content specialists formulate distractors using the common errors and misconception clusters identified in the previous stage. We propose several methods that could promote more systematic distractor development using students’ misconceptions. The distractor generation process can be distinguished based on the question type (or stem) that content specialists pose regarding a topic. First, the content specialists could decide to change the format of the original question from the constructed-response item to a multiple choice item format, while attempting to measure the same construct of interest (e.g., which of the following procedures is correct about cell movement?). In this case, we could use the cluster summarizations and the key words and phrases directly. In stage 2, we explored how each misconception cluster can be represented using key words and summarization. Thus, using key words or summarized sentences as distractors would be able to attract students with different levels of understanding effectively. Alternatively, content specialists could develop a question that focuses on specific sub-concepts of a topic. Active- or passive-transport could be good examples of sub-concepts to evaluate, that is closely associated with the original question. In this case, distractors could be directly located based on students’ responses from the cluster, where students appeared to have trouble understanding the concepts of active- and passive-transport. We will present how the two methods can be utilized more thoroughly using examples in the next section.

Generating distractors using students’ misconceptions have been identified as one of the most effective way in developing multiple-choice items (

). However, with our augmented intelligence approach, which require content specialists’ judgment in the evolution process, we believe the effectiveness of distractors could still significantly depend on the content specialists judgments. Therefore, while we encourage further studies on the effectiveness of the distractors generated using the proposed methods, it was out of our scope of research to provide empirical results on behaviors of distractors in a real test setting. We will discuss such concerns more thoroughly in the limitation section with several suggestions for future research.

Topic Clustering and Cluster Evaluation Results

In the original constructed-response item, students were asked to provide three correct responses to the following item: “List and describe three processes used by cells to control the movement of substances across the cell membrane.” The results indicated that the optimal LDA model identified 22 common misconceptions. The number of topic clusters were selected based on the log-likelihood measure as well as the KL divergence. The model achieved a perplexity of 34.76 after 800 iterations and the lowest KL divergence of 40.50 with 22 topics. As discussed earlier, the log-likelihood measure provides the probability of the observed data given the model (

In addition, the interpretability and plausibility of each topic cluster was evaluated using extracted key words and summaries. A full list of topic key words and summaries can be found in Appendix

. Six to eight topic key words were used for each topic cluster. They were chosen based on the strength of association to represent the topic cluster and the strength was measured by weights assigned to each word. In addition, summaries were generated for each cluster to increase their interpretability. This information was designed to help the content specialists to interpret students’ common errors and misconceptions and to evaluate the representativeness of the clusters to form plausible distractors. For example, topic 20 included several key words, such as ‘mRNA,’ ‘RNA,’ ‘tRNA,’ ‘DNA,’ ‘information,’ ‘translation,’ ‘transcription,’ and ‘messages.’ Content specialists formed their initial impression on each misconception based on these key words. In addition, by reading the summary which states “mRNA carries messages from the nucleus to other organs tRNA transports DNA to places with in the cell rRNA,” content specialists can understand specific contexts and associations among the key words more thoroughly so they can make more informed decision about whether the cluster could be used to create a plausible distractor which represents a common error or misconception.

A set of distractors were generated using the evaluated clusters of students’ common errors and misconceptions. In addition to create distractors for the originally proposed item, where students were required to describe three processes used by cells to control the movement of substances across the cell membrane, we explored the capacity of the current method in generating distractors on additional cluster-specific items. The following examples introduce a step-by-step breakdown of the distractor generation procedures.

Example 1: Generating Distractors for the Original Prompt

, a multiple-choice item was created from the original constructed-response item. Reflecting the original prompt, the stem was changed to “What are the three processes used by cells to control the movement of substance across the cell membrane?” To generate distractors that could each reflect different common error and misconception, the list of options was created by locating students’ responses with key words from the stem, such as ‘processes,’ ‘movement,’ or ‘substances’ from each misconception topic cluster. More specifically, the option

), where students describe the movement of flagellum as part of the movement of substances across the cell membrane. In this example, the correct answer is i, while the other options were produced to represent students’ misconceptions.

An example question and distractors generated for the original prompt.

Example 2: Generating Distractors Using Additional Prompts

, the proposed method could be extended to generate distractors for cluster-specific items. Cluster-specific items refer to items that are generated to further evaluate students’ understanding that reflect the misconceptions captured in a particular content cluster. For example,

introduces two cluster-specific items, which were posed based on students’ responses in cluster 2 (see Appendix

). In cluster 2, students had trouble correctly explaining and distinguishing between the two concepts of active and passive transports. Therefore, to evaluate students’ understanding on active and passive transport, two additional multiple-choice stems were created: “Which of the following is true about active transport?” and “Which of the following is true about the passive transport?” To generate distractors for the cluster-specific items, we implemented the same process where the key words and phrases (i.e., active transport, passive transport) were used to locate students’ responses that included these key terms. Unlike the first example, the distractors were only located among the responses in cluster 2 as the items were created based on cluster 2. The correct option is

Example questions and distractors generated for the sub-topics of the original prompt.

The recent introduction of different applications of augmented intelligence in educational assessment have brought about dramatic changes in the field by promoting efficient new test development and administration procedures (

). Augmented intelligence, which is a branch of artificial intelligence, helps content experts broaden their capabilities and make more informed decision in a timely manner with appropriate technological support. For instance, with a machine-aided scoring system, experts can score essays more efficiently because the machine can be used to help distinguish problematic essays that fail to map onto a scoring rubric from more coherent essays. Currently, little research has been conducted to investigate the application of augmented intelligence in item development, especially as it relates to creating distractors. Effective distractors can attract students with a partial understanding, in other words, discriminating students who have not yet reached the mastery level of comprehension regarding the concept. Thus, generating effective distractors is directly associated with increasing the quality of an item and its characteristics (i.e., item difficulty and discrimination;

). Studies have been conducted to explore the significance of using students’ misconceptions and common errors to create distractors (e.g.,

). Misconceptions are typically gathered using students written or verbal responses on similar or connected topics and content experts manually categorize and identify plausible misconceptions using the written response evidence (

). In other cases, content experts attempt to mimic students’ thought processes in order to identify plausible errors (

). However, these approaches are unfeasible when large numbers of items must be created. To overcome this limitation, we introduced and illustrated a data-driven method for generating distractors based on misconceptions from students’ written responses using the workflow presented in

A comprehensive framework of the distractor generation process.

It is important to acknowledge that the current methods attempt to incorporate both machine- or data-driven and experts-driven approaches harmoniously in every stage. While the data-driven approach provides prominent benefits in facilitating a systematic and effective distractor generation process, we believe the intervention from experts could help improving the system, behaving as a gatekeeper for quality insurance of the final product, distractors. Especially in educational assessments, content experts’ decisions are often considered a reference or gold-standard in making the ultimate high-stakes decisions. The steps in

workflow were used to identify 22 distinct clusters of common errors and misconceptions using students’ written responses from a constructed-response item in Biology. In the first data processing stage, we primarily used the data-driven approach to pre-process the responses (e.g., lemmatization, tokenization, remove punctuations, and non-alphabetic words). Also, while we corrected the majority of misspelled words using the embedding-based approach, it was still required to conduct a few manual corrections. In the response analysis stage, clusters were created automatically using a topic-modeling approach, then, content experts were required to evaluate the interpretability and plausibility of the extracted clusters, the information was used to generate a list of 22 plausible distractors that, in turn, helped create a parallel multiple-choice item. A parallel multiple-choice item refers to an item originally presented as a constructed-response task that has been reformatted into a selective-response task. The quality of generated distractors can be further empirically evaluated by pilot testing in a classroom evaluation setting and we will discuss more details about the evaluation of item characteristics in the next section.

The current study has implications for distractor writing practices, specifically, and item development, more generally. Topic modeling allows content experts to use student responses in a more adaptive and productive way. Written responses represent an enormous source of valuable information about students’ understanding, which is not only related to the construct of interest, but also to misconceptions about that construct. To-date, little effort has been spent exploring the use of machine learning methods for gathering and using information about misconceptions that can be found is students constructed responses. Using the method described and illustrated in this study, researchers and practitioners can now use the written responses gathered in assignments and tests to plan future lessons and to create more student-adapted learning activities and assessments. The method can also be used to provide evidence for students’ developmental level of understanding about certain concepts. For example, by analyzing the responses from the higher-ability group and compare the misconception clusters with the ones from the lower-ability group, more in-depth information can be gathered to create a comprehensive picture of how students’ level of understanding develops on specific concepts and within specific content areas.

Distractor Development and Item Generation

Potentially the most important future application of this method resides in its application to automatic item generation (AIG;

). AIG is a relatively new but rapidly evolving research area where cognitive and psychometric modeling practices guide the production of tests that include items generated with the aid of computer technology.

) developed a three-step process for AIG. In step 1, content specialists create a cognitive model for AIG.

Currently, distractor development poses a unique and consequential problem in AIG in the step 2 item modeling stage. For the selected-response format, items must not only include a stem with a corresponding correct option, but also include a set of distractors. Distractors in AIG are typically designed from a list of plausible but incorrect alternatives linked to misconceptions identified by content specialists. Because AIG produces 100s of items, strategies are needed to create a correspondingly large number of plausible but erroneous distractors. Distractor development for AIG is now guided by the distractor pool method with random selection (

). To identify the content for the distractors, content specialists identify a list of plausible but incorrect options that are appropriate for all possible items generated with a given item model. Then, distractors are randomly selected from this pool of plausible but erroneous content and added to each generated item. This method is based on the assumption that a pool of plausible distractors can be created. A sample of these plausible distractors are selected at random to complete the item generation process. The strength of this method is its simplicity. This method can yield large numbers of distractors. The weakness of this method resides with the strong assumption that all pooled distractors are equally plausible and appropriate for all generated items. Equal plausibility and appropriateness is strong and, in many cases, restrictive assumption. Also, there is little reasoning to guide how distractors are paired with the correct option because pairing is achieved with random assignment.

To improve the plausibility and appropriateness of the distractors, rules, and rationales that yield errors or misconceptions can be used to create distractors. Distractor rationales are short descriptions that specify the reasoning which underlies each option. These rationales are currently provided by content specialists. But the rules can also be created using the method presented in our study to produce distractors that conform to specific, empirically-based, student misconceptions. Hence, distractors can be created systematically so that each distractor matches a rationale. This proposed approach could be called the

systematic generation with rationales method

. It would be based on the assumption that algorithms, rules, and procedures can first be articulated by content specialists and then used to create plausible but incorrect alternatives linked to students’ actual misconceptions or errors in thinking, reasoning, and problem-solving. The strength of this method is that the distractors are much more specific and, hence, plausible and appropriate, especially when compared to the distractor pool method with random assignment. Hence, integrating the outcomes from the topic modeling methods presented in this paper with new developments in AIG should be considered an important area of future research.

Even though the study was carefully designed and structured to minimize potential error with results and further interpretations, we found the three key limitations that should be addressed and carefully considered for future research: the main purposes of our study were to introduce a novel method of identifying students’ misconceptions in a systematic manner to encourage efficient distractor generation for multiple-choice item development. Thus, our study could not investigate the item behaviors with generated distractors in a real test setting. Investigating the item behaviors in relation to the distractor quality would help us further understand the importance of item development with well-performing distractors. For example,

demonstrated how the plausibility of distractors significantly affects item characteristics (e.g., item discrimination) in classroom assessment. Therefore, we encourage future researchers to evaluate the plausibility and effectiveness of the generated distractors to explore the significance of our proposed method thoroughly. Second, our current method required labeled responses to identify students’ responses with incorrect answers. Scoring students’ responses manually can be a very expensive and tedious procedure, especially in a large-scale assessment. However, as the current method attempts to extract students’ misconceptions that could be located from their incorrect responses, it is necessary to score or use pre-labeled data set to properly implement the proposed method. This could somewhat limit the usability of the proposed method as locating domain specific and pre-labeled data can be a daunting challenge. However, we believe such limitations can be readily overcome by using automated essay scoring systems (see

) to generate labeled responses in advanced to implement the current method. Last, augmented intelligence approach of our method aim to create a systematic method to distractor development supporting content experts to make informed decisions using misconception clusters. Therefore, it is important to investigate whether content specialists, indeed, feel supported to make informed decisions in creating distractors. We encourage future research to carefully evaluate the affective factors of content experts in using this method to fully evaluate the capacity of the current method.

JS, QG, and MG contributed in conceptualization and formalization of research ideas of the study. JS located and organized the data. JS and QG performed the analysis. JS and MG wrote the first draft of the manuscript. All authors contributed to manuscript revision, read and approved the submitted version.

The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

The Supplementary Material for this article can be found online at:

https://www.frontiersin.org/articles/10.3389/fpsyg.2019.00825/full#supplementary-material

Online courses recommendation based on LDA

Proceedings of the Symposium on Information Management and Big Data - SIMBig

On finding the natural number of topics with latent dirichlet allocation: some observations

Proceedings of the Pacific-Asia Conference on Knowledge Discovery and Data Mining

Distractor similarity and item-stem structure: effects on item difficulty.

Variations of the similarity function of textrank for automated summarization.

Uncovering students’ misconceptions by assessment of their written questions.

Natural Language Processing with PYTHON: Analyzing Text with the Natural Language Toolkit.

Diagnostic assessment with ordered multiple-choice ite

A density-based method for adaptive LDA model selection.

Constructing Written Test Questions for the Basic and Clinical Sciences

Reading tea leaves: how humans interpret topic models

Proceeding of the 23rd Annual Conference on Neural Information Processing Systems

Strength in Numbers: State Spending on K-12 Assessment Systems.

https://www.brookings.edu/research/strength-in-numbers-state-spending-on-k-12-assessment-systems/

Writing multiple-choice questions for continuing medical education activities and self-assessment modules.

A cognitive diagnosis model for cognitively based multiple-choice options.

Examination of the quality of multiple-choice items on classroom tests.

Selected-response item formats in test development

Developing, analyzing, and using distractors for multiple-choice tests in education: a comprehensive review.

Automatic Item Generation: An Introduction. Automatic Item Generation: Theory and Practice.

Using automated processes to generate test items.

Developing and Validating Multiple-Choice Test Items

Validity of a taxonomy of multiple-choice item-writing rules.

How many options is enough for a multiple-choice test item?

Relationship between types of distractor and difficulty of multiple-choice vocabulary tests in sentential context.

Topic Model Evaluation in Python with Tmtoolkit.

https://datascience.blog.wzb.eu/2017/11/09/topic-modeling-evaluation-in-python-with-tmtoolkit/

Using automatic item generation to improve the quality of MCQ distractors.

Impact of semantic similarity to training responses on automated scoring accuracy.

Paper presented at the Annual Meeting of the National Council on Measurement in Education

Proceedings of the 2004 Conference on Empirical Methods in Natural Language Processing

New guidelines for developing multiple-choice items.

Guidelines based on validity criteria for the development of multiple choice items.

Application of sentiment and topic analysis to teacher evaluation policy in the US

Proceedings of the 8th International Conference on Educational Data Mining

Developing the TIMSS advanced 2015 achievement items

Adaptive spelling error correction models for learner english.

PISA 2015 Results (Volume I): Excellence and Equity in Education.

Heading toward artificial intelligence 2.0.

Glove: global vectors for word representation

Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP)

Exploring the impact of artificial intelligence on teaching and learning in higher education.

Fast collapsed gibbs sampling for latent dirichlet allocation

Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining

Handbook of Accessible Achievement Tests for all Student: Bridging the Gaps Between Research, Practice, and Policy

State-of-the-art automated essay scoring: competition, results, and future directions from a United States demonstration.

Contrasting state-of-the-art in the machine scoring of short-form constructed responses.

An assessment of functioning and non-functioning distractors in multiple-choice questions: a descriptive analysis.

Guide to developing high-quality, reliable, and valid multiple-choice assessments.

Assessment: Issues and Challenges for the Millennium

Hybrid-augmented intelligence: collaboration and cognition.

List and describe three processes used by cells to control the movement of substances across the cell membrane.

Selective permeability is used by the cell membrane to allow certain substances to move across.

Passive transport occurs when substances move from an area of higher concentration to an area of lower concentration.

Osmosis is the diffusion of water across the cell membrane.

Facilitated diffusion occurs when the membrane controls the pathway for a particle to enter or leave a cell.

Active transport occurs when a cell uses energy to move a substance across the cell membrane, and/or a substance moves from an area of low to high concentration, or against the concentration gradient.

Pumps are used to move charged particles like sodium and potassium ions through membranes using energy and carrier proteins.

Membrane-assisted transport occurs when the membrane of the vesicle fuses with the cell membrane forcing large molecules out of the cell as in exocytosis.

Membrane-assisted transport occurs when molecules are engulfed by the cell membrane as in endocytosis.

Membrane-assisted transport occurs when vesicles are formed around large molecules as in phagocytosis.

Membrane-assisted transport occurs when vesicles are formed around liquid droplets as in pinocytosis.

Protein channels or channel proteins allow for the movement of specific molecules or substances into or out of the cell.

Cell, osmosis, water, diffusion, membrane, process, permeable, moving

Three processes used by cells to control the movement of substances across the cell membrane are being selectively or semi permeable, osmosis, and diffusion

Transport, active, diffusion, passive, osmosis, processes, facilitated, type

Three types of controlled movement of substances across the cell membrane include passive transport, active transport, and diffusion

Cell, substance, membrane, way, moves, cytoplasm, goes, organism

Another one is where the organism extends out sections of its cell membrane and fills it with cytoplasm while the opposite end goes away and it moves by a crawling type movement

Cells, blood, body, make, flow, need, brain, send

The movements of substances across the cell membrane flow through the blood streams

Cell, membrane, wall, help, nucleus, things, outside, inside

Three processes used by cells to control the movement of substances across the cell membrane is flagella which helps the cell get through the membrane, the nucleus that is the control center, and the cell wall to protect the cell from any unwanted cells or anything unwanted

Cell, waste, food, gets, stuff, nutrients, needed, needs

The Golgi bodies help by getting rid of stuff not needed in the cell

Protein, proteins, cell, enzymes, synthesis, channel

The cell uses three basic processes for movement across the membrane one is the flagellum, another cytoplasm and finally the protein in the ribonuclease acid

Cell, membrane, movement, control, substances, helps, plasma, different

Pores in the membrane allow substances in and out of the cell and Golgi body helps transport substances in and out of cell

Cells, use, proteins, way, membrane, ribosomes, carry, proteins

Cells use vesicles, transport chains, and proteins to control the movement of substances across the cell membrane

Cell, substance, membrane, diffusion, concentration, substances, movement, uses

Osmosis is the movement of water going from a low concentration to a high concentration in the cell membrane

Golgi, nucleus, proteins, apparatus, ribosomes, reticulum, endoplasmic, use

The ribosomes produce the energy for the cell the Golgi apparatus gets rid of waste and the nucleus hold all the information and DNA

Cell, things, wall, membrane, inside, getting, substances, lets

Cell wall makes the plant cell stiff but also keeps out unwanted items or organism’s cell membrane lets things in and out of the cell with permission from the nucleus and chloroplast help the plants maintain energy

Like, flagellum, flagella, use, cilia, cell, helps, help

One way of movement is the use of flagellum which is a long tail like structure the moves behind the cell

Cells, substances, use, process, place, organelles, moving, help

Another processes but which cells use to control the substances that cross the cell membranes are the phospholipids that line that cell wall these help keep unwanted thing out as well

Movement, cells, control, used, cell, processes, substances, membrane

Three processes that cells use to control the movement of substances across the cell membrane is protein synthesis, transfusion, and moving waste out

Cells, mitosis, meiosis process, reproduce, make, makes, meiosis

Another processes but which cells use to control the substances that cross the cell membranes are the phospholipids that line that cell wall these help keep unwanted thing out as well

Cell, controls, membrane, nucleus, goes, wall, tells, comes

The cell uses three processes by the names of meiosis, mitosis, and cell reproduction

Cell, uses, energy, things, membrane, moves, mitochondria, endocytosis

The nucleus controls everything and the mitochondria tell what enters and leaves the cell

Respiration, cellular, reproduction, photosynthesis, process, food, division, homeostasis

Endocytosis which is part of active transport, where the cell uses energy to pull items through the selectively permeable membrane

mRNA, tRNA, RNA, DNA, information, translation, transcription, messages

---

## Multiple Choice Distractor Design: How to Write | SimpleQuizMaker

`https://simplequizmaker.com/blog/multiple-choice-distractor-design`

Multiple Choice Distractor Design: How to Write | SimpleQuizMaker

Multiple Choice Distractor Design: How to Write Wrong Answers That Work

Cognitive Psychology Writer & Study Skills Coach

Why distractors matter more than the right answer

How to evaluate your existing distractors

A quick decision framework for writing distractors under time pressure

Common mistakes that undermine otherwise good distractors

Worked example: turning a weak item into a strong one

A multiple-choice question is only as good as its wrong answers. Plausible distractors test knowledge; obvious distractors test elimination. Three patterns produce strong distractors: common student misconceptions, partially correct statements, and confusable adjacent concepts. Random wrong answers are the most common — and most damaging — mistake.

Why distractors matter more than the right answer

In a four-choice question, the test-taker has a 25% chance of guessing correctly. That floor moves up dramatically based on

A question with three obvious distractors tests *recognition of obviously wrong answers*, not knowledge of the right one. It's a question that grades nothing.

The rule of thumb in assessment design: spend more time writing your distractors than your correct answer.

Pattern 1 — Common student misconceptions

The strongest distractor is the answer a student *would* give if they confused two related concepts.

Question: "What gas do plants release during photosynthesis?"

Weak distractors: nitrogen, hydrogen, methane (random gases).

Strong distractors: carbon dioxide (the *input*, commonly confused with output), water vapor (a related but distinct exchange), nitrogen (a real plant intake confusing with photosynthesis).

The student who picks "carbon dioxide" reveals a specific misconception (confusing input with output). The teacher learns something useful from the wrong answer. This is what good assessment does.

To find common misconceptions: ask the topic teacher "what do students get wrong here, and why?". The answers become your distractors.

A distractor that's *true* but doesn't fully answer the question.

Question: "Which factor was the most immediate cause of World War I?"

Weak distractor: "the invention of the printing press" (obviously wrong, off-topic).

Strong distractor: "the rise of nationalism in Europe" (true and contributing, but not the *most immediate* cause; the assassination of Archduke Franz Ferdinand was).

The student must distinguish between contributing factors and the precipitating event — Bloom's Analyze level. The question now tests reasoning, not just memory.

In any field, certain concept pairs get confused. Use both as choices.

Programming: assignment (=) vs equality (==)

If your topic has a known confusion pair, the wrong half is your strongest distractor.

The mistakes that destroy multiple choice questions:

These are not distractors; they're escape hatches. Students who don't know learn to pick "all of the above" for safety, and the question loses its discrimination. Skip them entirely.

Students learn that the longest answer is usually the correct one (because writers add qualifiers to avoid technical errors). If your correct answer is twice as long as your distractors, you're giving away the answer.

Fix: make all four choices roughly the same length, or vary length across questions so length doesn't correlate with correctness.

The stem and the correct answer must agree grammatically. If three distractors are noun phrases and one (the correct one) is a clause, students notice.

If the stem says "the muscle responsible for…" and the correct answer is "the cardiac muscle", that's a tell. The word "muscle" appearing in both flags the answer.

Fix: rewrite the correct answer so it doesn't echo stem keywords. Echo them in distractors instead.

The single biggest sin. "What's the capital of France? A) Paris B) Wednesday C) Mitochondrion D) 47" tests nothing. Distractors must come from the same conceptual neighborhood as the correct answer.

Start by writing the correct answer. Then ask three questions:

What would a student who *almost* understands this say?

What's the related concept this gets confused with?

What's a partially-true claim about this topic?

If you can answer all three, you have a strong question. If you can't, the question may not be testing what you think it's testing.

For more on the broader question-writing process, see

Use AI to generate quizzes from your own study materials in seconds.

Out of the box, AI quiz generators default to weak distractors — random wrong answers that share keywords with the topic but no conceptual relationship.

"For each multiple-choice question, the three distractors must each represent one of: (a) a common student misconception about this topic, (b) a partially-correct statement that doesn't fully answer the question, or (c) a confusable adjacent concept. Do not include random wrong answers."

With this instruction, modern LLMs produce distractor quality close to a human expert. Without it, they don't. See

How to evaluate your existing distractors

Take any multiple-choice quiz you've made. For each question:

Ask: would a student who didn't read the material be able to eliminate any distractor?

If yes → that distractor is too obvious. Replace it.

Run this check on 10 questions and you'll spot the patterns in your own writing.

How many distractors should a multiple-choice question have?

Three (four total choices) is standard. Two distractors (three choices) is acceptable for younger students or when you can't write three plausible options. More than four creates fatigue without adding meaningful discrimination.

Should distractors be the same length as the correct answer?

Yes. Length is the most common giveaway. Aim for choices that are within ±20% of each other in word count.

What if I can only think of two good distractors?

Make it a 3-option question. Better to have three strong choices than four with one obvious filler.

Yes — see Pattern 2 above. The key is they must be *insufficient* answers, not *correct* ones. An answer that's defensible by some standard isn't a distractor; it's a flaw.

How do I tell if my distractors are working?

Item analysis. After 30+ students take the quiz, look at which wrong answer was picked most often. If 60% of wrong answers cluster on one distractor, it's a strong distractor. If wrong answers spread evenly across all three, two of them are too obvious.

Want quizzes with AI-generated, misconception-based distractors out of the box?

A quick decision framework for writing distractors under time pressure

Most teachers don't have 20 minutes per question to craft the perfect wrong answer. Here's a faster path that still avoids the "obviously wrong" trap.

Before you write anything, ask: "If a student got this wrong, what did they actually think?" If you can't imagine a specific wrong-but-reasonable thought process, you don't have a distractor yet — you have filler.

The single richest source of realistic distractors is last term's short-answer or open-response mistakes. If three different students wrote "mitosis" when the answer was "meiosis," that's a distractor with field-tested pulling power — a made-up wrong answer rarely competes with a real one.

Hide the correct answer and read the remaining three choices alone. If any one of them reads as obviously silly or off-topic without the correct answer for contrast, rewrite it.

Beyond word count (covered above), match tone and specificity. A precise, technical correct answer next to a vague, casual distractor telegraphs itself even at equal length.

Common mistakes that undermine otherwise good distractors

Distractors that use absolute language ("always," "never," "completely") get eliminated by test-savvy students regardless of content, because absolutes are statistically likely to be wrong in most academic domains. Reserve absolute language for the correct answer only when the correct answer is genuinely absolute.

Alphabetical or numerical ordering that leaks the pattern.

If your correct answers cluster at "C" across a quiz, or numeric distractors are always rounder numbers than the correct answer, students learn to game the shape of the quiz instead of the content.

Distractors copied from the previous question.

Reusing a wrong answer as this question's distractor and last question's correct answer creates cross-item cues — a sharp student can rule out a distractor because it "was already used."

Testing reading comprehension instead of subject knowledge.

A distractor built on convoluted phrasing measures whether a student can parse a sentence, not whether they know the material. Keep every choice grammatically simple.

If you're building quizzes by hand, running these checks question-by-question adds up fast. Tools like

are trained to lean on the misconception and partial-truth patterns above by default, which is a useful starting draft even if you plan to hand-edit before publishing — free accounts get 5 AI generations a month to test the workflow, with paid plans (see

) raising that ceiling for classroom-scale use.

Worked example: turning a weak item into a strong one

Weak version — "What is the capital of France?" A) Paris B) A car C) A sandwich D) Blue. Every wrong answer is a different category entirely; a student who has never heard of France still scores 100% by elimination.

Strengthened version — "What is the capital of France?" A) Paris B) Lyon C) Marseille D) Nice. Now every distractor is a real French city, so guessing correctly requires actually knowing which one is the capital, not just knowing the topic is geography. This is the partially-correct-category pattern applied to a simple factual question, and it works the same way whether you're writing for

style summative exams or a quick formative check.

For teachers building this into a full workflow — importing existing material as source content rather than writing from scratch —

and then hand-tuning the generated distractors against the patterns above is usually faster than writing every item cold.

Join teachers and students who get practical tips on quizzing, active recall, and AI-powered learning.

Cognitive Psychology Writer & Study Skills Coach

Use AI to generate quizzes from your own study materials in seconds.

Grammar Quiz With Answers and Explanations (40 Items)

90 Pub Quiz Questions With Answers (Mixed Difficulty)

80 General Knowledge Questions for Kids (with Answers)

---

## Generating Plausible Distractors for Multiple-Choice Questionsvia Student Choice Prediction

`https://arxiv.org/html/2501.13125v2`

Generating Plausible Distractors for Multiple-Choice Questionsvia Student Choice Prediction

License: arXiv.org perpetual non-exclusive license

Generating Plausible Distractors for Multiple-Choice Questions

{lyooseop, yohan.jo}@snu.ac.krsuin@elicer.com

In designing multiple-choice questions (MCQs) in education, creating

is crucial for identifying students’ misconceptions and gaps in knowledge and accurately assessing their understanding.

However, prior studies on distractor generation have not paid sufficient attention to enhancing the difficulty of distractors, resulting in reduced effectiveness of MCQs.

This study presents a pipeline for training a model to generate distractors that are more likely to be selected by students.

to reason about students’ misconceptions and assess the relative plausibility of two distractors. Using this model, we create a dataset of pairwise distractor ranks and then train a

via Direct Preference Optimization (DPO) to generate more plausible distractors.

Experiments on computer science subjects (Python, DB, MLDL) demonstrate that our pairwise ranker effectively identifies students’ potential misunderstandings and achieves ranking accuracy comparable to human experts. Furthermore, our distractor generator outperforms several baselines in generating plausible distractors and produces questions with a higher item discrimination index (DI).

This paper is currently under review. All source code, fine-tuned models, and a subset of our data will be made publicly available upon publication.

Examples of distractor generation. A question and a correct answer are provided as input, and the output is a set of generated distractors. The plausibility rank metric indicates how likely students are to select the distractors.

Multiple-Choice Questions (MCQs) hold significant educational value as they provide a useful tool for assessing students’ knowledge.

Among the most critical elements in MCQs are

While the growing demand for education has amplified the need for numerous MCQs, manually creating distractors is time-consuming and costly, even for experts

Consequently, the automation of distractor generation has emerged as a promising solution

However, prior research has focused primarily on generating distractors similar to human-authored ones

, with insufficient emphasis on enhancing their plausibility.

Plausible distractors are crucial as they encourage students to deliberate longer over their answers, and high-quality MCQs must possess an appropriate level of difficulty to differentiate among levels of achievement

By contrast, overly simplistic distractors are easily dismissed, failing to adequately assess student proficiency and reducing the educational value of the assessment.

Therefore, creating plausible distractors that target students’ common mistakes or misconceptions is essential for developing highly discriminative MCQs

Based on these needs, this study presents a model training pipeline for distractor generation.

illustrates example distractors generated by GPT and our model.

Our main idea is to assign relative ranks to distractors based on which ones students are more likely to select, and use this information to train a model to generate plausible distractors. To achieve this, the process involves three steps (Figure

to predict which distractors are more plausible and likely to confuse students (Step 1).

that includes pairwise ranking information among distractors (Step 2).

Finally, leveraging this dataset, we train a

by applying Direct Preference Optimization (DPO,

According to evaluation on computer science (CS) subjects (Python, DB, MLDL), our pairwise ranker effectively identifies students’ common misconceptions, achieving ranking accuracy comparable to human experts. In addition, the distractor generator surpasses several baselines in generating plausible distractors in both automated metrics and human studies. Notably, the distractors generated by our model exhibit a high discrimination index (DI), an essential educational metric that measures a question’s ability to distinguish high-performing students from low-performing ones.

The key contributions of our study are threefold.

We build a pairwise ranker that reasons through students’ misconceptions and predicts which distractor they are more likely to choose.

We construct a student choice dataset with plausibility rankings among distractors and use it to train a plausible distractor generator.

We apply our method to MCQs in CS subjects (Python, DB, MLDL) and demonstrate the generator’s capability of generating distractors with high plausibility and DI.

Training pipeline for the distractor generation.

Previous studies on distractor generation can be categorized according to the question format and domain.

This format is used for exams that evaluate accurate knowledge based on provided textual content, with datasets such as RACE

, and Wikipedia commonly used to generate MCQs

. As a distractor generation model for this format,

fine-tuned GPT-2 and ensured the validity of MCQs through an external QA filtering step.

framework, which reformulates passages and questions through attention mechanisms to generate distractors.

introduced a dual-task training approach in which separate training was conducted using passages and questions as input to generate both answers and distractors.

However, since our study focuses on MCQs in the CS domain without relying on passages, these prior works are not directly comparable to ours.

This format is commonly used in literacy tests and science quizzes, where test-takers fill in blanks with appropriate words

method to regulate distractor generation by considering item discrimination factors.

used a knowledge graph to generate distractors by retrieving relevant triplets and selecting those most aligned with the QA context.

Our framework is not limited to cloze-style questions, which are relatively rare in our dataset, and instead supports a broader range of question types.

improved the process of generating distractors for math problems by dividing it into two main steps:

. In the overgeneration phase, they used a large language model (LLM) to generate

distractors, while in the ranking phase, a ranker was employed to select the top-

distractors most likely to be chosen by students.

explored a kNN-based approach to retrieve in-context examples similar to the target question and used them to generate distractors.

, which generates distractors based on learned error representations in math MCQs.

utilize retrieval-augmented generation (RAG) and chain-of-thought (CoT) for generating relevant and challenging MCQs.

as baselines for comparison with our model. We cannot compare with

since their method requires error explanations for each distractor.

, a method to sequentially generate distractors for multimodal questions requiring image interpretation, enhancing quality by leveraging contextually similar examples.

Meanwhile, research on distractor generation in the CS domain remains limited. While

developed a pipeline for generating MCQs aligned with

for programming education using GPT-4, our study emphasizes the plausibility of distractors by leveraging a smaller language model.

Our study aims to assign plausibility ranks among distractors using an LLM (Figure

, Step 1 and 2). This approach is motivated by prior findings demonstrating that LLMs exhibit strong inferential abilities, closely aligning with human performance in many evaluation tasks

Moreover, distilling these abilities from LLMs into smaller models, such as Prometheus 2

, has achieved comparable performance to LLMs while offering faster inference and reduced positional biases.

However, the reasoning abilities of LLMs to rank plausible distractors remain underexplored. A related study by

proposed an approach that trains a pairwise ranker for distractors using data on the actual selection rates of distractors by students. They further applied DPO to prioritize more plausible distractors. However, their model neither examines nor leverages LLMs’ reasoning abilities, and the trained model lacks interpretability. In contrast, our study extensively evaluates LLMs’ reasoning abilities by comparing various prompting approaches that are broadly applicable across diverse subjects. Additionally, our ranker generates reasoning behind its choices, enhancing its interpretability.

In this study, we propose a training pipeline to build a model capable of automatically generating more plausible distractors (as shown in Figure

Below, we first describe the base MCQ dataset used for training (§

), then introduce the modeling methods for the pairwise ranker (§

To train both the pairwise ranker and the distractor generator, we use an MCQ dataset created by educators on a nationwide online learning platform in South Korea.

The MCQs in this dataset have been provided to K12 institutions, large corporations, and government agencies, and contain a variety of CS-related questions and student answers. We retained only those related to Python, DB (SQL), and Machine Learning & Deep Learning (MLDL).

We target two categories of MCQs—coding and statement (see Figure

The statistics of this dataset are described in Table

A key feature of this dataset is that it includes information on how many students answered each question and the

This allows us to determine which distractors were more confusing and plausible to students. Since each question was solved by hundreds of students from diverse sectors, the selection rate information is considered reliable.

This information will play a key role in training the pairwise ranker and distractor generator, as discussed later.

We will release a subset of this dataset—52 questions with no licensing issues—to the community.

Statistics of the base MCQ dataset. The correctness rate refers to the percentage of students who answered the question correctly.

, Step 1), and determine which distractor is more likely to be selected by students.

M^{Rank}(Q,A,D^{A},D^{B})\rightarrow\{R,C^{A\,\text{or}\,B}\}

To enhance the interpretability and accuracy of ranking results, we utilize the reasoning abilities of LLMs through a structured prompt.

Specifically, we instruct the model to generate reasoning about (1) the knowledge being tested (e.g., “When students approach this problem, they first need to understand …”) based on the question and the correct answer, and (2) why each of the two given distractors might appear plausible to students (e.g., “Distractor A might confuse students who misunderstand the syntax …”).

The model outputs the result of the reasoning process as a single token (either A or B), indicating which distractor is more likely to be selected by students.

To train a relatively small LM to perform as a ranker, we prepare some training data of reasoning for supervised fine-tuning (SFT).

Specifically, for each question in the training set of the base MCQ dataset, we prompt GPT-4o with a distractor pair and the indicator of which one was more frequently selected by students, and instruct it to generate reasoning about the two distractors that concludes in favor of the more frequently chosen one. This reasoning (

However, the SFT model exhibited suboptimal accuracy and became more erroneous as the reasoning grew longer.

To address this, we use DPO to further train the model’s reasoning process.

After inference on the training set using the SFT model, samples diverging from the ground-truth choice were labeled as

, while the original training samples were set as

DPO is then applied to ensure the model generates correct reasoning and choices.

Examples of the model’s prompts are provided in Appendix

Statistics of the student choice dataset. Columns 2 and 3 show the number of training samples used for SFT and DPO, respectively.

The student choice dataset is created to build training data for the distractor generator (Figure

For each question in the base MCQ dataset, GPT-4o is used to generate three new distractors distinct from the human-authored ones (Appendix

These new distractors, along with the original ones, are scored using the pairwise ranker.

At this stage, the relative rankings of the original distractors are preserved, while rankings between the original and new distractors, as well as among the new distractors, are determined by our pairwise ranker. Each question ultimately has approximately six distractors ranked in plausible order. This dataset serves for training the distractor generator for both SFT and DPO (§

shows that, on average, 1.45 newly added distractors are ranked among the top 3 for each question, indicating that the newly added distractors are as plausible as the human-authored ones.

, which specifies the number of distractors to generate (Figure

) of distractor (e.g., Correct/Incorrect knowledge) it will generate, and then outputs

M^{Gen}(Q,A,n)\rightarrow\{T,D_{1}\,\text{...}\,D_{n}\}

We ensure that the model produces distractors that are both valid and plausible as follows.

Before generating distractors, the model first determines the type (

specifies whether the question requires selecting a correct or incorrect statement.

This step is critical for questions involving negation (e.g., “Select the

statement …”) as the model has a strong tendency to generate incorrect statements as distractors, even in such cases (see Appendix

To enhance the plausibility of distractors, we train the model through two stages: SFT and DPO.

We use the student choice dataset to create training data

ranges from 1 to the maximum number of distractors available for each question). The trained model learns the basic ability to generate distractors for a given question with varying

, but without prioritizing more plausible ones.

To enhance the model to generate more plausible distractors, we apply DPO using the student choice dataset.

Specifically, for each question, we construct all possible pairs between the top-

distractors, labeling the distractor from the top-

This allows the model to adjust its generation process to prioritize more plausible distractors that are more likely to challenge students.

An example of the model’s prompt is provided in Appendix

We also explored an alternative pairing method for increasing the combinations (Appendix

In this section, we describe the model training setup (§

) and introduce the metrics used to evaluate each model (§

For all experiments, both the pairwise ranker and the distractor generator are fine-tuned by applying LoRA

The numbers of training and test data are described in Table

The detailed settings for SFT and DPO are provided in Appendix

To assess the performance of the proposed pairwise ranker, we compare it against the following baseline models (the prompts for each baseline are included in Appendix

We instruct these GPT models to predict the ranking between two distractros in a zero-shot manner.

To examine the impact of different prompt formats, we experiment with four approaches: (1)

: the reasoning-based prompt format described in §

: scoring based on evaluation criteria for assessing plausibility, (3)

: simulating a collaborative learning scenario where two teacher agents discuss while observing students’ problem-solving processes.

We follow the pairwise ranker prompt and training/inference method proposed in this paper, replacing their data with ours.

We use two distinct settings for training data (Table

Models trained separately with data for each subject—Python, DB, and MLDL.

A model trained with data from all subjects combined.

One known limitation of LLM-based pairwise ranking is

, where the output may vary depending on whether two choices, A and B, are presented in the input prompt as AB or BA

To address this, we set the temperature to 0.5 and repeat the reasoning process with both AB and BA input sequences until consistent outputs are achieved, or randomly select a result after 10 attempts.

The evaluation metrics for the pairwise ranker are as follows:

measures how often the ranker correctly identifies the distractor with the higher student selection rate in the test set.

aims to compare the model’s performance with human experts. First, two professors in data science perform the pairwise ranking task on 60 test samples (20 per subject), and their results are compared with our model’s rank accuracy.

Second, three Master’s students majoring in data science assess the quality of model-generated reasoning and ranking results. For this, 30 samples (10 per subject) of reasoning and choices generated by our pairwise ranker (‘DPO, Comb.’ in Table

) are randomly selected from the test set.

The survey form and the rubric are in Appendix

tracks the number of iterations required for the model to predict the same choice for both AB and BA inputs.

Fewer iterations indicate lower positional bias.

The performance of our distractor generator is evaluated using the following metrics:

We compare the plausibility of distractors generated by our model, GPT models, a kNN approach

, and human experts (from the base MCQ dataset) as measured by our pairwise ranker (‘DPO, Comb.’ in Table

Win/tie/lose counts are calculated per question/distractor in two settings:

For each test question, three distractors are generated by each model (

), and only valid ones are retained. These are then compared pairwise between two models, with one point awarded to the winner. Identical distractors are excluded from comparisons.

To account for cases where models generate fewer than three valid distractors, each model’s temperature is increased to generate up to five valid distractors per model. After excluding identical distractors between the models, the top-3 are selected for pairwise comparison.

We conduct a human evaluation where actual students assess the difficulty of distractors generated by our method.

The test comprises 40 MCQs (Python: 20, DB: 10, MLDL: 10). Each question was sampled from the test set of the base MCQ dataset and paired with four distractors, one from each model (SFT, DPO, GPT-3.5-turbo, and GPT-4o), along with a ‘None of the above’ option.

The test is taken by 15 college students enrolled in AI courses at our university

The sample size is larger than the one tested on three individuals in

Based on the selection counts for each distractor, we calculate the plausibility and discrimination index for each model. The discrimination index indicates the ability of each item to differentiate between high- and low-performing students and is calculated as

denote the number of students in the upper (

) groups who answered the item correctly, and

(i.e., whether each distractor is clearly written without ambiguity) and

(i.e., whether a student with relevant knowledge can reasonably answer the question, as defined by

) of MCQs composed solely of the distractors generated by our DPO model with 11 Master’s students in data science.

More details about the human evaluation are provided in Appendix

In this section, we present the experimental results for the pairwise ranker (§

Evaluation results on pairwise rankers. The results were averaged over five generations for each model.

, in terms of accuracy, our DPO model achieved an accuracy of 67.5% (row 10), outperforming GPT-3.5-turbo (58.7%, row 1) and GPT-4o (64.0%, row 2) on average. This result is somewhat surprising because our model was trained on reasoning generated by GPT-4o.

Moreover, the DPO model significantly outperformed the SFT models (58.7%–65.7%, rows 8–9), particularly in Python, showing the effectiveness of DPO in enhancing the reasoning capability of the model.

’s method achieved strong performance on math questions in their original work, it exhibited lower accuracy on the CS subjects (48.8%, row 7).

Human evaluation on our pairwise ranker. The results from participants were averaged.

Human experts (two professors) tasked with choosing the more plausible distractor for 60 questions achieved an accuracy of 71.7%, compared to 70% achieved by our DPO model on the same task. This result suggests that the task is challenging even for experts and that GPT-like LLMs trained on large data can predict the confusion experienced by students at a level comparable to human performance.

presents survey results from three Master’s students evaluating the reasoning quality of the DPO model on a 5-point Likert scale.

These results provide mild to moderate evidence supporting the model’s ability to infer students’ misconceptions through logical reasoning and accurate knowledge.

Plausibility factors in our pairwise ranker’s reasoning.

We analyzed main factors revealed in the model’s reasoning to determine plausibility. We selected reasoning outputs where the DPO model predicted correct choices, and categorized plausibility factors in collaboration with GPT-4o. Figure

visualizes the proportion of each category.

In the code type questions (e.g., determining the output of a code snippet or filling in blanks), factors such as incorrect assumptions about function outputs or operations were the most common, while in the statement type questions (e.g., selecting statements about concepts), factors like conceptual overlap with other similar terms appeared most frequently.

Definitions for each category can be found in Appendix

We conducted an ablation study to examine the effectiveness of our reasoning method for rank accuracy. As shown in Table

, for GPT-4o, using our reasoning structure (row 2) substantially outperformed other reasoning methods (rows 4–6), leading us to adopt the current reasoning format for the trained models.

Training the model without the reasoning process (row 11) significantly reduced ranking accuracy, highlighting the importance of our reasoning method.

We evaluated the consistency of predictions when input order was altered and found that our model exhibits lower positional bias compared to GPT-3.5-turbo. The experimental results are provided in Appendix

Upon analyzing cases where our pairwise ranker produced incorrect reasoning, we identified several types of error, such as misjudging implausible errors as plausible and struggling with reasoning for unfamiliar questions that were underrepresented in the training data.

A detailed analysis and suggestions for future work can be found in Appendix

Plausibility evaluation on distractor generators. Win/lose counts of our models (columns) against baselines (rows), averaged over two evaluations.

summarizes the win/lose counts of our distractor generators against GPT models,

and human-authored distractors, as evaluated by our pairwise ranker (DPO-based). Our DPO model generated more plausible distractors than baseline models in most cases. Compared to human-authored distractors, our DPO model excelled in Python but underperformed in DB and MLDL. This discrepancy may be due to the underrepresentation of these subjects in our dataset, leading to limited exposure during training.

We assessed the benefit of augmenting the base MCQ dataset with synthetic distractors and automated ranking (i.e., the student choice dataset). Using only the base MCQ dataset for SFT and DPO led to a significant performance drop compared to using the whole student choice dataset, and no significant difference was observed between SFT and DPO (Appendix

). This highlights the importance of incorporating diverse chosen-rejected samples and sufficient distractors during training.

Overall, the results demonstrate that our approach of creating the student choice dataset and employing DPO using this data effectively enhances distractor plausibility.

We further examined the models’ performance based on question type (i.e., code vs. statement).

Our model outperformed GPT-3.5-turbo in generating plausible distractors for code type questions but was slightly less effective for statement type questions in Python and DB. In contrast, compared to GPT-4o, our model tended to perform better in statement type questions.

Human evaluation on distractor generators.

compares the frequency of distractors selected by students, showing that our DPO model generated more plausible distractors than GPT-4o across all subjects and outperformed GPT-3.5-turbo in all but one subject.

To evaluate whether the distractors have differing impacts based on students’ proficiency levels, we divided the students into two groups—Top 50% and Low 50%—based on their average scores. The distractors generated by the DPO model were most frequently chosen by both groups.

These findings suggest that our model may effectively identify areas of confusion across varying proficiency levels as a versatile tool for a wide range of students.

Our DPO model achieved the highest discrimination index (DI) of 0.212, falling within the acceptable range of discrimination (0.21–0.24)

This indicates that the distractors generated by our model are better at differentiating between high-performing students and low-performing ones than the baseline models.

This is desirable because MCQs with a high DI can identify misconceptions and gaps in students’ knowledge, and challenging MCQs can promote deeper learning.

using a 5-point Likert scale showed that all metrics scored above 4, confirming that most distractors were clear enough to answer the question. Detailed results are provided in Appendix

We additionally evaluated the similarity between model-generated distractors and human-authored ones, as well as their validity. Our DPO model showed greater text similarity to human-authored distractors than GPT-3.5-turbo and GPT-4o. It also demonstrated higher validity compared to GPT-3.5-turbo, particularly excelling in questions that ask for incorrect statements.

Furthermore, we examined the similarity between model-generated distractors and the correct answer to assess the potential issue of distractors being too similar to the correct answer. Our analysis found no evidence that our models pose a particularly high risk to students because of this issue.

Detailed analyses can be found in Appendix

We analyzed the suboptimal distractors generated by our model and identified several types of issues.

For code type questions, the distractors lacked variation in format, while for statement type questions, they were overly similar to the correct answers and failed to incorporate broader conceptual differences.

Examples of each type and future improvement strategies are detailed in Appendix

Plausibility evaluation of distractor generators on four publicly available datasets (GPT-generated CS questions and a Korean high school English exam). For the English questions, plausibility was evaluated using GPT-4o due to its higher performance. Win/lose counts of our models (columns) against baselines (rows), averaged over two evaluations.

Evaluation results on pairwise rankers for English questions. The results were averaged over five generations for each model.

To verify the generalizability of our approach beyond the base MCQ dataset and the CS domain, we conducted additional experiments on two publicly available datasets: (1) newly generated CS questions created using GPT-4o and (2) high school English exam questions.

For CS questions, we generated 100 MCQs per subject using GPT-4o and built a new student choice dataset to train a distractor generator.

, evaluated using our pairwise ranker, are consistent with those from the base MCQ dataset, reaffirming that plausibility improves with DPO over SFT.

For English questions, we used 88 questions from a South Korean high school exam dataset to train a pairwise ranker and a distractor generator. In Table

, our pairwise ranker, despite limited training data, outperformed GPT-3.5-turbo and closely approached GPT-4o. Similarly, Table

shows that in Setting B, where more distractors were compared, our DPO model achieved higher plausibility than GPT models, reflecting the trends observed in CS subjects.

In this study, we proposed a pipeline for training a model to generate more plausible distractors for MCQs and demonstrated its effectiveness across computer science subjects.

We trained the pairwise ranker to evaluate the relative plausibility of distractors, and used this to create the student choice dataset where distractors for each question are ranked by plausibility.

From this dataset, we created chosen-rejected pairs of distractors to train the distractor generator using DPO.

Our models outperformed GPT and other baseline models and performed comparably to humans in various metrics, including pairwise rank accuracy and distractor plausibility.

We believe that our work can advance automated educational tools, contributing to more adaptive and effective learning environments.

The models presented in this study have the following limitations.

First, the pairwise ranker’s method of comparing distractors pairwise significantly increases the number of combinations and requires substantial computing resources due to the need for generating reasoning. A listwise approach using an encoder-decoder structure could be explored as a solution

Second, the distractor generator occasionally produces invalid distractors, necessitating review by human experts or high-performing LLMs (e.g., GPT-4o) to accurately evaluate students’ knowledge. To address this limitation, future work could include an additional supervision phase, such as integrating feedback loops with other models or applying constraints like

Finally, our method focuses on generating difficult distractors, but there are instances where adjusting the difficulty level of MCQs to suit the needs of the target students is necessary. While our pairwise ranker can be utilized to select distractors with varying degrees of plausibility, future work could explore more direct approaches, such as incorporating student knowledge tracing or adaptive decoding, to address this challenge

Theory and Practice of Educational Evaluation

Shang-Hsuan Chiang, Ssu-Cheng Wang, and Yao-Chung Fan. 2022.

---

## Research: Developing, Analyzing, and Using Distractors for Multiple-Choice Tests in Education - Tips for Teachers by Cra

`https://tipsforteachers.co.uk/research-developing-analyzing-and-using-distractors-for-multiple-choice-tests-in-education/`

Research: Developing, Analyzing, and Using Distractors for Multiple-Choice Tests in Education - Tips for Teachers by Craig Barton

Research: Developing, Analyzing, and Using Distractors for Multiple-Choice Tests in Education

Title: Developing, Analyzing, and Using Distractors for Multiple-Choice Tests in Education: A Comprehensive Review

Authors: Gierl, M. J., Bulut, O., Guo, Q., & Zhang, X.

examines the creation, analysis, and use of distractors in multiple-choice tests. The authors synthesize existing research on distractor development strategies, focusing on identifying common misconceptions and creating similar-but-incorrect options. They explore various psychometric methods for evaluating distractor quality, including classical test theory and item response theory. The optimal number and placement of distractors are also discussed, along with recommendations for best practices. Finally, the authors propose innovative distractor development methods using automatic item generation and key features to address challenges in creating large numbers of high-quality items.

What are the key implications for teachers in the classroom?

Based on the provided document, here are some key implications for teachers in the classroom regarding the development, analysis, and use of multiple-choice tests, particularly focusing on the role of distractors:

Teachers should focus on creating plausible distractors that reflect common student misconceptions or errors in thinking. This can be achieved by reviewing students’ responses to open-ended questions, using verbal reports, or considering typical student errors.

Distractors should be similar in content and structure to the correct option. This includes similarities in length, complexity, formatting, and grammar. For numeric options, this could mean using factors from the correct answer to create incorrect options.

Teachers should analyze the frequency with which students select each distractor. Distractors chosen by less than 5% of students might be nonfunctioning and need revision.

Teachers should utilize trace line plots to identify distractors that do not differentiate between low and high-achieving students.

The choice mean of the correct option should be higher than the choice mean of any distractor. If a distractor has a higher choice mean than the correct option, it needs to be reviewed.

Teachers can use the point-biserial correlation to evaluate the effectiveness of distractors. A value greater than -0.05 indicates a distractor is not discriminating adequately.

Distractors can provide valuable diagnostic information about student understanding and misconceptions. By analyzing which distractors students choose, teachers can identify areas where students need additional instruction.

Teachers should adhere to item-writing guidelines for creating multiple-choice questions. Key guidelines include using plausible distractors, placing them in a logical order, keeping them independent and homogeneous, and avoiding clues to the correct answer.

two distractors and one correct option is often optimal

. This can reduce test development time, reduce student test-taking time, and improve item quality.

The position of the correct answer and distractors can affect the difficulty of a multiple-choice item. While some researchers suggest placing distractors in a logical or numerical order, others recommend randomizing the order to avoid bias.

Teachers may use automated processes to generate test items, as this process can help with efficiency. In order to generate multiple choice items, teachers can use key features to generate plausible distractors. Teachers can also create distractors based on content similarity by searching databases for semantically related concepts.

In summary, teachers should see distractors not just as incorrect options, but as a valuable tool to understand student thinking, improve test quality, and enhance instruction. Teachers should therefore invest time in careful development and analysis of distractors when designing multiple choice tests.

Multiple-choice testing is considered one of the most effective and enduring forms of educational assessment that remains in practice today

---

## ⚠️ Paginas que NAO deram texto

- `https://journals.sagepub.com/doi/full/10.3102/0034654317726529` — HTTP 403
- `https://www.researchgate.net/publication/319470426_Developing_Analyzing_and_Using_Distractors_for_Multiple-Choice_Tests_in_Education_A_Comprehensive_Review` — HTTP 403
