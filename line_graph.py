import zmq
import io
import matplotlib.pyplot as plt
from datetime import datetime


def createLineGraph():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5689")

    try:
        while True:
            if socket.poll(1000):
                data = socket.recv_json()
                print(data['product']['metrics'])
                metrics = data['product']['metrics']
                dates = [datetime.fromisoformat(
                    item['record_date'].replace("Z", "+00:00")) for item in metrics]
                prices = [float(item['price']) for item in metrics]

                plt.figure(figsize=(18, 10))
                plt.plot(dates, prices, marker='o', linestyle='-',
                         color='b', label=data['product']['name'])
                plt.title('Price vs. Dates Recorded', fontsize=14)
                plt.xlabel('Dates Recorded', fontsize=14)
                plt.ylabel('Price', fontsize=14)
                plt.xticks(rotation=45, fontsize=12)
                plt.yticks(fontsize=12)
                plt.legend(fontsize=12)
                plt.grid(True, linewidth=0.5)
                plt.tight_layout()

                graph = io.BytesIO()
                plt.savefig(graph, format='png')
                graph.seek(0)
                plt.close()

                socket.send(graph.read())

    except KeyboardInterrupt:
        print("Graph microservice is shutting down")

    finally:

        print("Graph socket closed")


if __name__ == "__main__":
    createLineGraph()
