import kim

kim.CreateOrUpdate("tool", "verbose", 1)
kim.CreateOrUpdate("tooling", "verbose", "po")
kim.CreateOrUpdate("loss", "dict", {"a":1, "b":0})

kim.Remove("tool", "verbose")

print(kim.tool.verbose)