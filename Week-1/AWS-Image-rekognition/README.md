# 🚀 AWS Image Rekognition — Serverless Label Detection

This repository demonstrates a serverless image analysis workflow using **Amazon Rekognition** and **Amazon S3**. The project uses the AWS SDK for Python (`boto3`) to automatically identify objects and scenes within images.

## 🛠 Project Workflow

1. **Storage:** Images are uploaded to an Amazon S3 bucket.
2. **Analysis:** A Python script (run from AWS CloudShell or locally) sends the images to the Rekognition API.
3. **Extraction:** The script prints top-level labels (e.g., "Car", "Coffee", "Dog") with confidence scores.

---

## 📂 Project Structure

- `image-rekog.py`: Main Python script utilizing `boto3`.
- `requirements.txt`: Project dependencies.
- `s3-bucket/`: Local directory containing the sample dataset:
  - `car.png`
  - `coffee.png`
  - `dog.png`

## 🚀 Running the Script

### Installation

```powershell
python -m pip install -r requirements.txt
```

### Execution

```powershell
python image-rekog.py
```

## 📊 Sample Images

The images used in the CloudShell demo are included locally in the `s3-bucket/` folder.

![car sample](./s3-bucket/car.png)

![coffee sample](./s3-bucket/coffee.png)

![dog sample](./s3-bucket/dog.png)

> If the images still don't render in your Markdown preview, try one of the following:
>
> - Verify the `s3-bucket/` folder exists at the repository root and contains the listed files.
> - Ensure your editor preview reads files from the workspace root (some previewers use the file directory as the base path).

## Rekog Results

![alt text](AWS-img-rekog.png)

## S3 Bucket
![alt text](AWS-S3-imgRekog.png)

## Contents of S3 Bucket
![alt text](S3-Bucket-contents.png)