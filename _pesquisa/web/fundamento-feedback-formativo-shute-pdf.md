# 🔎 Pesquisa: fundamento-feedback-formativo-shute-pdf

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## THE FUSION MODEL FOR SKILLS DIAGNOSIS: BLENDING THEORY WITH PRACTICALITY (PDF, 61 pag.)

`https://files.eric.ed.gov/fulltext/EJ1111305.pdf`

The Fusion Model for Skills Diagnosis: Blending Theory With Practicality

Washington University, St. Louis, Missouri

Copyright © 2008 by Educational Testing Service. All rights reserved.

ETS, the ETS logo, and LISTENING. LEARNING.

LEADING. are registered trademarks of Educational Testing

As part of its nonprofit mission, ETS conducts and disseminates the results of research to advance

quality and equity in education and assessment for the benefit of ETS’s constituents and the field.

ETS Research Reports provide preliminary and limited dissemination of ETS research prior to

publication. To obtain a PDF or a print copy of a report, please visit:

This paper presents the development of the fusion model skills diagnosis system (fusion

model system), which can help integrate standardized testing into the learning process

with both skills-level examinee parameters for modeling examinee skill mastery and

skills-level item parameters, giving information about the diagnostic power of the test. The

development of the fusion model system involves advancements in modeling, parameter

estimation, model-ﬁtting methods, and model-ﬁt evaluation procedures, which are described

in detail in the paper. To document the accuracy of the estimation procedure and

the eﬀectiveness of the model-ﬁtting and model-ﬁt evaluation procedures, this paper

also presents a series of simulation studies. Special attention is given to evaluating the

robustness of the fusion model system to violations of various modeling assumptions. The

results demonstrate that the fusion model system is a promising tool for skills diagnosis

that merits further research and development.

Key words: Formative assessment, skills diagnosis, Markov chain Monte Carlo methods,

fusion model, model ﬁt, stepwise algorithm, item response theory, simulation, robustness,

Education and training, which constitute 9% ($722 billion) of the U.S. gross

national product, require two kinds of test-inﬂuenced decision making. On one hand,

high-stakes dichotomous decision making, including high school graduation, National

Merit college scholarship awards, and admission to the college of one’s choice, requires

that the individual’s performance scores be judged to be above a variety of diﬀerent

application-speciﬁc thresholds on a continuous unidimensional scale. As a result, test

theory is dominated by the challenge of locating individuals on such unidimensional scales.

On the other hand, the day-to-day aﬀairs of teaching and learning are predominantly

characterized by relatively low-stakes decision making that classiﬁes individuals based on

dichotomous traits or attributes, often called skills. For example, a good teacher uses skill

proﬁling in the classroom. After grading tests and noticing the classroom performance of

each student on diﬀerent relevant skills, the teacher has a sense of the speciﬁc skills for

which each student needs targeted remediation. The focus of this paper is on advancing

The necessity for such categorical skills analysis has been most recently highlighted

by the U.S. government’s No Child Left Behind Act of 2001 (NCLB), which calls for

classifying examinees into the categorical standards-based achievement levels of below

basic, basic, procient , or above procient (U.S. House of Representatives, 2001). Further,

the U.S. Department of Education draft regulations for NCLB proposes mandatory skills

diagnosis in response to the Act itself (U.S. Department of Education, 2002):

a) Student reports. A State’s academic assessment system must produce indi-

vidual student interpretive, descriptive, and diagnostic reports that . . .

(1)(ii) Help parents, teachers, and principals to understand and address the

(2) Are provided to parents, teachers, and principals.

Skills diagnosis, sometimes referred to as skills assessment or skills proling , is

a relatively new area of psychometrics developed to statistically rigorize the process of

evaluating (a) each examinee on the basis of his or her level of competence on an array of

skills and (b) the test by assessing the strength of the relationship between the individual

skills being assessed and the individual test items. Such examinee evaluations, often

administered periodically throughout the teaching-and-learning process, is understood to

be relatively low stakes and to have a valuable inﬂuence on the teaching and learning

process. It is frequently referred to as formative assessment, in contrast to summative

assessment, which takes place at the end of the teaching-and-learning process. A student’s

