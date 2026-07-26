# Prompt Engineering Cheatsheet

## Basic Techniques
- **Zero-shot**: Direct instructions without examples
- **One-shot**: Single example for demonstration
- **Few-shot**: Multiple examples for pattern establishment

## Configuration Parameters
- **Temperature**: 0.0 (deterministic) → 1.5 (creative)
- **Top-p**: Nucleus sampling threshold
- **Top-k**: Number of top tokens to consider

## Reasoning Techniques
- **Chain-of-Thought**: Show reasoning steps
- **Self-Consistency**: Multiple samples + majority vote
- **Plan-and-Solve**: Break down complex problems

## Complex Workflows
- **Chain of Draft**: Concise reasoning steps (~5 words each), ~80% fewer tokens than CoT
- **System 2 Attention**: Filter irrelevant context before answering (2-step process)
- **Prompt Chaining**: Sequential prompts, output feeds input (validate between steps)
- **Meta Prompting**: Model generates/optimizes its own prompts (evaluate → optimize → repeat)

## Safety Considerations
- Validate user inputs
- Implement content filtering
- Test for adversarial attacks

## Best Practices
1. Be specific and clear
2. Use examples when helpful
3. Iterate and test
4. Consider edge cases
5. Document your prompts
