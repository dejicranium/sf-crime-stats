from kafka import KafkaProducer
import json
import time


class ProducerServer(KafkaProducer):

    def __init__(self, input_file, topic, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic

    #TODO we're generating a dummy data
    def generate_data(self):
        with open(self.input_file) as f:
            index = 0
            f = json.load(f)
            for line in f:
                
                message = self.dict_to_binary(line)
                # TODO send the correct data
                self.send(self.topic, message)
                print(json.dumps(message.decode('utf-8')))
                index = index + 1
                time.sleep(1)

    # TODO fill this in to return the json dictionary to binary
    def dict_to_binary(self, json_dict):
        # first encode json_dict as json, since there's no 
        # encoding in generate_data
        json_dict = json.dumps(json_dict)
        binary_encoded = json_dict.encode('utf-8')

        return binary_encoded
    
    
        