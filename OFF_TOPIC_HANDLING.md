# Off-Topic Question Handling

## How It Works

The app now intelligently detects when a question is not related to the website content and provides helpful feedback.

## Implementation

### Relevance Checking

When a user asks a question:

1. **Embedding Search**: The question is converted to an embedding and searched against the website content
2. **Distance Calculation**: The system calculates the "distance" between the question and the most relevant content
3. **Relevance Threshold**: If the distance is > 1.5, the question is considered off-topic

```python
min_distance = D[0][0]  # Get the closest match distance

if min_distance > 1.5:
    # Question is off-topic
    answer = "I couldn't find relevant information..."
else:
    # Question is relevant, generate answer
    answer = generate_answer(prompt)
```

### Distance Scores

- **0.0 - 0.5**: Highly relevant (exact or very close match)
- **0.5 - 1.0**: Relevant (good match)
- **1.0 - 1.5**: Somewhat relevant (weak match)
- **> 1.5**: Not relevant (off-topic)

## Examples

### Example 1: On-Topic Question

**Website**: Documentation about Python programming
**Question**: "What is a Python list?"
**Distance**: 0.3
**Result**: ✅ Answers from website content

### Example 2: Off-Topic Question

**Website**: Documentation about Python programming
**Question**: "What is the capital of France?"
**Distance**: 2.1
**Result**: ⚠️ "I couldn't find relevant information in the website to answer your question..."

### Example 3: Partially Related Question

**Website**: Documentation about Python programming
**Question**: "How do I cook pasta?"
**Distance**: 1.8
**Result**: ⚠️ Off-topic message

## User Experience

### When Question is Relevant:
```
User: What is AI?
Bot: AI is artificial intelligence, which refers to...
     [Shows sources in expander]
```

### When Question is Off-Topic:
```
User: What is the weather today?
Bot: ⚠️ I couldn't find relevant information in the website 
     to answer your question. This question might be outside 
     the scope of the processed website content. Please ask 
     questions related to the website's content.
```

## Benefits

1. **Prevents Confusion**: Users know when their question is off-topic
2. **Saves Time**: No need to wait for irrelevant answers
3. **Better UX**: Clear feedback about what the bot can and cannot answer
4. **Accurate Responses**: Only answers questions it has information about

## Improved Prompt

The prompt now also instructs the model to be honest when it doesn't have enough information:

```python
prompt = """Answer the question using only the information in the context. 
If the context doesn't contain enough information to answer the question, 
say "I don't have enough information to answer this question based on 
the website content."

Context:
{retrieved_text}

Question:
{question}

Answer:"""
```

## Testing

### Test Case 1: Relevant Question
1. Process a website about technology
2. Ask: "What is mentioned about AI?"
3. Expected: Relevant answer with sources

### Test Case 2: Off-Topic Question
1. Process a website about technology
2. Ask: "What is the recipe for chocolate cake?"
3. Expected: Warning message about off-topic question

### Test Case 3: Borderline Question
1. Process a website about Python
2. Ask: "What is Java?" (different programming language)
3. Expected: Either off-topic message or "I don't have enough information..."

## Adjusting the Threshold

If you find the threshold too strict or too lenient, you can adjust it:

```python
# More strict (fewer off-topic warnings)
if min_distance > 2.0:

# More lenient (more off-topic warnings)
if min_distance > 1.0:

# Current setting (balanced)
if min_distance > 1.5:
```

## Technical Details

### Distance Metric
- Uses cosine distance in the embedding space
- Calculated by FAISS during similarity search
- Lower distance = more similar embeddings

### Why This Works
- Questions about unrelated topics have very different embeddings
- The embedding model captures semantic meaning
- Unrelated concepts are far apart in embedding space

## Limitations

1. **Model Dependent**: Accuracy depends on the embedding model quality
2. **Threshold Tuning**: May need adjustment for different content types
3. **Edge Cases**: Some borderline questions might be misclassified
4. **Language**: Works best with English content

## Future Improvements

Potential enhancements:
- Dynamic threshold based on content type
- Multiple relevance levels (high/medium/low)
- Suggest related questions when off-topic
- Learn from user feedback to improve threshold

## Summary

The app now:
- ✅ Detects off-topic questions using distance scores
- ✅ Provides helpful feedback when questions are unrelated
- ✅ Only attempts to answer relevant questions
- ✅ Improves user experience with clear communication
- ✅ Prevents confusing or incorrect answers

This makes the chatbot more reliable and user-friendly by being honest about its limitations.