ﬁnal grade in a class is typically heavily dependent on some weighted average of such

summative assessments. Moreover, in the United States, all 50 states have embraced the use

of summative assessments in the form of single-score-scale standardized tests to determine

the proportion of students who have achieved state-designated academic standards at the

Instead of assigning a single ability estimate to each examinee, as in typical item

response theory model-based summative assessments, skills diagnosis model-based formative

assessments partition the latent space into more ﬁne-grained, often discrete or dichotomous,

skills (or other latent attributes), and evaluate examinees with respect to their level of

competence on each skill. For example, suppose designers of an algebra test are interested

in a standard set of algebra skills: factoring, using the laws of exponents, solving quadratic

equations, and so on. A skills-diagnosis-based analysis attempts to evaluate each examinee

with respect to each skill, whereas a standard summative psychometric analysis typically

evaluates each examinee with respect to an overall scaled score on the algebra exam.

The focus of published skills-diagnosis modeling methodologies has been primarily

on the selection of the skills-diagnosis model itself. However, developing a model is only the

ﬁrst step in developing a skills-diagnosis system. A complete skills-diagnosis system must

not only have (a) a well-selected model but also (b) a reliable, accurate, and eﬃcient

statistical estimation method and (c) eﬀective implementation procedures for real data

To accomplish this ﬁrst step, we reviewed the many skills-diagnosis models that have

been presented in the literature. Of these models, the uniﬁed model of DiBello, Stout, and

Roussos (1995) was chosen as the foundation for the model developed in this paper, which

we call the fusion model. The uniﬁed model was chosen as our starting point because it

includes a greater variety of components than other models, thus giving us more ﬂexibility

for shaping our own model. However, the uniﬁed model’s large number of parameters also

required some reparameterization and simpliﬁcation due to nonidentiﬁability of some of the

uniﬁed model parameters. This is discussed in more detail below.

To accomplish the second step, selecting the estimation method and probability

framework, we considered a number of approaches, such as the EM algorithm and Bayesian

networks, and ﬁnally settled on using a Bayesian probability framework in conjunction with

a Markov chain Monte Carlo (MCMC) estimation algorithm.

Although estimation procedures have been developed for many skills-diagnosis

models, it does not appear that any of these modeling approaches go beyond estimation

to develop dynamic implementation procedures, facilitating skills diagnosis of real data

by evaluating the ﬁt of the model to the data, and manipulating the model structure as

a result of this evaluation. In contrast, the methodology presented in the current paper

represents a complete skills-diagnosis system:

1. An identiﬁable and interpretable model called the fusion model, an enhancement of

the uniﬁed model (DiBello, Stout, & Roussos, 1995),

2. An eﬀective and eﬃcient parameter-estimation method operationalized in a software

program referred to as Arpeggio, which employs a Markov Chain Monte Carlo algo-

3. A model-ﬁtting procedure referred to as the stepwise algorithm that is used to eliminate

noninformative item parameters from the model, and

4. Practical model-ﬁt evaluation procedures.

After brieﬂy summarizing some of the past research on skills-diagnosis modeling (to

place the fusion model system in its historical and technical context in relation to past

work), this paper presents detailed descriptions of the fusion model item response function,

the Bayesian framework for the estimation method, the stepwise algorithm model-ﬁtting

procedure, and the model-ﬁt evaluation procedures. This methodology is then tested on

simulated data, using data generated from the model as well as data generated with a

limited number of serious, but realistic, violations of model assumptions.

3 Diagnostic Modeling in Education Testing

Skills-diagnosis modeling has two major practical foci: (a) to determine the

mastery/nonmastery skill proﬁles of examinees taking a test and (b) to evaluate the test

and its items in terms of their eﬀectiveness in measuring the individual skills. Psychometric

techniques addressing these speciﬁc issues were created as early as 1973, when Fischer

proposed the linear logistic trait model (LLTM) to decompose item-diﬃculty parameters

from a logistic model into discrete skills-based components. Rather than evaluating

examinees with respect to the individual skills as well, he maintained a unidimensional

ability parameter in the LLTM. Conversely, Tatsuoka and Tatsuoka (1982) proposed the

