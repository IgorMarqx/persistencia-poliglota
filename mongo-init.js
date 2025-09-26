// Script de inicialização do MongoDB
// Cria o banco de dados e usuário específico para a aplicação

db = db.getSiblingDB('geolocalizacao');

// Criar usuário para a aplicação
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'geolocalizacao'
    }
  ]
});

// Criar coleção de locais
db.createCollection('locais');

// Inserir alguns dados de exemplo
db.locais.insertMany([
  {
    "nome_local": "Praça da Independência",
    "cidade": "João Pessoa",
    "coordenadas": {
      "latitude": -7.11532,
      "longitude": -34.861
    },
    "descricao": "Ponto turístico central da cidade.",
    "categoria": "Praça",
    "endereco": "Centro, João Pessoa - PB",
    "data_cadastro": new Date(),
    "ativo": true
  },
  {
    "nome_local": "Estação Cabo Branco",
    "cidade": "João Pessoa",
    "coordenadas": {
      "latitude": -7.14111,
      "longitude": -34.7947
    },
    "descricao": "Ponto mais oriental das Américas.",
    "categoria": "Ponto Turístico",
    "endereco": "Cabo Branco, João Pessoa - PB",
    "data_cadastro": new Date(),
    "ativo": true
  },
  {
    "nome_local": "Praça do Marco Zero",
    "cidade": "Recife",
    "coordenadas": {
      "latitude": -8.04756,
      "longitude": -34.8770
    },
    "descricao": "Marco zero de Recife, centro histórico.",
    "categoria": "Ponto Turístico",
    "endereco": "Recife Antigo, Recife - PE",
    "data_cadastro": new Date(),
    "ativo": true
  },
  {
    "nome_local": "Centro Dragão do Mar",
    "cidade": "Fortaleza",
    "coordenadas": {
      "latitude": -3.73111,
      "longitude": -38.5264
    },
    "descricao": "Centro cultural e de arte de Fortaleza.",
    "categoria": "Cultura",
    "endereco": "Praia de Iracema, Fortaleza - CE",
    "data_cadastro": new Date(),
    "ativo": true
  }
]);

print('Banco de dados inicializado com sucesso!');
