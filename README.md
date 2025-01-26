# High-Performance Transformer Approach for Intrusion Detection  

This repository contains the implementation of a high-performance transformer approach for Intrusion Detection  designed to identify and classify network traffic anomalies. By leveraging state-of-the-art machine learning (ML) and deep learning (DL) techniques, including Transformer Encoder-Decoder models, voting classifier, this system ensures robust and scalable detection of threats in network traffic.  

---

## Features  

- **Algorithms**:  
  - Machine Learning: Support Vector Machine (SVM), Bagging Classifier, Voting Classifier.  
  - Deep Learning: Long Short-Term Memory (LSTM), Recurrent Neural Network (RNN), Feedforward Neural Network (FNN).  
  - Transformer Encoder-Decoder: Advanced model for optimized feature extraction and detection.  

- **Key Capabilities**:  
  - Detection of benign traffic and multiple attack types, including:  
    - Denial of Service (DoS)  
    - Probe Attacks  
    - Remote to Local (R2L)  
  - Real-time traffic capture and feature extraction using **Wireshark**.  
  - Extracting parameters from `.pcapng` files when users choose not to manually input data.  
  - Interactive front-end for user inputs and parameter customization.  
  - High accuracy and low false-positive rate through ensemble and Transformer-based models.  

---

## System Architecture  

1. **Data Collection**: Traffic is captured via **Wireshark**, simulating real-world scenarios with benign and attack packets.  
2. **Feature Extraction**: Key parameters, such as packet size and flow duration are extracted for analysis using `pcap_reader.py`.  
3. **Model Training**: The system trains multiple ML and DL models on labeled datasets to classify traffic.  
4. **Front-End Interface**: Users can input network traffic parameters through an interactive interface or use pre-captured `.pcapng` data.  
5. **Prediction and Analysis**: The system outputs the type of traffic (benign or specific attack).  

---

## Installation  

### Prerequisites  

1. **Anaconda3-2019.10**  
   Download and install Anaconda3-2019.10 (64-bit):  
   [Download Link](https://repo.anaconda.com/archive/Anaconda3-2019.10-Windows-x86_64.exe).  

2. **Wireshark**  
   Install Wireshark for traffic capture:  
   [Wireshark Download](https://www.wireshark.org/download.html).  

---

### Steps to Set Up  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/Kethan3/major_project_highperformance_transformer_approach_for_intrusiondetection.git  
   cd major_project_highperformance_transformer_approach_for_intrusiondetection  

2. Install the required dependencies:
```bash
   pip install tensorflow==2.5.0 --user  
   pip install --user scikit-learn==1.0.2 markupsafe==2.0.1 protobuf==3.20 numpy==1.19.5 keras==2.5.0rc0 werkzeug==0.16.0 itsdangerous==2.0.1 jinja2==3.0.3  
   pip install --user opencv-python==4.1.1.26  
   pip uninstall flask werkzeug -y  
   pip install flask==1.1.1 werkzeug==0.16.0
```

3. Run the application:
```bash
     python app.py
```
If users prefer not to input parameters manually through the front-end, you can process a .pcapng file using the provided script:

Place your Wireshark-captured .pcapng file in the test directory (e.g., test.pcapng).
Run the following command to extract parameters :
```bash
 python .\test\pcap_reader.py
```
The extracted parameters will be sent to the  system for analysis, bypassing manual input through the front end.
