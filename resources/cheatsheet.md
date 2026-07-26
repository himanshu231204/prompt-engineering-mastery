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
