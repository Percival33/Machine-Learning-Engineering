# Machine Learning Engineering

## Team

- Miłosz Mizak
- Marcin Jarczewski

## Project Overview

This project is a part of the Machine Learning Engineering at Warsaw University of Technology course aimed at developing a practical solution for "Pozytywka," an online music streaming service. As analysts, we step into the role of tackling a vaguely described task, requiring us to specify details for implementation. The challenge involves understanding the problem, analyzing data, and sometimes negotiating with management (tutor) to ensure the models are production-ready and future-proof for subsequent versions.

### Data Collection

"Pozytywka" collects data crucial for this project, including:

- A list of available artists and music tracks
- A user database
- User session history
- Technical information regarding the caching level of individual tracks

## Task

Extend the "Pozytywka" service by generating popular playlists – sets of matching songs tailored to capture the interest of a broad audience. This initiative aims to enhance user engagement by offering compilations based on the most popular music genres, updated weekly with 10 to 20 songs each.

## Project Phases

### Stage 1

- Define the business problem, modeling tasks, assumptions, and success criteria.
- Analyze the provided data to assess sufficiency for task realization, identifying any gaps or requirements for additional data.

Report available [here](./reports/JarczewskiMizak_05wariant02_etap1.ipynb) (in Polish).

### Stage 2

1. **Model Development:**
   - Develop a baseline model (the simplest possible for the given task).
   - Develop an advanced target model.
   - Report detailing the model building process and comparing results.
2. **Application Implementation:**
   - Implement an application (as a microservice) that:
     - Serves predictions using the developed model.
     - Conducts an A/B experiment comparing both models and collects data for later quality assessment.
3. **Demonstration Materials:**
   - Provide materials showing the implementation is functional.

Report available [here](./reports/JarczewskiMizak_05wariant02_etap2.ipynb) (in Polish).

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
