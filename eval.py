from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Chota sa labeled dataset check karne ke liye
eval_data = [
    {"post": "A beautiful orange animal with a bushy tail in the snow.", "expected": "fox.jpg"},
    {"post": "A wild gray canine walking through the snowy field.", "expected": "wolf.jpg"}
]

def run_evaluation():
    print("--- Starting AI Precision Evaluation ---\n")
    correct = 0
    total = len(eval_data)
    
    for item in eval_data:
        print(f"Testing Post: '{item['post']}'")
        response = client.post("/recommend", json={"blog_text": item["post"]})
        
        if response.status_code == 200:
            recommended = response.json().get("recommended_image")
            if recommended == item["expected"]:
                correct += 1
                print(f"✅ Result: Got '{recommended}' (Correct)\n")
            else:
                print(f"❌ Result: Expected '{item['expected']}', but got '{recommended}'\n")
        else:
            print("❌ API Error or No Match Found\n")

    precision = (correct / total) * 100
    print(f"🎯 Top-1 Precision: {precision:.0f}%")
    print("----------------------------------------")

if __name__ == "__main__":
    run_evaluation()