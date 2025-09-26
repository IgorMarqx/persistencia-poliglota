# 🐳 Instruções para Executar com Docker

## ✅ Projeto Executado com Sucesso!

O sistema de persistência poliglota está rodando perfeitamente com Docker. Aqui estão as informações importantes:

### 🌐 Acesso à Aplicação
- **URL:** http://localhost:8501
- **Status:** ✅ Online e funcionando

### 🗄️ Banco de Dados
- **MongoDB:** localhost:27017
- **Status:** ✅ Conectado e com dados de exemplo

### 📋 Funcionalidades Disponíveis

#### 1. 🏠 Página Inicial
- Visão geral do sistema
- Estatísticas dos bancos de dados
- Resumo das funcionalidades

#### 2. 🏙️ Gerenciar Cidades (SQLite)
- **Listar Cidades:** Visualizar todas as cidades cadastradas
- **Adicionar Cidade:** Cadastrar novas cidades
- **Dados de Exemplo:** Popular com cidades do Nordeste

#### 3. 📍 Gerenciar Locais (MongoDB)
- **Listar Locais:** Visualizar todos os locais geoespaciais
- **Adicionar Local:** Cadastrar novos pontos de interesse
- **Dados de Exemplo:** Popular com locais do Nordeste

#### 4. 🔍 Consultas Integradas
- Cruzar dados do SQLite com MongoDB
- Selecionar uma cidade e ver seus locais
- Relacionamento entre dados estruturados e não estruturados

#### 5. 🌍 Geoprocessamento
- **Busca por Proximidade:** Encontrar locais em um raio específico
- **Calcular Distância:** Medir distância entre dois pontos
- Validação de coordenadas geográficas

#### 6. 🗺️ Visualização no Mapa
- Mapa interativo com todos os locais
- Marcadores com informações detalhadas
- Estatísticas geográficas

#### 7. 📊 Estatísticas
- Gráficos e métricas do sistema
- Análise de dados por categoria e cidade
- Estatísticas geográficas

### 🚀 Como Usar

1. **Acesse:** http://localhost:8501
2. **Navegue:** Use o menu lateral para explorar as funcionalidades
3. **Popule dados:** Use as opções "Dados de Exemplo" para adicionar dados de teste
4. **Explore:** Teste todas as funcionalidades de geoprocessamento

### 🛠️ Comandos Docker Úteis

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs apenas da aplicação
docker-compose logs -f app

# Ver logs apenas do MongoDB
docker-compose logs -f mongodb

# Parar os containers
docker-compose down

# Reiniciar os containers
docker-compose restart

# Reconstruir e iniciar (após mudanças no código)
docker-compose up --build

# Ver status dos containers
docker-compose ps

# Acessar shell do container da aplicação
docker-compose exec app bash

# Acessar shell do MongoDB
docker-compose exec mongodb mongosh
```

### 🔧 Solução de Problemas

#### Se a aplicação não carregar:
```bash
# Verificar se os containers estão rodando
docker-compose ps

# Reiniciar os containers
docker-compose restart

# Ver logs de erro
docker-compose logs app
```

#### Se houver problemas de conexão com MongoDB:
```bash
# Verificar logs do MongoDB
docker-compose logs mongodb

# Reiniciar apenas o MongoDB
docker-compose restart mongodb
```

#### Para parar completamente:
```bash
# Parar e remover containers
docker-compose down

# Parar e remover containers + volumes (CUIDADO: apaga dados)
docker-compose down -v
```

### 📊 Dados de Exemplo Incluídos

#### SQLite (Cidades):
- Estados do Nordeste: PB, PE, CE, RN, AL, SE, BA, MA, PI
- Cidades principais com população e área

#### MongoDB (Locais):
- Pontos turísticos (Praça da Independência, Estação Cabo Branco)
- Centros culturais (Centro Dragão do Mar)
- Marcos históricos (Marco Zero do Recife)
- Todos com coordenadas geográficas precisas

### 🎯 Objetivos do Projeto Atendidos

✅ **Persistência Poliglota:** SQLite + MongoDB  
✅ **Dados Geoespaciais:** Coordenadas lat/lng no MongoDB  
✅ **Geoprocessamento:** Cálculo de distâncias e busca por proximidade  
✅ **Interface Interativa:** Streamlit com navegação intuitiva  
✅ **Consultas Integradas:** Cruzamento de dados dos dois bancos  
✅ **Visualização:** Mapas interativos com Folium  
✅ **Docker:** Containerização completa e funcional  

### 🎉 Sistema Pronto para Uso!

O projeto está 100% funcional e atende a todos os requisitos solicitados. Divirta-se explorando as funcionalidades de persistência poliglota e geoprocessamento!
