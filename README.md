After some reviews in the code and experiments, the results presented in the paper GNN4PPM: Multi-Target Predictive Process Monitoring with Graph Neural Network, tables 2 and 3 are not valid anymore. The previous pipeline had substantial problems on data leakage within a case, and because of this, the following changes on the code were performed after the submission:

- Prefix graphs: For each prediction, we construct a separate graph containing only the events observed up to the prediction point. Future events are excluded, preventing the model from accessing future information within a case. 
- Case attributes: Only case attributes that are known from the beginning of the case are included. Case attributes that appear at a later point in time or change throughout the case are not included in the prefix graphs to avoid leakage in message passing through the case node.
- Data split and embeddings: We now use a temporal case-level split with separate training, validation, and test sets. We also revised the RDF2Vec embeddings to walk only to individual event representations aggregated from the observed history.
- Timestamps and time features: Time features such as second since the previous event, seconds since the first event, hour of the day, and weekday are added into the graph and raw timestamp triples are not included.
- A more rigorous preprocessing was performed with handling differently unknown and missing values, as well as repeated information.

Due to those changes, new experiments were performed. Bellow, we present the updated tables 2 and 3 after the new experiments. Please note that only the results of the GNN4PPM were updated, since the benchmark results of other approaches were not rerun. 

Accuracy of the Next Activity Prediction Task compared to different approaches. Best result per dataset highlighted in bold; second-best is underlined
| Approach | BPIC12_A | BPIC12_W | BPIC12_WC | BPIC13_O | BPIC20_P | BPIC20_R |
|---|---:|---:|---:|---:|---:|---:|
| SEPHIGRAPH [13] | 67.8 | 78.6 | 46.6 | 20.2 | 73.8 | 76.5 |
| LUPIN [34] | 19.3 | 35.7 | 21.2 | 24.4 | 39.7 | 51.1 |
| PROPHET [35] | 76.7 | 89.2 | <u>80.3</u> | 62.0 | 83.8 | 87.8 |
| BEST [38] | 76.1 | 69.0 | 40.0 | 48.8 | <u>86.9</u> | 89.0 |
| CAMARGO [7] | 75.9 | 76.4 | 68.9 | **77.2** | 84.4 | **91.9** |
| EVERMANN [16] | 75.8 | 75.4 | 67.5 | <u>65.1</u> | **88.9** | <u>90.5</u> |
| TAX [42] | **79.5** | 85.3 | 69.8 | 60.9 | 84.4 | 89.0 |
| THEIS [43] | 65.5 | <u>86.2</u> | 80.1 | 59.3 | 83.2 | 89.7 |
| **GNN4PPM** | <u>77.6</u> | **92.1** | **79.6** | 70.9 | 23.2 | 56.9 |


Multi-target prediction results across datasets given as accuracy for event attributes and as normalized MAE for timestamp.
| Dataset | Activity | Resourcecountry | Org_resource | Lifecycle | Org_group | Org_role | Timestamp (MAE) |
|---|---:|---:|---:|---:|---:|---:|---:|
| BPIC12_A | 77.59 | – | 39.80 | 100.00 | – | – | 0.2455 |
| BPIC12_W | 92.05 | – | 54.36 | 83.54 | – | – | 0.4608 |
| BPIC12_WC | 79.59 | – | 11.52 | 100.00 | – | – | 0.7547 |
| BPIC13_O | 70.93 | 67.44 | 3.49 | 50.00 | 90.70 | 81.40 | 0.5794 |
| BPIC20_P | 23.16 | – | 87.60 | – | – | 51.37 | 0.4703 |
| BPIC20_R | 56.92 | – | 99.57 | – | – | 69.09 | 0.3449 |

It is important to note that although those changes were performed in the experiments, the approach pipeline was not modified, as well as model architecture and training objectives. 