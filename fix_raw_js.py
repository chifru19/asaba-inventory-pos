with open("app/templates/pos.html", "r") as f:
    content = f.read()

# If raw JS text is loose in the body, let's wrap it properly or clean up
if "function completeSale()" in content and "<script>" not in content[content.find("function completeSale()"):]:
    # Ensure proper script encapsulation if broken
    print("Fixing unscripted JavaScript blocks in pos.html...")

# Let us do a clean reset of pos.html template structure to ensure no stray text
