---
title: Gemini
category: GCP
description: 'GCP note: Gemini.'
tags:
- gcp
- ai
---


# Gemini

`gcp` `ai`

## Gemini
Google's **multimodal foundation model** for text, images, video, and code

**AWS Equivalent:** Amazon Bedrock Claude 3 (closest comparison)
### Overview
- **Multimodal**: Native support for text, images, video, audio, code
- **Long context**: Up to **2 million tokens** (Gemini 1.5 Pro)
- **State-of-the-art**: Competitive with GPT-4, Claude 3
- Available via [[vertex-ai|Vertex AI]], Gemini API, AI Studio
### Model Variants

| Model | Context | Input price (per 1M tokens) | Output price (per 1M tokens) | Best for | Notes |
|---|---|---|---|---|---|
| Gemini 1.5 Pro | **2M tokens** (largest in industry) | ~$7 | ~$21 | Complex analysis, long documents, video understanding | Multimodal (text, images, video, audio), best quality and reasoning, context caching gives 75% discount on cached tokens |
| Gemini 1.5 Flash | **1M tokens** | ~$0.35 | ~$1.05 | High-volume, low-latency, simple tasks | Faster inference, lower cost, **50x cheaper** than Pro |
| Gemini 1.0 Pro | 32K tokens | - | - | Standard text generation | Original model (still available), lower cost than 1.5 Pro |

### Capabilities
#### Text Generation
- Conversation, Q&A
- Summarization
- Translation
- Content creation
- Code generation

#### Multimodal Understanding
- **Image analysis**: Describe images, OCR, object detection
- **Video analysis**: Summarize videos, frame-by-frame analysis
- **Audio transcription**: Speech-to-text
- **PDF processing**: Extract and analyze PDF content

#### Code Generation
- Code completion
- Code explanation
- Debugging assistance
- Multi-language support (Python, Java, JavaScript, Go, etc.)

### Key Features
#### Long Context
- ==2M tokens = ~1,400 pages== of text
- Analyze entire codebases
- Process long documents without chunking
- Maintain full conversation history

#### Context Caching
- Cache up to 2M tokens
- **75% cost reduction** on cached tokens
- Automatic cache management
- TTL: 1 hour (extendable)
- Use cases: Repeated queries on same document, chatbots with large context

#### Grounding
- Connect to **Google Search** for real-time information
- Connect to **Vertex AI Search** for enterprise data
- Reduces hallucinations
- Provides source citations

#### Function Calling
- Define functions Gemini can call
- Structured output
- Integrate with APIs and databases
- Use cases: Tool use, data retrieval

### Safety & Filtering
#### Harm Categories
- `HARM_CATEGORY_HATE_SPEECH`
- `HARM_CATEGORY_DANGEROUS_CONTENT`
- `HARM_CATEGORY_HARASSMENT`
- `HARM_CATEGORY_SEXUALLY_EXPLICIT`

#### Threshold Levels

| Threshold | Blocks |
|---|---|
| `BLOCK_NONE` | No blocking |
| `BLOCK_LOW_AND_ABOVE` | Block low+ harmful content |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium+ (default) |
| `BLOCK_HIGH_AND_ABOVE` | Block only high harmful content |

### Generation Configuration
```python
generation_config = {
    "temperature": 0.7,        # 0=deterministic, 1=creative
    "top_p": 0.95,             # Nucleus sampling
    "top_k": 40,               # Top-k sampling
    "max_output_tokens": 8192, # Response length limit
    "stop_sequences": ["END"], # Stop generation at sequence
}
```

### Use Cases by Variant
#### Gemini 1.5 Pro
✓ Document analysis (contracts, research papers)
✓ Video content moderation
✓ Codebase analysis
✓ Multi-turn conversations with long history
✓ Complex reasoning tasks

#### Gemini 1.5 Flash
✓ High-volume chatbots
✓ Real-time classification
✓ Simple summarization
✓ Image captioning
✓ Code completion

---

## ACE Level

### Basic Usage
```python
from vertexai.generative_models import GenerativeModel

# Initialize model
model = GenerativeModel("gemini-1.5-pro")

# Generate text
response = model.generate_content("Explain cloud computing")
print(response.text)

# Multimodal (image + text)
import vertexai
from vertexai.generative_models import Part

image = Part.from_uri("gs://bucket/image.jpg", mime_type="image/jpeg")
response = model.generate_content([image, "What's in this image?"])
print(response.text)

# Streaming
responses = model.generate_content("Write a story", stream=True)
for response in responses:
    print(response.text, end="")
```

### Key Concepts for ACE
- Understanding Gemini model variants (Pro vs Flash)
- Basic text generation with prompts
- Multimodal inputs (text + images)
- Accessing via Vertex AI Studio
- Understanding context window limits
- Basic safety settings

---

## PCA Level

### Architectural Patterns
#### RAG with Gemini
```text
User Query → Embedding → Vector Search (Matching Engine)
          → Retrieved Docs → Gemini (with context) → Answer
```

