from pymongo import MongoClient
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime

class MongoDB:
    def __init__(self, connection_string: str = None, db_name: str = "geolocalizacao"):
        # Usar string de conexão do ambiente ou padrão
        if connection_string is None:
            connection_string = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db.locais
    
    def insert_local(self, nome_local: str, cidade: str, latitude: float, longitude: float, 
                    descricao: str = "", categoria: str = "", endereco: str = "") -> str:
        """Insere um novo local no MongoDB"""
        documento = {
            "nome_local": nome_local,
            "cidade": cidade,
            "coordenadas": {
                "latitude": latitude,
                "longitude": longitude
            },
            "descricao": descricao,
            "categoria": categoria,
            "endereco": endereco,
            "data_cadastro": datetime.now(),
            "ativo": True
        }
        
        resultado = self.collection.insert_one(documento)
        return str(resultado.inserted_id)
    
    def get_locais_by_cidade(self, cidade: str) -> List[Dict[str, Any]]:
        """Retorna todos os locais de uma cidade específica"""
        locais = self.collection.find(
            {"cidade": {"$regex": cidade, "$options": "i"}, "ativo": True}
        )
        
        resultado = []
        for local in locais:
            local['_id'] = str(local['_id'])  # Converter ObjectId para string
            resultado.append(local)
        
        return resultado
    
    def get_locais_by_coordenadas(self, latitude: float, longitude: float, 
                                 raio_km: float = 10) -> List[Dict[str, Any]]:
        """Retorna locais próximos a uma coordenada específica"""
        # Usar operador $geoWithin para buscar em um raio específico
        # Para simplificar, vamos buscar todos e filtrar depois no geoprocessamento
        locais = self.collection.find({"ativo": True})
        
        resultado = []
        for local in locais:
            local['_id'] = str(local['_id'])
            resultado.append(local)
        
        return resultado
    
    def get_all_locais(self) -> List[Dict[str, Any]]:
        """Retorna todos os locais ativos"""
        locais = self.collection.find({"ativo": True})
        
        resultado = []
        for local in locais:
            local['_id'] = str(local['_id'])
            resultado.append(local)
        
        return resultado
    
    def get_local_by_id(self, local_id: str) -> Optional[Dict[str, Any]]:
        """Retorna um local específico pelo ID"""
        from bson import ObjectId
        
        try:
            local = self.collection.find_one({"_id": ObjectId(local_id), "ativo": True})
            if local:
                local['_id'] = str(local['_id'])
            return local
        except:
            return None
    
    def update_local(self, local_id: str, dados_atualizacao: Dict[str, Any]) -> bool:
        """Atualiza um local existente"""
        from bson import ObjectId
        
        try:
            # Remover campos que não devem ser atualizados
            dados_atualizacao.pop('_id', None)
            dados_atualizacao.pop('data_cadastro', None)
            
            resultado = self.collection.update_one(
                {"_id": ObjectId(local_id)},
                {"$set": dados_atualizacao}
            )
            return resultado.modified_count > 0
        except:
            return False
    
    def delete_local(self, local_id: str) -> bool:
        """Remove um local (soft delete)"""
        from bson import ObjectId
        
        try:
            resultado = self.collection.update_one(
                {"_id": ObjectId(local_id)},
                {"$set": {"ativo": False}}
            )
            return resultado.modified_count > 0
        except:
            return False
    
    def search_locais(self, termo: str) -> List[Dict[str, Any]]:
        """Busca locais por nome ou descrição"""
        locais = self.collection.find({
            "$or": [
                {"nome_local": {"$regex": termo, "$options": "i"}},
                {"descricao": {"$regex": termo, "$options": "i"}},
                {"categoria": {"$regex": termo, "$options": "i"}}
            ],
            "ativo": True
        })
        
        resultado = []
        for local in locais:
            local['_id'] = str(local['_id'])
            resultado.append(local)
        
        return resultado
    
    def get_locais_by_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        """Retorna locais de uma categoria específica"""
        locais = self.collection.find({
            "categoria": {"$regex": categoria, "$options": "i"},
            "ativo": True
        })
        
        resultado = []
        for local in locais:
            local['_id'] = str(local['_id'])
            resultado.append(local)
        
        return resultado
    
    def populate_sample_data(self):
        """Popula o banco com dados de exemplo"""
        locais_exemplo = [
            {
                "nome_local": "Praça da Independência",
                "cidade": "João Pessoa",
                "coordenadas": {"latitude": -7.11532, "longitude": -34.861},
                "descricao": "Ponto turístico central da cidade.",
                "categoria": "Praça",
                "endereco": "Centro, João Pessoa - PB"
            },
            {
                "nome_local": "Estação Cabo Branco",
                "cidade": "João Pessoa",
                "coordenadas": {"latitude": -7.14111, "longitude": -34.7947},
                "descricao": "Ponto mais oriental das Américas.",
                "categoria": "Ponto Turístico",
                "endereco": "Cabo Branco, João Pessoa - PB"
            },
            {
                "nome_local": "Mercado Central",
                "cidade": "João Pessoa",
                "coordenadas": {"latitude": -7.12056, "longitude": -34.8819},
                "descricao": "Mercado tradicional com artesanato local.",
                "categoria": "Comércio",
                "endereco": "Centro, João Pessoa - PB"
            },
            {
                "nome_local": "Praça do Marco Zero",
                "cidade": "Recife",
                "coordenadas": {"latitude": -8.04756, "longitude": -34.8770},
                "descricao": "Marco zero de Recife, centro histórico.",
                "categoria": "Ponto Turístico",
                "endereco": "Recife Antigo, Recife - PE"
            },
            {
                "nome_local": "Mercado de São José",
                "cidade": "Recife",
                "coordenadas": {"latitude": -8.06278, "longitude": -34.8806},
                "descricao": "Mercado público tradicional de Recife.",
                "categoria": "Comércio",
                "endereco": "São José, Recife - PE"
            },
            {
                "nome_local": "Praia de Boa Viagem",
                "cidade": "Recife",
                "coordenadas": {"latitude": -8.11944, "longitude": -34.9006},
                "descricao": "Principal praia urbana de Recife.",
                "categoria": "Praia",
                "endereco": "Boa Viagem, Recife - PE"
            },
            {
                "nome_local": "Centro Dragão do Mar",
                "cidade": "Fortaleza",
                "coordenadas": {"latitude": -3.73111, "longitude": -38.5264},
                "descricao": "Centro cultural e de arte de Fortaleza.",
                "categoria": "Cultura",
                "endereco": "Praia de Iracema, Fortaleza - CE"
            },
            {
                "nome_local": "Mercado Central de Fortaleza",
                "cidade": "Fortaleza",
                "coordenadas": {"latitude": -3.73111, "longitude": -38.5264},
                "descricao": "Mercado tradicional com artesanato cearense.",
                "categoria": "Comércio",
                "endereco": "Centro, Fortaleza - CE"
            }
        ]
        
        # Inserir locais de exemplo
        for local in locais_exemplo:
            self.insert_local(
                local["nome_local"],
                local["cidade"],
                local["coordenadas"]["latitude"],
                local["coordenadas"]["longitude"],
                local["descricao"],
                local["categoria"],
                local["endereco"]
            )
    
    def close_connection(self):
        """Fecha a conexão com o MongoDB"""
        self.client.close()
