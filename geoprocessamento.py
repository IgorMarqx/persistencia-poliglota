from geopy.distance import geodesic
from typing import List, Dict, Any, Tuple
import math

class GeoProcessamento:
    """Classe para operações de geoprocessamento"""
    
    @staticmethod
    def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula a distância entre dois pontos geográficos em quilômetros
        
        Args:
            lat1, lon1: Coordenadas do primeiro ponto
            lat2, lon2: Coordenadas do segundo ponto
        
        Returns:
            Distância em quilômetros
        """
        ponto1 = (lat1, lon1)
        ponto2 = (lat2, lon2)
        return geodesic(ponto1, ponto2).kilometers
    
    @staticmethod
    def locais_proximos(locais: List[Dict[str, Any]], lat_central: float, 
                       lon_central: float, raio_km: float = 10) -> List[Dict[str, Any]]:
        """
        Encontra locais dentro de um raio específico de um ponto central
        
        Args:
            locais: Lista de locais do MongoDB
            lat_central, lon_central: Coordenadas do ponto central
            raio_km: Raio de busca em quilômetros
        
        Returns:
            Lista de locais próximos com distância calculada
        """
        locais_proximos = []
        
        for local in locais:
            if 'coordenadas' in local:
                lat_local = local['coordenadas']['latitude']
                lon_local = local['coordenadas']['longitude']
                
                distancia = GeoProcessamento.calcular_distancia(
                    lat_central, lon_central, lat_local, lon_local
                )
                
                if distancia <= raio_km:
                    local_com_distancia = local.copy()
                    local_com_distancia['distancia_km'] = round(distancia, 2)
                    locais_proximos.append(local_com_distancia)
        
        # Ordenar por distância
        locais_proximos.sort(key=lambda x: x['distancia_km'])
        return locais_proximos
    
    @staticmethod
    def locais_por_cidade(locais: List[Dict[str, Any]], cidade: str) -> List[Dict[str, Any]]:
        """
        Filtra locais por cidade específica
        
        Args:
            locais: Lista de locais do MongoDB
            cidade: Nome da cidade para filtrar
        
        Returns:
            Lista de locais da cidade especificada
        """
        return [local for local in locais if local.get('cidade', '').lower() == cidade.lower()]
    
    @staticmethod
    def calcular_bounding_box(lat_central: float, lon_central: float, 
                            raio_km: float) -> Tuple[float, float, float, float]:
        """
        Calcula uma caixa delimitadora (bounding box) para otimizar consultas
        
        Args:
            lat_central, lon_central: Coordenadas do ponto central
            raio_km: Raio em quilômetros
        
        Returns:
            Tuple com (lat_min, lat_max, lon_min, lon_max)
        """
        # Aproximação: 1 grau de latitude ≈ 111 km
        # 1 grau de longitude varia com a latitude
        lat_delta = raio_km / 111.0
        lon_delta = raio_km / (111.0 * math.cos(math.radians(lat_central)))
        
        return (
            lat_central - lat_delta,  # lat_min
            lat_central + lat_delta,  # lat_max
            lon_central - lon_delta,  # lon_min
            lon_central + lon_delta   # lon_max
        )
    
    @staticmethod
    def centroide(locais: List[Dict[str, Any]]) -> Tuple[float, float]:
        """
        Calcula o centroide (centro de massa) de uma lista de locais
        
        Args:
            locais: Lista de locais com coordenadas
        
        Returns:
            Tuple com (latitude_centro, longitude_centro)
        """
        if not locais:
            return (0.0, 0.0)
        
        lat_total = 0.0
        lon_total = 0.0
        
        for local in locais:
            if 'coordenadas' in local:
                lat_total += local['coordenadas']['latitude']
                lon_total += local['coordenadas']['longitude']
        
        return (lat_total / len(locais), lon_total / len(locais))
    
    @staticmethod
    def estatisticas_geograficas(locais: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula estatísticas geográficas de uma lista de locais
        
        Args:
            locais: Lista de locais com coordenadas
        
        Returns:
            Dicionário com estatísticas
        """
        if not locais:
            return {}
        
        latitudes = []
        longitudes = []
        
        for local in locais:
            if 'coordenadas' in local:
                latitudes.append(local['coordenadas']['latitude'])
                longitudes.append(local['coordenadas']['longitude'])
        
        if not latitudes:
            return {}
        
        return {
            'total_locais': len(locais),
            'latitude_media': sum(latitudes) / len(latitudes),
            'longitude_media': sum(longitudes) / len(longitudes),
            'latitude_min': min(latitudes),
            'latitude_max': max(latitudes),
            'longitude_min': min(longitudes),
            'longitude_max': max(longitudes),
            'centroide': (sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes))
        }
    
    @staticmethod
    def validar_coordenadas(latitude: float, longitude: float) -> bool:
        """
        Valida se as coordenadas são válidas
        
        Args:
            latitude: Latitude (-90 a 90)
            longitude: Longitude (-180 a 180)
        
        Returns:
            True se as coordenadas são válidas
        """
        return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)
    
    @staticmethod
    def converter_para_graus_decimais(graus: int, minutos: int, segundos: float, 
                                    direcao: str) -> float:
        """
        Converte coordenadas de graus, minutos e segundos para graus decimais
        
        Args:
            graus: Graus
            minutos: Minutos
            segundos: Segundos
            direcao: 'N', 'S', 'E', 'W'
        
        Returns:
            Coordenada em graus decimais
        """
        decimal = graus + (minutos / 60.0) + (segundos / 3600.0)
        
        if direcao in ['S', 'W']:
            decimal = -decimal
        
        return decimal
    
    @staticmethod
    def distancia_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distância usando a fórmula de Haversine (alternativa ao geopy)
        
        Args:
            lat1, lon1: Coordenadas do primeiro ponto
            lat2, lon2: Coordenadas do segundo ponto
        
        Returns:
            Distância em quilômetros
        """
        # Raio da Terra em quilômetros
        R = 6371.0
        
        # Converter para radianos
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        # Diferenças
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        # Fórmula de Haversine
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
