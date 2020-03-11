import producer_server

BOOTSTRAP_SERVER = 'localhost:9092'
def run_kafka_server():
	# TODO get the json file path
    input_file = "./police-department-calls-for-service.json"
    
    # TODO fill in blanks
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic="com.deji.streams.crimes",
        bootstrap_servers=BOOTSTRAP_SERVER,
        client_id="client-1"
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
