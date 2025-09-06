Structured data response with Amazon Bedrock: Prompt Engineering and Tool Use
by Adam Nemeth and Dominic Searle on 26 JUN 2025 in Amazon Bedrock, Best Practices, Generative AI, Intermediate (200), Technical How-to Permalink  Comments  Share
Generative AI is revolutionizing industries by streamlining operations and enabling innovation. While textual chat interactions with GenAI remain popular, real-world applications often depend on structured data for APIs, databases, data-driven workloads, and rich user interfaces. Structured data can also enhance conversational AI, enabling more reliable and actionable outputs. A key challenge is that LLMs (Large Language Models) are inherently unpredictable, which makes it difficult for them to produce consistently structured outputs like JSON. This challenge arises because their training data mainly includes unstructured text, such as articles, books, and websites, with relatively few examples of structured formats. As a result, LLMs can struggle with precision when generating JSON outputs, which is crucial for seamless integration into existing APIs and databases. Models vary in their ability to support structured responses, including recognizing data types and managing complex hierarchies effectively. These capabilities can make a difference when choosing the right model.

This blog demonstrates how Amazon Bedrock, a managed service for securely accessing top AI models, can help address these challenges by showcasing two alternative options:

Prompt Engineering: A straightforward approach to shaping structured outputs using well-crafted prompts.
Tool Use with the Bedrock Converse API: An advanced method that enables better control, consistency, and native JSON schema integration.
We will use a customer review analysis example to demonstrate how Bedrock generates structured outputs, such as sentiment scores, with simplified Python code.

Building a prompt engineering solution
This section will demonstrate how to use prompt engineering effectively to generate structured outputs using Amazon Bedrock. Prompt engineering involves crafting precise input prompts to guide large language models (LLMs) in producing consistent and structured responses. It is a fundamental technique for developing Generative AI applications, particularly when structured outputs are required.Here are the five key steps we will follow:

Configure the Bedrock client and runtime parameters.
Create a JSON schema for structured outputs.
Craft a prompt and guide the model with clear instructions and examples.
Add a customer review as input data to analyse.
Invoke Bedrock, call the model, and process the response.
While we demonstrate customer review analysis to generate a JSON output, these methods can also be used with other formats like XML or CSV.

Step 1: Configure Bedrock
To begin, we’ll set up some constants and initialize a Python Bedrock client connection object using the Python Boto3 SDK for Bedrock runtime, which facilitates interaction with Bedrock:

Python code configuring AWS Bedrock client with Anthropic Claude model and parameters

The REGION specifies the AWS region for model execution, while the MODEL_ID identifies the specific Bedrock model. The TEMPERATURE constant controls the output randomness, where higher values increase creativity, and lower values maintain precision, such as when generating structured output. MAX_TOKENS determines the output length, balancing cost-efficiency and data completeness.

Step 2: Define the Schema
Defining a schema is essential for facilitating structured and predictable model outputs, maintaining data integrity, and enabling seamless API integration. Without a well-defined schema, models may generate inconsistent or incomplete responses, leading to errors in downstream applications. The JSON standard schema used in the code below serves as a blueprint for structured data generation, guiding the model on how to format its output with explicit instructions.

Let’s create a JSON schema for customer reviews with three required fields: reviewId (string, max 50 chars), sentiment (number, -1 to 1), and summary (string, max 200 chars).

JSON schema for customer reviews with fields for ID, sentiment score, and summary, specifying data types and constraints
Step 3: Craft the Prompt text
To generate consistent, structured, and accurate responses, prompts must be clear and well-structured, as LLMs rely on precise input to produce reliable outputs. Poorly designed prompts can lead to ambiguity, errors, or formatting issues, disrupting structured workflows, so we follow these best practices:

Clearly outline the AI’s role and objectives to avoid ambiguity.
Divide tasks into smaller, manageable numbered steps for clarity.
Indicate that a JSON schema will be provided (see Step 5 below) to maintain a consistent and valid structure.
Use one-shot prompting with a sample output to guide the model; add more examples if needed for consistency, but avoid too many, as they may limit the model’s ability to handle new inputs.
Define how to handle missing or invalid data.
Instructions for AI system to analyze customer reviews and return JSON data with example response format

Step 4: Integrate Input Data
For demonstration purposes, we’ll include a review text in the prompt as a Python variable:

Customer review input data showing positive feedback about delivery, product quality, and service

Separating the input data with <input> tags improve readability and clarity, making it straightforward to identify and reference. This hardcoded input simulates real-world data integration. For production use, you might dynamically populate input data from APIs or user submissions.

Step 5: Call Bedrock
In this section, we construct a Bedrock request by defining a body object that includes the JSON schema, prompt, and input review data from previous steps. This structured request makes sure the model receives clear instructions, adheres to a predefined schema, and processes sample input data correctly. Once the request is prepared, we invoke Amazon Bedrock to generate a structured JSON response.

AWS Bedrock client setup with model parameters, message content, and API call for customer review analysis

