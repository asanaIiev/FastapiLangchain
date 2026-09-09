# from langchain.messages import HumanMessage, SystemMessage
# from langchain_ollama.chat_models import ChatOllama
# from time import perf_counter

# start_time = perf_counter()
# first_chunk: None = None
# full_response = None

# model = ChatOllama(
#     model='llama3.2:latest',
#     temperature=0,
#     top_k=3,
#     num_predict=500,
#     seed=1
# )

# message = [
#     SystemMessage(
#         content='U are a 10 years experienced dart specialist.' \
#         'U reply to every user based on their level of understanding dart language,' \
#         'or based on their question'
#     ),
#     HumanMessage(
#         content='What is the difference between dart, flutter, swift'
#     )
# ]

# for i in model.stream(message):
#     if i.text and first_chunk is None:
#         first_chunk = perf_counter()

#     print(str(i.text), end='', flush=True)

#     full_response = i if full_response is None else full_response + i

# finish_time = perf_counter()

# if full_response is not None:
#     ttft = first_chunk - start_time
#     print()
#     print()
#     print(f'TTFT: {round(ttft, 2)} seconds')

#     total_time = finish_time - start_time
#     print(f'total_time: {total_time:.2f} seconds')


# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import ChatOllama

# promt = ChatPromptTemplate.from_messages(
#     [
#         (
#             'system',
#             'U are a {language} teacher.'
#             'U have to teach to students whose level is {level}.'
#             'Always give code examples',
#         ),
#         ('human', 'Explain this topic: {topic}'),
#     ]
# )

# model = ChatOllama(
#     model='llama3.2:latest', temperature=0, top_k=3, num_predict=500
# )

# chain = promt | model

# for chunk in chain.stream({
#     'language': 'Python',
#     'level': 'Starter',
#     'topic': 'Is it true that the generator is one of the ways of realization iterator?',
# }):
#     print(chunk.content, end='', flush=True)