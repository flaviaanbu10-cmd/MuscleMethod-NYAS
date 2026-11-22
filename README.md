
# MuscleMethod: AI-Powered Stroke Rehabilitation Using EEG–EMG Fusion

### Multimodal Machine Learning | Neurotechnology | Rehabilitation Engineering | Biomedical AI

**Developed for the New York Academy of Sciences Junior Academy — BrainTech Challenge**

## Overview

MuscleMethod is a research-stage AI prototype exploring how brain and muscle signals can be combined to support adaptive hand rehabilitation for stroke survivors.

Stroke rehabilitation presents a major challenge: patients may attempt a movement without generating sufficient muscle activation, experience fatigue, or compensate by activating unintended muscles.

Our proposed solution combines:

- **Electroencephalography (EEG)** to represent movement intention.
- **Electromyography (EMG)** to represent muscle activation.
- **Machine learning** to classify rehabilitation assistance decisions.
- **Compensation and fatigue monitoring** to investigate safer, more individualized rehabilitation.
- **An interactive dashboard** to communicate model outputs and support human oversight.
- **A proposed soft robotic glove** to provide adaptive physical assistance.

The current implementation is a research prototype evaluated using synthetic data, not a clinically validated medical device.

---

## Research Question

**Can combining EEG and EMG features improve the classification of rehabilitation assistance decisions compared with EEG-only features, and how might multimodal analysis support compensation-aware stroke rehabilitation?**

### Hypothesis

Combining EEG and EMG features will provide more information about movement attempts than EEG features alone, improving classification performance under simulated conditions.

We also hypothesize that identifying discrepancies between intended movement and muscle activation could eventually support more personalized assistance and compensation monitoring.

---

## System Architecture

Our proposed rehabilitation system follows this pipeline:

```text
EEG Signals ──────┐
                  ├──> Signal Processing / Feature Extraction
EMG Signals ──────┘
                              |
                              v
                    Multimodal AI Model
                              |
                              v
                   Assistance Classification
                              |
            ┌─────────────────┼─────────────────┐
            v                 v                 v
       Assist More       Assist Less          Rest
            |                 |                 |
            └─────────────────┼─────────────────┘
                              |
                     Unclear / No Action
                              |
                              v
                 Interactive AI Dashboard
                              |
                              v
               Proposed Soft Robotic Glove
                              |
                              v
                  Patient / Therapist Feedback
```

The dashboard demonstrates the proposed decision-support workflow. Physical robotic-glove integration and clinical feedback control remain future development goals.

---

## Machine Learning Approach

The prototype investigates whether combining EEG and EMG features provides better classification performance than EEG features alone.

### Experimental Design

Two approaches were compared:

**Model 1: EEG-only**

- Uses simulated EEG-related features.
- Serves as a baseline for comparison.
- Evaluates how well movement-related information alone distinguishes assistance decisions.

**Model 2: EEG + EMG Fusion**

- Combines simulated EEG and EMG-related features.
- Evaluates whether additional muscle-activation information improves classification.
- Investigates multimodal feature fusion for rehabilitation decision support.

### Output Classes

The classification system uses five possible outputs:

| Decision | Intended Meaning |
|---|---|
| Assist More | Additional movement assistance may be needed |
| Assist Less | Less movement assistance may be appropriate |
| Rest | A rest period may be appropriate |
| Unclear | Available signals do not support a clear decision |
| No Action | No assistance adjustment is indicated |

These outputs represent simulated decision categories, not validated clinical recommendations.

---

## Experimental Results

We conducted an initial comparison using synthetic feature data.

### Dataset

- Training samples: 200
- Testing samples: 100
- Classification categories: 5
- Data source: Synthetic, programmatically generated examples

### Model Comparison

| Model | Test Accuracy |
|---|---:|
| EEG-only baseline | 44% |
| EEG + EMG fusion | 98% |

### Interpretation

The fusion model achieved higher classification accuracy on our synthetic test dataset.

This supports the preliminary observation that the additional EMG features provided useful information for distinguishing the simulated classes.

However, the experiment does **not** establish that the model would achieve similar results with real EEG/EMG recordings.

Because the data were synthetically generated, the performance difference may reflect how the simulated labels and features were constructed.

### Limitations

- The dataset contains simulated rather than real patient signals.
- The sample size is small.
- Real physiological signals contain noise, artifacts, and substantial individual variability.
- The current results do not demonstrate generalization to unseen patients.
- Compensation detection requires additional testing and physiological validation.
- The system has not been evaluated in clinical rehabilitation settings.

Future experiments should investigate realistic datasets, subject-independent testing, robustness to signal degradation, and more rigorous baselines.

---

## Compensation Detection and Adaptive Rehabilitation

A central research direction of MuscleMethod is distinguishing intended movement from potentially compensatory muscle activity.

Stroke survivors may recruit unintended muscle groups to complete movement tasks, which can complicate rehabilitation assessment.

Our proposed system investigates three types of information:

1. **Movement intention:** Whether EEG-related features indicate an attempted movement.
2. **Muscle activation:** Whether EMG-related features indicate a corresponding muscle response.
3. **Compensation patterns:** Whether activation suggests unintended muscle recruitment.

