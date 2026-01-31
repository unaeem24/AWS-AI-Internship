### **Week 1 Portfolio: AWS AI Fundamentals & Service Integration**

This summary captures your four key internship tasks at **Cloudelligent**, covering core AWS infrastructure and specialized AI services using **Python** and **Boto3**.


### **Task 1: Serverless Image Resizer & Automation**

* **Goal**: Implement a serverless image processing workflow while practicing **Least Privilege** security.
* **Implementation**:
* Developed an **AWS Lambda** function to automatically resize images uploaded to an **S3 bucket**.
* Configured a **CloudWatch Events (EventBridge)** cron job to trigger a "Cleanup Lambda" that empties the bucket at the End of Day (EOD).


* **Outcome**: Automated the image lifecycle from processing to storage cleanup.

---

### **Task 2: Computer Vision with Amazon Rekognition**

* **Goal**: Use pre-trained AI models to extract metadata from visual content.
* **Implementation**:
* Uploaded a sample dataset (`car.png`, `coffee.png`, `dog.png`) to an **S3 bucket**.
* Authored a Python script using **Boto3** to call the `detect_labels` API.


* **Outcome**: Successfully identified objects with high confidence scores directly from the CLI.

---

### **Task 3: NLP & Sentiment Analysis with Amazon Comprehend**

* **Goal**: Analyze text to determine the underlying emotional tone (Sentiment).
* **Implementation**:
* Built a Python script to send text strings ("tweets") to the **Comprehend** service.
* Used the `detect_sentiment` API to classify text as **Positive**, **Negative**, or **Neutral**.


* **Outcome**: Demonstrated real-time natural language processing without managing underlying ML models.

---

### **Task 4: Amazon SageMaker Studio Navigation**

* **Goal**: Explore the primary AWS environment for end-to-end Machine Learning workflows.
* **Exploration Points**:
* **Notebooks**: Interface for data science experimentation.
* **Experiments**: System for tracking model training iterations.
* **Models**: The model registry for managing versioning and deployment.


* **Outcome**: Gained familiarity with the Studio UI and ML lifecycle management without incurring compute costs.

---

### **Summary of Tech Stack**

* **Core Services**: Lambda, S3, EventBridge.
* **AI Services**: Rekognition, Comprehend, SageMaker.
* **Automation**: Boto3 (Python SDK), AWS CloudShell.

