# AI Receptionist Demo

A demo AI voice/chat receptionist for a local business ("Bright Smile Dental", Sydney).
Answers customer questions, quotes services, and captures bookings; triages
emergencies. Built as a scripted demo for Loom recordings.

## How it works

- **Offline rule-based brain** — no API key needed, works out of the box.
- **Optional Gemini mode** — set `GEMINI_API_KEY` to route replies through
  Gemini's free tier instead of the rule engine.

## Run

```bash
python3 receptionist.py            # interactive chat
python3 receptionist.py --demo    # scripted demo conversation
```

Zero dependencies — Python 3 standard library only.

## Note

This is a demo, not a production booking system. The clinic, prices, and
conversation flow are illustrative examples.

## Learn more

Built by [VisionQuantech](https://visionquantech.com) — see our comparison of the [best AI chatbots for small business in 2026](https://visionquantech.com/blog/best-ai-chatbots-small-business.html).

## Built by VisionQuantech

This project is built by [VisionQuantech](https://visionquantech.com/) — AI agents, websites & SEO for small business.

Related guides:
- [AI receptionist service](https://visionquantech.com/blog/ai-receptionist-service.html)
- [virtual receptionist for small business](https://visionquantech.com/blog/virtual-receptionist-for-small-business.html)