The goal is to investigate whether combining these signals can improve rehabilitation feedback beyond basic movement detection.

Compensation monitoring is an ongoing research direction and has not been clinically validated by the current synthetic-data experiment.

---

## Interactive AI Dashboard

An interactive dashboard was developed to demonstrate how the rehabilitation decision system could communicate model outputs.

The prototype explores:

- EEG and EMG signal information
- Predicted assistance decisions
- Signal-quality considerations
- Compensation and fatigue indicators
- Rehabilitation-session feedback
- Patient and therapist visibility into system decisions

The dashboard is intended as a research demonstration rather than a clinical monitoring tool.

**Dashboard screenshots and demonstrations can be added to this repository to illustrate the prototype.**

---

## Human-in-the-Loop Design

Clinical AI should support, rather than replace, human judgment.

Our proposed system includes opportunities for therapists and patients to review rehabilitation outputs and provide feedback.

Future implementations could allow clinicians to:

- Examine relevant signal features.
- Review model confidence and limitations.
- Identify potentially incorrect decisions.
- Adjust rehabilitation parameters within safety constraints.
- Evaluate longitudinal rehabilitation progress.

These capabilities are proposed extensions and require implementation and testing before clinical use.

---

## Research Contributions

This project explores:

**1. Multimodal sensor fusion**

Comparing EEG-only and EEG+EMG features for rehabilitation assistance classification.

**2. Experimental evaluation**

Using a baseline comparison to investigate whether multimodal features improve simulated classification performance.

**3. Compensation-aware rehabilitation**

Exploring how discrepancies between brain and muscle activity might indicate movement difficulties or compensatory patterns.

**4. Interpretable decision support**

Designing a dashboard that communicates rehabilitation classifications and relevant supporting information.

**5. Human-centered rehabilitation AI**

Investigating how therapist oversight and patient feedback could be incorporated into adaptive assistance systems.

---

## Future Research Directions

### 1. Real-World EEG/EMG Datasets

Evaluate multimodal models using appropriately sourced physiological recordings rather than relying exclusively on synthetic features.

### 2. Model Generalization

Investigate whether trained models perform reliably across different patients, rehabilitation tasks, and recording conditions.

### 3. Ablation Studies

Measure the contribution of individual EEG and EMG features and determine which information is most important for classification.

### 4. Compensation Detection

Develop and evaluate methods for distinguishing intended muscle recruitment from compensatory activation patterns.

### 5. Uncertainty and Robustness

Investigate model behavior under noisy signals, missing data, sensor artifacts, and ambiguous movement attempts.

### 6. Therapist-in-the-Loop Evaluation

Explore approaches for incorporating clinician feedback, transparent decision explanations, and safety-constrained adjustments.

---

## Tools and Technologies

- Python
- Machine learning and classification
- Synthetic dataset generation
- Multimodal feature analysis
- Experimental evaluation
- Interactive AI dashboard development
- Git and GitHub

---

## Project Team

Developed by an international student research team through the **New York Academy of Sciences Junior Academy BrainTech Challenge**.

The project involved collaboration across:

- AI development and experimentation
- Scientific research and literature review
- System architecture
- Prototype development
- User experience
- Research communication

### My Contributions

As a team lead and AI developer, my primary contributions included:

- Developing and evaluating the Python-based AI experiment.
- Comparing EEG-only and EEG+EMG classification performance.
- Analyzing experimental results and documenting limitations.
- Developing the AI decision-support demonstration.
- Coordinating research tasks and interdisciplinary collaboration.
- Communicating with an external research expert to obtain feedback.
- Helping integrate technical findings into the final research presentation.

---

## Research Status

**Status:** Research-stage prototype

**Validation:** Synthetic-data experiments only

**Clinical testing:** Not conducted

**Medical-device readiness:** Not established

The project is intended for educational and exploratory scientific research. It should not be used for medical diagnosis, treatment decisions, or unsupervised rehabilitation assistance.

---

## Acknowledgments

We acknowledge the New York Academy of Sciences Junior Academy for providing the BrainTech Challenge research environment and the researchers and mentors who provided feedback on our proposed system.

---

## Contact and Collaboration

I am interested in research collaborations involving:

- Biomedical machine learning
- Neurotechnology and brain–computer interfaces
- Multimodal representation learning
- Trustworthy and interpretable AI
- Human-centered rehabilitation technologies

I welcome opportunities to contribute to reproducible research, collaborate with researchers, and explore ways to improve the scientific rigor and real-world relevance of biomedical AI systems.


The original V4 training labels include `Pattern Review Recommended` as a classifier class. The final interface maps that class to `Unclear` for its assistance recommendation and adds a separate pattern-review result. This is a **compatibility bridge**, not a retrained five-assistance-class model. The original V4 uses simulated EEG, EMG, fatigue, and IMU-derived features. It cannot establish real compensation detection or clinical performance.

Thresholds in `movement_review.py` and `safety.py` are hand-set demonstration thresholds, not medical limits. Therapist feedback is saved locally only and never retrains the model.
