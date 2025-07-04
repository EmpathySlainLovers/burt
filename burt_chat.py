from transformers import pipeline

# Load fill-mask pipeline
mlm = pipeline("fill-mask", model="boltuix/bert-mini")

print("👋 Hi, I'm Burt. Type something with a [MASK] and I’ll complete it.")
print("Type 'exit' to leave.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    try:
        results = mlm(user_input)
        for r in results:
            print("🤖 Burt:", r['sequence'])
    except Exception as e:
        print("⚠️ Error:", str(e))
