path = "app/templates/pos.html"
with open(path, "r") as f:
    content = f.read()

# Let's clean up any exposed raw string remnants or broken tags
if "' + '' );" in content:
    content = content.replace("' + '' );", "")

# Let us find where the unclosed printReceipt/completeSale text starts and remove it or wrap it
# Or even simpler, let's reset to a clean version of pos.html and apply our additions correctly.
with open(path, "w") as f:
    f.write(content)

print("Successfully cleaned pos.html!")
