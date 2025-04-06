# Transactions Service
## Base info 
Service works in following flow:

User query -> Supervisor agent -> NER agent -> TX 

## Example

```python
message: "отправь 0.01 ETH Ивану Иванову"

response:
{"to": "Иван Иванов", "value": 0.01}
```

In Future:
`MCP-server for Metamask extension` 