We reuse the MAX_TOKENS, TEMPERATURE, and MODEL_ID constants defined in Step 1. The body object has essential inference configurations like anthropic_version for model compatibility and the messages array, which includes a single message to provide the model with task instructions, the schema, and the input data. The role defines the “speaker” in the interaction context, with user value representing the program sending the request. Alternatively, we could simplify the input by combining instructions, schema, and data into one text prompt, which is straightforward to manage but less modular.

Finally, we use the client.invoke_model method to send the request. After invoking, the model processes the request, and the JSON data must be properly (not explained here) extracted from the Bedrock response. For example:

JSON format customer feedback data showing high sentiment (0.9) with positive comments on delivery, quality, and service

Tool Use with the Amazon Bedrock Converse API
In the previous chapter, we explored a solution using Bedrock Prompt Engineering. Now, let’s look at an alternative approach for generating structured responses with Bedrock.

We will extend the previous solution by using the Amazon Bedrock Converse API, a consistent interface designed to facilitate multi-turn conversations with Generative AI models. The API abstracts model-specific configurations, including inference parameters, simplifying integration.

A key feature of the Converse API is Tool Use (also known as Function Calling), which enables the model to execute external tools, such as calling an external API. This method supports standard JSON schema integration directly into tool definitions, facilitating output alignment with predefined formats. Not all Bedrock models support Tool Use, so make sure you check which models are compatible with these feature.

Building on the previously defined data, the following code provides a straightforward example of Tool Use tailored to our curstomer review use case:

AWS Bedrock API implementation code showing tool configuration, message structure, and model inference setup for review analysis

In this code the tool_list defines a custom customer review analysis tool with its input schema and purpose, while the messages provide the earlier defined instructions and input data. Unlike in the previous prompt engineering example we used the earlier defined JSON schema in the definition of a tool. Finally, the client.converse call combines these components, specifying the tool to use and inference configurations, resulting in outputs tailored to the given schema and task. After exploring Prompt Engineering and Tool Use in Bedrock solutions for structured response generation, let’s now evaluate how different foundation models perform across these approaches.

Test Results: Claude Models on Amazon Bedrock
Understanding the capabilities of foundation models in structured response generation is essential for maintaining reliability, optimizing performance, and building scalable, future-proof Generative AI applications with Amazon Bedrock. To evaluate how well models handle structured outputs, we conducted extensive testing of Anthropic’s Claude models, comparing prompt-based and tool-based approaches across 1,000 iterations per model. Each iteration processed 100 randomly generated items, providing broad test coverage across different input variations.The examples shown earlier in this blog are intentionally simplified for demonstration purposes, where Bedrock performed seamlessly with no issues. To better assess the models under real-world challenges, we used a more complex schema that featured nested structures, arrays, and diverse data types to identify edge cases and potential issues. The outputs were validated for adherence to the JSON format and schema, maintaining consistency and accuracy. The following diagram summarizes the results, showing the number of successful, valid JSON responses for each model across the two demonstrated approaches: Prompt Engineering and Tool Use.

Bar graph showing success rates of prompt vs tool approaches in structured generation for haiku and sonnet AI models

The results demonstrated that all models achieved over 93% success across both approaches, with Tool Use methods consistently outperforming prompt-based ones. While the evaluation was conducted using a highly complex JSON schema, simpler schemas result in significantly fewer issues, often nearly none. Future updates to the models are expected to further enhance performance.

Final Thoughts
In conclusion, we demonstrated two methods for generating structured responses with Amazon Bedrock: Prompt Engineering and Tool Use with the Converse API. Prompt Engineering is flexible, works with Bedrock models (including those without Tool Use support), and handles various schema types (e.g., Open API schemas), making it a great starting point. However, it can be fragile, requiring exact prompts and struggling with complex needs. On the other hand, Tool Use offers greater reliability, consistent results, seamless API integration, and runtime validation of JSON schema for enhanced control.

For simplicity, we did not demonstrate a few areas in this blog. Other techniques for generating structured responses include using models with built-in support for configurable response formats, such as JSON, when invoking models, or leveraging constraint decoding techniques with third-party libraries like LMQL. Additionally, generating structured data with GenAI can be challenging due to issues like invalid JSON, missing fields, or formatting errors. To maintain data integrity and handle unexpected outputs or API failures, effective error handling, thorough testing, and validation are essential.

To try the Bedrock techniques demonstrated in this blog, follow the steps to Run example Amazon Bedrock API requests through the AWS SDK for Python (Boto3). With pay-as-you-go pricing, you’re only charged for API calls, so little to no cleanup is required after testing. For more details on best practices, refer to the Bedrock prompt engineering guidelines and model-specific documentation, such as Anthropic’s best practices.

Structured data is key to leveraging Generative AI in real-world scenarios like APIs, data-driven workloads, and rich user interfaces beyond text-based chat. Start using Amazon Bedrock today to unlock its potential for reliable structured responses.