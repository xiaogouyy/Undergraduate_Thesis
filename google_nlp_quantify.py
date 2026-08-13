
import os
import pandas as pd
from google.cloud import language_v1
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ====== 配置 ======
INPUT_FILE = "LIWC_annotations.xlsx"
OUTPUT_FILE = "output_nlp.xlsx"
TEXT_COLUMN = "Text"
NEW_COLUMN = "Net Emotion"

# ====== 初始化客户端 ======
from google.oauth2 import service_account
from google.cloud import language_v1

credentials = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
)

client = language_v1.LanguageServiceClient(credentials=credentials)

def analyze_sentiment(text):
    """
    调用 Google NLP 进行情感分析
    返回 score（-1 到 1）
    """
    if pd.isna(text) or str(text).strip() == "":
        return None

    try:
        document = language_v1.Document(
            content=str(text),
            type_=language_v1.Document.Type.PLAIN_TEXT
        )

        response = client.analyze_sentiment(
            request={"document": document}
        )

        score = response.document_sentiment.score
        magnitude = response.document_sentiment.magnitude

        # ===== 选择你的 Net Emotion 计算方式 =====
        net_emotion = score
        # net_emotion = score * magnitude   # 可选：强度加权

        return net_emotion

    except Exception as e:
        print(f"Error processing text: {text[:30]}... | {e}")
        return None


def main():
    df = pd.read_excel(INPUT_FILE)

    results = []

    for i, text in enumerate(df[TEXT_COLUMN]):
        print(f"Processing {i+1}/{len(df)}")

        score = analyze_sentiment(text)
        results.append(score)

        # 防止触发API限速
        time.sleep(0.1)

    df[NEW_COLUMN] = results

    df.to_excel(OUTPUT_FILE, index=False)
    print("Done! Saved to", OUTPUT_FILE)


if __name__ == "__main__":
    main()