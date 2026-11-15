path = "app/templates/pos.html"
with open(path, "r") as f:
    content = f.read()

# Clean up any broken string literals or raw js leaks from previous edits
if "' + '' );" in content:
    content = content.replace("' + '' );", "")

# Ensure all scripts are properly closed and structured
if "<script>" in content and "</script>" not in content[content.rfind("<script>"):]:
    content += "\n</script>"

with open(path, "w") as f:
    f.write(content)

print("Successfully cleaned and repaired pos.html!")
