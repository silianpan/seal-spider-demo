import re

content = 'Hello 1234567 World_This is a Regex Demo'
result = re.match('^Hello(\s(\d+)\s(World))', content)
print(result)
print(result.group(0))
print(result.group(1))
print(result.group(2))
print(result.group(3))
print(result.span())