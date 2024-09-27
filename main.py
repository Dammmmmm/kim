import kim
import importlib.util


kim.Remove(True)
kim.CreateOrUpdate(category="tool", name="verbose", value=155)

print(kim.tool.verbose)

