
from smart_insights import (
    generate_smart_insights,
    generate_ai_recommendations
)

print("Calculating financial insights...")

insights = generate_smart_insights()

print("Sending insights to Gemini...")

recommendations = generate_ai_recommendations(insights)

print("\nFINORA SMART INSIGHTS")
print("=" * 45)
print(recommendations)
print("=" * 45)
