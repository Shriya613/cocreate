from mistralai import Mistral
from app.config import MISTRAL_API_KEY, MISTRAL_MODEL

client = Mistral(api_key=MISTRAL_API_KEY)

SYSTEM_PROMPT = """You are an expert React developer. Your job is to generate complete, working React applications.

RULES:
- Output ONLY a single complete App.tsx file with no explanation, no markdown, no code fences.
- Use React with TypeScript (tsx).
- Use Tailwind CSS for ALL styling. Do not import any CSS files.
- Use only React hooks (useState, useEffect, useCallback, useMemo, useRef). No external libraries except those listed below.
- You MAY import from: react, react-dom, lucide-react.
- Use lucide-react for icons (import { IconName } from 'lucide-react').
- Use localStorage for persistence where appropriate.
- Make the UI beautiful, modern, and mobile-first with smooth UX.
- The app must be fully functional and self-contained in a single file.
- Export the App component as default: export default function App() { ... }
- NEVER use external API calls or fetch. All data must be local.
- NEVER import from '@/components' or any path alias. Only the allowed imports above.
- Include a nice header with the app name and a clean layout.
"""

ITERATE_SYSTEM_PROMPT = """You are an expert React developer iterating on an existing app.

RULES:
- Output ONLY the complete updated App.tsx file with no explanation, no markdown, no code fences.
- Apply the user's requested changes while preserving all existing functionality.
- Use React with TypeScript (tsx).
- Use Tailwind CSS for ALL styling.
- Use only React hooks and lucide-react for icons.
- Maintain localStorage persistence from the original.
- Export the App component as default: export default function App() { ... }
- NEVER import from '@/components' or any path alias.
"""


async def generate_app_code(description: str) -> str:
    response = await client.chat.complete_async(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Build me this app: {description}"},
        ],
        temperature=0.7,
        max_tokens=8000,
    )
    return _clean_code(response.choices[0].message.content or "")


async def iterate_app_code(current_code: str, instruction: str, history: list[dict]) -> str:
    response = await client.chat.complete_async(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": ITERATE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Here is the current App.tsx:\n\n{current_code}\n\nNow apply this change: {instruction}",
            },
        ],
        temperature=0.7,
        max_tokens=8000,
    )
    return _clean_code(response.choices[0].message.content or "")


async def fix_build_error(code: str, error: str) -> str:
    response = await client.chat.complete_async(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"This App.tsx has a build error. Fix it and return the complete corrected file.\n\n"
                    f"ERROR:\n{error}\n\nCURRENT CODE:\n{code}"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=8000,
    )
    return _clean_code(response.choices[0].message.content or "")


def _clean_code(code: str) -> str:
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        if lines[-1].strip() == "```":
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        code = "\n".join(lines)
    return code.strip()
