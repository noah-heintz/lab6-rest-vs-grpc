| Method | Local (ms/op) | Same-Zone (ms/op) | Different Region (ms/op) |
|---|---:|---:|---:|
| REST add | 2.244 | 4.625 | 445.714 |
| gRPC add | 0.549 | 1.560 | 161.875 |
| REST rawimg | 3.929 | 11.955 | 1353.728 |
| gRPC rawimg | 3.127 | 9.426 | 167.031 |
| REST dotproduct | 2.531 | 5.393 | 432.619 |
| gRPC dotproduct | 0.546 | 1.543 | 157.132 |
| REST jsonimg | 24.013 | 57.799 | 1478.436 |
| gRPC jsonimg | 10.154 | 35.364 | 219.328 |
| PING (RTT, ms) | 0.038 | 0.562 | 288.765 |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.

While the gRPC setup was more involved, it was clear throughout the all of the testing that gRPC was consistently faster than REST. The improvements in serialization, image encoding, and protocol overhead were significant especially in image processing, where you see times as much as 6-7 times faster in the third test.

The ping times are also interesting--jumping from 0.038, to 0.562 between same zones, to 288.765 to Europe. This latency increase really came to a head during the third test, where running the minimum of 100 tests still took 5+ minutes total to run with the REST server. The gRPC had this done in about a minute or two, showing how powerful the protobuf approach can be. 

The outcome is striking--while my familiarity with exposing Flask endpoints and its familiar code structure was my comfort zone, the gRPC approach demonstrates how these processes can be streamlined by reducing much of the overhead especially over long distances.