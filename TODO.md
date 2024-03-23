# TODOs

## Models

- [ ] **Data Grouping and Selection for Baseline Model:**

  - Clarify and document the criteria for song selection within the 10 defined music genre groups.
  - Include results from testing different numbers of groups in the project documentation.

- [ ] **Attribute Selection and Importance:**

  - Investigate and justify the limited number of input attributes for the advanced model. Consider adding more relevant features.

- [ ] **Model Comparison and Evaluation:**

  - Implement a systematic offline comparison of the models. Document the differences in performance clearly.
  - Address the lack of tuning and discussion regarding the hyperparameters of the K-means algorithm.

- [ ] **Success Criteria:**

  - Revisit and clearly document how the previously defined success criteria are being evaluated, including both business and analytical aspects.

## Service

- [ ] **Endpoint for Model Selection:**

  - Implement a single endpoint that automatically selects the model for generating predictions, removing the need for client-side model selection.

- [ ] **A/B Experiment Setup:**

  - Address the current separation of endpoints for models and lack of an A/B testing environment. Consider integrating an A/B testing framework.

## Performance and Efficiency

- [ ] **Efficiency of Traffic Splitting:**

  - Review and optimize the current method of running separate Python processes for each user, aiming to improve performance and efficiency.

- [ ] **Experiment A/B Control:**

  - Implement functionality to enable/disable the A/B testing split easily, allowing for the experiment's conclusion or pause as needed.

- [ ] **Logging for A/B Experiment:**
  - Set up a comprehensive logging system to capture and analyze data from the A/B experiment, enabling effective evaluation of model performance.
