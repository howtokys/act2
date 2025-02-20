import pickle

# Example local inventory data
local_inventory = {
    0xA1: 10,
    0xB2: 5,
}

# Save the local inventory to a file
with open("localInv.pickle", "wb") as f:
    pickle.dump(local_inventory, f)

print("localInv.pickle created.")