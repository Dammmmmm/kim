import kim

kim.CreateOrUpdate("tool", "verbose", 1)
kim.CreateOrUpdate("tooling", "verbose", "po")
kim.CreateOrUpdate("loss", "dict", {"a":1, "b":0})

print(kim.tool.verbose)
print(kim.tooling.verbose)
print(kim.loss.dict)

