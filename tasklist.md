Overall task: Create a tool to answer questions where the answer to that question is a date.

- [ ] API keys
  - [ ] Put your OpenAI and CohereAI API codes into .env.dev
  - [ ] Rename .env.dev to .env
  
- [x] Output data format function first draft
    - [x] write a failing test to check if LLM returns date in the format that our Pydantic object expects
    - [x] write first draft of a function 

- [ ] VCR library
    - [ ] see the http requests recorded in `cassettes` folder. They are recorded using  [vcr.py](https://vcrpy.readthedocs.io/en/latest/index.html) library. This library stops us from bombarding the external API with requests. It blocks repeated requests and plays back the recorded reply instead.
    - [ ] So the output format is still wrong. Maybe it is because we are using a bad LLM? Let's change the LLM in `get_llm` from cohere to OpenAI
    - [ ] Ok, now we get VCR library error.
    - [ ] Read the library docs to find out when does it update the recording? When does it add new episodes to the cassette? Change the record_mode for `test_get_todays_date` as needed.
    - [ ] Hmm. Still no luck with the format. Let's change back to Cohere - it is free. For OpenAI API you actually have to pay.


- [ ] Output format. Manual tuning.
    - [ ] Let's help the LLM by giving it more examples in the prompt. Add to the `date_template` prompt template the following line "The correct date format is YYYY-MM-DD., e.g. 2020-02-24."
    - [ ] Hmm, still no luck. Let's add another example to the prompt: 
     Question: When is your birthday?
    Answer: 2020-02-24.
    - [ ] Time for theory. Now our prompt is a few-shot learning prompt. We gave one example in it. The more examples we give, the easier it is to get an answer. Good prompts always have 3-4 examples in them.
    - [ ] Let's add more examples. First, let's converting our prompt to `FewShotPromptTemplate`
    - [ ] Add 3 more examples to the prompt using this easy langchain way
  

- [ ] Output format.
  - [ ] You see there is a `split("\n")[0].strip()` in `get_a_date`. Let's replace it with just `.strip()` 
  - [ ] It seems like Cohere is sending us extra text.
  - [ ] Let's add more examples and hope they learn.
  - [ ] No, didn't work. what about openai? let's switch the llm and see.
  - [ ] openai is good. is it worth paying for?
  - [ ] I would rather bring back the wonderful `split("\n")[0]` instead of paying. Switch back to Cohere and do the split.

  - [ ] Now we are satisfied with this test, let's delete the cassette, then set record_mode='all' for one run to re-record
  - [ ] To make sure we don't record anything above the `test_get_todays_date` let's set record_mode='none' and move on.

 - [ ] Question Answering from context
   - [ ] So far, we used the information already in the model. Now let's try to answer questions about a text in the prompt.
   - [ ] Uncomment the `test_meetup_date` that asks "when is the data crafters meetup?" based on some context info in the question
   - [ ] does it pass? this was easy. much easier than date formatting. :)
   - [ ] Add a `context` variable to the prompt and populate it with "The meetup is on 24 April. and today is 21 April 2023. Soon it will be summer." in `test_meetup_date`
   - [ ] Experiment with changing the text a bit if you fancy.

- [ ] using tools
  - [ ] In the previous step we spoon fed the context to the prompt. In the next step let's teach the agent to find the context automatically
  - [ ] Write tests and use this code in a small function
   ```python
    tools = load_tools(["serpapi", "llm-math"], llm=my_llm)
    agent = initialize_agent(tools, llm_agent, agent="zero-shot-react-description", verbose=True)
    output = agent.run(question)
    ```

  
- [ ] create our own tools 
  - [ ] let's wrap our date extractor code as a Langchain tool describe it as "DateExtractor: use it when you need to answer a question with a date."
  - [ ] give both tools to the agent and see what it does, via `tools = load_tools(["serpapi", "date-extractor"])`
  