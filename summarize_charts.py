import base64
import os

import openai
import pandas as pd

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"


def encode_image(image_path):
    """Encodes an image into base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def summarize_chart(client, csv_file, png_file):
    """Summarizes a chart using the GPT-4-vision-preview model."""

    # Load chart data from CSV
    data = pd.read_csv(csv_file)
    chart_csv = data.to_csv(index=False)
    chart_lines = chart_csv.splitlines()
    chart_data = "\n".join(chart_lines)

    # Load chart image
    base64_image = encode_image(png_file)

    # Create the prompt
    system_prompt = f"""Your role is to summarize charts in less than 200 words. The user always provides the chart data in the text message.
Notes:
- You MUST extract necessary and valuable insight in the provided data.
- You should write paragraphs instead of listing points.
- You should provide highlighted numbers in your summarization.
- Your response MUST ONLY include the chart summarization, not ANYTHING ELSE.
- Your response MUST NOT exceed 200 words, even if the data is extremely big, so please select the most important insight to write about.
""".strip()

    user_prompt = f"""Chart data:
{chart_data}""".strip()

    print(system_prompt)
    print(user_prompt)

    # Call the OpenAI API with the gpt-4-vision-preview model
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=256,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            },
        ],
    )

    print(response)

    return response.choices[0].message.content.strip()


def summarize_charts(
    client,
    start_index,
    num_charts,
    csv_folder="csv",
    png_folder="png",
    txt_folder="txt",
):
    os.makedirs(txt_folder, exist_ok=True)
    num_chart_summarized = 0

    csv_files = os.listdir(csv_folder)
    csv_files.sort(key=lambda x: os.path.getsize(os.path.join(csv_folder, x)))

    for i, csv_filename in enumerate(csv_files[start_index : start_index + num_charts]):
        base_filename, _ = os.path.splitext(csv_filename)
        png_filepath = os.path.join(png_folder, base_filename + ".png")
        txt_filepath = os.path.join(txt_folder, base_filename + ".txt")
        print()
        print("-" * 80)
        print(f"Summarizing chart {base_filename} ({i+1}/{num_charts})")

        if not os.path.exists(txt_filepath):  # Check if summarization exists
            try:
                summary = summarize_chart(
                    client, os.path.join(csv_folder, csv_filename), png_filepath
                )
                with open(txt_filepath, "w") as f:
                    f.write(summary)
                print(f"Chart summarized: {csv_filename}")
                num_chart_summarized += 1
            except Exception as e:
                print(f"Error summarizing chart {base_filename}: {e}")
        else:
            print(f"Chart already summarized: {csv_filename}")

    print(f"Summarized {num_chart_summarized} charts")
