import os, shutil
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline

# These categories must match the ones used in cash_flow records.
CATEGORIES = ["rent", "electricity", "phone", "subscriptions", "other"]

def aggregate_cash_flow(cash_flow_records):
    """
    Sums up amounts per category.
    """
    agg = {cat: 0.0 for cat in CATEGORIES}
    for record in cash_flow_records:
        cat = record.get("category", "other").lower()
        if cat not in CATEGORIES:
            cat = "other"
        agg[cat] += float(record.get("amount", 0))
    return agg

async def train_model(db):
    # Fetch applications
    apps_cursor = db.applications.find({})
    apps = await apps_cursor.to_list(length=1000)
    if not apps:
        raise Exception("No application data found, fuck off.")

    spark = SparkSession.builder.appName("CreditAppTraining").getOrCreate()
    rows = []
    for app in apps:
        cash_flow = app.get("cash_flow", [])
        agg = aggregate_cash_flow(cash_flow)
        label = int(app.get("history_data", {}).get("eligible", 0))
        row = [agg[cat] for cat in CATEGORIES] + [label]
        rows.append(tuple(row))
    columns = CATEGORIES + ["eligible"]
    df = spark.createDataFrame(rows, columns)

    assembler = VectorAssembler(inputCols=CATEGORIES, outputCol="features")
    rf = RandomForestClassifier(featuresCol="features", labelCol="eligible")
    pipeline = Pipeline(stages=[assembler, rf])
    model = pipeline.fit(df)

    model_path = "credit_rf_model"
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    model.save(model_path)
    spark.stop()
    return model_path