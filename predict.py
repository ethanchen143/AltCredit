import os
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

CATEGORIES = ["rent", "electricity", "phone", "subscriptions", "other"]

def aggregate_cash_flow(cash_flow_records):
    agg = {cat: 0.0 for cat in CATEGORIES}
    for record in cash_flow_records:
        cat = record.get("category", "other").lower()
        if cat not in CATEGORIES:
            cat = "other"
        agg[cat] += float(record.get("amount", 0))
    return agg

def predict_eligibility(user_data):
    return 1
    spark = SparkSession.builder.appName("CreditAppPrediction").getOrCreate()
    model_path = "credit_rf_model"
    if not os.path.exists(model_path):
        spark.stop()
        raise Exception("Model not found. Train it first, asshole.")
    
    model = PipelineModel.load(model_path)
    agg = aggregate_cash_flow(cash_flow_records)
    data = [tuple(agg[cat] for cat in CATEGORIES)]
    columns = CATEGORIES
    df = spark.createDataFrame(data, columns)
    prediction = model.transform(df).select("prediction").collect()[0]["prediction"]
    spark.stop()
    return int(prediction)