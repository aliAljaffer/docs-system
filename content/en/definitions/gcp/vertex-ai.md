---
title: vertex-ai
category: GCP
description: 'GCP note: Vertex-ai.'
tags:
- gcp
- ai
---


# vertex-ai

## Vertex AI
Vertex AI is a **unified artificial intelligence (AI) and machine learning (ML) platform** for building, deploying, and scaling ML models.

**AWS Equivalent:** Amazon SageMaker + Bedrock (combined)
### Overview
- End-to-end ML platform
- **Unified API** for all ML workflows
- Pre-trained models and custom models
- AutoML and custom training
- Model deployment and monitoring
- **Generative AI support** (Gemini, PaLM, Imagen)
### Key Components
#### Vertex AI Studio
- **Prompt design**: Test and iterate on prompts
- **Model tuning**: Fine-tune foundation models
- **Model Garden**: Pre-trained models (Gemini, PaLM, Llama, Claude, etc.)
- **Generative AI App Builder**: Build AI apps with minimal code
#### Vertex AI Workbench
- **Managed Jupyter notebooks**
- Pre-configured for ML frameworks (TensorFlow, PyTorch)
- Git integration
- BigQuery, Cloud Storage integration
- Executor for scheduled notebooks 
#### AutoML
- **AutoML Vision**: Image classification, object detection
- **AutoML Natural Language**: Text classification, entity extraction, sentiment analysis
- **AutoML Tables**: Structured data (classification, regression)
- **AutoML Video**: Video classification, object tracking
- **No code required** - automated model training
#### Custom Training
- Bring your own code (TensorFlow, PyTorch, scikit-learn)
- Distributed training
- Hyperparameter tuning
- Training pipelines
- GPU/TPU support
### Generative AI Features
#### Foundation Models
- **Gemini** (Google's latest multimodal model)
  - Gemini 1.5 Pro: Long context (2M tokens), multimodal
  - Gemini 1.5 Flash: Faster, lower cost
  - Gemini 1.0 Pro: General purpose
- **PaLM 2**: Text generation, code generation
- **Imagen**: Image generation
- **Codey**: Code generation and completion
- **Chirp**: Speech-to-text
#### Model Garden
- Access to 100+ models
- Google models (Gemini, PaLM, Imagen)
- Open source models (Llama 3, Mistral, Falcon)
- Third-party models (Anthropic Claude, Meta Llama)
- **One-click deployment**
### Prompt Design & Management
- **Prompt Gallery**: Pre-built prompts
- **Prompt testing**: A/B test prompts
- **Context caching**: Reduce costs for repeated context
- **Grounding**: Connect to Google Search, Vertex AI Search
- **Safety filters**: Block harmful content
### Model Tuning
- **Supervised fine-tuning**: Custom datasets
- **Adapter tuning**: Parameter-efficient fine-tuning
- **Distillation**: Smaller, faster models
- **RLHF**: Reinforcement learning from human feedback
### RAG (Retrieval-Augmented Generation)
- Vertex AI Search integration
- Connect to your own data ([[gcp/cloud-storage|Cloud Storage]], [[gcp/bigquery|BigQuery]], [[alloydb|AlloyDB]])
- Embeddings API for vector search
- Matching Engine for similarity search
### Model Deployment
#### Prediction Endpoints
- **Online prediction**: Low-latency, real-time
- **Batch prediction**: High-throughput, asynchronous
- **Private endpoints**: VPC-only access
- **Auto-scaling** based on traffic
- Multi-model endpoints
#### Model Monitoring
- **Feature skew detection**: Training vs serving data drift
- **Prediction drift**: Output distribution changes
- **Feature attribution**: Explainable AI
- Alerts on anomalies
### MLOps with Vertex AI
#### Pipelines
- **Vertex AI Pipelines**: Orchestrate ML workflows
- Based on Kubeflow Pipelines
- **DAG-based** workflow definition
- Reusable components
- Artifact lineage tracking
#### Experiments
- Track training runs
- Compare hyperparameters
- Visualize metrics
- Metadata tracking
#### Feature Store
- Centralized feature repository
- **Online serving** (low-latency)
- **Offline serving** (batch)
- Feature versioning
- Point-in-time lookup
#### Model Registry
- Centralized model repository
- Model versioning
- Model lineage
- Deploy from registry
### Pricing

| Product | Item | Price |
|---|---|---|
| Generative AI (Gemini) | Gemini 1.5 Pro | ~$7 per 1M input tokens, ~$21 per 1M output tokens |
| Generative AI (Gemini) | Gemini 1.5 Flash | ~$0.35 per 1M input tokens, ~$1.05 per 1M output tokens |
| Generative AI (Gemini) | Context caching | 75% discount on cached tokens |
| AutoML | Training | Per node-hour (~$20-40/hour depending on model type) |
| AutoML | Prediction | Per prediction + infrastructure |
| Custom Training | General | Per vCPU/GPU/TPU hour |
| Custom Training | N1 standard | ~$0.05/vCPU-hour |
| Custom Training | NVIDIA T4 GPU | ~$0.35/GPU-hour |
| Custom Training | TPU v3 | ~$8/TPU-hour |
| Prediction | Online | Per node-hour + request count |
| Prediction | Batch | Per node-hour |

---

## ACE Level

### Essential Commands
```bash
# List foundation models
gcloud ai models list --region=us-central1

# Generate text with Gemini
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT/locations/us-central1/publishers/google/models/gemini-1.5-pro:generateContent \
  -d '{
    "contents": {
      "role": "user",
      "parts": { "text": "Explain quantum computing" }
    }
  }'

# Create AutoML dataset
gcloud ai datasets create \
  --display-name=my-dataset \
  --region=us-central1

# Deploy model to endpoint
gcloud ai endpoints deploy-model ENDPOINT_ID \
  --region=us-central1 \
  --model=MODEL_ID \
  --display-name=my-deployment
```

### Key Concepts for ACE
- Understanding Vertex AI as unified ML platform
- Accessing Gemini and other foundation models
- Using AutoML for no-code ML
- Deploying models to endpoints
- Basic prompt engineering with Gemini
- Understanding online vs batch prediction
- Viewing model predictions in console

---

## PCA Level

### Architectural Patterns
#### Generative AI Application
```text
User Request → Cloud Run (API) → Vertex AI (Gemini) → Response
                                → RAG (Vertex AI Search) → Context
                                → Safety Filters → Validation
```

#### MLOps Pipeline
```text
Data Prep → Feature Store → Training (Vertex Pipelines) → Model Registry
                                                         → A/B Testing
                                                         → Production Endpoint
                                                         → Monitoring
```

#### Multimodal AI
```text
Images → Gemini 1.5 Pro → Analysis
Text   → (multimodal)   → Generation
Video  →                → Summarization
```

### Use Cases by Model Type
#### Gemini Models
- **Gemini 1.5 Pro**: Complex reasoning, long documents (2M tokens), multimodal
- **Gemini 1.5 Flash**: High-volume, low-latency, cost-sensitive
- **Use cases**: Chatbots, document analysis, code generation, summarization

#### RAG Applications
- Customer support with company docs
- Legal document search and analysis
- Technical documentation Q&A
- Knowledge base assistants

#### Custom Models
- Domain-specific predictions (fraud detection, churn prediction)
- Computer vision (defect detection, medical imaging)
- NLP (sentiment analysis, entity extraction)
### Cost Optimization
- **Context caching**: 75% savings on repeated context
- **Gemini Flash**: 50x cheaper than Pro for simple tasks
- **Batch prediction**: Cheaper than online for non-real-time
- **Model distillation**: Smaller models, lower cost
- **AutoML**: Cheaper than custom training for simple cases
- **Committed use**: Discounts for prediction endpoints
### Performance Optimization
#### Prompt Engineering
- Clear instructions, few-shot examples
- System instructions for consistent behavior
- Temperature tuning (0 = deterministic, 1 = creative)
- Token limits to control costs
#### Model Selection
- Gemini Flash for speed
- Gemini Pro for quality
- Context caching for repeated context
- Smaller models for simple tasks
#### Endpoint Configuration
- **Autoscaling**: Min/max replicas
- **Machine types**: Balance cost vs latency
- **Accelerators**: GPUs for custom models
- **Private endpoints**: VPC for security
### Security & Compliance
- **VPC Service Controls**: Prevent data exfiltration
- **CMEK**: Customer-managed encryption
- **IAM**: Fine-grained permissions
  - `aiplatform.user`: Use models
  - `aiplatform.admin`: Manage resources
- **Private endpoints**: No internet exposure
- **Data residency**: Regional model deployment
- **Safety filters**: Content moderation (Gemini)
### Responsible AI
- **Safety filters**: HARM_CATEGORY_* settings
- **Bias detection**: Model fairness evaluation
- **Explainable AI**: Feature attributions
- **Model monitoring**: Drift detection
- **Human review**: For sensitive applications
### Integration Patterns
#### With GCP Services
```text
BigQuery → Vertex AI (training data)
         → AutoML → Model
         → Batch Prediction → BigQuery (results)
```
#### Real-Time Inference
```text
Cloud Run → Vertex AI Endpoint → Gemini
         → Memorystore (caching) → Fast response
```
#### Batch Processing
```text
Cloud Storage (data) → Vertex AI Batch Prediction → Cloud Storage (results)
                                                   → BigQuery (analytics)
```
### Migration Strategies

| AWS service | Vertex AI equivalent |
|---|---|
| SageMaker Notebooks | Vertex AI Workbench |
| SageMaker Training | Vertex AI Custom Training |
| SageMaker Endpoints | Vertex AI Endpoints |
| SageMaker Feature Store | Vertex AI Feature Store |
| SageMaker Pipelines | Vertex AI Pipelines |
| Bedrock Claude | Vertex Model Garden (Claude) |
| Bedrock Titan | Gemini |
| Bedrock RAG | Vertex AI Search + Gemini |

Bedrock and Vertex AI use similar API patterns (REST, streaming).

### Monitoring & Observability
- **[[cloud-monitoring|Cloud Monitoring]]**: Prediction latency, error rate
- **[[cloud-logging|Cloud Logging]]**: Prediction logs, training logs
- **Model monitoring**: Feature drift, prediction drift
- **Vertex AI Experiments**: Training metrics tracking
- **Cost tracking**: Per-model cost attribution

### Well-Architected Considerations
- **Operational Excellence**: MLOps pipelines, automated retraining, monitoring
- **Reliability**: Multi-region endpoints, A/B testing, gradual rollouts
- **Security**: VPC SC, CMEK, IAM, safety filters, private endpoints
- **Performance**: Model selection, caching, autoscaling, right-sizing
- **Cost**: Context caching, Flash vs Pro, batch prediction, distillation
- **Sustainability**: Efficient models, right-sizing, batch processing

### PCA Exam Focus Areas
- **Model selection**: Gemini Pro vs Flash vs AutoML vs custom
- **RAG architecture**: Grounding with enterprise data
- **MLOps**: Pipelines, Feature Store, Model Registry
- **Cost optimization**: Caching, model selection, batch vs online
- **Security**: VPC SC, CMEK, responsible AI
- **Integration**: With BigQuery, Cloud Storage, Cloud Run
- **Monitoring**: Drift detection, explainability
