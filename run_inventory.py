def view_inventory(inventory):
    print("\n" + "="*70)
    for idx, item in enumerate(inventory, 1):
        print(f"{idx}. {item['name']}")
    print("="*70)

# Test run
view_inventory([{"name": "DEO ROLLON mn"}])
