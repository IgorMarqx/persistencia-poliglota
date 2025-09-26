import sqlite3
import pandas as pd
from typing import List, Dict, Any

class SQLiteDB:
    def __init__(self, db_path: str = "cidades.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de estados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                uf TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Criar tabela de cidades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                estado_id INTEGER,
                populacao INTEGER,
                area_km2 REAL,
                FOREIGN KEY (estado_id) REFERENCES estados (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_estado(self, nome: str, uf: str) -> int:
        """Insere um novo estado e retorna o ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO estados (nome, uf) VALUES (?, ?)", (nome, uf))
            estado_id = cursor.lastrowid
            conn.commit()
            return estado_id
        except sqlite3.IntegrityError:
            # Estado já existe, buscar o ID
            cursor.execute("SELECT id FROM estados WHERE uf = ?", (uf,))
            estado_id = cursor.fetchone()[0]
            return estado_id
        finally:
            conn.close()
    
    def insert_cidade(self, nome: str, estado_uf: str, populacao: int = None, area_km2: float = None) -> int:
        """Insere uma nova cidade e retorna o ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar ou criar estado
        estado_id = self.insert_estado("", estado_uf)  # Nome será atualizado depois
        
        try:
            cursor.execute(
                "INSERT INTO cidades (nome, estado_id, populacao, area_km2) VALUES (?, ?, ?, ?)",
                (nome, estado_id, populacao, area_km2)
            )
            cidade_id = cursor.lastrowid
            conn.commit()
            return cidade_id
        finally:
            conn.close()
    
    def get_cidades(self) -> List[Dict[str, Any]]:
        """Retorna todas as cidades com informações do estado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.nome, e.nome as estado_nome, e.uf, c.populacao, c.area_km2
            FROM cidades c
            JOIN estados e ON c.estado_id = e.id
            ORDER BY c.nome
        ''')
        
        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        conn.close()
        return resultados
    
    def get_cidade_by_id(self, cidade_id: int) -> Dict[str, Any]:
        """Retorna uma cidade específica pelo ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.nome, e.nome as estado_nome, e.uf, c.populacao, c.area_km2
            FROM cidades c
            JOIN estados e ON c.estado_id = e.id
            WHERE c.id = ?
        ''', (cidade_id,))
        
        colunas = [desc[0] for desc in cursor.description]
        resultado = cursor.fetchone()
        
        conn.close()
        
        if resultado:
            return dict(zip(colunas, resultado))
        return None
    
    def get_estados(self) -> List[Dict[str, Any]]:
        """Retorna todos os estados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, uf FROM estados ORDER BY nome")
        
        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        conn.close()
        return resultados
    
    def populate_sample_data(self):
        """Popula o banco com dados de exemplo"""
        # Estados brasileiros
        estados_brasil = [
            ("Paraíba", "PB"),
            ("Pernambuco", "PE"),
            ("Ceará", "CE"),
            ("Rio Grande do Norte", "RN"),
            ("Alagoas", "AL"),
            ("Sergipe", "SE"),
            ("Bahia", "BA"),
            ("Maranhão", "MA"),
            ("Piauí", "PI")
        ]
        
        # Cidades de exemplo
        cidades_brasil = [
            ("João Pessoa", "PB", 825796, 211.475),
            ("Campina Grande", "PB", 413830, 620.223),
            ("Recife", "PE", 1653461, 218.435),
            ("Olinda", "PE", 393115, 41.681),
            ("Fortaleza", "CE", 2703391, 312.353),
            ("Natal", "RN", 890480, 167.264),
            ("Maceió", "AL", 1025360, 511.149),
            ("Aracaju", "SE", 664908, 181.857),
            ("Salvador", "BA", 2886698, 693.453),
            ("São Luís", "MA", 1115932, 834.785)
        ]
        
        # Inserir estados
        for nome, uf in estados_brasil:
            self.insert_estado(nome, uf)
        
        # Inserir cidades
        for nome, uf, populacao, area in cidades_brasil:
            self.insert_cidade(nome, uf, populacao, area)
