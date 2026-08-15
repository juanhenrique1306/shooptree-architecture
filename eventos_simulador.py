from abc import ABC, abstractmethod

# ==========================================
# DESIGN PATTERN: OBSERVER
# ==========================================

# A interface do Consumer (Observer)
class EventConsumer(ABC):
    @abstractmethod
    def update(self, evento_dados: dict):
        pass

# A classe do Producer (Subject)
class EventProducer:
    def __init__(self):
        self._consumers = []

    def inscrever(self, consumer: EventConsumer):
        self._consumers.append(consumer)

    def notificar(self, evento_dados: dict):
        print(f"\n[PRODUCER] Evento Gerado: {evento_dados['tipo']}")
        for consumer in self._consumers:
            consumer.update(evento_dados)

# ==========================================
# CONSUMERS ESPECÍFICOS (Os Serviços que "escutam")
# ==========================================

class PagamentoConsumer(EventConsumer):
    def update(self, evento_dados: dict):
        if evento_dados["tipo"] == "COMPRA_REALIZADA":
            print(f"[CONSUMER - Pagamento] Processando cobrança de R$ {evento_dados['valor']} para o pedido #{evento_dados['pedido_id']}")

class NotificacaoConsumer(EventConsumer):
    def update(self, evento_dados: dict):
        if evento_dados["tipo"] == "COMPRA_REALIZADA":
            print(f"[CONSUMER - Notificação] Enviando e-mail para {evento_dados['cliente']}: 'Sua compra foi confirmada!'")

# ==========================================
# SIMULAÇÃO DA ARQUITETURA
# ==========================================
if __name__ == "__main__":
    # 1. Instanciamos o Producer (O nosso "Kafka" simulado)
    broker = EventProducer()

    # 2. Instanciamos os Consumers
    servico_pagamento = PagamentoConsumer()
    servico_notificacao = NotificacaoConsumer()

    # 3. Inscrevemos os Consumers no Producer (Eles ficam aguardando)
    broker.inscrever(servico_pagamento)
    broker.inscrever(servico_notificacao)

    # 4. Simulamos uma compra acontecendo no sistema
    nova_compra = {
        "tipo": "COMPRA_REALIZADA",
        "pedido_id": 1042,
        "valor": 299.90,
        "cliente": "cliente@shooptree.com.br"
    }

    # 5. O serviço de compras apenas publica o evento e não precisa saber o que acontece depois
    broker.notificar(nova_compra)