statistical rule space approach to decompose examinee abilities into skill components.

Although the rule space approach estimates skill proﬁles of each examinee taking the exam,

it does not statistically evaluate how well the test and its items measure the skills. While

both the LLTM and rule space approaches have been applied to test data, they have not

been widely implemented in practical education assessment settings. This may be because

practical skills diagnosis cannot go far without modeling both the relationship between the

items and the skills and the relationship between the examinees and the skills.

Many models for skills diagnosis have been developed subsequently to improve

on either LLTM (Fischer, 1973) or rule space (Tatsuoka & Tasuoka, 1982). Notable

examples include the multicomponent latent trait model (MLTM) of Whitley (name

now changed to Embretson) (1980); the general component latent trait model (GLTM)

of Embretson (1984); the restricted latent class model of Haertel (1989); the HYBRID

model of Gitomer and Yamomoto (1991); the uniﬁed model of DiBello, Stout, and Roussos

(1995); the Bayesian networks of Mislevy (1994) and of Yan, Mislevy, and Almond (2003);

the tree-based approach of Sheehan (1997); the discrete mixture Rasch model of Bolt

(1999); the conjunctive, disjunctive, and compensatory models of Maris (1999); and the

dichotomization of the MLTM by Junker (2000). These advancements in skills-diagnosis

modeling have ﬂuctuated between complex models representing cognitive views of problem

solving that are statistically intractable when applied to test data and simpler models (still

complex in comparison to standard unidimensional models) that are more reliably applied

Despite a great need for practical skills diagnosis, for the models that have estimation

algorithms, we are unaware of any further development of implementation procedures for

ﬁtting the models to real data and evaluating the subsequent ﬁt to the data. Thus, to

further advance the ﬁeld of skills diagnosis, this paper develops the fusion model skills

diagnosis system (fusion model system), which not only provides a model that includes

both examinee- and item-diagnostic parameters but also provides ﬁtting methods and

model-ﬁt evaluation procedures. First, we describe the fusion model item response function

(a reparameterization of the uniﬁed model item parameters) and its Bayesian framework,

and then we describe the estimation algorithm and the implementation methodology

(model-ﬁtting and model-ﬁt evaluation methods). Establishing an eﬀective estimation

algorithm and eﬀective implementation procedures provides a critical link for bridging the

gap between skills-diagnosis model development and the practical use of skills-diagnosis

methods in mainstream test evaluation. For more detailed reviews of skills-diagnosis

models, see DiBello, Roussos, and Stout (2007), Embretson (1999), Junker (1999, 2000),

Like all other IRT models, IRT-based skills-diagnosis models deﬁne the probability

of observing examinee j response to item i given examinee ability parameters and item

parameters. Symbolically, this probability is represented as P (Xij = x j #j; i), where

Xij = x is the response of examinee j to item i (with x = 1 indicating a correct response

and x = 0 an incorrect response), #j is a vector of examinee j ability parameters, and

i is a vector of item i parameters. The fundamental assumption of IRT modeling is

that, conditioned on the examinee ability parameters, examinee response to any item i

is independent of examinee response to any other item i′. The distinguishing feature of

skills-diagnosis models from other IRT models is that the items i = 1; :::; I relate to a set of

cognitive skills k = 1; : : : ; K in a particular manner. Although Fischer (1973) speciﬁed this

relationship as fik (the “weight” of skill k in item i), the weights are usually either 1 or 0,

in which case they reduce to what is now known as the Q matrix, namely, Q = fqikg, where

qik = 1 when skill k is required by item i and qik = 0 when skill k is not required by item i.

Although the concept had been used previously in several diﬀerent models, the Q matrix

notation was ﬁrst introduced by Tatsuoka (1990). Further, Tatsuoka’s work emphasized the

importance of the Q matrix to skills diagnosis.

The uniﬁed model (DiBello, Stout, & Roussos, 1995) features both skills-based item

parameters and skills-based examinee parameters. Furthermore, the uniﬁed model includes

additional parameters to improve the ﬁt of the model to the data. As discussed by Samejima

(1994) in her competency space theory, let the examinee parameter # = fQ; bg (examinee

subscript j suppressed) denote the complete latent space of all relevant skills. Let Q be the