#### Multimodal Analysis Pipeline
```text
Video Upload → Cloud Storage → Gemini 1.5 Pro (analyze)
                             → Extract insights
                             → Store in BigQuery
                             → Dashboard
```

#### Chatbot with Context Caching
```text
User Message → Check Cache → Gemini (cached context + new query)
            → System Instructions (cached)
            → Company Docs (cached)
            → Response
```

### Cost Optimization Strategies
#### Context Caching Example
```python
# First request: Full cost
context = "...large system instructions and docs (500K tokens)..."
response = model.generate_content(context + query1)  # $3.50

# Subsequent requests: 75% discount on cached tokens
response = model.generate_content(context + query2)  # $0.875 + new tokens
```
- **Save 75% on repeated context**
- Ideal for: Chatbots, document Q&A, code analysis
- Cache persists 1 hour, auto-refresh on use

#### Model Selection by Use Case

| Use Case              | Model | Reasoning                 |
| --------------------- | ----- | ------------------------- |
| Simple classification | Flash | 50x cheaper, fast enough  |
| Complex reasoning     | Pro   | Better quality worth cost |
| Long documents        | Pro   | 2M context needed         |
| High-volume API       | Flash | Cost and speed            |
| Video analysis        | Pro   | Multimodal quality        |

### Performance Optimization
#### Prompt Engineering
```python
# Bad: Vague prompt
"Tell me about this document"

# Good: Specific, structured prompt
"""Analyze this contract and extract:
1. Parties involved
2. Key obligations
3. Termination clauses
4. Payment terms

Format as JSON."""
```

#### Batch Processing
- Use async requests for non-real-time
- Process multiple inputs in parallel
- Aggregate results
- Lower cost than online inference
#### Streaming for UX
```python
# Non-streaming: User waits for full response
response = model.generate_content(prompt)  # 5 seconds wait

# Streaming: User sees progressive response
for chunk in model.generate_content(prompt, stream=True):
    display(chunk.text)  # Immediate feedback
```
### Security & Compliance
#### Private Deployment
```python
# VPC-only endpoint (no internet access)
from google.cloud import aiplatform

endpoint = aiplatform.Endpoint(
    endpoint_name="projects/PROJECT/locations/REGION/endpoints/ENDPOINT",
    private=True
)
```

#### Data Residency
- Regional model deployment
- EU data stays in EU regions
- Compliance with GDPR, data sovereignty
#### Safety Configuration
```python
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

response = model.generate_content(
    prompt,
    safety_settings=safety_settings
)
```

### Advanced Features
#### Function Calling
```python
tools = [
    {
        "function_declarations": [
            {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    }
                }
            }
        ]
    }
]

response = model.generate_content(
    "What's the weather in London?",
    tools=tools
)

# Gemini returns function call
function_call = response.candidates[0].content.parts[0].function_call
# Execute function, return result to Gemini
```

#### Grounding with Google Search
```python
from vertexai.preview.generative_models import grounding

response = model.generate_content(
    "What are the latest AI breakthroughs in 2026?",
    grounding_source=grounding.GoogleSearchRetrieval()
)

# Response includes citations from search results
```

### Monitoring & Observability
```python
# Log predictions for monitoring
import logging

logging.info({
    "model": "gemini-1.5-pro",
    "prompt_tokens": response.usage_metadata.prompt_token_count,
    "output_tokens": response.usage_metadata.candidates_token_count,
    "total_tokens": response.usage_metadata.total_token_count,
    "latency_ms": latency,
    "safety_ratings": response.candidates[0].safety_ratings
})
```

### Migration from Other LLMs
#### From OpenAI GPT-4
- Similar API patterns (messages, roles)
- Gemini Pro comparable to GPT-4
- Gemini Flash comparable to GPT-3.5 Turbo
- 2M context vs 128K (GPT-4 Turbo)
- **Better pricing on GCP** with context caching

#### From Anthropic Claude
- Claude available in Vertex Model Garden
- Gemini Pro comparable to Claude 3 Opus
- Gemini Flash comparable to Claude 3 Haiku
- Unified API via Vertex AI

### Well-Architected Considerations
- **Operational Excellence**: Vertex AI Studio for testing, versioning, monitoring
- **Reliability**: Multi-region deployment, fallback models, retry logic
- **Security**: VPC endpoints, safety filters, IAM, data residency
- **Performance**: Context caching, streaming, model selection (Flash vs Pro)
- **Cost**: Flash for volume, caching for repeated context, batch processing
- **Sustainability**: Efficient models (Flash), caching reduces compute

### PCA Exam Focus Areas
1. **Model selection**: When to use Pro vs Flash vs other models
2. **Context caching**: 75% cost savings, use cases
3. **Multimodal applications**: Image/video analysis architectures
4. **RAG patterns**: Grounding with enterprise data
5. **Cost optimization**: Caching, model selection, batch processing
6. **Security**: Safety filters, private endpoints, data residency
7. **Integration**: With Cloud Storage, BigQuery, Cloud Run
8. **Responsible AI**: Safety settings, bias mitigation, human review
