import pprint
import grpc,json
import QUANTAXIS as QA
from QAStrategy import QAStrategyCTABase

from rpc import ml_service_rpc_pb2, ml_service_rpc_pb2_grpc

# stub = blockdet_rpc_pb2_grpc.grpcServerStub(channle)
# response = stub.process(blockdet_rpc_pb2.DataProto(img = img_byte, traceid = '1'))


_HOST = '123.56.159.222'
_PORT = '6606'


class MLService(QAStrategyCTABase):

    def on_bar(self, bar):

        res = self.ml_factor()

        print(res.iloc[-1])

        if res.DIF[-1] > res.DEA[-1]:

            print('LONG')

            if self.positions.volume_long == 0:
                self.send_order('BUY', 'OPEN', price=bar['close'], volume=1)
            if self.positions.volume_short > 0:
                self.send_order('BUY', 'CLOSE', price=bar['close'], volume=1)

        else:
            print('SHORT')
            if self.positions.volume_short == 0:
                self.send_order('SELL', 'OPEN', price=bar['close'], volume=1)
            if self.positions.volume_long > 0:
                self.send_order('SELL', 'CLOSE', price=bar['close'], volume=1)

    def ml_factor(self,):
        data_json = self.market_data.to_json()
        print (type(data_json))
        with grpc.insecure_channel(_HOST + ':' + _PORT) as channel:
            stub = ml_service_rpc_pb2_grpc.grpcServerStub(channel)
            response = stub.process(ml_service_rpc_pb2.DataProto(data_json = data_json))
            data_json = json.loads(response.data_json)
        print (data_json)
        exit()

        return QA.QA_indicator_MACD(self.market_data)

    def risk_check(self):
        pass
        # pprint.pprint(self.qifiacc.message)


if __name__ == '__main__':
    ml_strategy = MLService(code='rbl8', frequence='1min',strategy_id='1dds1s2d-7902-4a85-adb2-fbac4bb977fe', start='2021-02-01', end='2021-02-02', model= 'rust')
    ml_strategy.run_backtest()