vector of cognitive skills speciﬁed by the Q matrix. The remaining latent space, b, includes

the relevant skills outside those speciﬁed by the Q matrix. Samejima (1995) referred to b

as skills associated with “higher order processing,” and suggested that these skills may be

more substantively important than Q. From the uniﬁed model perspective, however, b

does not need to be interpreted as higher order processing; it is simply a representation of

the latent skills outside the Q matrix. The uniﬁed model is the ﬁrst skills-diagnosis model

to incorporate b into the model by deﬁning a single unidimensional ability parameter j as

a unidimensional projection of examinee j’s b ability. The inclusion of this concept in the

uniﬁed model will be shown below to be connected to a type of item parameter that can

be used to diagnose whether a test item is well modeled by the Q matrix skills that have

been assigned to it. The explicit acknowledgment that the Q matrix is not necessarily a

complete representation of all the skill requirements for every item on the test diﬀerentiates

the uniﬁed model from the other skills-diagnosis models.

Deﬁne ik = P (Yikj = 1 j jk = 1) and rik = P (Yikj = 1 j jk = 0), where Yikj = 1

refers to the event that examinee j correctly applies skill k to item i, jk = 1 indicates that

examinee j has mastered skill k, and jk = 0 indicates that examinee j has not mastered

skill k. The item response function (IRF) for the uniﬁed model is given in equation 1:

1+exp{−1:7[j −(−h)]} , a Rasch model with diﬃculty parameter  h.

The product term in the model indicates the assumption of conditional independence

of applying the skills, provided the Q-based strategy is used. By further assuming local

independence of the item responses, Equation 1 can be used to model the probability of

any given response pattern, x. For each item i on the test, there are 2 ki + 3 ( ki = number

of skills required by item i) uniﬁed model item parameters: ik and rik, two IRT Rasch

model parameters ci and bi, and the ﬁnal parameter di, the probability of selecting the Q

based strategy over all other strategies.

In addition to building an IRF based on the Q matrix, the uniﬁed model allows the

predicted Q-based response to be inﬂuenced by non- Q skills with the term Pci(j), and

allows for alternate non- Q strategies with the term Pbi(j). As with the models of Maris

(1999) and the GLTM of Embretson (1984), the uniﬁed model has cognitively interpretable

parameters; but unfortunately, not all the parameters are statistically estimable.

The ﬂexibility and interpretability of the uniﬁed model parameters led it to be

chosen as the foundation for the fusion model skills-diagnosis system developed in this

paper. However, because nonidentiﬁable parameters existed in the original uniﬁed model

(Jiang, 1996), a reduction in the parameter space was required before its parameters could

be estimated. The initial attempts to reparameterize the model included retaining all item

parameters except for ki   1 ik’s for each item, where ki refers to the number of skills

required for item i (DiBello, Stout, & Jiang, 1998; Jiang, 1996). Speciﬁcally, Jiang set

ik = 1 and i = 1 ; :::; ki   1. However, when ki   1 ik’s are ﬁxed at 1, the interpretation

of all the other item parameters is distorted, and the highly useful capacity to interpret

the strength of a skill in modeling item response correctness is lost. Instead, Hartz (2002)

reparameterized the uniﬁed model to be identiﬁable in a way that retains interpretability

of the parameters. To further reduce the complexity of the parameter space and to enhance

the estimability of the parameters, the modeling of the possibility of alternate strategies

has been dropped for the work reported here by setting di = 1 for i = 1; :::; I. The reduced

model (reparameterized uniﬁed model) now has 2 + ki parameters per item, compared

to the 2 ki + 3 parameters per item in the original uniﬁed model. The reduced model

maintains the uniﬁed model’s ﬂexible capacity to ﬁt diagnostic test datasets as compared

to other skills-diagnosis models, retaining the most substantively important components,

like the capacity for skill discrimination to vary from item to item and the residual ability

parameter , an additional and potentially important component of the original uniﬁed

model that is missing from all the other models. Equation 2 presents the resulting fusion

model IRF, often referred to as the reparameterized unied model. It is based on the same

