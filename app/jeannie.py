from openai import OpenAI

client = OpenAI(
    api_key="<YOUR API KEY>",
    base_url="https://api.deepseek.com",
)


def generate_content(prompt):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )

    return response.choices[0].message.content