examinee parameters, j and j, that are used in the original uniﬁed model. The Pci(j)

term again refers to the Rasch model with diﬃculty parameter  ci (the lower the value of

It is important for understanding and applying the fusion model that the interpretation of

these parameters be clearly understood. Here,

i = P (correctly applying all item i required skills given

ik (under the assumption of conditional independence of

ci = the value of j for which Pci(j) = 0 :5,

ik  1, and 0  ci  3. (The bounds of 0 and 3 on the

c parameter were chosen for convenience rather than because of any strict theoretical

or logical constraint.) The fusion model reparameterization replaces ik and rik in the

ik. In addition to producing an identiﬁable parameter

set, the new parameters are conceptually interpretable in a particularly appropriate way

from the applications perspective. The parameter ∗

having mastered all the Q required skills for item i will correctly apply all the skills

when solving item i. The correct item response probability for an examinee who has not

mastered a required skill k0 is proportional to r∗

on mastery of this skill, the lower the item response probability for a nonmaster of the

skill, which translates to a lower r∗. Thus, r∗

ik is like a reverse indicator of the strength of

evidence provided by item i about mastery of skill k. The closer r∗

The distinctiveness of the ∗s and r∗s in comparison to parameters in other models

is important to note. Other models have indeed included components similar to ∗

ik. The models in Maris (1999) have the ik and rik parameters of the uniﬁed model

(DiBello et al., 1995), which are nonidentiﬁable. Conversely, the discrete MLTM of Junker

(2000) has skill-based item parameters that are identiﬁable, but not item speciﬁc, so the

inﬂuence of the skill on each individual item response probability is lost. This is especially

important from the perspective of skills-based test design, where one wishes to know for

each skill which items are most eﬀectively discriminating between examinee possession and

The Pci(j) component is an important unique component retained from the uniﬁed

model because it acknowledges the fact that the Q matrix does not necessarily contain

all relevant cognitive skills for all the items. Interestingly, it is not present in any other

skills-diagnosis model. In this component, ci indicates the reliance of the IRF on skills

other than those assigned to that item by the Q matrix. As an approximation, these other

skills are modeled, on average over all the items, by a unidimensional ability parameter, j.

When ci is 3 or more, the IRF is practically uninﬂuenced by j, because Pci(j) will be

very close to 1 for most values of j. When ci is near 0, j variation will have increased

inﬂuence on the item response probability, even with j ﬁxed. Thus, the estimate of ci

can provide valuable diagnostic information about whether a skill is missing from the Q

matrix or whether a skill already in the Q matrix needs to be added to an item’s list of

measured skills. Indeed, one of our robustness studies below provides a demonstration of

the eﬀectiveness of c as this kind of a diagnostic.

In summary, the fusion model enables the estimation of the most critical examinee

parameters from the original uniﬁed model while reparameterizing the uniﬁed model’s

item parameters so that they are not only estimable but also retain their skills-based

interpretability, a feature that makes such models more attractive to users of educational

tests in comparison to traditional unidimensional psychometric models.

After reparameterizing the uniﬁed model, a variety of possible methods for

estimating the fusion model parameters were explored. In order to incorporate ﬂexibility

in fusion model parameter relationships and to simplify estimation procedures, we decided

to use a Bayesian approach to estimating the parameters. While using Bayesian networks

is one type of Bayesian approach that could be adopted, we found that the probability

structure of interest could be combined with relationships between the skills more easily

by using a hierarchical Bayesian modeling approach instead. This, in eﬀect, enhances the

reparameterized uniﬁed model of Equation 2 by adding further parameters and their priors

(typically vague or estimated from the data).

To frame a complex non-Bayesian model into a reasonable Bayesian model, the

priors, hyperparameters (parameters of the prior distributions that in turn have completely

speciﬁed prior distributions), and the priors of the hyperparameters must be constructed so

that the estimated values of the model parameters will be determined predominantly by the

data, not by the priors (assuming, as is usual, that little information about likely parameter

values is known a priori and that the data contain parameter estimation information).

Thus, the goal in building the Bayesian framework for our model was to incorporate

hypothesized structural relationships between variables that are justiﬁed by the scientiﬁc

theory governing the setting being modeled, and to construct noninformative priors for

the unknown relationships or distributions so that the data can reveal detailed aspects of

the relationships between the variables. This approach was believed to have the potential

for greater inferential power than a non-Bayesian approach because it exploits aspects

that are already known about parameter relationships while allowing the data to provide

information about the unknown aspects of the relationships.

The most obvious example of the type of relationship that would be more diﬃcult

to account for in a non-Bayesian approach is the matrix of positive correlations that

exists among the pairs of examinee skills. Incorporating this relationship is particularly

important in skills-diagnosis models for education. More speciﬁcally, mastery of one skill

is not statistically independent of mastery of another. Additionally, an examinee who has

mastered many skills among  can be expected to have a higher . Such correlations have

been observed in education testing even for abilities that are seen as highly distinct, like

mathematics ability and reading ability. Thus, this assumption would certainly hold for a

diagnostic test where the skills are designed to be dimensionally close to one another.

Although typical hierarchical Bayesian models would simply specify a prior

distribution for the dichotomous jks directly (for example, see the work of Yan et al.,

2003), incorporating multidimensional correlations of the dichotomously parameterized

skills (mastery versus nonmastery) is a very diﬃcult task. In particular, raw correlations

between the dichotomous skills are highly dependent on the diﬀering proportions of masters

for each skill. To deal with this problem, we used a modiﬁed version of a well-known latent

variable technique — tetrachoric correlations. Tetrachoric correlations were developed to

model the relationship between two dichotomously measured variables where it is assumed

that a normally distributed latent variable generates each observed dichotomous variable

(see, for example, Hambleton & Swaminathan, 1985).

In the fusion model application, tetrachoric correlations are used to model the

relationship between two dichotomous mastery variables. Thus, the Bayesian framework of

the fusion model incorporates continuous ˜ jk, k = 1 ; : : : ; K with standard normal priors.

Once the ˜jk variables are generated, they are converted to the dichotomous jk variables

by comparing their values to k cutoﬀ values, which are estimated as hyperparameters.

Speciﬁcally, jk = 1 when ˜jk >  k. That is, the examinee is considered to have mastered

the skill because the examinee latent ability is greater than the mastery cutoﬀ value.

Likewise, j is given a standard normal prior. Since it is assumed that the examinee skills

have positive correlations, ( ˜j; j)  N (0; Σ) where Σ = fmng has 1s on the diagonal for

the marginal variances of the skills and the non-negative pairwise correlations between

( ˜j; j) as the oﬀ-diagonal elements. These correlations are estimated as hyperparameters

and are given a Uniform prior over some interval: m;n  Unif(a; b), where the variables

a and b were set to 0 :01 and 0 :99, respectively, to prevent boundary problems. The

hierarchical Bayesian model for the examinee parameters is seen in Figure 1.

Since the values of the item parameters ∗

datasets (indeed, they often vary greatly within a single dataset), the distribution functions

for the item parameter priors were chosen to be beta distributions, allowing maximum

ﬂexibility of the shape the priors can take. For some datasets, one of the item parameters

may vary little across items, in which case a highly peaked prior distribution would be

expected to yield the best results. For other datasets, an item parameter may vary so

greatly across items that a uniform distribution would be the most appropriate choice. By

careful choice of its parameters, the shape of a beta distribution can be made to resemble

either the highly peaked distribution or the uniform distribution, or nearly any distribution

This valuable ﬂexibility of the beta distribution, however, cannot be taken advantage

of unless we already know the distribution of the item parameters. This seemingly

insurmountable problem has a solution: The parameters of the beta priors can themselves

be estimated by assigning them priors and estimating the corresponding hyperparameters.

Thus, by estimating the parameters of the beta distributions used for the item parameter

priors, we allow the data to intelligently inform the shape of the item parameter priors that

are most appropriate for the given situation.

Using the above Bayesian framework to produce the fusion model, a Markov chain

Monte Carlo (MCMC) estimation software program called Arpeggio was written in Fortran

using the Metropolis-Hastings within Gibbs algorithm (see, for example, Patz & Junker,

1999a, 1999b) to simultaneously estimate examinee and item parameters. Since MCMC is

used simply as an estimation tool in this perspective, the algorithm is not discussed in detail

here. The reader is referred to Hartz (2002) for a detailed discussion of our application of

Figure 1. Fusion model hierarchical Bayesian formulation (examinee parame-

6 Stepwise Algorithm Model-Fitting Procedure

To conduct eﬀective skills diagnosis, it is not enough to have merely a good model

and a good parameter estimation algorithm. One also needs accompanying procedures

for ensuring model ﬁt. To this end, we have developed a stepwise algorithm to help

eliminate statistically non-inﬂuential item parameters, speciﬁcally, noninﬂuential r∗s or cs,

Even when a Q matrix is very carefully developed for estimation of the fusion model

with real data, or even when one generates simulated data and uses the known Q matrix

in one’s estimation model, there may be item parameters that, for the given data, are

For example, in a real data setting, a skill may be assigned by the Q matrix to

an item, but it may be that examinees do not actually need or use the skill in correctly

responding to the item (for example, the item may require only a very elementary

application of the skill and thus play an almost nonexistent role statistically, even though

it is required for the item), or a skill may be needed to a much lesser degree than other

skills that also are delineated by the Q matrix. (This real data setting can be emulated in

simulation studies by using a Q matrix in the estimation model that does not match the

one used in simulating the data; see below.)

Even when simulated data are analyzed using the Q matrix that was used in

generating the data and all the item parameters are identiﬁable, the structure of the data

may not contain suﬃcient information to well estimate all the parameters used to generate

An example of this situation is when data are simulated with low r∗, high ∗ (referred

to as high cognitive structure ), and moderate c values. In this case, the c parameters may

not be estimable because the item responses are largely determined by whether examinees

have or have not mastered the skills and are very little aﬀected by their proﬁciency on

non-Q skills. Additionally, if an item measures both a hard skill and an easy skill, and the

r∗ for the harder skill is very low, the r∗ for the easier skill will have little inﬂuence in the

item response function. Thus, eliminating such noninformative parameters is considered a

critical component of the fusion model system because it helps the model to concentrate its

statistical power where there is diagnostic information to be found.

To identify noninﬂuential parameters, the stepwise algorithm estimates the inﬂuence

of each parameter, either r∗ or c, on the IRF that uses that parameter, employing a

common probability scale for measuring this inﬂuence. Thus, the algorithm uses the same

statistical decision rule for both r∗ and c in determining whether or not the estimated

inﬂuence is large enough to warrant keeping the parameter in the model. In our simulation

studies, these decisions are based solely on a statistical hypothesis-testing framework in

which the null hypothesis is that the item parameter under investigation has negligible

inﬂuence on the parameter’s item response function. It is important to note, however,

that in practice, such decision making would typically be based on an interaction of both

statistical and substantive input. Because a Q matrix is often developed with strong

theoretical arguments to back it up, eliminating Q matrix entries (which is what happens

when an r∗ is eliminated) in practice requires not only strong statistical evidence but strong

To estimate the inﬂuence of a particular item parameter, three diﬀerent item

response probabilities are calculated for each examinee from its fusion model IRF. With all

the other parameters ﬁxed at their estimated means, three IRF probabilities are calculated:

(a) with the parameter ﬁxed at its null hypothesis (no inﬂuence) value (an r∗ would be ﬁxed

at 1 :0, and a c would be ﬁxed at 10 :0), (b) with the parameter set to its estimated mean

minus its estimated standard deviation, and (c) with the parameter set to its estimated

mean plus its estimated standard deviation. For an r∗

for all examinees who are estimated as non-masters of skill k (these are the only examinees

ik would appear in their item response function). For a c parameter, the

calculation is done using all the examinees. When on average over all these examinees,

the item response probability (a) is close (as deﬁned below) to that for either (b) or (c)

(or both, depending on the preference of the practitioner), the parameter is said to be

Determining whether a diﬀerence in average probabilities is close is ultimately a

subjective decision, but still there does exist experience from other IRT domains of interest

---

## ⚠️ Paginas que NAO deram texto

- `https://www.ets.org/Media/Research/pdf/RR-07-11.pdf` — HTTP 404
